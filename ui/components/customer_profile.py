"""
Customer Profile component for the Streamlit UI.

Displays customer information, financial overview, and charts.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

def render_customer_profile():
    """Render the customer profile interface."""
    if not st.session_state.get('customer_id'):
        st.warning("No customer selected")
        return
    
    customer_id = st.session_state.customer_id
    
    # Get customer data from database via MCP tools
    customer_data = get_customer_data_from_db(customer_id)
    
    # Customer header
    render_customer_header(customer_data)
    
    # Financial overview
    render_financial_overview(customer_data)
    
    # Financial charts
    render_financial_charts(customer_data)
    
    # Financial health score
    render_financial_health_score(customer_data)

def get_customer_data_from_db(customer_id: int) -> Dict[str, Any]:
    """Get customer data from database via database client."""
    try:
        # Import the database client functions
        from utils.database_client import (
            get_customer_profile, get_transactions_by_customer, get_financial_goals
        )
        
        # Get customer profile
        customer_profile = get_customer_profile(customer_id)
        
        # Get transactions
        transactions = get_transactions_by_customer(customer_id)
        
        # Get financial goals
        goals = get_financial_goals(customer_id)
        
        # Calculate financial metrics
        monthly_expenses = calculate_monthly_expenses(transactions)
        savings_rate = calculate_savings_rate(transactions)
        emergency_fund = calculate_emergency_fund(transactions)
        goals_on_track = count_goals_on_track(goals)
        spending_categories = analyze_spending_categories(transactions)
        monthly_trends = calculate_monthly_trends(transactions)
        
        return {
            'profile': customer_profile,
            'transactions': transactions,
            'goals': goals,
            'monthly_income': customer_profile.get('monthly_income', 0),
            'monthly_expenses': monthly_expenses,
            'savings_rate': savings_rate,
            'emergency_fund': emergency_fund,
            'total_goals': len(goals),
            'goals_on_track': goals_on_track,
            'credit_score': customer_profile.get('credit_score', 0),
            'spending_categories': spending_categories,
            'monthly_trends': monthly_trends
        }
        
    except Exception as e:
        logger.error(f"Error getting customer data from database: {e}")
        # Return empty data structure on error
        return {
            'profile': {},
            'transactions': [],
            'goals': [],
            'monthly_income': 0,
            'monthly_expenses': 0,
            'savings_rate': 0,
            'emergency_fund': 0,
            'total_goals': 0,
            'goals_on_track': 0,
            'credit_score': 0,
            'spending_categories': {},
            'monthly_trends': {}
        }

def calculate_monthly_expenses(transactions: list) -> float:
    """Calculate monthly expenses from transactions."""
    if not transactions:
        return 0.0
    
    # Get current month
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    monthly_expenses = 0.0
    for transaction in transactions:
        if transaction.get('transaction_type') == 'expense':
            # Parse transaction date - handle both string and date objects
            trans_date = transaction.get('transaction_date')
            try:
                if isinstance(trans_date, str):
                    parsed_date = datetime.strptime(trans_date, '%Y-%m-%d')
                elif isinstance(trans_date, date):
                    parsed_date = datetime.combine(trans_date, datetime.min.time())
                elif hasattr(trans_date, 'date'):
                    parsed_date = datetime.combine(trans_date.date(), datetime.min.time())
                else:
                    continue
                
                if parsed_date.month == current_month and parsed_date.year == current_year:
                    monthly_expenses += float(transaction.get('amount', 0))
            except (ValueError, TypeError, AttributeError):
                continue
    
    return monthly_expenses

def calculate_savings_rate(transactions: list) -> float:
    """Calculate savings rate from transactions."""
    if not transactions:
        return 0.0
    
    # Get current month
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    monthly_income = 0.0
    monthly_expenses = 0.0
    
    for transaction in transactions:
        try:
            trans_date = transaction.get('transaction_date')
            if isinstance(trans_date, str):
                parsed_date = datetime.strptime(trans_date, '%Y-%m-%d')
            elif isinstance(trans_date, date):
                parsed_date = datetime.combine(trans_date, datetime.min.time())
            elif hasattr(trans_date, 'date'):
                parsed_date = datetime.combine(trans_date.date(), datetime.min.time())
            else:
                continue
            
            if parsed_date.month == current_month and parsed_date.year == current_year:
                if transaction.get('transaction_type') == 'income':
                    monthly_income += float(transaction.get('amount', 0))
                elif transaction.get('transaction_type') == 'expense':
                    monthly_expenses += float(transaction.get('amount', 0))
        except (ValueError, TypeError, AttributeError):
            continue
    
    if monthly_income <= 0:
        return 0.0
    
    savings = monthly_income - monthly_expenses
    return (savings / monthly_income) * 100

def calculate_emergency_fund(transactions: list) -> float:
    """Calculate emergency fund from transactions."""
    if not transactions:
        return 0.0
    
    # Look for emergency fund transactions (savings type)
    emergency_fund = 0.0
    for transaction in transactions:
        if (transaction.get('transaction_type') == 'income' and 
            transaction.get('category') == 'Savings & Investment'):
            emergency_fund += transaction.get('amount', 0)
    
    return emergency_fund

def count_goals_on_track(goals: list) -> int:
    """Count goals that are on track."""
    on_track = 0
    for goal in goals:
        current = goal.get('current_amount', 0)
        target = goal.get('target_amount', 0)
        if target > 0 and (current / target) >= 0.8:  # 80% or more complete
            on_track += 1
    return on_track

def analyze_spending_categories(transactions: list) -> Dict[str, float]:
    """Analyze spending by category."""
    categories = {}
    
    for transaction in transactions:
        if transaction.get('transaction_type') == 'expense':
            category = transaction.get('category', 'Other')
            amount = transaction.get('amount', 0)
            categories[category] = categories.get(category, 0) + amount
    
    return categories

def calculate_monthly_trends(transactions: list) -> list:
    """Calculate monthly income/expense trends."""
    trends = []
    
    # Get last 6 months with proper month boundaries
    current_date = datetime.now()
    
    for i in range(6):
        # Calculate month date by subtracting months, not days
        if current_date.month - i <= 0:
            year = current_date.year - 1
            month = 12 + (current_date.month - i)
        else:
            year = current_date.year
            month = current_date.month - i
        
        month_name = datetime(year, month, 1).strftime('%b %Y')
        
        month_income = 0.0
        month_expenses = 0.0
        
        for transaction in transactions:
            try:
                trans_date = transaction.get('transaction_date')
                if isinstance(trans_date, str):
                    parsed_date = datetime.strptime(trans_date, '%Y-%m-%d')
                elif isinstance(trans_date, date):
                    parsed_date = datetime.combine(trans_date, datetime.min.time())
                elif hasattr(trans_date, 'date'):
                    parsed_date = datetime.combine(trans_date.date(), datetime.min.time())
                else:
                    continue
                
                # Check if transaction is in the current month/year
                if parsed_date.month == month and parsed_date.year == year:
                    if transaction.get('transaction_type') == 'income':
                        month_income += float(transaction.get('amount', 0))
                    elif transaction.get('transaction_type') == 'expense':
                        month_expenses += float(transaction.get('amount', 0))
            except (ValueError, TypeError, AttributeError):
                continue
        
        trends.append({
            'month': month_name,
            'income': month_income,
            'expenses': month_expenses,
            'savings': month_income - month_expenses
        })
    
    return trends[::-1]  # Reverse to show oldest first

def render_customer_header(customer_data: Dict[str, Any]):
    """Render customer header information."""
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"## 👤 {customer_data.get('profile', {}).get('name', 'Unknown')}")
        st.markdown(f"**Email:** {customer_data.get('profile', {}).get('email', 'N/A')}")
        st.markdown(f"**Age:** {customer_data.get('profile', {}).get('age', 'N/A')}")
    
    with col2:
        st.metric(
            label="💰 Monthly Income",
            value=f"${float(customer_data.get('monthly_income', 0)):,.0f}",
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
    
    # Calculate key metrics - convert Decimal to float
    monthly_income = float(customer_data.get('monthly_income', 0))
    monthly_expenses = float(customer_data.get('monthly_expenses', 0))
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
        emergency_fund = float(customer_data.get('emergency_fund', 0))
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
