"""
Goal Management component for the Streamlit UI.

Allows users to create, view, and manage their financial goals.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional

def render_goal_management():
    """Render the goal management interface."""
    if not st.session_state.get('customer_id'):
        st.warning("No customer selected")
        return
    
    # Create tabs for different goal management functions
    tab1, tab2, tab3 = st.tabs(["📊 Goal Overview", "➕ Add Goal", "📈 Progress Tracking"])
    
    with tab1:
        render_goals_overview()
    
    with tab2:
        render_add_goal_form()
    
    with tab3:
        render_progress_tracking()

def render_goals_overview():
    """Render overview of all customer goals."""
    st.markdown("#### 🎯 Your Financial Goals")
    
    goals = get_customer_goals(st.session_state.customer_id)
    
    if not goals:
        st.info("🎯 No financial goals set yet. Use the 'Add Goal' tab to create your first goal!")
        return
    
    # Summary metrics
    render_goals_summary_metrics(goals)
    
    # Goals list with progress bars
    render_goals_list(goals)
    
    # Goals visualization
    render_goals_charts(goals)

def render_goals_summary_metrics(goals: List[Dict[str, Any]]):
    """Render summary metrics for goals."""
    total_goals = len(goals)
    completed_goals = len([g for g in goals if g['status'] == 'completed'])
    active_goals = len([g for g in goals if g['status'] == 'active'])
    total_target = sum(g['target_amount'] for g in goals if g['status'] in ['active', 'completed'])
    total_current = sum(g['current_amount'] for g in goals if g['status'] in ['active', 'completed'])
    overall_progress = (total_current / total_target * 100) if total_target > 0 else 0
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📊 Total Goals", total_goals)
    
    with col2:
        st.metric("✅ Completed", completed_goals)
    
    with col3:
        st.metric("🎯 Active", active_goals)
    
    with col4:
        st.metric("💰 Total Target", f"${total_target:,.0f}")
    
    with col5:
        st.metric(
            "📈 Overall Progress", 
            f"{overall_progress:.1f}%",
            delta=f"${total_current:,.0f} saved"
        )

def render_goals_list(goals: List[Dict[str, Any]]):
    """Render list of goals with progress indicators."""
    st.markdown("#### 📋 Goal Details")
    
    for goal in goals:
        render_single_goal_card(goal)

def render_single_goal_card(goal: Dict[str, Any]):
    """Render a single goal as a card."""
    # Determine status color and icon
    status_config = {
        'active': {'color': '#1f77b4', 'icon': '🎯', 'bg': '#e8f4fd'},
        'completed': {'color': '#2ca02c', 'icon': '✅', 'bg': '#e8f5e8'},
        'paused': {'color': '#ff7f0e', 'icon': '⏸️', 'bg': '#fff3e0'},
        'cancelled': {'color': '#d62728', 'icon': '❌', 'bg': '#fde8e8'}
    }
    
    config = status_config.get(goal['status'], status_config['active'])
    
    # Calculate progress
    progress = (goal['current_amount'] / goal['target_amount']) * 100 if goal['target_amount'] > 0 else 0
    remaining = goal['target_amount'] - goal['current_amount']
    
    # Create expandable goal card
    with st.expander(f"{config['icon']} {goal['goal_name']} - {progress:.1f}% complete", expanded=False):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**Type:** {goal['goal_type'].replace('_', ' ').title()}")
            st.markdown(f"**Description:** {goal.get('description', 'No description provided')}")
            st.markdown(f"**Priority:** {goal['priority'].title()}")
            st.markdown(f"**Status:** {goal['status'].title()}")
            
            if goal.get('target_date'):
                target_date = datetime.strptime(goal['target_date'], '%Y-%m-%d').date()
                days_remaining = (target_date - date.today()).days
                st.markdown(f"**Target Date:** {target_date} ({days_remaining} days remaining)")
        
        with col2:
            st.metric("Target Amount", f"${goal['target_amount']:,.2f}")
            st.metric("Current Amount", f"${goal['current_amount']:,.2f}")
            st.metric("Remaining", f"${remaining:,.2f}")
        
        # Progress bar
        st.progress(progress / 100, text=f"Progress: {progress:.1f}%")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button(f"💰 Add Contribution", key=f"contribute_{goal['id']}"):
                show_contribution_dialog(goal)
        
        with col2:
            if st.button(f"✏️ Edit Goal", key=f"edit_{goal['id']}"):
                show_edit_goal_dialog(goal)
        
        with col3:
            if goal['status'] == 'active':
                if st.button(f"⏸️ Pause Goal", key=f"pause_{goal['id']}"):
                    update_goal_status(goal['id'], 'paused')
                    st.rerun()

def render_add_goal_form():
    """Render form to add a new financial goal."""
    st.markdown("#### ➕ Create New Financial Goal")
    
    with st.form("add_goal_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            goal_name = st.text_input(
                "Goal Name *",
                placeholder="e.g., Emergency Fund, Vacation to Europe",
                help="Give your goal a descriptive name"
            )
            
            goal_type = st.selectbox(
                "Goal Type *",
                options=["savings", "investment", "debt_payoff", "purchase"],
                format_func=lambda x: {
                    "savings": "💰 Savings",
                    "investment": "📈 Investment", 
                    "debt_payoff": "💳 Debt Payoff",
                    "purchase": "🛒 Purchase"
                }[x],
                help="Select the type of financial goal"
            )
            
            target_amount = st.number_input(
                "Target Amount ($) *",
                min_value=1.0,
                max_value=1000000.0,
                value=1000.0,
                step=100.0,
                format="%.2f",
                help="How much money do you want to save/invest?"
            )
        
        with col2:
            current_amount = st.number_input(
                "Current Amount ($)",
                min_value=0.0,
                max_value=target_amount if 'target_amount' in locals() else 1000000.0,
                value=0.0,
                step=10.0,
                format="%.2f",
                help="How much have you already saved toward this goal?"
            )
            
            target_date = st.date_input(
                "Target Date",
                value=date.today() + timedelta(days=365),
                min_value=date.today(),
                help="When do you want to achieve this goal?"
            )
            
            priority = st.selectbox(
                "Priority Level *",
                options=["low", "medium", "high"],
                index=1,  # Default to medium
                format_func=lambda x: {
                    "low": "🟢 Low",
                    "medium": "🟡 Medium", 
                    "high": "🔴 High"
                }[x],
                help="How important is this goal compared to others?"
            )
        
        description = st.text_area(
            "Description",
            placeholder="Describe your goal and why it's important to you...",
            help="Optional: Add details about your goal"
        )
        
        # Calculate and display goal metrics
        if target_amount > current_amount and target_date > date.today():
            remaining_amount = target_amount - current_amount
            days_remaining = (target_date - date.today()).days
            months_remaining = days_remaining / 30.44  # Average days per month
            
            if months_remaining > 0:
                monthly_savings_needed = remaining_amount / months_remaining
                
                st.info(f"""
                📊 **Goal Analysis:**
                - Amount needed: ${remaining_amount:,.2f}
                - Time remaining: {days_remaining} days ({months_remaining:.1f} months)
                - Monthly savings needed: ${monthly_savings_needed:.2f}
                """)
        
        submitted = st.form_submit_button(
            "🎯 Create Goal",
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            if goal_name and target_amount > 0:
                success = add_financial_goal(
                    customer_id=st.session_state.customer_id,
                    goal_name=goal_name,
                    goal_type=goal_type,
                    target_amount=target_amount,
                    current_amount=current_amount,
                    target_date=target_date,
                    priority=priority,
                    description=description if description else None
                )
                
                if success:
                    st.success("✅ Goal created successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to create goal. Please try again.")
            else:
                st.error("❌ Please fill in all required fields (marked with *)")

def render_progress_tracking():
    """Render goal progress tracking interface."""
    st.markdown("#### 📈 Goal Progress Tracking")
    
    goals = get_customer_goals(st.session_state.customer_id)
    active_goals = [g for g in goals if g['status'] == 'active']
    
    if not active_goals:
        st.info("No active goals to track. Create some goals first!")
        return
    
    # Progress tracking chart
    render_progress_chart(active_goals)
    
    # Monthly contribution tracker
    render_contribution_tracker(active_goals)

def render_progress_chart(goals: List[Dict[str, Any]]):
    """Render progress chart for goals."""
    st.markdown("##### 📊 Progress Overview")
    
    # Prepare data for chart
    goal_names = [g['goal_name'] for g in goals]
    progress_percentages = [(g['current_amount'] / g['target_amount'] * 100) if g['target_amount'] > 0 else 0 for g in goals]
    target_amounts = [g['target_amount'] for g in goals]
    current_amounts = [g['current_amount'] for g in goals]
    
    # Create horizontal bar chart
    fig = go.Figure()
    
    # Add progress bars
    fig.add_trace(go.Bar(
        y=goal_names,
        x=progress_percentages,
        orientation='h',
        name='Progress %',
        text=[f"{p:.1f}%" for p in progress_percentages],
        textposition='inside',
        marker_color='lightblue'
    ))
    
    fig.update_layout(
        title="Goal Progress Overview",
        xaxis_title="Progress (%)",
        yaxis_title="Goals",
        height=max(300, len(goals) * 60),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_contribution_tracker(goals: List[Dict[str, Any]]):
    """Render contribution tracking interface."""
    st.markdown("##### 💰 Quick Contribution")
    
    selected_goal = st.selectbox(
        "Select Goal",
        options=goals,
        format_func=lambda g: f"{g['goal_name']} (${g['current_amount']:,.0f} / ${g['target_amount']:,.0f})",
        help="Choose a goal to add a contribution"
    )
    
    if selected_goal:
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            contribution_amount = st.number_input(
                "Contribution Amount ($)",
                min_value=0.01,
                max_value=10000.0,
                value=100.0,
                step=10.0,
                key="contribution_amount"
            )
        
        with col2:
            if st.button("💰 Add Contribution", use_container_width=True):
                success = update_goal_progress(selected_goal['id'], contribution_amount)
                if success:
                    st.success(f"✅ Added ${contribution_amount:.2f} to {selected_goal['goal_name']}!")
                    st.rerun()
                else:
                    st.error("❌ Failed to add contribution")
        
        with col3:
            remaining = selected_goal['target_amount'] - selected_goal['current_amount']
            st.metric("Remaining", f"${remaining:,.2f}")

def render_goals_charts(goals: List[Dict[str, Any]]):
    """Render various goal-related charts."""
    if not goals:
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Goal types distribution
        goal_types = {}
        for goal in goals:
            goal_type = goal['goal_type'].replace('_', ' ').title()
            goal_types[goal_type] = goal_types.get(goal_type, 0) + 1
        
        if goal_types:
            fig_types = px.pie(
                values=list(goal_types.values()),
                names=list(goal_types.keys()),
                title="Goals by Type"
            )
            st.plotly_chart(fig_types, use_container_width=True)
    
    with col2:
        # Priority distribution
        priorities = {}
        for goal in goals:
            priority = goal['priority'].title()
            priorities[priority] = priorities.get(priority, 0) + 1
        
        if priorities:
            fig_priority = px.bar(
                x=list(priorities.keys()),
                y=list(priorities.values()),
                title="Goals by Priority",
                color=list(priorities.keys()),
                color_discrete_map={'High': 'red', 'Medium': 'orange', 'Low': 'green'}
            )
            st.plotly_chart(fig_priority, use_container_width=True)

def get_customer_goals(customer_id: int) -> List[Dict[str, Any]]:
    """Get financial goals for a customer (mock implementation)."""
    # Mock goals data
    mock_goals = {
        1: [  # Alice's goals
            {
                'id': 1,
                'customer_id': 1,
                'goal_name': 'Emergency Fund',
                'goal_type': 'savings',
                'target_amount': 10000.0,
                'current_amount': 3000.0,
                'target_date': '2024-12-31',
                'priority': 'high',
                'status': 'active',
                'description': 'Build emergency fund covering 6 months of expenses'
            },
            {
                'id': 2,
                'customer_id': 1,
                'goal_name': 'Vacation to Europe',
                'goal_type': 'purchase',
                'target_amount': 5000.0,
                'current_amount': 800.0,
                'target_date': '2024-08-15',
                'priority': 'medium',
                'status': 'active',
                'description': 'Save for 2-week European vacation'
            },
            {
                'id': 3,
                'customer_id': 1,
                'goal_name': 'New Car Down Payment',
                'goal_type': 'purchase',
                'target_amount': 8000.0,
                'current_amount': 1200.0,
                'target_date': '2025-06-01',
                'priority': 'medium',
                'status': 'active',
                'description': 'Save for down payment on new car'
            },
            {
                'id': 4,
                'customer_id': 1,
                'goal_name': 'Retirement Fund',
                'goal_type': 'investment',
                'target_amount': 100000.0,
                'current_amount': 15000.0,
                'target_date': '2030-12-31',
                'priority': 'high',
                'status': 'active',
                'description': 'Long-term retirement savings goal'
            }
        ],
        2: [  # Bob's goals
            {
                'id': 5,
                'customer_id': 2,
                'goal_name': 'Emergency Fund',
                'goal_type': 'savings',
                'target_amount': 8000.0,
                'current_amount': 1500.0,
                'target_date': '2024-10-31',
                'priority': 'high',
                'status': 'active',
                'description': 'Build emergency fund covering 4 months of expenses'
            },
            {
                'id': 6,
                'customer_id': 2,
                'goal_name': 'Home Down Payment',
                'goal_type': 'purchase',
                'target_amount': 50000.0,
                'current_amount': 8000.0,
                'target_date': '2026-12-31',
                'priority': 'high',
                'status': 'active',
                'description': 'Save for house down payment'
            }
        ],
        3: []  # Carol has no goals yet
    }
    
    # Get mock goals for this customer
    customer_goals = mock_goals.get(customer_id, [])
    
    # Add any goals from session state (added via form)
    session_goals = st.session_state.get('financial_goals', [])
    customer_session_goals = [
        g for g in session_goals if g['customer_id'] == customer_id
    ]
    
    return customer_goals + customer_session_goals

def add_financial_goal(
    customer_id: int,
    goal_name: str,
    goal_type: str,
    target_amount: float,
    current_amount: float,
    target_date: date,
    priority: str,
    description: Optional[str] = None
) -> bool:
    """Add a new financial goal (mock implementation)."""
    try:
        goal_data = {
            'id': len(st.session_state.get('financial_goals', [])) + 100,  # Simple ID generation
            'customer_id': customer_id,
            'goal_name': goal_name,
            'goal_type': goal_type,
            'target_amount': target_amount,
            'current_amount': current_amount,
            'target_date': target_date.isoformat(),
            'priority': priority,
            'status': 'active',
            'description': description,
            'created_at': datetime.now().isoformat()
        }
        
        # Store in session state for demo purposes
        if 'financial_goals' not in st.session_state:
            st.session_state.financial_goals = []
        
        st.session_state.financial_goals.append(goal_data)
        return True
        
    except Exception as e:
        st.error(f"Error adding goal: {e}")
        return False

def update_goal_progress(goal_id: int, additional_amount: float) -> bool:
    """Update goal progress by adding a contribution (mock implementation)."""
    try:
        # In a real app, this would call the MCP server to update the goal
        # For now, we'll just show success
        return True
        
    except Exception as e:
        st.error(f"Error updating goal progress: {e}")
        return False

def update_goal_status(goal_id: int, new_status: str) -> bool:
    """Update goal status (mock implementation)."""
    try:
        # In a real app, this would call the MCP server to update the goal status
        return True
        
    except Exception as e:
        st.error(f"Error updating goal status: {e}")
        return False

def show_contribution_dialog(goal: Dict[str, Any]):
    """Show dialog for adding contribution to a goal."""
    # This would typically be implemented as a modal dialog
    # For now, we'll use the contribution tracker section
    st.info(f"Use the 'Progress Tracking' tab to add contributions to {goal['goal_name']}")

def show_edit_goal_dialog(goal: Dict[str, Any]):
    """Show dialog for editing a goal."""
    # This would typically be implemented as a modal dialog
    st.info(f"Goal editing functionality would be implemented here for {goal['goal_name']}")
