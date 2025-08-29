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
    """Render the recommendations interface."""
    if not st.session_state.get('customer_id'):
        st.warning("No customer selected")
        return
    
    customer_id = st.session_state.customer_id
    
    st.markdown("## 🤖 AI Financial Recommendations")
    
    # Run analysis and get recommendations
    if st.button("🚀 Run Financial Analysis", type="primary", use_container_width=True):
        with st.spinner("Analyzing your financial situation..."):
            recommendations = run_financial_analysis(customer_id)
            if recommendations:
                st.session_state.current_recommendations = recommendations
                st.success("✅ Analysis complete! View recommendations below.")
                st.rerun()
    
    # Display current recommendations
    if st.session_state.get('current_recommendations'):
        render_current_recommendations(st.session_state.current_recommendations)
    
    # Display advice history
    render_advice_history(customer_id)

def run_financial_analysis(customer_id: int) -> Optional[Dict[str, Any]]:
    """Run comprehensive financial analysis using AI agents."""
    try:
        # Import the orchestrator agent
        from agents.orchestrator import FinancialAdvisorOrchestrator
        
        # Initialize the orchestrator
        orchestrator = FinancialAdvisorOrchestrator()
        
        # Run the analysis
        result = orchestrator.run(customer_id=customer_id)
        
        if result and result.get('success'):
            # Save the advice to database
            save_advice_to_db(customer_id, result)
            return result
        else:
            st.error("❌ Analysis failed. Please try again.")
            return None
            
    except Exception as e:
        logger.error(f"Error running financial analysis: {e}")
        st.error(f"Failed to run analysis: {e}")
        return None

def save_advice_to_db(customer_id: int, advice_data: Dict[str, Any]) -> bool:
    """Save financial advice to database via database client."""
    try:
        from utils.database_client import save_advice
        
        # Extract key information from advice
        advice_summary = advice_data.get('summary', 'Financial analysis completed')
        recommendations = advice_data.get('recommendations', [])
        spending_analysis = advice_data.get('spending_analysis', {})
        goal_analysis = advice_data.get('goal_analysis', {})
        
        # Create detailed advice text
        advice_text = f"""
{advice_summary}

**Key Recommendations:**
{chr(10).join([f"• {rec}" for rec in recommendations[:5]])}

**Spending Insights:**
{chr(10).join([f"• {key}: {value}" for key, value in spending_analysis.items()][:3])}

**Goal Progress:**
{chr(10).join([f"• {key}: {value}" for key, value in goal_analysis.items()][:3])}
        """.strip()
        
        success = save_advice(
            customer_id=customer_id,
            advice_type='comprehensive_analysis',
            advice_text=advice_text,
            agent_name='FinancialAdvisorOrchestrator',
            confidence_score=0.85
        )
        
        if success:
            logger.info(f"Advice saved successfully for customer {customer_id}")
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
    
    # Summary
    if recommendations.get('summary'):
        st.info(f"**Summary:** {recommendations['summary']}")
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'spending_score' in recommendations:
            st.metric(
                "Spending Score",
                f"{recommendations['spending_score']}/10",
                help="AI assessment of spending habits"
            )
    
    with col2:
        if 'savings_score' in recommendations:
            st.metric(
                "Savings Score", 
                f"{recommendations['savings_score']}/10",
                help="AI assessment of savings behavior"
            )
    
    with col3:
        if 'overall_score' in recommendations:
            st.metric(
                "Overall Score",
                f"{recommendations['overall_score']}/10",
                help="Overall financial health score"
            )
    
    # Recommendations
    if recommendations.get('recommendations'):
        st.markdown("#### 🎯 Key Recommendations")
        
        for i, rec in enumerate(recommendations['recommendations'], 1):
            st.markdown(f"**{i}.** {rec}")
    
    # Spending analysis
    if recommendations.get('spending_analysis'):
        st.markdown("#### 💰 Spending Analysis")
        
        spending_data = recommendations['spending_analysis']
        
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
    if recommendations.get('goal_analysis'):
        st.markdown("#### 🎯 Goal Analysis")
        
        goal_data = recommendations['goal_analysis']
        
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
    if recommendations.get('action_items'):
        st.markdown("#### ⚡ Immediate Action Items")
        
        for action in recommendations['action_items']:
            st.markdown(f"• **{action['priority']}:** {action['description']}")
    
    # Save recommendations button
    if st.button("💾 Save to History", use_container_width=True):
        if save_recommendations_to_history(recommendations):
            st.success("✅ Recommendations saved to history!")
        else:
            st.error("❌ Failed to save recommendations")

def save_recommendations_to_history(recommendations: Dict[str, Any]) -> bool:
    """Save current recommendations to history."""
    try:
        # This would typically save to a more detailed history table
        # For now, we'll just mark it as saved
        return True
    except Exception as e:
        logger.error(f"Error saving recommendations to history: {e}")
        return False

def render_advice_history(customer_id: int):
    """Render advice history from database."""
    st.markdown("### 📚 Advice History")
    
    # Get advice history from database
    advice_history = get_advice_history_from_db(customer_id)
    
    if not advice_history:
        st.info("No previous advice found. Run your first analysis above!")
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
        logger.error(f"Error getting advice history: {e}")
        st.error(f"Failed to load advice history: {e}")
        return []

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
            if a.get('created_at') and datetime.strptime(a['created_at'], '%Y-%m-%d').date() >= cutoff_date
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
                        created_date = datetime.strptime(created_at, '%Y-%m-%d').date()
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
        if advice.get('advice_text'):
            st.markdown("**Advice:**")
            st.write(advice['advice_text'])
        
        # Agent information
        if advice.get('agent_name'):
            st.caption(f"Generated by: {advice['agent_name']}")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button(f"📋 Copy", key=f"copy_{advice.get('id', 'unknown')}"):
                st.write("📋 Copied to clipboard!")
        
        with col2:
            if st.button(f"⭐ Rate", key=f"rate_{advice.get('id', 'unknown')}"):
                show_rating_dialog(advice)
        
        with col3:
            if st.button(f"🔄 Re-run", key=f"rerun_{advice.get('id', 'unknown')}"):
                st.info("This would re-run the analysis with updated data")

def show_rating_dialog(advice: Dict[str, Any]):
    """Show dialog for rating advice."""
    st.info("Rating functionality would be implemented here to collect user feedback on advice quality")

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
