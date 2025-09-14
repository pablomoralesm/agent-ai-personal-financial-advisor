"""
Recommendations component for the Streamlit UI.

Displays AI-generated financial recommendations and advice history.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

def render_recommendations():
    """Render the simplified recommendations interface."""
    if not st.session_state.get('customer_id'):
        st.warning("No customer selected")
        return
    
    customer_id = st.session_state.customer_id
    
    st.markdown("## 🤖 AI Financial Analysis")
    
    # Single analysis button - Full Analysis only
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🚀 Run Full Financial Analysis", type="primary", use_container_width=True):
            # Create a progress container for better UX
            progress_container = st.container()
            with progress_container:
                st.info("🔄 Starting financial analysis...")
            
            with st.spinner("Running comprehensive financial analysis with multi-agent coordination..."):
                try:
                    recommendations = run_financial_analysis(customer_id)
                    if recommendations:
                        st.session_state.current_recommendations = recommendations
                        progress_container.empty()  # Clear the progress message
                        st.success("✅ Full analysis complete! View recommendations below.")
                        st.rerun()
                    else:
                        progress_container.empty()
                        st.error("❌ Analysis failed. Please try again.")
                except Exception as e:
                    progress_container.empty()
                    st.error(f"❌ Analysis failed: {str(e)}")
                    logger.error(f"Analysis error for customer {customer_id}: {e}")
    
    # Analysis description
    st.markdown("""
    **Full Analysis includes:**
    - 📊 **Spending Analysis**: Detailed transaction analysis and spending patterns
    - 🎯 **Goal Planning**: Financial goal evaluation and savings planning  
    - 💡 **Financial Advice**: Comprehensive recommendations and action items
    - 🔄 **Multi-Agent Coordination**: Step-by-step analysis using specialized agents
    """)
    
    # Display current recommendations if available
    if st.session_state.get('current_recommendations'):
        render_current_recommendations(st.session_state.current_recommendations)
    
    # Display advice history
    render_advice_history(customer_id)

def run_financial_analysis(customer_id: int) -> Optional[Dict[str, Any]]:
    """Run comprehensive financial analysis using ADK agents."""
    try:
        from utils.adk_agent_manager import run_full_analysis_adk
        import asyncio
        
        # Run the analysis using ADK agents
        result = asyncio.run(run_full_analysis_adk(customer_id))
        
        if result and result.get('status') == 'success':
            # Save the advice to database
            save_advice_to_db(customer_id, result)
            return {
                'analysis_type': 'full',
                'customer_id': customer_id,
                'agent_used': result.get('agent_used', 'SequencerAgent'),
                'result': result.get('result'),
                'timestamp': datetime.now().isoformat()
            }
        else:
            st.error(f"Analysis failed: {result.get('error', 'Unknown error')}")
            return None
            
    except Exception as e:
        st.error(f"Error running analysis: {str(e)}")
        logger.error(f"Error in run_financial_analysis: {str(e)}")
        return None


def save_advice_to_db(customer_id: int, advice_data: Dict[str, Any]) -> bool:
    """Save financial advice to database via database client."""
    try:
        from utils.database_client import save_advice
        
        # Extract key information from ADK agent result
        agent_used = advice_data.get('agent_used', 'SequencerAgent')
        analysis_type = advice_data.get('analysis_type', 'full')
        result_data = advice_data.get('result', {})
        
        # Create advice summary from ADK agent result
        if isinstance(result_data, dict):
            # Use the actual summary from agent outputs
            advice_summary = result_data.get('summary', f'{analysis_type.title()} analysis completed using {agent_used}')
            
            # Extract agent summaries (the actual generated content)
            agent_summaries = result_data.get('agent_summaries', {})
            agent_outputs = result_data.get('agent_outputs', {})
            spending_analysis = result_data.get('spending_analysis', {})
            goal_planning = result_data.get('goal_planning', {})
            financial_advice = result_data.get('financial_advice', {})
            
            # Extract recommendations from agent summaries or structured outputs
            recommendations = []
            if agent_summaries:
                # Use agent summaries for recommendations
                for agent_name, summaries in agent_summaries.items():
                    if summaries and 'recommendation' in ' '.join(summaries).lower():
                        recommendations.extend(summaries)
            elif isinstance(financial_advice, dict):
                recommendations = financial_advice.get('recommendations', [])
            elif isinstance(financial_advice, str) and 'recommendation' in financial_advice.lower():
                recommendations = [financial_advice]
        else:
            # If result is a string or other format
            advice_summary = f'{analysis_type.title()} analysis completed using {agent_used}'
            recommendations = []
            agent_summaries = {}
            spending_analysis = {}
            goal_planning = {}
            financial_advice = {}
        
        # Create detailed advice content from actual agent summaries
        advice_content = f"""
{advice_summary}

**Analysis Type:** {analysis_type.title()}
**Agent Used:** {agent_used}

**Key Recommendations:**
{chr(10).join([f"• {rec}" for rec in recommendations[:5]]) if recommendations else "• No specific recommendations available"}

**Individual Agent Summaries:**
{self._format_agent_summaries(agent_summaries) if agent_summaries else "• No agent summaries available"}

**Structured Analysis:**
**Spending Analysis:** {self._format_agent_output(spending_analysis) if spending_analysis else "• No spending analysis available"}

**Goal Planning:** {self._format_agent_output(goal_planning) if goal_planning else "• No goal planning available"}

**Financial Advice:** {self._format_agent_output(financial_advice) if financial_advice else "• No financial advice available"}
        """.strip()
        
        success = save_advice(
            customer_id=customer_id,
            advice_type=f'{analysis_type}_analysis',
            advice_content=advice_content,
            agent_name=agent_used,
            confidence_score=0.85
        )
        
        if success:
            logger.info(f"Advice saved successfully for customer {customer_id} using {agent_used}")
            return True
        else:
            logger.error("Failed to save advice to database")
            return False
            
    except Exception as e:
        logger.error(f"Error saving advice: {e}")
        return False

def render_current_recommendations(recommendations: Dict[str, Any]):
    """Render current analysis recommendations."""
    st.markdown("### 📊 Current Analysis Results")
    
    # Analysis info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        analysis_type = recommendations.get('analysis_type', 'full')
        st.metric("Analysis Type", analysis_type.title())
    
    with col2:
        agent_used = recommendations.get('agent_used', 'SequencerAgent')
        st.metric("Agent Used", agent_used)
    
    with col3:
        timestamp = recommendations.get('timestamp', 'Unknown')
        if timestamp != 'Unknown':
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                formatted_time = dt.strftime('%Y-%m-%d %H:%M')
                st.metric("Completed", formatted_time)
            except:
                st.metric("Completed", "Unknown")
        else:
            st.metric("Completed", "Unknown")
    
    # Get the actual result data (needed for both paths)
    result_data = recommendations.get('result', {})
    
    # Get the newly created advice records from database
    customer_id = recommendations.get('customer_id')
    if customer_id:
        st.markdown("#### 🆕 Newly Generated Advice")
        
        # Get the most recent advice records (last 5)
        try:
            from utils.database_client import get_advice_history
            recent_advice = get_advice_history(customer_id)
            
            if recent_advice:
                # Show only the most recent 3-5 records
                display_count = min(5, len(recent_advice))
                for i, advice in enumerate(recent_advice[:display_count]):
                    with st.expander(f"📋 {advice.get('advice_type', 'Advice').replace('_', ' ').title()} - {advice.get('agent_name', 'Unknown Agent')}", expanded=(i == 0)):
                        if advice.get('advice_content'):
                            st.markdown(advice['advice_content'])
                        else:
                            st.info("No detailed content available for this advice record.")
                        
                        # Show metadata
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if advice.get('confidence_score'):
                                st.caption(f"Confidence: {float(advice['confidence_score'])*100:.0f}%")
                        with col2:
                            if advice.get('created_at'):
                                st.caption(f"Generated: {advice['created_at']}")
                        with col3:
                            st.caption(f"Agent: {advice.get('agent_name', 'Unknown')}")
            else:
                st.info("No advice records found. The analysis may still be processing.")
        except Exception as e:
            st.error(f"Unable to load advice records: {str(e)}")
            logger.error(f"Error loading advice records: {e}")
    
    # Fallback: Show summary if no database records
    else:
        if isinstance(result_data, dict) and result_data.get('summary'):
            st.info(f"**Summary:** {result_data['summary']}")
        elif isinstance(result_data, str):
            st.info(f"**Analysis Result:** {result_data}")
    
    # Key metrics (if available in result)
    if isinstance(result_data, dict):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'spending_score' in result_data:
                st.metric(
                    "Spending Score",
                    f"{result_data['spending_score']}/10",
                    help="AI assessment of spending habits"
                )
        
        with col2:
            if 'savings_score' in result_data:
                st.metric(
                    "Savings Score", 
                    f"{result_data['savings_score']}/10",
                    help="AI assessment of savings behavior"
                )
        
        with col3:
            if 'overall_score' in result_data:
                st.metric(
                    "Overall Score",
                    f"{result_data['overall_score']}/10",
                    help="Overall financial health score"
                )
        
        # Recommendations
        if result_data.get('recommendations'):
            st.markdown("#### 🎯 Key Recommendations")
            
            for i, rec in enumerate(result_data['recommendations'], 1):
                st.markdown(f"**{i}.** {rec}")
        
        # Spending analysis
        if result_data.get('spending_analysis'):
            st.markdown("#### 💰 Spending Analysis")
            
            spending_data = result_data['spending_analysis']
            
            col1, col2 = st.columns(2)
            
            with col1:
                if 'top_categories' in spending_data:
                    st.markdown("**Top Spending Categories:**")
                    for category, amount in spending_data['top_categories'][:3]:
                        st.write(f"• {category}: ${amount:,.0f}")
            
            with col2:
                if 'monthly_trend' in spending_data:
                    trend = spending_data['monthly_trend']
                    st.markdown("**Monthly Trend:**")
                    st.write(f"• {trend}")
        
        # Goal analysis
        if result_data.get('goal_analysis'):
            st.markdown("#### 🎯 Goal Analysis")
            
            goal_data = result_data['goal_analysis']
            
            col1, col2 = st.columns(2)
            
            with col1:
                if 'goals_on_track' in goal_data:
                    st.metric(
                        "Goals On Track",
                        goal_data['goals_on_track'],
                        help="Number of goals meeting their targets"
                    )
            
            with col2:
                if 'goals_behind' in goal_data:
                    st.metric(
                        "Goals Behind",
                        goal_data['goals_behind'],
                        help="Number of goals needing attention"
                    )
        
        # Action items
        if result_data.get('action_items'):
            st.markdown("#### ⚡ Immediate Action Items")
            
            for action in result_data['action_items']:
                st.markdown(f"• **{action['priority']}:** {action['description']}")
    
    # Display raw result if it's a string
    elif isinstance(result_data, str):
        st.markdown("#### 📋 Analysis Details")
        st.text_area("Full Analysis Result", result_data, height=200)
    
    # Note: Recommendations are automatically saved to history when generated
    # No manual save button needed - this improves UX by removing confusion

# Removed save_recommendations_to_history function - was a placeholder
# Recommendations are automatically saved when generated via save_advice_to_db()

def _format_agent_output(agent_output: Any) -> str:
    """Format agent output for display in advice content."""
    if isinstance(agent_output, dict):
        # Extract key information from structured output
        if 'summary' in agent_output:
            return f"• {agent_output['summary']}"
        elif 'recommendations' in agent_output:
            recs = agent_output['recommendations']
            if isinstance(recs, list):
                return chr(10).join([f"• {rec}" for rec in recs[:3]])
            else:
                return f"• {recs}"
        else:
            # Format key-value pairs
            items = list(agent_output.items())[:3]
            return chr(10).join([f"• {key}: {value}" for key, value in items])
    elif isinstance(agent_output, str):
        # Truncate long strings
        if len(agent_output) > 200:
            return f"• {agent_output[:200]}..."
        else:
            return f"• {agent_output}"
    else:
        return f"• {str(agent_output)[:100]}..."

def _format_agent_summaries(agent_summaries: Dict[str, list]) -> str:
    """Format agent summaries for display in advice content."""
    if not agent_summaries:
        return "• No agent summaries available"
    
    formatted_summaries = []
    for agent_name, summaries in agent_summaries.items():
        if summaries:
            # Join all summaries from this agent
            agent_summary = "\n".join(summaries)
            # Truncate if too long
            if len(agent_summary) > 300:
                agent_summary = agent_summary[:300] + "..."
            formatted_summaries.append(f"**{agent_name}:**\n{agent_summary}")
    
    return "\n\n".join(formatted_summaries) if formatted_summaries else "• No agent summaries available"

def clear_old_advice_records(customer_id: int) -> bool:
    """Clear advice records older than 30 days."""
    try:
        from utils.database_client import clear_old_advice_records
        return clear_old_advice_records(customer_id)
    except Exception as e:
        logger.error(f"Error clearing old advice records: {e}")
        return False

def clear_all_advice_records(customer_id: int) -> bool:
    """Clear all advice records for a customer."""
    try:
        from utils.database_client import clear_all_advice_records
        return clear_all_advice_records(customer_id)
    except Exception as e:
        logger.error(f"Error clearing all advice records: {e}")
        return False

def render_advice_history(customer_id: int):
    """Render advice history from database."""
    st.markdown("### 📚 Advice History")
    
    # Add cleanup controls at the top
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("Manage your advice history:")
    
    with col2:
        if st.button("🗑️ Clear Old Records", help="Remove advice records older than 30 days"):
            if clear_old_advice_records(customer_id):
                st.success("✅ Old advice records cleared!")
                st.rerun()
            else:
                st.error("❌ Failed to clear old records")
    
    with col3:
        if st.button("🧹 Clear All", help="Remove all advice records (use with caution)"):
            if st.session_state.get('confirm_clear_all', False):
                if clear_all_advice_records(customer_id):
                    st.success("✅ All advice records cleared!")
                    st.session_state.confirm_clear_all = False
                    st.rerun()
                else:
                    st.error("❌ Failed to clear all records")
            else:
                st.session_state.confirm_clear_all = True
                st.warning("⚠️ Click again to confirm clearing ALL advice records")
    
    # Show loading state while fetching advice history
    with st.spinner("Loading advice history..."):
        advice_history = get_advice_history_from_db(customer_id)
    
    if not advice_history:
        st.info("No previous advice found. Run your first analysis above!")
        
        # Add retry button if there was an error
        if st.button("🔄 Retry Loading Advice History", key="retry_advice_history"):
            st.rerun()
        return
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        advice_type_filter = st.selectbox(
            "Filter by Type",
            options=["All"] + list(set([advice.get('advice_type', 'Unknown') for advice in advice_history])),
            help="Filter advice by type"
        )
    
    with col2:
        date_filter = st.selectbox(
            "Filter by Date",
            options=["All", "Last 7 days", "Last 30 days", "Last 90 days"],
            help="Filter advice by recency"
        )
    
    # Apply filters
    filtered_advice = apply_advice_filters(advice_history, advice_type_filter, date_filter)
    
    if not filtered_advice:
        st.info("No advice matches the selected filters.")
        return
    
    # Show summary of filtered results
    st.info(f"📊 Showing {len(filtered_advice)} of {len(advice_history)} advice records")
    
    # Display filtered advice
    for advice in filtered_advice:
        render_advice_card(advice)

def get_advice_history_from_db(customer_id: int) -> List[Dict[str, Any]]:
    """Get advice history from database via database client."""
    try:
        from utils.database_client import get_advice_history
        
        advice_list = get_advice_history(customer_id)
        
        logger.info(f"Retrieved {len(advice_list)} advice records for customer {customer_id}")
        return advice_list
            
    except Exception as e:
        logger.error(f"Error getting advice history for customer {customer_id}: {e}")
        # Show user-friendly error message
        st.error(f"❌ Unable to load advice history. Please try refreshing the page.")
        st.caption(f"Technical details: {str(e)[:100]}...")
        return []

def parse_advice_date(date_str: str) -> date:
    """Parse advice date string with multiple format support."""
    if not date_str:
        return date.min
    
    try:
        # Try parsing as datetime first (with time component)
        if 'T' in date_str or ' ' in date_str:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00')).date()
        else:
            # Try parsing as date only
            return datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        # Return earliest date if parsing fails
        return date.min

def apply_advice_filters(
    advice_history: List[Dict[str, Any]], 
    advice_type_filter: str, 
    date_filter: str
) -> List[Dict[str, Any]]:
    """Apply filters to advice history."""
    filtered = advice_history
    
    # Filter by type
    if advice_type_filter != "All":
        filtered = [a for a in filtered if a.get('advice_type') == advice_type_filter]
    
    # Filter by date
    if date_filter != "All":
        today = date.today()
        
        if date_filter == "Last 7 days":
            cutoff_date = today.replace(day=today.day - 7)
        elif date_filter == "Last 30 days":
            cutoff_date = today.replace(day=today.day - 30)
        elif date_filter == "Last 90 days":
            cutoff_date = today.replace(day=today.day - 90)
        else:
            cutoff_date = today
        
        filtered = [
            a for a in filtered 
            if a.get('created_at') and parse_advice_date(a['created_at']) >= cutoff_date
        ]
    
    return filtered

def render_advice_card(advice: Dict[str, Any]):
    """Render individual advice card."""
    with st.container():
        st.markdown("---")
        
        # Header with type and date
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            advice_type = advice.get('advice_type', 'Unknown').replace('_', ' ').title()
            st.markdown(f"#### 🤖 {advice_type}")
        
        with col2:
            if advice.get('confidence_score'):
                confidence = advice['confidence_score']
                if confidence >= 0.8:
                    confidence_icon = "🟢"
                elif confidence >= 0.6:
                    confidence_icon = "🟡"
                else:
                    confidence_icon = "🔴"
                
                st.metric(
                    "Confidence",
                    f"{confidence*100:.0f}%",
                    help="AI confidence in this advice"
                )
        
        with col3:
            if advice.get('created_at'):
                try:
                    created_at = advice['created_at']
                    if isinstance(created_at, str):
                        created_date = parse_advice_date(created_at)
                    elif isinstance(created_at, datetime):
                        created_date = created_at.date()
                    elif hasattr(created_at, 'date'):
                        created_date = created_at.date()
                    else:
                        created_date = None
                    
                    if created_date:
                        days_ago = (date.today() - created_date).days
                        
                        if days_ago == 0:
                            st.write("**Today**")
                        elif days_ago == 1:
                            st.write("**Yesterday**")
                        else:
                            st.write(f"**{days_ago} days ago**")
                    else:
                        st.write("**Unknown date**")
                except (ValueError, TypeError, AttributeError):
                    st.write("**Invalid date**")
        
        # Advice content
        if advice.get('advice_content'):
            st.markdown("**Advice:**")
            st.write(advice['advice_content'])
        
        # Agent information
        if advice.get('agent_name'):
            st.caption(f"Generated by: {advice['agent_name']}")
        
        # Action buttons - Removed non-functional buttons for better UX
        # (Copy, Rate, Re-run buttons were placeholders and have been removed)

# Removed show_rating_dialog function - was a placeholder

def render_quick_insights(customer_id: int):
    """Render quick financial insights."""
    st.markdown("### 💡 Quick Insights")
    
    # Get recent transactions and goals for quick analysis
    try:
        from utils.database_client import get_transactions_by_customer, get_financial_goals
        
        # Get recent transactions
        transactions_result = get_transactions_by_customer(customer_id=customer_id, limit=10)
        recent_transactions = transactions_result.get('transactions', []) if transactions_result.get('success') else []
        
        # Get goals
        goals_result = get_financial_goals(customer_id=customer_id)
        goals = goals_result.get('goals', []) if goals_result.get('success') else []
        
        if recent_transactions or goals:
            col1, col2 = st.columns(2)
            
            with col1:
                if recent_transactions:
                    st.markdown("**Recent Spending:**")
                    total_recent = sum(t.get('amount', 0) for t in recent_transactions)
                    st.metric("Last 10 transactions", f"${total_recent:,.2f}")
                    
                    # Show top category
                    if recent_transactions:
                        categories = {}
                        for t in recent_transactions:
                            cat = t.get('category', 'Unknown')
                            categories[cat] = categories.get(cat, 0) + t.get('amount', 0)
                        
                        if categories:
                            top_category = max(categories.items(), key=lambda x: x[1])
                            st.write(f"Top category: **{top_category[0]}** (${top_category[1]:,.2f})")
            
            with col2:
                if goals:
                    st.markdown("**Goal Progress:**")
                    active_goals = len([g for g in goals if g.get('current_amount', 0) < g.get('target_amount', 0)])
                    completed_goals = len([g for g in goals if g.get('current_amount', 0) >= g.get('target_amount', 0)])
                    
                    st.metric("Active Goals", active_goals)
                    st.metric("Completed Goals", completed_goals)
                    
                    if active_goals > 0:
                        avg_progress = sum(
                            min(g.get('current_amount', 0) / g.get('target_amount', 1), 1.0) 
                            for g in goals if g.get('current_amount', 0) < g.get('target_amount', 0)
                        ) / active_goals * 100
                        
                        st.metric("Avg Progress", f"{avg_progress:.1f}%")
        else:
            st.info("No recent data available for quick insights.")
            
    except Exception as e:
        logger.error(f"Error getting quick insights: {e}")
        st.error("Failed to load quick insights")
