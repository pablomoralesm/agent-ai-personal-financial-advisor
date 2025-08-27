"""
Main Streamlit application for the Financial Advisor AI system.

This application provides a user-friendly interface for:
- Customer profile management
- Transaction entry and tracking
- Financial goal setting
- AI-powered analysis and recommendations
"""

import streamlit as st
import asyncio
from datetime import date, datetime, timedelta
from typing import Dict, Any, Optional
import pandas as pd
from decimal import Decimal

# Configure Streamlit page
st.set_page_config(
    page_title="Financial Advisor AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import application modules
from financial_mcp.server import mcp_server
from financial_mcp.models import TransactionCategory, GoalType
from orchestrator.agent_coordinator import agent_coordinator
from ui.utils import (
    format_currency, format_percentage, get_transaction_categories, get_goal_types,
    create_spending_chart, create_spending_trend_chart, create_goal_progress_chart,
    create_financial_health_gauge, display_workflow_progress, display_agent_response,
    display_adk_response, validate_transaction_form, validate_goal_form, load_custom_css
)
from ui.input_helpers import working_number_input, currency_input, integer_input

# Load custom CSS
load_custom_css()


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'customer_id' not in st.session_state:
        st.session_state.customer_id = None
    if 'current_workflow' not in st.session_state:
        st.session_state.current_workflow = None
    if 'last_analysis' not in st.session_state:
        st.session_state.last_analysis = None


def render_customer_selection():
    """Render customer selection/creation interface."""
    st.sidebar.header("Customer Profile")
    
    # Check if we have a health check first
    try:
        health = mcp_server.health_check()
        if health['status'] != 'healthy':
            st.sidebar.error("⚠️ Database connection issue")
            st.error("Unable to connect to database. Please check your configuration.")
            return None
    except Exception as e:
        st.sidebar.error("⚠️ System error")
        st.error(f"System initialization error: {e}")
        return None
    
    # Customer selection
    customer_option = st.sidebar.radio(
        "Customer Action",
        ["Select Existing Customer", "Create New Customer"]
    )
    
    if customer_option == "Create New Customer":
        return render_customer_creation()
    else:
        return render_customer_selection_existing()


def render_customer_creation():
    """Render customer creation form."""
    st.sidebar.subheader("Create New Customer")
    
    with st.sidebar.form("customer_creation"):
        name = st.text_input("Full Name*", placeholder="Enter your full name")
        email = st.text_input("Email*", placeholder="Enter your email")
        age = integer_input("Age", value=30, min_value=18, max_value=120, key="customer_age")
        annual_income = working_number_input("Annual Income ($)", value=50000.0, min_value=0.0, step=1000.0, format_str="%.0f", key="customer_income")
        
        submitted = st.form_submit_button("Create Customer")
        
        if submitted:
            if not name or not email:
                st.sidebar.error("Name and email are required")
                return None
            
            try:
                customer = mcp_server.create_customer_profile(
                    name=name,
                    email=email,
                    age=age,
                    income=annual_income
                )
                st.sidebar.success(f"Customer created: {customer.name}")
                st.session_state.customer_id = customer.id
                return customer.id
            except Exception as e:
                st.sidebar.error(f"Error creating customer: {e}")
                return None
    
    return None


def render_customer_selection_existing():
    """Render existing customer selection."""
    try:
        customers = mcp_server.db.get_all_customers()
        
        if not customers:
            st.sidebar.info("No customers found. Please create a new customer.")
            return None
        
        customer_options = {f"{c.name} ({c.email})": c.id for c in customers}
        
        selected_customer = st.sidebar.selectbox(
            "Select Customer",
            [""] + list(customer_options.keys())
        )
        
        if selected_customer:
            customer_id = customer_options[selected_customer]
            st.session_state.customer_id = customer_id
            return customer_id
        
        return None
        
    except Exception as e:
        st.sidebar.error(f"Error loading customers: {e}")
        return None


def render_transaction_entry(customer_id: int):
    """Render transaction entry form."""
    st.header("Add Transaction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.form("transaction_form"):
            amount = currency_input("Amount ($)*", value=10.0, min_value=0.01, key="transaction_amount")
            category = st.selectbox("Category*", [""] + get_transaction_categories())
            description = st.text_input("Description", placeholder="Optional description")
            transaction_date = st.date_input("Date*", value=date.today(), max_value=date.today())
            is_income = st.checkbox("This is income (not an expense)")
            
            submitted = st.form_submit_button("Add Transaction", type="primary")
            
            if submitted:
                errors = validate_transaction_form(amount, category, description, transaction_date)
                
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    try:
                        transaction = mcp_server.add_transaction(
                            customer_id=customer_id,
                            amount=amount,
                            category=category,
                            description=description,
                            transaction_date=transaction_date,
                            is_income=is_income
                        )
                        st.success(f"✅ Transaction added: {format_currency(amount)} for {category}")
                        # Clear form by rerunning
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error adding transaction: {e}")
    
    with col2:
        # Recent transactions
        try:
            transactions = mcp_server.get_customer_transactions(customer_id, limit=10)
            if transactions:
                st.subheader("Recent Transactions")
                
                # Convert to DataFrame for display
                trans_data = []
                for t in transactions:
                    trans_data.append({
                        "Date": t.transaction_date,
                        "Amount": format_currency(t.amount),
                        "Category": t.category.replace('_', ' ').title(),
                        "Type": "Income" if t.is_income else "Expense",
                        "Description": t.description or "No description"
                    })
                
                df = pd.DataFrame(trans_data)
                st.dataframe(df, width='stretch', hide_index=True)
            else:
                st.info("No transactions yet. Add your first transaction!")
        except Exception as e:
            st.error(f"Error loading transactions: {e}")


def render_goal_management(customer_id: int):
    """Render goal creation and management interface."""
    st.header("Financial Goals")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Create New Goal")
        
        with st.form("goal_form"):
            title = st.text_input("Goal Title*", placeholder="e.g., Emergency Fund")
            goal_type = st.selectbox("Goal Type*", [""] + get_goal_types())
            target_amount = working_number_input("Target Amount ($)*", value=1000.0, min_value=1.0, step=100.0, format_str="%.0f", key="goal_target")
            description = st.text_area("Description", placeholder="Optional goal description")
            target_date = st.date_input("Target Date", value=date.today() + timedelta(days=365), min_value=date.today())
            
            submitted = st.form_submit_button("Create Goal", type="primary")
            
            if submitted:
                errors = validate_goal_form(title, target_amount, goal_type, target_date)
                
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    try:
                        goal = mcp_server.create_financial_goal(
                            customer_id=customer_id,
                            title=title,
                            goal_type=goal_type,
                            target_amount=target_amount,
                            description=description,
                            target_date=target_date
                        )
                        st.success(f"✅ Goal created: {title}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error creating goal: {e}")
    
    with col2:
        # Display existing goals
        try:
            goals = mcp_server.get_customer_goals(customer_id, active_only=True)
            if goals:
                st.subheader("Active Goals")
                
                for goal in goals:
                    with st.container():
                        st.markdown(f"**{goal.title}**")
                        
                        current = float(goal.current_amount)
                        target = float(goal.target_amount)
                        progress = (current / target) * 100 if target > 0 else 0
                        
                        # Progress bar
                        st.progress(progress / 100)
                        st.write(f"Progress: {format_currency(current)} / {format_currency(target)} ({format_percentage(progress)})")
                        
                        if goal.target_date:
                            days_left = (goal.target_date - date.today()).days
                            if days_left > 0:
                                st.write(f"📅 {days_left} days remaining")
                            else:
                                st.write("🔴 Past target date")
                        
                        # Update progress form
                        with st.form(f"update_goal_{goal.id}"):
                            new_amount = st.number_input(
                                f"Update current amount ($)",
                                value=float(goal.current_amount),
                                min_value=0.0,
                                step=0.01,
                                format="%.2f",
                                key=f"amount_{goal.id}",
                                help=f"Current: {format_currency(current)}, Target: {format_currency(target)}"
                            )
                            
                            col1, col2 = st.columns([1, 3])
                            with col1:
                                submitted = st.form_submit_button("Update Progress", type="secondary")
                            with col2:
                                if new_amount != current:
                                    diff = new_amount - current
                                    if diff > 0:
                                        st.write(f"🟢 +{format_currency(diff)}")
                                    else:
                                        st.write(f"🔴 {format_currency(diff)}")
                            
                            if submitted:
                                try:
                                    mcp_server.update_goal_progress(goal.id, new_amount)
                                    st.success(f"Goal progress updated! New amount: {format_currency(new_amount)}")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error updating goal: {e}")
                        
                        st.divider()
            else:
                st.info("No active goals. Create your first financial goal!")
        except Exception as e:
            st.error(f"Error loading goals: {e}")


def render_ai_analysis(customer_id: int):
    """Render AI analysis interface."""
    st.header("AI Financial Analysis")
    
    # Framework selection
    col_framework, col_analysis = st.columns([1, 1])
    
    with col_framework:
        framework = st.selectbox(
            "Choose Framework",
            [
                "Original Custom Implementation",
                "Google ADK Implementation"
            ],
            help="Compare the original custom agent implementation with Google's Agent Development Kit (ADK)"
        )
    
    with col_analysis:
        # Analysis type selection
        analysis_type = st.selectbox(
            "Choose Analysis Type",
            [
                "Comprehensive Analysis (All Agents)",
                "Spending Analysis Only",
                "Goal Planning Only"
            ]
        )
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Analysis controls
        st.subheader("Run Analysis")
        
        if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
            try:
                with st.spinner(f"Running AI analysis using {framework}..."):
                    if framework == "Google ADK Implementation":
                        # Use ADK implementation
                        from adk_agents.adk_orchestrator import adk_orchestrator
                        
                        if analysis_type == "Comprehensive Analysis (All Agents)":
                            results = adk_orchestrator.run_analysis_sync(customer_id)
                            st.session_state.last_analysis = results
                            st.session_state.analysis_framework = "ADK"
                            
                        elif analysis_type == "Spending Analysis Only":
                            from adk_agents.spending_analyzer_adk import spending_analyzer_adk
                            results = spending_analyzer_adk.analyze_spending(customer_id)
                            st.session_state.last_analysis = {"spending_analysis": results}
                            st.session_state.analysis_framework = "ADK"
                            
                        elif analysis_type == "Goal Planning Only":
                            from adk_agents.goal_planner_adk import goal_planner_adk
                            # Get first goal for analysis (simplified)
                            goals = mcp_server.get_goals_by_customer(customer_id)
                            if goals:
                                goal_data = {
                                    'title': goals[0].title,
                                    'target_amount': float(goals[0].target_amount),
                                    'current_amount': float(goals[0].current_amount or 0),
                                    'target_date': goals[0].target_date.isoformat() if goals[0].target_date else None,
                                    'goal_type': goals[0].goal_type.value
                                }
                                results = goal_planner_adk.analyze_goal(customer_id, goal_data)
                                st.session_state.last_analysis = {"goal_planning": results}
                            else:
                                results = {"error": "No goals found for analysis"}
                                st.session_state.last_analysis = {"goal_planning": results}
                            st.session_state.analysis_framework = "ADK"
                    
                    else:
                        # Use original custom implementation
                        if analysis_type == "Spending Analysis Only":
                            workflow_id = agent_coordinator.create_spending_analysis_workflow(customer_id)
                        elif analysis_type == "Goal Planning Only":
                            # For goal planning, we need goal info
                            goals = mcp_server.get_customer_goals(customer_id, active_only=True)
                            goal_info = {"existing_goals": [g.model_dump() for g in goals]} if goals else {}
                            workflow_id = agent_coordinator.create_goal_planning_workflow(customer_id, goal_info)
                        else:
                            # Comprehensive analysis
                            goals = mcp_server.get_customer_goals(customer_id, active_only=True)
                            goal_info = {"existing_goals": [g.model_dump() for g in goals]} if goals else {}
                            workflow_id = agent_coordinator.create_comprehensive_analysis_workflow(customer_id, goal_info)
                        
                        st.session_state.current_workflow = workflow_id
                        
                        # Run the workflow (this is a simplified sync version)
                        import asyncio
                        results = asyncio.run(agent_coordinator.execute_workflow(workflow_id))
                        st.session_state.last_analysis = results
                        st.session_state.analysis_framework = "Original"
                    
                    st.success("✅ Analysis completed!")
                        
            except Exception as e:
                st.error(f"Analysis failed: {e}")
        
        # Workflow status
        if st.session_state.current_workflow:
            st.subheader("Analysis Status")
            try:
                workflow_status = agent_coordinator.get_workflow_status(st.session_state.current_workflow)
                display_workflow_progress(workflow_status)
            except Exception as e:
                st.error(f"Error checking workflow status: {e}")
    
    with col2:
        # Display results
        st.subheader("Analysis Results")
        
        if st.session_state.last_analysis:
            results = st.session_state.last_analysis
            framework_used = getattr(st.session_state, 'analysis_framework', 'Unknown')
            
            # Show framework indicator
            st.info(f"📊 Results from: **{framework_used}** Implementation")
            
            if framework_used == "ADK":
                # Handle ADK results format
                if 'success' in results and results['success']:
                    # Comprehensive ADK analysis
                    if 'spending_analysis' in results:
                        display_adk_response(results['spending_analysis'], "💸 Spending Analysis (ADK)")
                    if 'goals_analysis' in results:
                        display_adk_response(results['goals_analysis'], "🎯 Goal Planning (ADK)")
                    if 'comprehensive_advice' in results:
                        display_adk_response(results['comprehensive_advice'], "🤖 Comprehensive Advice (ADK)")
                else:
                    # Individual agent results or error
                    for step_name, response in results.items():
                        if step_name == "spending_analysis":
                            display_adk_response(response, "💸 Spending Analysis (ADK)")
                        elif step_name == "goal_planning":
                            display_adk_response(response, "🎯 Goal Planning (ADK)")
                        elif step_name == "comprehensive_advice":
                            display_adk_response(response, "🤖 Comprehensive Advice (ADK)")
            else:
                # Handle original implementation results
                for step_name, response in results.items():
                    if step_name == "spending_analysis":
                        display_agent_response(response.model_dump(), "💸 Spending Analysis (Original)")
                    elif step_name == "goal_planning":
                        display_agent_response(response.model_dump(), "🎯 Goal Planning (Original)")
                    elif step_name == "comprehensive_advice":
                        display_agent_response(response.model_dump(), "🤖 Comprehensive Advice (Original)")
        else:
            st.info("Run an analysis to see results here.")


def render_dashboard(customer_id: int):
    """Render main dashboard with overview."""
    st.header("Financial Dashboard")
    
    try:
        # Get customer context
        context = mcp_server.get_customer_context(customer_id)
        customer = context['customer']
        spending_analysis = context['spending_analysis']
        goals = context['active_goals']
        
        # Customer info
        st.subheader(f"Welcome, {customer['name']}! 👋")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Monthly Income",
                format_currency(float(customer.get('income', 0)) / 12) if customer.get('income') else "Not set",
                delta=None
            )
        
        with col2:
            st.metric(
                "Monthly Spending",
                format_currency(spending_analysis.get('total_spending', 0)),
                delta=None
            )
        
        with col3:
            st.metric(
                "Monthly Savings",
                format_currency(spending_analysis.get('net_savings', 0)),
                delta=None
            )
        
        with col4:
            savings_rate = 0
            if customer.get('income'):
                monthly_income = float(customer['income']) / 12
                if monthly_income > 0:
                    savings_rate = (spending_analysis.get('net_savings', 0) / monthly_income) * 100
            
            st.metric(
                "Savings Rate",
                format_percentage(savings_rate),
                delta=None
            )
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Spending breakdown
            category_data = spending_analysis.get('category_breakdown', {})
            if category_data:
                fig = create_spending_chart(category_data)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No spending data available yet.")
        
        with col2:
            # Goal progress
            if goals:
                fig = create_goal_progress_chart(goals)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No active goals. Create a goal to track progress!")
        
        # Financial health score (if available from recent analysis)
        recent_advice = mcp_server.get_advice_history(customer_id, "comprehensive_advice")
        if recent_advice:
            latest_advice = recent_advice[0]
            # Try to extract health score from advice content
            # This is a simplified approach - in production, you'd store structured data
            st.subheader("Financial Health")
            
            # For demo, show a placeholder gauge
            health_score = 75  # Default score
            fig = create_financial_health_gauge(health_score)
            st.plotly_chart(fig, use_container_width=True)
        
        # Recent transactions trend
        transactions = context.get('recent_transactions', [])
        if transactions:
            st.subheader("Spending Trend")
            fig = create_spending_trend_chart(transactions)
            st.plotly_chart(fig, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")


def main():
    """Main application function."""
    initialize_session_state()
    
    # App title
    st.markdown("<h1 class='main-header'>💰 Financial Advisor AI</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Customer selection
    customer_id = render_customer_selection()
    
    if not customer_id:
        st.info("Please select or create a customer profile to continue.")
        return
    
    # Main navigation
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "💳 Transactions", "🎯 Goals", "🤖 AI Analysis"])
    
    with tab1:
        render_dashboard(customer_id)
    
    with tab2:
        render_transaction_entry(customer_id)
    
    with tab3:
        render_goal_management(customer_id)
    
    with tab4:
        render_ai_analysis(customer_id)


if __name__ == "__main__":
    main()
