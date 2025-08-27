"""
Recommendations component for the Streamlit UI.

Displays AI-generated financial recommendations and advice from the agents.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

def render_recommendations():
    """Render the AI recommendations interface."""
    if not st.session_state.get('customer_id'):
        st.warning("No customer selected")
        return
    
    # Check if we have recent analysis results
    analysis_results = st.session_state.get('last_analysis_results')
    
    if not analysis_results:
        render_no_recommendations()
        return
    
    # Display recommendations based on analysis type
    if analysis_results['type'] == 'full':
        render_comprehensive_recommendations(analysis_results)
    elif analysis_results['type'] == 'quick':
        render_quick_recommendations(analysis_results)
    elif analysis_results['type'] == 'goal_focused':
        render_goal_recommendations(analysis_results)
    
    # Always show advice history
    render_advice_history()

def render_no_recommendations():
    """Render interface when no recommendations are available."""
    st.info("🤖 No AI recommendations available yet. Run an analysis to get personalized financial advice!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Run Full Analysis", use_container_width=True):
            st.session_state.analysis_running = True
            st.rerun()
    
    with col2:
        if st.button("⚡ Get Quick Insights", use_container_width=True):
            # Trigger quick analysis
            st.info("Quick analysis feature would be triggered here")
    
    with col3:
        if st.button("🎯 Analyze Goals", use_container_width=True):
            # Trigger goal analysis
            st.info("Goal analysis feature would be triggered here")
    
    # Show sample recommendations for demonstration
    render_sample_recommendations()

def render_comprehensive_recommendations(results: Dict[str, Any]):
    """Render comprehensive financial recommendations."""
    st.markdown("### 💡 Comprehensive Financial Recommendations")
    
    # Analysis summary
    render_analysis_summary(results)
    
    # Priority recommendations
    render_priority_recommendations()
    
    # Detailed recommendations by category
    render_detailed_recommendations()
    
    # Implementation timeline
    render_implementation_timeline()

def render_quick_recommendations(results: Dict[str, Any]):
    """Render quick insights and recommendations."""
    st.markdown("### ⚡ Quick Financial Insights")
    
    insights = results.get('insights', [])
    
    if insights:
        st.markdown("#### 🔍 Key Insights")
        for i, insight in enumerate(insights, 1):
            st.markdown(f"**{i}.** {insight}")
    
    # Quick action items
    render_quick_actions()

def render_goal_recommendations(results: Dict[str, Any]):
    """Render goal-focused recommendations."""
    st.markdown("### 🎯 Goal-Focused Recommendations")
    
    analysis = results.get('goal_analysis', {})
    
    if analysis:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Goals On Track", analysis.get('on_track', 0))
        with col2:
            st.metric("Goals Behind", analysis.get('behind', 0))
        with col3:
            st.metric("Recommendations", analysis.get('recommendations', 0))
    
    # Goal-specific recommendations
    render_goal_specific_recommendations()

def render_analysis_summary(results: Dict[str, Any]):
    """Render analysis summary."""
    st.markdown("#### 📊 Analysis Summary")
    
    summary = results.get('summary', {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Spending Health",
            summary.get('spending_health', 'N/A'),
            help="Overall assessment of spending patterns"
        )
    
    with col2:
        st.metric(
            "Goal Feasibility", 
            summary.get('goal_feasibility', 'N/A'),
            help="How achievable your financial goals are"
        )
    
    with col3:
        st.metric(
            "Priority Actions",
            summary.get('priority_actions', 0),
            help="Number of high-priority recommendations"
        )
    
    with col4:
        savings_potential = summary.get('savings_potential', 0)
        st.metric(
            "Savings Potential",
            f"${savings_potential:.0f}/mo",
            help="Estimated monthly savings opportunity"
        )

def render_priority_recommendations():
    """Render priority recommendations."""
    st.markdown("#### 🚨 Priority Actions")
    
    # Mock priority recommendations (in real app, from agent analysis)
    priority_recommendations = [
        {
            'title': 'Reduce Dining Out Expenses',
            'description': 'Your dining expenses are 25% above recommended levels. Consider meal planning and cooking at home more often.',
            'impact': 'High',
            'effort': 'Medium',
            'savings': 200.0,
            'timeline': '30 days',
            'category': 'spending'
        },
        {
            'title': 'Increase Emergency Fund Contributions',
            'description': 'Your emergency fund covers only 2.1 months of expenses. Aim for 3-6 months coverage.',
            'impact': 'High',
            'effort': 'Low',
            'savings': -150.0,  # Negative because it\'s an investment
            'timeline': '12 months',
            'category': 'savings'
        },
        {
            'title': 'Optimize Transportation Costs',
            'description': 'Consider carpooling or public transport for daily commute to reduce gas and parking expenses.',
            'impact': 'Medium',
            'effort': 'Medium',
            'savings': 75.0,
            'timeline': '60 days',
            'category': 'spending'
        }
    ]
    
    for i, rec in enumerate(priority_recommendations, 1):
        render_recommendation_card(rec, i)

def render_recommendation_card(rec: Dict[str, Any], index: int):
    """Render a single recommendation card."""
    # Determine colors based on impact and category
    impact_colors = {
        'High': '#ff4444',
        'Medium': '#ffaa00', 
        'Low': '#44aa44'
    }
    
    category_icons = {
        'spending': '💸',
        'savings': '💰',
        'investment': '📈',
        'debt': '💳',
        'goals': '🎯'
    }
    
    impact_color = impact_colors.get(rec['impact'], '#666666')
    category_icon = category_icons.get(rec['category'], '💡')
    
    with st.expander(f"{index}. {category_icon} {rec['title']} - {rec['impact']} Impact", expanded=True):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**Description:** {rec['description']}")
            st.markdown(f"**Timeline:** {rec['timeline']}")
            
            # Progress indicator (mock)
            if st.button(f"✅ Mark as Completed", key=f"complete_{index}"):
                st.success("Recommendation marked as completed!")
        
        with col2:
            st.markdown(f"**Impact:** {rec['impact']}")
            st.markdown(f"**Effort:** {rec['effort']}")
            
            if rec['savings'] > 0:
                st.metric("Monthly Savings", f"+${rec['savings']:.0f}")
            elif rec['savings'] < 0:
                st.metric("Monthly Investment", f"${abs(rec['savings']):.0f}")
            
            # Action button
            if st.button(f"📋 Create Action Plan", key=f"plan_{index}"):
                show_action_plan(rec)

def render_detailed_recommendations():
    """Render detailed recommendations by category."""
    st.markdown("#### 📝 Detailed Recommendations")
    
    categories = {
        'Spending Optimization': [
            'Review subscription services and cancel unused ones',
            'Negotiate better rates for insurance and utilities',
            'Use cashback credit cards for regular purchases',
            'Set up automatic transfers to prevent overspending'
        ],
        'Goal Achievement': [
            'Increase emergency fund contributions by $100/month',
            'Set up automatic savings for vacation goal',
            'Consider high-yield savings account for short-term goals',
            'Review and adjust goal timelines based on current capacity'
        ],
        'Investment Strategy': [
            'Maximize employer 401(k) matching',
            'Consider opening a Roth IRA for tax-free growth',
            'Diversify investment portfolio across asset classes',
            'Review investment fees and consider low-cost index funds'
        ],
        'Risk Management': [
            'Review life insurance coverage adequacy',
            'Ensure adequate emergency fund before investing',
            'Consider disability insurance if not covered by employer',
            'Review and update beneficiaries on all accounts'
        ]
    }
    
    for category, recommendations in categories.items():
        with st.expander(f"📊 {category}", expanded=False):
            for rec in recommendations:
                st.markdown(f"• {rec}")

def render_implementation_timeline():
    """Render implementation timeline for recommendations."""
    st.markdown("#### 📅 Implementation Timeline")
    
    timeline_data = [
        {'Period': '0-30 Days', 'Actions': 'Reduce dining out, cancel unused subscriptions', 'Impact': '$200/month'},
        {'Period': '1-3 Months', 'Actions': 'Optimize transportation, increase emergency fund', 'Impact': '$225/month'},
        {'Period': '3-6 Months', 'Actions': 'Review insurance, set up investment accounts', 'Impact': '$250/month'},
        {'Period': '6-12 Months', 'Actions': 'Maximize retirement contributions, goal review', 'Impact': '$300/month'}
    ]
    
    df = pd.DataFrame(timeline_data)
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Period": st.column_config.TextColumn("Time Period"),
            "Actions": st.column_config.TextColumn("Key Actions"),
            "Impact": st.column_config.TextColumn("Expected Impact")
        }
    )

def render_quick_actions():
    """Render quick actionable items."""
    st.markdown("#### ⚡ Quick Actions")
    
    quick_actions = [
        {
            'action': 'Set up automatic savings transfer',
            'time': '5 minutes',
            'impact': 'High',
            'description': 'Automate $200 monthly transfer to savings'
        },
        {
            'action': 'Review and cancel subscriptions',
            'time': '15 minutes', 
            'impact': 'Medium',
            'description': 'Check for unused streaming services and memberships'
        },
        {
            'action': 'Compare insurance rates',
            'time': '30 minutes',
            'impact': 'Medium', 
            'description': 'Get quotes for auto and home insurance'
        }
    ]
    
    for action in quick_actions:
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.markdown(f"**{action['action']}**")
            st.caption(action['description'])
        
        with col2:
            st.markdown(f"⏱️ {action['time']}")
        
        with col3:
            impact_color = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
            st.markdown(f"{impact_color.get(action['impact'], '⚪')} {action['impact']}")
        
        with col4:
            if st.button("✅ Done", key=f"quick_{action['action']}"):
                st.success("Great job! 🎉")

def render_goal_specific_recommendations():
    """Render goal-specific recommendations."""
    st.markdown("#### 🎯 Goal-Specific Advice")
    
    # Get customer goals
    from ui.components.goal_management import get_customer_goals
    goals = get_customer_goals(st.session_state.customer_id)
    
    if not goals:
        st.info("No goals set yet. Create some goals to get specific recommendations!")
        return
    
    for goal in goals[:3]:  # Show top 3 goals
        with st.expander(f"🎯 {goal['goal_name']}", expanded=False):
            progress = (goal['current_amount'] / goal['target_amount'] * 100) if goal['target_amount'] > 0 else 0
            remaining = goal['target_amount'] - goal['current_amount']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Progress", f"{progress:.1f}%")
                st.metric("Remaining", f"${remaining:,.0f}")
            
            with col2:
                # Generate mock recommendations based on goal
                if goal['goal_type'] == 'savings':
                    st.markdown("**Recommendations:**")
                    st.markdown("• Consider high-yield savings account")
                    st.markdown("• Set up automatic monthly transfers")
                    st.markdown("• Track progress weekly")
                elif goal['goal_type'] == 'investment':
                    st.markdown("**Recommendations:**")
                    st.markdown("• Diversify across asset classes")
                    st.markdown("• Consider dollar-cost averaging")
                    st.markdown("• Review fees and expenses")

def render_advice_history():
    """Render historical advice and recommendations."""
    st.markdown("### 📚 Advice History")
    
    # Mock advice history (in real app, from database via MCP)
    advice_history = [
        {
            'date': '2024-03-01',
            'agent': 'AdvisorAgent',
            'type': 'Comprehensive Advice',
            'confidence': 0.92,
            'summary': 'Provided complete financial analysis with 5 priority recommendations'
        },
        {
            'date': '2024-02-15',
            'agent': 'SpendingAnalyzerAgent',
            'type': 'Spending Analysis',
            'confidence': 0.87,
            'summary': 'Identified dining expenses 20% above recommended levels'
        },
        {
            'date': '2024-02-01',
            'agent': 'GoalPlannerAgent',
            'type': 'Goal Planning',
            'confidence': 0.95,
            'summary': 'Evaluated feasibility of 4 financial goals, all achievable with adjustments'
        }
    ]
    
    if advice_history:
        df = pd.DataFrame(advice_history)
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        df['confidence'] = df['confidence'].apply(lambda x: f"{x*100:.0f}%")
        
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "date": st.column_config.TextColumn("Date"),
                "agent": st.column_config.TextColumn("AI Agent"),
                "type": st.column_config.TextColumn("Advice Type"),
                "confidence": st.column_config.TextColumn("Confidence"),
                "summary": st.column_config.TextColumn("Summary")
            }
        )
    else:
        st.info("No advice history available yet.")

def render_sample_recommendations():
    """Render sample recommendations for demonstration."""
    st.markdown("### 💡 Sample Recommendations")
    st.info("Here are some example recommendations our AI agents might provide:")
    
    sample_recommendations = [
        {
            'title': 'Build Emergency Fund',
            'description': 'Start with $500 and gradually build to 3-6 months of expenses',
            'category': 'Financial Security',
            'priority': 'High'
        },
        {
            'title': 'Track Spending Patterns',
            'description': 'Monitor expenses for 30 days to identify optimization opportunities',
            'category': 'Spending Analysis',
            'priority': 'Medium'
        },
        {
            'title': 'Set SMART Financial Goals',
            'description': 'Create specific, measurable, achievable, relevant, and time-bound goals',
            'category': 'Goal Planning',
            'priority': 'Medium'
        }
    ]
    
    for rec in sample_recommendations:
        priority_colors = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
        
        st.markdown(f"""
        **{priority_colors.get(rec['priority'], '⚪')} {rec['title']}** ({rec['category']})
        
        {rec['description']}
        """)

def show_action_plan(recommendation: Dict[str, Any]):
    """Show detailed action plan for a recommendation."""
    st.info(f"""
    **Action Plan for: {recommendation['title']}**
    
    This would show a detailed step-by-step plan including:
    • Specific steps to implement the recommendation
    • Resources and tools needed
    • Timeline and milestones
    • How to track progress
    • Expected outcomes and benefits
    """)

def render_recommendation_metrics():
    """Render metrics about recommendation effectiveness."""
    st.markdown("#### 📈 Recommendation Impact")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Recommendations Given", "12", delta="3 this month")
    
    with col2:
        st.metric("Actions Completed", "8", delta="67% completion rate")
    
    with col3:
        st.metric("Estimated Savings", "$450/mo", delta="+$125 from last month")
    
    with col4:
        st.metric("Goal Progress", "+15%", delta="Above target")

def export_recommendations():
    """Export recommendations to various formats."""
    st.markdown("#### 📥 Export Recommendations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export to PDF"):
            st.info("PDF export functionality would be implemented here")
    
    with col2:
        if st.button("📧 Email Summary"):
            st.info("Email functionality would be implemented here")
    
    with col3:
        if st.button("📱 Share Mobile"):
            st.info("Mobile sharing functionality would be implemented here")
