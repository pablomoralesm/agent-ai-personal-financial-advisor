"""
Utility functions for the Streamlit UI.
"""

import streamlit as st
from typing import Dict, Any, List, Optional
from datetime import datetime, date
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from financial_mcp.models import TransactionCategory, GoalType


def format_currency(amount: float) -> str:
    """Format currency for display."""
    return f"${amount:,.2f}"


def format_percentage(value: float) -> str:
    """Format percentage for display."""
    return f"{value:.1f}%"


def get_transaction_categories() -> List[str]:
    """Get list of available transaction categories."""
    return [category.value for category in TransactionCategory]


def get_goal_types() -> List[str]:
    """Get list of available goal types."""
    return [goal_type.value for goal_type in GoalType]


def create_spending_chart(spending_data: Dict[str, float]) -> go.Figure:
    """Create a pie chart for spending by category."""
    if not spending_data:
        return go.Figure()
    
    categories = list(spending_data.keys())
    amounts = list(spending_data.values())
    
    # Format category names for display
    formatted_categories = [cat.replace('_', ' ').title() for cat in categories]
    
    fig = px.pie(
        values=amounts,
        names=formatted_categories,
        title="Spending by Category",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Amount: $%{value:,.2f}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        showlegend=True,
        height=400,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig


def create_spending_trend_chart(transactions: List[Dict[str, Any]]) -> go.Figure:
    """Create a trend chart showing spending over time."""
    if not transactions:
        return go.Figure()
    
    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(transactions)
    
    # Filter out income transactions
    spending_df = df[df['is_income'] == False].copy()
    
    if spending_df.empty:
        return go.Figure()
    
    # Convert transaction_date to datetime
    spending_df['transaction_date'] = pd.to_datetime(spending_df['transaction_date'])
    
    # Group by date and sum spending
    daily_spending = spending_df.groupby('transaction_date')['amount'].sum().reset_index()
    
    fig = px.line(
        daily_spending,
        x='transaction_date',
        y='amount',
        title='Daily Spending Trend',
        labels={'transaction_date': 'Date', 'amount': 'Amount ($)'}
    )
    
    fig.update_traces(
        mode='lines+markers',
        hovertemplate='<b>%{x}</b><br>Spending: $%{y:,.2f}<extra></extra>'
    )
    
    fig.update_layout(
        height=400,
        margin=dict(t=50, b=50, l=50, r=50),
        xaxis_title="Date",
        yaxis_title="Amount ($)"
    )
    
    return fig


def create_goal_progress_chart(goals: List[Dict[str, Any]]) -> go.Figure:
    """Create a progress chart for financial goals."""
    if not goals:
        return go.Figure()
    
    goal_names = []
    current_amounts = []
    target_amounts = []
    progress_percentages = []
    
    for goal in goals:
        goal_names.append(goal.get('title', 'Unknown Goal'))
        current = float(goal.get('current_amount', 0))
        target = float(goal.get('target_amount', 1))
        current_amounts.append(current)
        target_amounts.append(target)
        progress_percentages.append((current / target) * 100 if target > 0 else 0)
    
    fig = go.Figure()
    
    # Add target amounts as background bars
    fig.add_trace(go.Bar(
        y=goal_names,
        x=target_amounts,
        orientation='h',
        name='Target Amount',
        marker_color='lightgray',
        opacity=0.6
    ))
    
    # Add current amounts as foreground bars
    fig.add_trace(go.Bar(
        y=goal_names,
        x=current_amounts,
        orientation='h',
        name='Current Amount',
        marker_color='steelblue'
    ))
    
    fig.update_layout(
        title='Goal Progress',
        xaxis_title='Amount ($)',
        yaxis_title='Goals',
        height=max(400, len(goals) * 60),
        margin=dict(t=50, b=50, l=150, r=50),
        barmode='overlay'
    )
    
    return fig


def create_financial_health_gauge(health_score: int) -> go.Figure:
    """Create a gauge chart for financial health score."""
    # Determine color based on score
    if health_score >= 80:
        color = "green"
    elif health_score >= 60:
        color = "yellow"
    else:
        color = "red"
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = health_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Financial Health Score"},
        delta = {'reference': 70},  # Reference value for comparison
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 40], 'color': "lightgray"},
                {'range': [40, 70], 'color': "gray"},
                {'range': [70, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig


def display_workflow_progress(workflow_status: Dict[str, Any]):
    """Display workflow execution progress."""
    if not workflow_status or workflow_status.get('error'):
        st.error("Unable to retrieve workflow status")
        return
    
    st.subheader("Analysis Progress")
    
    # Overall workflow status
    status = workflow_status.get('status', 'unknown')
    if status == 'completed':
        st.success("✅ Analysis completed successfully!")
    elif status == 'running':
        st.info("🔄 Analysis in progress...")
    elif status == 'failed':
        st.error("❌ Analysis failed")
    else:
        st.warning(f"Status: {status}")
    
    # Progress bar based on completed steps
    steps = workflow_status.get('steps', [])
    if steps:
        completed_steps = [s for s in steps if s['status'] == 'completed']
        progress = len(completed_steps) / len(steps)
        st.progress(progress)
        
        # Step details
        st.write("**Step Details:**")
        for step in steps:
            step_status = step['status']
            agent_name = step['agent']
            
            if step_status == 'completed':
                emoji = "✅"
            elif step_status == 'running':
                emoji = "🔄"
            elif step_status == 'failed':
                emoji = "❌"
            else:
                emoji = "⏳"
            
            st.write(f"{emoji} {agent_name}: {step_status}")
            
            if step.get('error'):
                st.error(f"Error: {step['error']}")


def display_agent_response(response: Dict[str, Any], title: str):
    """Display agent response in a formatted way."""
    st.subheader(title)
    
    # Confidence score
    confidence = response.get('confidence_score', 0)
    confidence_color = "green" if confidence >= 0.8 else "orange" if confidence >= 0.6 else "red"
    st.markdown(f"**Confidence:** <span style='color: {confidence_color}'>{confidence:.1%}</span>", 
                unsafe_allow_html=True)
    
    # Reasoning
    if response.get('reasoning'):
        st.write(f"**Analysis basis:** {response['reasoning']}")
    
    # Recommendations
    recommendations = response.get('recommendations', [])
    if recommendations:
        st.write("**Key Recommendations:**")
        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec}")
    
    # Additional data (expandable)
    with st.expander("View detailed analysis"):
        st.json(response.get('data', {}))


def display_adk_response(response: Dict[str, Any], title: str):
    """Display ADK agent response in a formatted way."""
    st.subheader(title)
    
    # Check if response was successful
    if not response.get('success', True):
        st.error(f"❌ Analysis failed: {response.get('error', 'Unknown error')}")
        return
    
    # Framework indicator
    st.info(f"🚀 Powered by Google ADK • Agent: {response.get('agent_name', 'Unknown')}")
    
    # Confidence score
    confidence = response.get('confidence_score', 0)
    if confidence > 0:
        confidence_color = "green" if confidence >= 0.8 else "orange" if confidence >= 0.6 else "red"
        st.markdown(f"**Confidence:** <span style='color: {confidence_color}'>{confidence:.1%}</span>", 
                    unsafe_allow_html=True)
    
    # Handle different response structures
    if 'analysis' in response:
        # Spending analysis format
        analysis = response['analysis']
        if isinstance(analysis, dict):
            if 'overall_assessment' in analysis:
                st.write(f"**Overall Assessment:** {analysis['overall_assessment']}")
            
            if 'spending_trends' in analysis:
                trends = analysis['spending_trends']
                if isinstance(trends, dict):
                    st.write(f"**Spending Trend:** {trends.get('trend', 'N/A')} (Confidence: {trends.get('confidence', 'N/A')})")
                    if 'details' in trends:
                        st.write(f"Details: {trends['details']}")
            
            if 'category_insights' in analysis and isinstance(analysis['category_insights'], list):
                st.write("**Category Insights:**")
                for insight in analysis['category_insights'][:5]:  # Show top 5
                    if isinstance(insight, dict):
                        st.write(f"• {insight.get('category', 'Unknown')}: ${insight.get('amount', 0):.2f} ({insight.get('percentage', 0):.1f}%)")
                        if 'insight' in insight:
                            st.write(f"  _{insight['insight']}_")
    
    elif 'goal_analysis' in response:
        # Goal planning format
        goal_analysis = response['goal_analysis']
        if isinstance(goal_analysis, dict):
            if 'feasibility_assessment' in goal_analysis:
                st.write(f"**Feasibility Assessment:** {goal_analysis['feasibility_assessment']}")
            
            if 'required_monthly_savings' in goal_analysis:
                st.write(f"**Required Monthly Savings:** ${goal_analysis['required_monthly_savings']:.2f}")
    
    elif 'overall_assessment' in response:
        # Comprehensive advice format
        assessment = response['overall_assessment']
        if isinstance(assessment, dict):
            if 'summary' in assessment:
                st.write(f"**Summary:** {assessment['summary']}")
            
            if 'key_strengths' in assessment and isinstance(assessment['key_strengths'], list):
                st.write("**Key Strengths:**")
                for strength in assessment['key_strengths']:
                    st.write(f"✅ {strength}")
            
            if 'primary_concerns' in assessment and isinstance(assessment['primary_concerns'], list):
                st.write("**Primary Concerns:**")
                for concern in assessment['primary_concerns']:
                    st.write(f"⚠️ {concern}")
    
    # Recommendations
    recommendations = response.get('recommendations', [])
    if recommendations:
        st.write("**Key Recommendations:**")
        if isinstance(recommendations, list):
            for i, rec in enumerate(recommendations[:5], 1):  # Show top 5
                if isinstance(rec, dict):
                    priority = rec.get('priority', 'medium')
                    action = rec.get('action', rec.get('recommendation', str(rec)))
                    priority_emoji = "🔴" if priority == "high" else "🟡" if priority == "medium" else "🟢"
                    st.write(f"{i}. {priority_emoji} {action}")
                else:
                    st.write(f"{i}. {rec}")
    
    # Action plan (for comprehensive advice)
    if 'prioritized_action_plan' in response and isinstance(response['prioritized_action_plan'], list):
        st.write("**Action Plan:**")
        for i, action in enumerate(response['prioritized_action_plan'][:5], 1):
            if isinstance(action, dict):
                priority = action.get('priority', i)
                action_text = action.get('action', 'No action specified')
                timeline = action.get('timeline', 'Not specified')
                st.write(f"{priority}. **{action_text}** _(Timeline: {timeline})_")
    
    # Additional data (expandable)
    with st.expander("View detailed ADK response"):
        st.json(response)


def validate_transaction_form(amount: float, category: str, description: str, 
                            transaction_date: date) -> List[str]:
    """Validate transaction form inputs."""
    errors = []
    
    if amount <= 0:
        errors.append("Amount must be greater than 0")
    
    if not category:
        errors.append("Category is required")
    
    if transaction_date > date.today():
        errors.append("Transaction date cannot be in the future")
    
    return errors


def validate_goal_form(title: str, target_amount: float, goal_type: str, 
                      target_date: Optional[date] = None) -> List[str]:
    """Validate goal form inputs."""
    errors = []
    
    if not title.strip():
        errors.append("Goal title is required")
    
    if target_amount <= 0:
        errors.append("Target amount must be greater than 0")
    
    if not goal_type:
        errors.append("Goal type is required")
    
    if target_date and target_date <= date.today():
        errors.append("Target date must be in the future")
    
    return errors


def load_custom_css():
    """Load custom CSS for better styling."""
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .warning-message {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.75rem;
        border-radius: 0.25rem;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 0.5rem;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    .agent-card {
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True)
