"""
Customer Profile component for the Streamlit UI.

Displays customer information, financial overview, and key metrics.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

def render_customer_profile():
    """Render the customer profile dashboard."""
    if not st.session_state.get('customer_id'):
        st.warning("No customer selected")
        return
    
    customer_id = st.session_state.customer_id
    
    # Mock customer data (in real app, this would come from database via MCP)
    customer_data = get_mock_customer_data(customer_id)
    
    # Customer header
    render_customer_header(customer_data)
    
    # Financial overview
    render_financial_overview(customer_data)
    
    # Charts and visualizations
    render_financial_charts(customer_data)

def get_mock_customer_data(customer_id: int) -> Dict[str, Any]:
    """Get mock customer data for demonstration."""
    customers = {
        1: {
            'name': 'Alice Johnson',
            'email': 'alice.johnson@email.com',
            'age': 39,
            'monthly_income': 5000.0,
            'monthly_expenses': 4200.0,
            'savings_rate': 16.0,
            'emergency_fund': 3000.0,
            'total_goals': 4,
            'goals_on_track': 3,
            'credit_score': 750,
            'recent_transactions': 45,
            'spending_categories': {
                'Housing': 1800,
                'Food & Dining': 600,
                'Transportation': 450,
                'Entertainment': 200,
                'Healthcare': 150,
                'Other': 300
            },
            'monthly_trends': [
                {'month': 'Jan', 'income': 5000, 'expenses': 4100, 'savings': 900},
                {'month': 'Feb', 'income': 5000, 'expenses': 4200, 'savings': 800},
                {'month': 'Mar', 'income': 5000, 'expenses': 4300, 'savings': 700},
            ]
        },
        2: {
            'name': 'Bob Smith',
            'email': 'bob.smith@email.com', 
            'age': 35,
            'monthly_income': 4200.0,
            'monthly_expenses': 3800.0,
            'savings_rate': 9.5,
            'emergency_fund': 1500.0,
            'total_goals': 2,
            'goals_on_track': 1,
            'credit_score': 680,
            'recent_transactions': 32,
            'spending_categories': {
                'Housing': 1200,
                'Food & Dining': 400,
                'Transportation': 300,
                'Entertainment': 250,
                'Healthcare': 100,
                'Other': 250
            },
            'monthly_trends': [
                {'month': 'Jan', 'income': 4200, 'expenses': 3700, 'savings': 500},
                {'month': 'Feb', 'income': 4200, 'expenses': 3800, 'savings': 400},
                {'month': 'Mar', 'income': 4200, 'expenses': 3900, 'savings': 300},
            ]
        },
        3: {
            'name': 'Carol Davis',
            'email': 'carol.davis@email.com',
            'age': 36,
            'monthly_income': 6500.0,
            'monthly_expenses': 5200.0,
            'savings_rate': 20.0,
            'emergency_fund': 8000.0,
            'total_goals': 3,
            'goals_on_track': 3,
            'credit_score': 810,
            'recent_transactions': 38,
            'spending_categories': {
                'Housing': 2200,
                'Food & Dining': 800,
                'Transportation': 600,
                'Entertainment': 300,
                'Healthcare': 200,
                'Other': 400
            },
            'monthly_trends': [
                {'month': 'Jan', 'income': 6500, 'expenses': 5100, 'savings': 1400},
                {'month': 'Feb', 'income': 6500, 'expenses': 5200, 'savings': 1300},
                {'month': 'Mar', 'income': 6500, 'expenses': 5300, 'savings': 1200},
            ]
        }
    }
    
    return customers.get(customer_id, {})

def render_customer_header(customer_data: Dict[str, Any]):
    """Render customer header information."""
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"## 👤 {customer_data.get('name', 'Unknown')}")
        st.markdown(f"**Email:** {customer_data.get('email', 'N/A')}")
        st.markdown(f"**Age:** {customer_data.get('age', 'N/A')}")
    
    with col2:
        st.metric(
            label="💰 Monthly Income",
            value=f"${customer_data.get('monthly_income', 0):,.0f}",
            help="Total monthly income"
        )
    
    with col3:
        st.metric(
            label="💳 Credit Score", 
            value=customer_data.get('credit_score', 'N/A'),
            help="Current credit score"
        )

def render_financial_overview(customer_data: Dict[str, Any]):
    """Render financial overview metrics."""
    st.markdown("### 📊 Financial Overview")
    
    # Calculate key metrics
    monthly_income = customer_data.get('monthly_income', 0)
    monthly_expenses = customer_data.get('monthly_expenses', 0)
    monthly_savings = monthly_income - monthly_expenses
    savings_rate = (monthly_savings / monthly_income * 100) if monthly_income > 0 else 0
    
    # Display metrics in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="📈 Monthly Income",
            value=f"${monthly_income:,.0f}",
            help="Total monthly income from all sources"
        )
    
    with col2:
        st.metric(
            label="📉 Monthly Expenses", 
            value=f"${monthly_expenses:,.0f}",
            help="Total monthly expenses across all categories"
        )
    
    with col3:
        savings_delta = f"{savings_rate:.1f}%" if savings_rate >= 20 else None
        st.metric(
            label="💰 Monthly Savings",
            value=f"${monthly_savings:,.0f}",
            delta=savings_delta,
            help="Monthly savings (Income - Expenses)"
        )
    
    with col4:
        rate_color = "normal" if savings_rate >= 20 else "inverse"
        st.metric(
            label="📊 Savings Rate",
            value=f"{savings_rate:.1f}%",
            delta="Good" if savings_rate >= 20 else "Below Target",
            delta_color=rate_color,
            help="Percentage of income saved each month (Target: 20%+)"
        )
    
    with col5:
        emergency_fund = customer_data.get('emergency_fund', 0)
        months_covered = emergency_fund / monthly_expenses if monthly_expenses > 0 else 0
        st.metric(
            label="🏦 Emergency Fund",
            value=f"${emergency_fund:,.0f}",
            delta=f"{months_covered:.1f} months",
            help="Emergency fund covers expenses for this many months"
        )

def render_financial_charts(customer_data: Dict[str, Any]):
    """Render financial charts and visualizations."""
    col1, col2 = st.columns(2)
    
    with col1:
        render_spending_breakdown_chart(customer_data)
    
    with col2:
        render_savings_trend_chart(customer_data)
    
    # Goals progress chart
    render_goals_overview(customer_data)

def render_spending_breakdown_chart(customer_data: Dict[str, Any]):
    """Render spending breakdown pie chart."""
    st.markdown("#### 🥧 Spending Breakdown")
    
    spending_categories = customer_data.get('spending_categories', {})
    
    if spending_categories:
        # Create pie chart
        fig = px.pie(
            values=list(spending_categories.values()),
            names=list(spending_categories.keys()),
            title="Monthly Spending by Category"
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Amount: $%{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
        )
        
        fig.update_layout(
            showlegend=True,
            height=400,
            font_size=12
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No spending data available")

def render_savings_trend_chart(customer_data: Dict[str, Any]):
    """Render savings trend chart."""
    st.markdown("#### 📈 Savings Trend")
    
    monthly_trends = customer_data.get('monthly_trends', [])
    
    if monthly_trends:
        df = pd.DataFrame(monthly_trends)
        
        fig = go.Figure()
        
        # Add income line
        fig.add_trace(go.Scatter(
            x=df['month'],
            y=df['income'],
            mode='lines+markers',
            name='Income',
            line=dict(color='green', width=3),
            marker=dict(size=8)
        ))
        
        # Add expenses line
        fig.add_trace(go.Scatter(
            x=df['month'],
            y=df['expenses'],
            mode='lines+markers',
            name='Expenses',
            line=dict(color='red', width=3),
            marker=dict(size=8)
        ))
        
        # Add savings line
        fig.add_trace(go.Scatter(
            x=df['month'],
            y=df['savings'],
            mode='lines+markers',
            name='Savings',
            line=dict(color='blue', width=3),
            marker=dict(size=8),
            fill='tonexty'
        ))
        
        fig.update_layout(
            title="Monthly Income, Expenses & Savings",
            xaxis_title="Month",
            yaxis_title="Amount ($)",
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No trend data available")

def render_goals_overview(customer_data: Dict[str, Any]):
    """Render goals overview section."""
    st.markdown("#### 🎯 Financial Goals Overview")
    
    total_goals = customer_data.get('total_goals', 0)
    goals_on_track = customer_data.get('goals_on_track', 0)
    
    if total_goals > 0:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Total Goals",
                value=total_goals,
                help="Total number of financial goals set"
            )
        
        with col2:
            st.metric(
                label="On Track",
                value=goals_on_track,
                delta=f"{goals_on_track/total_goals*100:.0f}%",
                help="Goals that are on track to be achieved"
            )
        
        with col3:
            behind = total_goals - goals_on_track
            st.metric(
                label="Need Attention",
                value=behind,
                delta=f"{behind/total_goals*100:.0f}%" if behind > 0 else "0%",
                delta_color="inverse" if behind > 0 else "normal",
                help="Goals that need attention or adjustment"
            )
        
        # Progress bar for overall goal achievement
        progress = goals_on_track / total_goals if total_goals > 0 else 0
        st.progress(progress, text=f"Overall Goal Progress: {progress*100:.0f}%")
        
    else:
        st.info("No financial goals set yet. Consider setting some goals to track your financial progress!")
        
        if st.button("➕ Set Your First Goal"):
            st.session_state.active_tab = "Goals"
            st.rerun()

def render_financial_health_score(customer_data: Dict[str, Any]):
    """Render financial health score."""
    st.markdown("#### 🏥 Financial Health Score")
    
    # Calculate simple health score based on key metrics
    score_components = []
    
    # Savings rate (0-30 points)
    savings_rate = customer_data.get('savings_rate', 0)
    savings_score = min(30, savings_rate * 1.5)
    score_components.append(('Savings Rate', savings_score, 30))
    
    # Emergency fund (0-25 points)
    monthly_expenses = customer_data.get('monthly_expenses', 1)
    emergency_fund = customer_data.get('emergency_fund', 0)
    emergency_months = emergency_fund / monthly_expenses if monthly_expenses > 0 else 0
    emergency_score = min(25, emergency_months * 5)
    score_components.append(('Emergency Fund', emergency_score, 25))
    
    # Goal progress (0-25 points)
    total_goals = customer_data.get('total_goals', 1)
    goals_on_track = customer_data.get('goals_on_track', 0)
    goal_score = (goals_on_track / total_goals * 25) if total_goals > 0 else 15
    score_components.append(('Goal Progress', goal_score, 25))
    
    # Credit score (0-20 points)
    credit_score = customer_data.get('credit_score', 600)
    credit_component = min(20, (credit_score - 600) / 15) if credit_score >= 600 else 0
    score_components.append(('Credit Score', credit_component, 20))
    
    # Calculate total score
    total_score = sum(score for _, score, _ in score_components)
    max_score = sum(max_score for _, _, max_score in score_components)
    
    # Display score
    score_percentage = (total_score / max_score) * 100
    
    # Color based on score
    if score_percentage >= 80:
        score_color = "🟢"
        score_status = "Excellent"
    elif score_percentage >= 60:
        score_color = "🟡"
        score_status = "Good"
    elif score_percentage >= 40:
        score_color = "🟠"
        score_status = "Fair"
    else:
        score_color = "🔴"
        score_status = "Needs Improvement"
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric(
            label="Financial Health Score",
            value=f"{score_color} {score_percentage:.0f}/100",
            delta=score_status,
            help="Overall financial health based on savings, emergency fund, goals, and credit"
        )
    
    with col2:
        st.markdown("**Score Breakdown:**")
        for component, score, max_score in score_components:
            percentage = (score / max_score) * 100
            st.markdown(f"- {component}: {score:.0f}/{max_score} ({percentage:.0f}%)")
