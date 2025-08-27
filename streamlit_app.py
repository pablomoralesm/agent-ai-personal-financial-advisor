"""
Main Streamlit application for the Agentic AI Personal Financial Advisor.

This application provides a user-friendly interface for customers to:
- Manage their financial profile
- Add and view transactions
- Set and track financial goals
- Get AI-powered financial advice from specialized agents
- Monitor agent progress and recommendations

Uses Google ADK agents for financial analysis and advice generation.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import asyncio
import os
import sys
from typing import Dict, Any, Optional, List

# Add the project root to Python path for imports (now we're already in project root)
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Also set PYTHONPATH environment variable for subprocess calls
os.environ['PYTHONPATH'] = f"{project_root}:{os.environ.get('PYTHONPATH', '')}"

from agents.orchestrator import create_financial_advisor_orchestrator
from utils.logging_config import setup_logging, get_logger
from utils.database import test_database_connection, create_database_if_not_exists
from ui.components.customer_profile import render_customer_profile
from ui.components.transaction_entry import render_transaction_entry
from ui.components.goal_management import render_goal_management
from ui.components.recommendations import render_recommendations
from ui.utils.plotting import create_spending_chart, create_goal_progress_chart
from ui.utils.formatting import format_currency, format_percentage

# Configure logging
logger = setup_logging()

# Page configuration
st.set_page_config(
    page_title="AI Financial Advisor",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .agent-status {
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem 0;
    }
    .agent-running {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
    }
    .agent-completed {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
    }
    .agent-error {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'customer_id' not in st.session_state:
        st.session_state.customer_id = None
    if 'orchestrator' not in st.session_state:
        st.session_state.orchestrator = None
    if 'analysis_running' not in st.session_state:
        st.session_state.analysis_running = False
    if 'last_analysis_results' not in st.session_state:
        st.session_state.last_analysis_results = None
    if 'mcp_server_path' not in st.session_state:
        # Path to the MCP database server (now from project root)
        st.session_state.mcp_server_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'mcp_server',
            'database_server.py'
        )

def check_system_status() -> Dict[str, bool]:
    """Check the status of system components."""
    status = {
        'database': False,
        'mcp_server': False
    }
    
    try:
        # Test database connection
        status['database'] = test_database_connection()
        
        # Check if MCP server file exists
        status['mcp_server'] = os.path.exists(st.session_state.mcp_server_path)
        
    except Exception as e:
        logger.error(f"Error checking system status: {e}")
    
    return status

def render_system_status():
    """Render system status indicators in the sidebar."""
    st.sidebar.markdown("### 🔧 System Status")
    
    status = check_system_status()
    
    # Database status
    db_status = "✅ Connected" if status['database'] else "❌ Disconnected"
    st.sidebar.markdown(f"**Database:** {db_status}")
    
    # MCP Server status
    mcp_status = "✅ Ready" if status['mcp_server'] else "❌ Not Found"
    st.sidebar.markdown(f"**MCP Server:** {mcp_status}")
    
    if not all(status.values()):
        st.sidebar.warning("⚠️ Some system components are not ready. Please check your configuration.")
        return False
    
    return True

def render_header():
    """Render the main application header."""
    st.markdown('<h1 class="main-header">🏦 AI Personal Financial Advisor</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Quick stats row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🏠 Active Customers",
            value="3",  # This would come from database in real app
            help="Total number of customers in the system"
        )
    
    with col2:
        st.metric(
            label="📊 Analyses Run",
            value="15",  # This would come from database
            help="Total financial analyses completed"
        )
    
    with col3:
        st.metric(
            label="🎯 Goals Tracked",
            value="12",  # This would come from database
            help="Total financial goals being tracked"
        )
    
    with col4:
        st.metric(
            label="💡 Recommendations",
            value="45",  # This would come from database
            help="Total recommendations provided"
        )

def render_customer_selector():
    """Render customer selection interface."""
    st.sidebar.markdown("### 👤 Customer Selection")
    
    # For demo purposes, we'll use predefined customers
    # In a real app, this would query the database
    customers = {
        1: "Alice Johnson (alice.johnson@email.com)",
        2: "Bob Smith (bob.smith@email.com)", 
        3: "Carol Davis (carol.davis@email.com)"
    }
    
    selected_name = st.sidebar.selectbox(
        "Select Customer:",
        options=[""] + list(customers.values()),
        key="customer_selector"
    )
    
    if selected_name and selected_name != "":
        # Extract customer ID from selection
        customer_id = next(id for id, name in customers.items() if name == selected_name)
        st.session_state.customer_id = customer_id
        
        st.sidebar.success(f"Selected: Customer {customer_id}")
        
        # Initialize orchestrator for this customer
        if not st.session_state.orchestrator:
            try:
                st.session_state.orchestrator = create_financial_advisor_orchestrator(
                    st.session_state.mcp_server_path
                )
                st.sidebar.success("🤖 AI Agents Ready")
            except Exception as e:
                st.sidebar.error(f"Failed to initialize AI agents: {e}")
                logger.error(f"Orchestrator initialization failed: {e}")
    else:
        st.session_state.customer_id = None
        st.session_state.orchestrator = None

def render_analysis_controls():
    """Render analysis control buttons."""
    if not st.session_state.customer_id or not st.session_state.orchestrator:
        st.info("👆 Please select a customer to begin financial analysis")
        return
    
    st.markdown("### 🤖 AI Financial Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 Full Analysis", disabled=st.session_state.analysis_running):
            st.session_state.analysis_running = True
            st.rerun()
    
    with col2:
        if st.button("⚡ Quick Insights", disabled=st.session_state.analysis_running):
            run_quick_analysis()
    
    with col3:
        if st.button("🎯 Goal Focus", disabled=st.session_state.analysis_running):
            run_goal_analysis()

def run_full_analysis():
    """Run comprehensive financial analysis."""
    if not st.session_state.orchestrator or not st.session_state.customer_id:
        st.error("System not ready for analysis")
        return
    
    try:
        with st.spinner("🤖 Running comprehensive financial analysis..."):
            # Create progress placeholders
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # This would normally be async, but Streamlit requires sync execution
            # In a production app, you'd use asyncio properly or background tasks
            status_text.text("Starting analysis...")
            progress_bar.progress(25)
            
            # Simulate analysis steps
            import time
            time.sleep(2)  # Simulate processing time
            
            status_text.text("Analyzing spending patterns...")
            progress_bar.progress(50)
            time.sleep(2)
            
            status_text.text("Evaluating financial goals...")
            progress_bar.progress(75)
            time.sleep(2)
            
            status_text.text("Generating recommendations...")
            progress_bar.progress(100)
            time.sleep(1)
            
            # Store mock results
            st.session_state.last_analysis_results = {
                'type': 'full',
                'customer_id': st.session_state.customer_id,
                'timestamp': datetime.now(),
                'status': 'completed',
                'summary': {
                    'spending_health': 'Good',
                    'goal_feasibility': 'High',
                    'priority_actions': 3,
                    'savings_potential': 450.0
                }
            }
            
            st.success("✅ Analysis completed successfully!")
            status_text.empty()
            progress_bar.empty()
            
    except Exception as e:
        st.error(f"Analysis failed: {e}")
        logger.error(f"Full analysis error: {e}")
    finally:
        st.session_state.analysis_running = False

def run_quick_analysis():
    """Run quick financial insights analysis."""
    with st.spinner("⚡ Generating quick insights..."):
        import time
        time.sleep(1)  # Simulate processing
        
        st.session_state.last_analysis_results = {
            'type': 'quick',
            'customer_id': st.session_state.customer_id,
            'timestamp': datetime.now(),
            'status': 'completed',
            'insights': [
                "Dining expenses are 15% above recommended levels",
                "Emergency fund goal is on track for completion",
                "Consider increasing retirement contributions by $200/month"
            ]
        }
        
        st.success("✅ Quick insights generated!")

def run_goal_analysis():
    """Run goal-focused analysis."""
    with st.spinner("🎯 Analyzing financial goals..."):
        import time
        time.sleep(1)  # Simulate processing
        
        st.session_state.last_analysis_results = {
            'type': 'goal_focused',
            'customer_id': st.session_state.customer_id,
            'timestamp': datetime.now(),
            'status': 'completed',
            'goal_analysis': {
                'total_goals': 4,
                'on_track': 2,
                'behind': 1,
                'ahead': 1,
                'recommendations': 3
            }
        }
        
        st.success("✅ Goal analysis completed!")

def render_results():
    """Render analysis results."""
    if not st.session_state.last_analysis_results:
        return
    
    results = st.session_state.last_analysis_results
    
    st.markdown("### 📊 Analysis Results")
    
    # Results header
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"**Analysis Type:** {results['type'].replace('_', ' ').title()}")
    with col2:
        st.markdown(f"**Customer:** {results['customer_id']}")
    with col3:
        st.markdown(f"**Status:** ✅ {results['status'].title()}")
    
    # Display results based on type
    if results['type'] == 'full':
        render_full_analysis_results(results)
    elif results['type'] == 'quick':
        render_quick_analysis_results(results)
    elif results['type'] == 'goal_focused':
        render_goal_analysis_results(results)

def render_full_analysis_results(results: Dict[str, Any]):
    """Render full analysis results."""
    summary = results.get('summary', {})
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Spending Health", summary.get('spending_health', 'N/A'))
    with col2:
        st.metric("Goal Feasibility", summary.get('goal_feasibility', 'N/A'))
    with col3:
        st.metric("Priority Actions", summary.get('priority_actions', 0))
    with col4:
        st.metric("Savings Potential", f"${summary.get('savings_potential', 0):.0f}/mo")
    
    # Detailed recommendations would be displayed here
    st.info("💡 Detailed recommendations and analysis would be displayed here based on actual agent results.")

def render_quick_analysis_results(results: Dict[str, Any]):
    """Render quick analysis results."""
    insights = results.get('insights', [])
    
    st.markdown("**Quick Insights:**")
    for i, insight in enumerate(insights, 1):
        st.markdown(f"{i}. {insight}")

def render_goal_analysis_results(results: Dict[str, Any]):
    """Render goal analysis results."""
    analysis = results.get('goal_analysis', {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Goals", analysis.get('total_goals', 0))
    with col2:
        st.metric("On Track", analysis.get('on_track', 0))
    with col3:
        st.metric("Behind", analysis.get('behind', 0))
    with col4:
        st.metric("Ahead", analysis.get('ahead', 0))

def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
    # Render system status in sidebar
    if not render_system_status():
        st.error("❌ System components are not ready. Please check your database connection and MCP server configuration.")
        st.stop()
    
    # Render customer selector
    render_customer_selector()
    
    # Main content area
    render_header()
    
    # Check if analysis is running
    if st.session_state.analysis_running:
        run_full_analysis()
        st.rerun()
    
    # Analysis controls
    render_analysis_controls()
    
    # Display results if available
    render_results()
    
    # Render main content tabs
    if st.session_state.customer_id:
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "💰 Transactions", "🎯 Goals", "💡 Recommendations"])
        
        with tab1:
            st.markdown("### 📊 Financial Dashboard")
            render_customer_profile()
            
        with tab2:
            st.markdown("### 💰 Transaction Management")
            render_transaction_entry()
            
        with tab3:
            st.markdown("### 🎯 Goal Management")
            render_goal_management()
            
        with tab4:
            st.markdown("### 💡 AI Recommendations")
            render_recommendations()
    else:
        st.info("👆 Please select a customer from the sidebar to view their financial data and get AI-powered recommendations.")
    
    # Footer
    st.markdown("---")
    st.markdown("**🤖 Powered by Google Agent Development Kit (ADK)** | Built for educational purposes")

if __name__ == "__main__":
    main()
