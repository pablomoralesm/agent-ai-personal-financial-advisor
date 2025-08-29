"""
Goal Management component for the Streamlit UI.

Allows users to set, track, and manage financial goals.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

def render_goal_management():
    """Render the goal management interface."""
    if not st.session_state.get('customer_id'):
        st.warning("No customer selected")
        return
    
    customer_id = st.session_state.customer_id
    
    st.markdown("## 🎯 Financial Goals Management")
    
    # Goal creation form
    render_goal_form(customer_id)
    
    # Goals overview and tracking
    render_goals_overview(customer_id)

def render_goal_form(customer_id: int):
    """Render goal creation form."""
    st.markdown("### ➕ Create New Financial Goal")
    
    with st.form("goal_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            goal_name = st.text_input(
                "Goal Name",
                placeholder="e.g., Emergency Fund, Vacation, New Car",
                help="Give your goal a descriptive name"
            )
            
            goal_type = st.selectbox(
                "Goal Type",
                options=[
                    "emergency_fund", "savings", "investment", "debt_payoff",
                    "purchase", "education", "retirement", "other"
                ],
                help="Type of financial goal"
            )
            
            target_amount = st.number_input(
                "Target Amount ($)",
                min_value=0.01,
                value=1000.0,
                step=100.0,
                help="How much money do you need to save?"
            )
        
        with col2:
            current_amount = st.number_input(
                "Current Amount ($)",
                min_value=0.0,
                value=0.0,
                step=100.0,
                help="How much have you saved so far?"
            )
            
            target_date = st.date_input(
                "Target Date",
                value=date.today().replace(year=date.today().year + 1),
                help="When do you want to achieve this goal?"
            )
            
            priority = st.selectbox(
                "Priority",
                options=["low", "medium", "high"],
                help="How important is this goal?"
            )
        
        description = st.text_area(
            "Description (Optional)",
            placeholder="Describe your goal and why it's important to you",
            help="Additional details about your goal"
        )
        
        submitted = st.form_submit_button("💾 Create Goal")
        
        if submitted:
            if not goal_name or target_amount <= 0:
                st.error("Please provide a goal name and target amount")
                return
            
            if current_amount > target_amount:
                st.error("Current amount cannot exceed target amount")
                return
            
            # Save goal to database
            success = save_goal_to_db(
                customer_id=customer_id,
                goal_name=goal_name,
                goal_type=goal_type,
                target_amount=target_amount,
                current_amount=current_amount,
                target_date=target_date.strftime('%Y-%m-%d'),
                priority=priority,
                description=description if description else None
            )
            
            if success:
                st.success("✅ Goal created successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to create goal")

def save_goal_to_db(
    customer_id: int,
    goal_name: str,
    goal_type: str,
    target_amount: float,
    current_amount: float,
    target_date: str,
    priority: str,
    description: str = None
) -> bool:
    """Save financial goal to database via database client."""
    try:
        from utils.database_client import create_financial_goal
        
        success = create_financial_goal(
            customer_id=customer_id,
            goal_name=goal_name,
            goal_type=goal_type,
            target_amount=target_amount,
            current_amount=current_amount,
            target_date=target_date,
            priority=priority,
            description=description
        )
        
        if success:
            logger.info(f"Goal '{goal_name}' created successfully for customer {customer_id}")
            return True
        else:
            logger.error("Failed to create goal in database")
            st.error("Failed to create goal in database")
            return False
            
    except Exception as e:
        logger.error(f"Error creating goal: {e}")
        st.error(f"Failed to create goal: {e}")
        return False

def render_goals_overview(customer_id: int):
    """Render goals overview and tracking."""
    st.markdown("### 📊 Your Financial Goals")
    
    # Get goals from database
    goals = get_goals_from_db(customer_id)
    
    if not goals:
        st.info("No financial goals set yet. Create your first goal above!")
        return
    
    # Display goals in a nice format
    for i, goal in enumerate(goals):
        render_goal_card(goal, i)
    
    # Goals summary
    render_goals_summary(goals)

def get_goals_from_db(customer_id: int) -> list:
    """Get financial goals from database via database client."""
    try:
        from utils.database_client import get_financial_goals
        
        goals = get_financial_goals(customer_id)
        
        logger.info(f"Retrieved {len(goals)} goals for customer {customer_id}")
        return goals
            
    except Exception as e:
        logger.error(f"Error getting goals: {e}")
        st.error(f"Failed to load goals: {e}")
        return []

def render_goal_card(goal: Dict[str, Any], index: int):
    """Render individual goal card."""
    with st.container():
        st.markdown("---")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"#### 🎯 {goal.get('goal_name', 'Unnamed Goal')}")
            st.caption(f"**Type:** {goal.get('goal_type', 'Unknown').replace('_', ' ').title()}")
            
            if goal.get('description'):
                st.write(goal.get('description'))
        
        with col2:
            current = goal.get('current_amount', 0)
            target = goal.get('target_amount', 1)
            progress = min(float(current) / float(target), 1.0) if target > 0 else 0
            
            st.metric(
                "Progress",
                f"${float(current):,.0f} / ${float(target):,.0f}",
                f"{progress*100:.0f}%"
            )
            
            # Progress bar
            st.progress(progress)
        
        with col3:
            # Priority indicator
            priority = goal.get('priority', 'medium')
            priority_colors = {
                'low': '🟢',
                'medium': '🟡', 
                'high': '🔴'
            }
            st.markdown(f"**Priority:** {priority_colors.get(priority, '⚪')} {priority.title()}")
            
            # Target date and days remaining
            target_date = goal.get('target_date')
            if target_date:
                try:
                    if isinstance(target_date, str):
                        date_obj = datetime.strptime(target_date, '%Y-%m-%d').date()
                    elif isinstance(target_date, date):
                        date_obj = target_date
                    elif hasattr(target_date, 'date'):
                        date_obj = target_date.date()
                    else:
                        date_obj = None
                    
                    if date_obj:
                        days_left = (date_obj - date.today()).days
                        
                        if days_left > 0:
                            st.metric("Days Left", f"{days_left} days")
                        elif days_left == 0:
                            st.metric("Due Today", "⚠️")
                        else:
                            st.metric("Overdue", f"{abs(days_left)} days", delta_color="inverse")
                except (ValueError, TypeError, AttributeError):
                    st.metric("Target Date", "Invalid date")
        
        # Update progress section
        with st.expander(f"📈 Update Progress for {goal.get('goal_name')}"):
            render_goal_progress_update(goal)

def render_goal_progress_update(goal: Dict[str, Any]):
    """Render goal progress update form."""
    with st.form(f"progress_form_{goal.get('id')}"):
        current_amount = st.number_input(
            "Current Amount ($)",
            min_value=0.0,
            value=float(goal.get('current_amount', 0)),
            step=100.0,
            key=f"current_{goal.get('id')}"
        )
        
        submitted = st.form_submit_button("💾 Update Progress")
        
        if submitted:
            success = update_goal_progress(goal.get('id'), current_amount)
            if success:
                st.success("✅ Progress updated successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to update progress")

def update_goal_progress(goal_id: int, current_amount: float) -> bool:
    """Update goal progress in database via database client."""
    try:
        from utils.database_client import update_goal_progress
        
        success = update_goal_progress(
            goal_id=goal_id,
            current_amount=current_amount
        )
        
        if success:
            logger.info(f"Goal {goal_id} progress updated to ${current_amount}")
            return True
        else:
            logger.error("Failed to update goal progress in database")
            st.error("Failed to update goal progress in database")
            return False
            
    except Exception as e:
        logger.error(f"Error updating goal progress: {e}")
        st.error(f"Failed to update progress: {e}")
        return False

def render_goals_summary(goals: list):
    """Render goals summary statistics."""
    st.markdown("### 📊 Goals Summary")
    
    if not goals:
        return
    
    # Calculate summary metrics
    total_goals = len(goals)
    total_target = sum(g.get('target_amount', 0) for g in goals)
    total_current = sum(g.get('current_amount', 0) for g in goals)
    overall_progress = (total_current / total_target * 100) if total_target > 0 else 0
    
    # Count goals by status
    on_track = 0
    behind = 0
    ahead = 0
    
    for goal in goals:
        current = goal.get('current_amount', 0)
        target = goal.get('target_amount', 0)
        target_date = goal.get('target_date')
        
        if target > 0:
            progress = current / target
            
            # Check if on track based on time and progress
            if target_date:
                try:
                    if isinstance(target_date, str):
                        date_obj = datetime.strptime(target_date, '%Y-%m-%d').date()
                    elif isinstance(target_date, date):
                        date_obj = target_date
                    elif hasattr(target_date, 'date'):
                        date_obj = target_date.date()
                    else:
                        date_obj = None
                    
                    if date_obj:
                        days_left = (date_obj - date.today()).days
                        total_days = (date_obj - date.today()).days + 365  # Rough estimate
                        
                        if total_days > 0:
                            time_progress = max(0, min(1, (total_days - days_left) / total_days))
                            overall_progress = (progress + time_progress) / 2
                            
                            if overall_progress >= 0.8:
                                status = "🟢 On Track"
                            elif overall_progress >= 0.6:
                                status = "🟡 Needs Attention"
                            else:
                                status = "🔴 Behind Schedule"
                        else:
                            status = "🔴 Overdue"
                    else:
                        status = "⚪ Unknown"
                except (ValueError, TypeError, AttributeError):
                    status = "⚪ Invalid Date"
            else:
                status = "⚪ No Target Date"
        else:
            status = "⚪ No Target Amount"

        if status == "🟢 On Track":
            on_track += 1
        elif status == "🟡 Needs Attention":
            behind += 1
        elif status == "🔴 Behind Schedule":
            ahead += 1
        elif status == "🔴 Overdue":
            behind += 1
        elif status == "⚪ Unknown":
            behind += 1
        elif status == "⚪ Invalid Date":
            behind += 1
        elif status == "⚪ No Target Amount":
            behind += 1

    # Display summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Goals",
            total_goals,
            help="Total number of financial goals"
        )
    
    with col2:
        st.metric(
            "Total Target",
            f"${total_target:,.0f}",
            help="Combined target amount for all goals"
        )
    
    with col3:
        st.metric(
            "Total Saved",
            f"${total_current:,.0f}",
            help="Combined current amount for all goals"
        )
    
    with col4:
        st.metric(
            "Overall Progress",
            f"{overall_progress:.1f}%",
            help="Average progress across all goals"
        )
    
    # Status breakdown
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "On Track",
            on_track,
            delta=f"{on_track/total_goals*100:.0f}%" if total_goals > 0 else "0%",
            delta_color="normal",
            help="Goals that are on track"
        )
    
    with col2:
        st.metric(
            "Behind",
            behind,
            delta=f"{behind/total_goals*100:.0f}%" if total_goals > 0 else "0%",
            delta_color="inverse",
            help="Goals that need attention"
        )
    
    with col3:
        st.metric(
            "Ahead",
            ahead,
            delta=f"{ahead/total_goals*100:.0f}%" if total_goals > 0 else "0%",
            delta_color="normal",
            help="Goals that are ahead of schedule"
        )
    
    # Overall progress bar
    st.markdown("#### 🎯 Overall Goals Progress")
    st.progress(float(overall_progress) / 100)
    st.caption(f"Combined progress: {float(overall_progress):.1f}% of total target amount")
