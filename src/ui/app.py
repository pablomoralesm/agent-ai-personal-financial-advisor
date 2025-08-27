"""Streamlit UI for the Financial Advisor app."""

import streamlit as st
import datetime
import sys
import os
import time
import threading
import logging
from typing import Dict, Any, List, Optional

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.agents.agent_manager import AgentManager
from src.utils.config import GOOGLE_API_KEY

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Initialize session state
if "agent_manager" not in st.session_state:
    st.session_state.agent_manager = AgentManager()
    
if "servers_started" not in st.session_state:
    st.session_state.servers_started = False
    
if "selected_customer" not in st.session_state:
    st.session_state.selected_customer = None
    
if "advice_generated" not in st.session_state:
    st.session_state.advice_generated = False
    
if "advice_result" not in st.session_state:
    st.session_state.advice_result = None

# Function to start servers in background
def start_servers():
    """Start all servers in background."""
    if not st.session_state.servers_started:
        try:
            st.session_state.agent_manager.initialize_agents()
            st.session_state.agent_manager.start_servers()
            st.session_state.servers_started = True
            time.sleep(2)  # Give servers time to start
        except Exception as e:
            st.error(f"Error starting servers: {e}")

# Start servers when app loads
if not st.session_state.servers_started:
    server_thread = threading.Thread(target=start_servers)
    server_thread.daemon = True
    server_thread.start()

# App title and description
st.title("Financial Advisor AI")
st.subheader("Personalized financial advice powered by AI agents")

# Sidebar for customer selection and creation
with st.sidebar:
    st.header("Customer Management")
    
    # Customer selection
    st.subheader("Select Customer")
    
    # Get customers
    customers = st.session_state.agent_manager.get_customers()
    customer_options = ["Select a customer..."] + [f"{c['id']} - {c['name']}" for c in customers]
    selected_customer_option = st.selectbox("Customer", customer_options)
    
    if selected_customer_option != "Select a customer...":
        customer_id = int(selected_customer_option.split(" - ")[0])
        if st.session_state.selected_customer is None or st.session_state.selected_customer["id"] != customer_id:
            st.session_state.selected_customer = st.session_state.agent_manager.get_customer(customer_id)
            st.session_state.advice_generated = False
            st.session_state.advice_result = None
    else:
        st.session_state.selected_customer = None
        st.session_state.advice_generated = False
        st.session_state.advice_result = None
    
    # Customer creation
    st.subheader("Create New Customer")
    with st.form("create_customer_form"):
        new_name = st.text_input("Name")
        new_email = st.text_input("Email")
        create_submitted = st.form_submit_button("Create Customer")
        
        if create_submitted:
            if new_name and new_email:
                result = st.session_state.agent_manager.create_customer(new_name, new_email)
                if result:
                    st.success(f"Customer {new_name} created successfully!")
                    st.experimental_rerun()
                else:
                    st.error("Failed to create customer. Please try again.")
            else:
                st.error("Please fill in all fields.")

# Main content
if st.session_state.selected_customer:
    customer = st.session_state.selected_customer
    st.header(f"Customer: {customer['name']}")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["Transactions", "Goals", "Analysis & Advice", "Advice History"])
    
    # Transactions tab
    with tab1:
        st.subheader("Transactions")
        
        # Transaction form
        with st.form("add_transaction_form"):
            st.write("Add New Transaction")
            amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
            category = st.selectbox(
                "Category",
                ["Housing", "Transportation", "Food", "Utilities", "Healthcare", 
                 "Insurance", "Entertainment", "Personal", "Education", "Savings", "Debt", "Other"]
            )
            transaction_date = st.date_input("Date", datetime.date.today())
            description = st.text_input("Description")
            
            transaction_submitted = st.form_submit_button("Add Transaction")
            
            if transaction_submitted:
                if amount > 0 and description:
                    result = st.session_state.agent_manager.add_transaction(
                        customer["id"],
                        amount,
                        category,
                        transaction_date.isoformat(),
                        description
                    )
                    if result:
                        st.success("Transaction added successfully!")
                    else:
                        st.error("Failed to add transaction. Please try again.")
                else:
                    st.error("Please fill in all fields.")
        
        # Display transactions
        transactions = st.session_state.agent_manager.get_customer_transactions(customer["id"])
        if transactions:
            st.write(f"Recent Transactions ({len(transactions)})")
            
            # Create a DataFrame-like display
            cols = st.columns([0.15, 0.15, 0.2, 0.5])
            cols[0].write("**Date**")
            cols[1].write("**Amount**")
            cols[2].write("**Category**")
            cols[3].write("**Description**")
            
            for transaction in transactions[:10]:  # Show only the 10 most recent
                cols = st.columns([0.15, 0.15, 0.2, 0.5])
                cols[0].write(transaction["transaction_date"])
                cols[1].write(f"${transaction['amount']:.2f}")
                cols[2].write(transaction["category"])
                cols[3].write(transaction["description"])
            
            if len(transactions) > 10:
                st.write(f"... and {len(transactions) - 10} more transactions")
        else:
            st.info("No transactions found. Add your first transaction above.")
    
    # Goals tab
    with tab2:
        st.subheader("Financial Goals")
        
        # Goal form
        with st.form("add_goal_form"):
            st.write("Add New Goal")
            goal_type = st.selectbox(
                "Goal Type",
                ["Emergency Fund", "Retirement", "Home Purchase", "Education", "Vacation", "Car Purchase", "Debt Payoff", "Other"]
            )
            target_amount = st.number_input("Target Amount ($)", min_value=1.0, step=100.0)
            current_amount = st.number_input("Current Amount ($)", min_value=0.0, step=100.0)
            target_date = st.date_input("Target Date", datetime.date.today() + datetime.timedelta(days=365))
            goal_description = st.text_input("Description")
            
            goal_submitted = st.form_submit_button("Add Goal")
            
            if goal_submitted:
                if target_amount > 0 and goal_description:
                    result = st.session_state.agent_manager.create_goal(
                        customer["id"],
                        goal_type,
                        target_amount,
                        current_amount,
                        target_date.isoformat(),
                        goal_description
                    )
                    if result:
                        st.success("Goal added successfully!")
                    else:
                        st.error("Failed to add goal. Please try again.")
                else:
                    st.error("Please fill in all fields.")
        
        # Display goals
        goals = st.session_state.agent_manager.get_customer_goals(customer["id"])
        if goals:
            st.write(f"Current Goals ({len(goals)})")
            
            for goal in goals:
                progress = (goal["current_amount"] / goal["target_amount"]) * 100 if goal["target_amount"] > 0 else 0
                
                st.write(f"**{goal['goal_type']}**: {goal['description']}")
                cols = st.columns([0.7, 0.3])
                cols[0].progress(min(progress, 100) / 100)
                cols[1].write(f"{progress:.1f}% (${goal['current_amount']:.2f} / ${goal['target_amount']:.2f})")
                st.write(f"Target date: {goal['target_date']}")
                st.write("---")
        else:
            st.info("No goals found. Add your first goal above.")
    
    # Analysis & Advice tab
    with tab3:
        st.subheader("Financial Analysis & Advice")
        
        # Analysis form
        months_to_analyze = st.slider("Months to analyze", 1, 12, 3)
        
        if st.button("Generate Financial Advice"):
            with st.spinner("Analyzing financial data and generating advice..."):
                try:
                    advice_result = st.session_state.agent_manager.get_financial_advice(
                        customer["id"],
                        months_to_analyze
                    )
                    
                    if "error" in advice_result:
                        st.error(f"Error generating advice: {advice_result['error']}")
                    else:
                        st.session_state.advice_generated = True
                        st.session_state.advice_result = advice_result
                        st.success("Financial advice generated successfully!")
                except Exception as e:
                    st.error(f"Error generating advice: {e}")
        
        # Display advice
        if st.session_state.advice_generated and st.session_state.advice_result:
            advice = st.session_state.advice_result
            
            # Spending Analysis
            st.write("### Spending Analysis")
            spending = advice["spending_analysis"]["spending_patterns"]
            
            cols = st.columns(3)
            cols[0].metric("Total Spending", f"${spending['total_spending']:.2f}")
            cols[1].metric("Monthly Average", f"${spending['avg_monthly_spending']:.2f}")
            cols[2].metric("Trend", advice["spending_analysis"]["trends"]["trend"].capitalize())
            
            # Top spending categories
            st.write("#### Top Spending Categories")
            categories = advice["spending_analysis"]["spending_patterns"]["spending_by_category"]
            if categories:
                for category in categories[:3]:
                    st.write(f"- {category['category']}: ${category['total_amount']:.2f} ({category.get('percentage', 0):.1f}%)")
            
            # Goals Assessment
            st.write("### Goal Assessment")
            if advice["goal_planning"]["has_goals"]:
                recommendations = advice["goal_planning"]["recommendations"]
                
                cols = st.columns(2)
                cols[0].metric("Monthly Contribution Needed", f"${recommendations['total_monthly_contribution']:.2f}")
                cols[1].metric("Estimated Savings Capacity", f"${recommendations['estimated_savings_capacity']:.2f}")
                
                st.write(f"Overall assessment: **{recommendations['overall_realistic']}**")
                
                # Goal-specific recommendations
                st.write("#### Goal-specific Recommendations")
                for goal_rec in recommendations["goal_recommendations"]:
                    st.write(f"- **{goal_rec['goal']['goal_type']}**: "
                           f"${goal_rec['monthly_contribution']:.2f}/month needed "
                           f"({'Realistic' if goal_rec['is_realistic'] else 'Needs adjustment'})")
            else:
                st.info("No financial goals have been set.")
            
            # Financial Advice
            st.write("### Personalized Financial Advice")
            if "advice_text" in advice["advice"]:
                st.write(advice["advice"]["advice_text"])
            
            # Next Steps
            st.write("### Recommended Next Steps")
            if "next_steps" in advice["next_steps"]:
                for step in advice["next_steps"]["next_steps"]:
                    priority_color = {
                        "high": "🔴",
                        "medium": "🟠",
                        "low": "🟢"
                    }.get(step["priority"], "⚪")
                    
                    st.write(f"{priority_color} **{step['action']}**: {step['description']}")
    
    # Advice History tab
    with tab4:
        st.subheader("Advice History")
        
        # Display advice history
        advice_history = st.session_state.agent_manager.get_customer_advice_history(customer["id"])
        if advice_history:
            for advice in advice_history:
                with st.expander(f"{advice['agent_name']} - {advice['created_at']}"):
                    st.write(advice["advice_text"])
        else:
            st.info("No advice history found. Generate advice in the Analysis & Advice tab.")
else:
    st.info("Please select or create a customer in the sidebar to get started.")

# Footer
st.markdown("---")
st.caption("Financial Advisor AI - Powered by Google ADK and Gemini LLM")

# Main function
def main():
    """Main function to run the Streamlit app."""
    pass  # App is already configured above

if __name__ == "__main__":
    main()
