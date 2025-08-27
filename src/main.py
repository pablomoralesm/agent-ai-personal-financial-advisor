"""Main entry point for the Financial Advisor app."""

import logging
import threading
import time
import subprocess
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.mcp.mcp_server import FinancialAdvisorMcpServer
from src.agents.agent_manager import AgentManager
from src.db.init_db import init_database
from src.utils.config import GOOGLE_API_KEY

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def start_mcp_server():
    """Start the MCP server."""
    mcp_server = FinancialAdvisorMcpServer()
    mcp_server.start(host="localhost", port=8080)

def start_a2a_servers():
    """Start the A2A servers."""
    agent_manager = AgentManager()
    agent_manager.initialize_agents()
    agent_manager.start_servers()

def start_streamlit():
    """Start the Streamlit UI."""
    streamlit_path = os.path.join(os.path.dirname(__file__), 'ui', 'app.py')
    subprocess.run(["streamlit", "run", streamlit_path])

def main():
    """Main function to start all components."""
    logging.info("Initializing Financial Advisor app...")
    
    # Initialize database
    logging.info("Initializing database...")
    init_database()
    
    # Start MCP server in a thread
    logging.info("Starting MCP server...")
    mcp_thread = threading.Thread(target=start_mcp_server, daemon=True)
    mcp_thread.start()
    
    # Wait for MCP server to start
    time.sleep(2)
    
    # Start A2A servers in a thread
    logging.info("Starting A2A servers...")
    a2a_thread = threading.Thread(target=start_a2a_servers, daemon=True)
    a2a_thread.start()
    
    # Wait for A2A servers to start
    time.sleep(2)
    
    # Start Streamlit UI
    logging.info("Starting Streamlit UI...")
    start_streamlit()

if __name__ == "__main__":
    main()
