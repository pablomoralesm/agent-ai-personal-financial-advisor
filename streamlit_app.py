"""
Personal Financial Advisor - Streamlit Application

A comprehensive financial advisory application built with Google Agent Development Kit (ADK)
that provides personalized financial advice through AI agents.
"""

import streamlit as st
import os
import sys
from pathlib import Path
import logging

# Add project root to Python path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
os.environ['PYTHONPATH'] = str(project_root)

# Configure logging
from utils.logging_config import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

# Import UI components
from ui.components.customer_profile import render_customer_profile
from ui.components.transaction_entry import render_transaction_entry
from ui.components.goal_management import render_goal_management
from ui.components.recommendations import render_recommendations

# Import utility functions
from ui.utils.plotting import create_spending_chart, create_goal_progress_chart
from ui.utils.formatting import format_currency, format_date

def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Personal Financial Advisor",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">💰 Personal Financial Advisor</h1>', unsafe_allow_html=True)
    st.markdown("**AI-powered financial advice through intelligent agents**")
    
    # Initialize session state
    if 'customer_id' not in st.session_state:
        st.session_state.customer_id = None
    
    if 'mcp_server_path' not in st.session_state:
        st.session_state.mcp_server_path = str(project_root / "mcp_server" / "database_server.py")
    
    # Sidebar for customer selection
    render_customer_selector()
    
    # Main content area
    if st.session_state.customer_id:
        render_main_content()
    else:
        render_welcome_screen()

def render_customer_selector():
    """Render customer selection interface."""
    st.sidebar.markdown("## 👤 Customer Selection")
    
    try:
        # Get customers from database
        from utils.database_client import get_all_customers
        customers = get_all_customers()
        
        if not customers:
            st.sidebar.warning("⚠️ No customers found in database")
            return
        
        # Find current customer index
        current_index = 0
        if st.session_state.customer_id:
            for i, customer in enumerate(customers):
                if customer['id'] == st.session_state.customer_id:
                    current_index = i
                    break
        
        selected_customer = st.sidebar.selectbox(
            "Choose Customer",
            options=customers,
            format_func=lambda x: f"{x['name']} ({x['email']})",
            index=current_index
        )
        
        if selected_customer and selected_customer['id'] != st.session_state.customer_id:
            st.session_state.customer_id = selected_customer['id']
            st.rerun()
            
    except Exception as e:
        st.sidebar.error(f"❌ Error loading customers: {str(e)}")
        # Fallback to hardcoded customers if database fails
        customers = [
            {"id": 1, "name": "Alice Johnson", "email": "alice@example.com"},
            {"id": 2, "name": "Bob Smith", "email": "bob@example.com"},
            {"id": 3, "name": "Carol Davis", "email": "carol@example.com"}
        ]
        
        selected_customer = st.sidebar.selectbox(
            "Choose Customer (Fallback)",
            options=customers,
            format_func=lambda x: f"{x['name']} ({x['email']})",
            index=0 if st.session_state.customer_id is None else st.session_state.customer_id - 1
        )
        
        if selected_customer and selected_customer['id'] != st.session_state.customer_id:
            st.session_state.customer_id = selected_customer['id']
            st.rerun()
    
    # Database Connection Status
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 🔧 System Status")
    
    # Test database connection
    try:
        from utils.database_client import db_client
        # Try to get a connection
        connection = db_client.get_connection()
        if connection.is_connected():
            st.sidebar.success("✅ Database: Connected")
            connection.close()
        else:
            st.sidebar.error("❌ Database: Connection Failed")
    except Exception as e:
        st.sidebar.error(f"❌ Database: Error - {str(e)[:50]}...")
    
    # MCP Server Status
    mcp_path = st.session_state.mcp_server_path
    if os.path.exists(mcp_path):
        st.sidebar.success("✅ MCP Server: Ready")
    else:
        st.sidebar.error("❌ MCP Server: Not Found")
        st.sidebar.info(f"Expected path: {mcp_path}")

def render_welcome_screen():
    """Render welcome screen when no customer is selected."""
    st.markdown("## 🎯 Welcome to Your Personal Financial Advisor")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        This AI-powered application provides personalized financial advice through intelligent agents:
        
        **🤖 AI Agents:**
        - **Spending Analyzer**: Reviews your spending habits and identifies optimization opportunities
        - **Goal Planner**: Helps set and track financial goals
        - **Financial Advisor**: Provides comprehensive recommendations and action plans
        
        **💾 Data Storage:**
        - Customer profiles and financial data stored securely in MySQL database
        - All data access through secure MCP (Model Context Protocol) tools
        - No direct database access from agents
        
        **🎯 Key Features:**
        - Transaction tracking and categorization
        - Financial goal setting and monitoring
        - AI-generated spending insights
        - Personalized financial recommendations
        - Progress tracking and historical analysis
        """)
    
    with col2:
        st.markdown("### 🚀 Getting Started")
        st.markdown("""
        1. **Select a customer** from the sidebar
        2. **Enter transactions** to build your financial profile
        3. **Set financial goals** for savings and investments
        4. **Run AI analysis** to get personalized advice
        5. **Track progress** and implement recommendations
        """)
        
        st.info("💡 **Tip**: Start by selecting a customer from the sidebar to begin using the application.")

def render_main_content():
    """Render main application content for selected customer."""
    customer_id = st.session_state.customer_id
    
    # Navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Profile & Overview",
        "💰 Transactions",
        "🎯 Goals",
        "🤖 AI Recommendations"
    ])
    
    with tab1:
        render_customer_profile()
    
    with tab2:
        render_transaction_entry()
    
    with tab3:
        render_goal_management()
    
    with tab4:
        render_recommendations()
        st.markdown("---")
        render_analysis_controls()

def render_analysis_controls():
    """Render analysis control buttons."""
    st.markdown("## 🚀 Financial Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Full Analysis", type="primary", use_container_width=True):
            run_full_analysis()
    
    with col2:
        if st.button("⚡ Quick Analysis", use_container_width=True):
            run_quick_analysis()
    
    with col3:
        if st.button("🎯 Goal Analysis", use_container_width=True):
            run_goal_analysis()

def run_full_analysis():
    """Run comprehensive financial analysis using AI agents."""
    customer_id = st.session_state.customer_id
    if not customer_id:
        st.error("Please select a customer first.")
        return
    
    try:
        with st.spinner("🤖 Running comprehensive financial analysis..."):
            # This would integrate with the FinancialAdvisorOrchestrator
            st.success("✅ Full analysis completed!")
            st.info("""
            **Analysis Results:**
            - Spending patterns analyzed
            - Goal progress evaluated
            - Personalized recommendations generated
            - Action plan created
            
            *Note: This is a demonstration. In a full implementation, this would call the AI agents through ADK.*
            """)
    except Exception as e:
        st.error(f"❌ Analysis failed: {str(e)}")

def run_quick_analysis():
    """Run quick financial insights."""
    customer_id = st.session_state.customer_id
    if not customer_id:
        st.error("Please select a customer first.")
        return
    
    try:
        with st.spinner("⚡ Running quick analysis..."):
            # This would integrate with the SpendingAnalyzerAgent
            st.success("✅ Quick analysis completed!")
            st.info("""
            **Quick Insights:**
            - Recent spending trends
            - Category analysis
            - Budget recommendations
            
            *Note: This is a demonstration. In a full implementation, this would call the SpendingAnalyzerAgent.*
            """)
    except Exception as e:
        st.error(f"❌ Quick analysis failed: {str(e)}")

def run_goal_analysis():
    """Run goal-focused analysis."""
    customer_id = st.session_state.customer_id
    if not customer_id:
        st.error("Please select a customer first.")
        return
    
    try:
        with st.spinner("🎯 Analyzing financial goals..."):
            # This would integrate with the GoalPlannerAgent
            st.success("✅ Goal analysis completed!")
            st.info("""
            **Goal Analysis Results:**
            - Progress tracking
            - Timeline adjustments
            - Savings recommendations
            - Investment suggestions
            
            *Note: This is a demonstration. In a full implementation, this would call the GoalPlannerAgent.*
            """)
    except Exception as e:
        st.error(f"❌ Goal analysis failed: {str(e)}")

if __name__ == "__main__":
    main()
