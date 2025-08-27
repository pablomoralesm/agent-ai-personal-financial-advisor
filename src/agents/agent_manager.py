"""Agent manager for the Financial Advisor app.

This module orchestrates the creation and interaction of all agents.
"""

import logging
import threading
from typing import Dict, Any, List, Optional

from src.mcp.mcp_client import FinancialAdvisorMcpClient
from src.mcp.mcp_server import FinancialAdvisorMcpServer
from src.agents.spending_analyzer_agent import SpendingAnalyzerAgent
from src.agents.goal_planner_agent import GoalPlannerAgent
from src.agents.advisor_agent import AdvisorAgent
from src.agents.a2a_server import (
    SpendingAnalyzerA2AServer,
    GoalPlannerA2AServer,
    AdvisorA2AServer
)
from src.utils.config import GOOGLE_API_KEY

class AgentManager:
    """Manager for all agents in the Financial Advisor app."""
    
    def __init__(self):
        """Initialize the agent manager."""
        self.mcp_server = None
        self.mcp_client = None
        self.spending_analyzer_agent = None
        self.goal_planner_agent = None
        self.advisor_agent = None
        self.spending_analyzer_a2a_server = None
        self.goal_planner_a2a_server = None
        self.advisor_a2a_server = None
        self.servers_running = False
        self.server_threads = []
    
    def initialize_agents(self):
        """Initialize all agents and servers."""
        # Create MCP client
        self.mcp_client = FinancialAdvisorMcpClient(host="localhost", port=8080)
        
        # Create agents
        self.spending_analyzer_agent = SpendingAnalyzerAgent(
            mcp_client=self.mcp_client,
            api_key=GOOGLE_API_KEY
        )
        
        self.goal_planner_agent = GoalPlannerAgent(
            mcp_client=self.mcp_client,
            api_key=GOOGLE_API_KEY
        )
        
        self.advisor_agent = AdvisorAgent(
            mcp_client=self.mcp_client,
            api_key=GOOGLE_API_KEY,
            spending_analyzer_url="http://localhost:8081",
            goal_planner_url="http://localhost:8082"
        )
        
        # Create A2A servers
        self.spending_analyzer_a2a_server = SpendingAnalyzerA2AServer(
            agent=self.spending_analyzer_agent,
            host="localhost",
            port=8081
        )
        
        self.goal_planner_a2a_server = GoalPlannerA2AServer(
            agent=self.goal_planner_agent,
            host="localhost",
            port=8082
        )
        
        self.advisor_a2a_server = AdvisorA2AServer(
            agent=self.advisor_agent,
            host="localhost",
            port=8083
        )
        
        logging.info("All agents initialized successfully")
    
    def start_servers(self):
        """Start all servers in separate threads."""
        if self.servers_running:
            logging.warning("Servers are already running")
            return
        
        # Create MCP server
        self.mcp_server = FinancialAdvisorMcpServer()
        
        # Start MCP server in a thread
        mcp_thread = threading.Thread(
            target=self.mcp_server.start,
            args=("localhost", 8080),
            daemon=True
        )
        mcp_thread.start()
        self.server_threads.append(mcp_thread)
        
        # Start A2A servers in threads
        spending_analyzer_thread = threading.Thread(
            target=self.spending_analyzer_a2a_server.start,
            daemon=True
        )
        spending_analyzer_thread.start()
        self.server_threads.append(spending_analyzer_thread)
        
        goal_planner_thread = threading.Thread(
            target=self.goal_planner_a2a_server.start,
            daemon=True
        )
        goal_planner_thread.start()
        self.server_threads.append(goal_planner_thread)
        
        advisor_thread = threading.Thread(
            target=self.advisor_a2a_server.start,
            daemon=True
        )
        advisor_thread.start()
        self.server_threads.append(advisor_thread)
        
        self.servers_running = True
        logging.info("All servers started successfully")
    
    def get_spending_analysis(self, customer_id: int, months: int = 3) -> Dict[str, Any]:
        """Get spending analysis for a customer.
        
        Args:
            customer_id: Customer ID
            months: Number of months to analyze
            
        Returns:
            Dict[str, Any]: Spending analysis
        """
        if not self.spending_analyzer_agent:
            self.initialize_agents()
        
        return self.spending_analyzer_agent.analyze_customer_spending(customer_id, months)
    
    def get_goal_planning(self, customer_id: int, avg_monthly_spending: float) -> Dict[str, Any]:
        """Get goal planning for a customer.
        
        Args:
            customer_id: Customer ID
            avg_monthly_spending: Average monthly spending
            
        Returns:
            Dict[str, Any]: Goal planning
        """
        if not self.goal_planner_agent:
            self.initialize_agents()
        
        return self.goal_planner_agent.plan_customer_goals(customer_id, avg_monthly_spending)
    
    def get_financial_advice(self, customer_id: int, months: int = 3) -> Dict[str, Any]:
        """Get comprehensive financial advice for a customer.
        
        Args:
            customer_id: Customer ID
            months: Number of months to analyze
            
        Returns:
            Dict[str, Any]: Financial advice
        """
        if not self.advisor_agent:
            self.initialize_agents()
        
        return self.advisor_agent.provide_financial_advice(customer_id, months)
    
    def get_customers(self) -> List[Dict[str, Any]]:
        """Get all customers.
        
        Returns:
            List[Dict[str, Any]]: List of customers
        """
        if not self.mcp_client:
            self.mcp_client = FinancialAdvisorMcpClient(host="localhost", port=8080)
        
        try:
            return self.mcp_client.get_customers()
        except Exception as e:
            logging.error(f"Error getting customers: {e}")
            return []
    
    def get_customer(self, customer_id: int) -> Optional[Dict[str, Any]]:
        """Get customer by ID.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            Optional[Dict[str, Any]]: Customer data
        """
        if not self.mcp_client:
            self.mcp_client = FinancialAdvisorMcpClient(host="localhost", port=8080)
        
        try:
            return self.mcp_client.get_customer(customer_id)
        except Exception as e:
            logging.error(f"Error getting customer {customer_id}: {e}")
            return None
    
    def create_customer(self, name: str, email: str) -> Optional[Dict[str, Any]]:
        """Create a new customer.
        
        Args:
            name: Customer name
            email: Customer email
            
        Returns:
            Optional[Dict[str, Any]]: Created customer data
        """
        if not self.mcp_client:
            self.mcp_client = FinancialAdvisorMcpClient(host="localhost", port=8080)
        
        try:
            return self.mcp_client.create_customer(name, email)
        except Exception as e:
            logging.error(f"Error creating customer: {e}")
            return None
    
    def add_transaction(self, customer_id: int, amount: float, category: str,
                       transaction_date: str, description: str) -> Optional[Dict[str, Any]]:
        """Add a new transaction for a customer.
        
        Args:
            customer_id: Customer ID
            amount: Transaction amount
            category: Transaction category
            transaction_date: Transaction date (YYYY-MM-DD)
            description: Transaction description
            
        Returns:
            Optional[Dict[str, Any]]: Created transaction data
        """
        if not self.mcp_client:
            self.mcp_client = FinancialAdvisorMcpClient(host="localhost", port=8080)
        
        try:
            return self.mcp_client.add_transaction(
                customer_id, amount, category, transaction_date, description
            )
        except Exception as e:
            logging.error(f"Error adding transaction: {e}")
            return None
    
    def create_goal(self, customer_id: int, goal_type: str, target_amount: float,
                   current_amount: float, target_date: str, description: str) -> Optional[Dict[str, Any]]:
        """Create a new goal for a customer.
        
        Args:
            customer_id: Customer ID
            goal_type: Goal type
            target_amount: Target amount
            current_amount: Current amount
            target_date: Target date (YYYY-MM-DD)
            description: Goal description
            
        Returns:
            Optional[Dict[str, Any]]: Created goal data
        """
        if not self.mcp_client:
            self.mcp_client = FinancialAdvisorMcpClient(host="localhost", port=8080)
        
        try:
            return self.mcp_client.create_goal(
                customer_id, goal_type, target_amount, current_amount, target_date, description
            )
        except Exception as e:
            logging.error(f"Error creating goal: {e}")
            return None
    
    def get_customer_transactions(self, customer_id: int) -> List[Dict[str, Any]]:
        """Get all transactions for a customer.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            List[Dict[str, Any]]: List of transactions
        """
        if not self.mcp_client:
            self.mcp_client = FinancialAdvisorMcpClient(host="localhost", port=8080)
        
        try:
            return self.mcp_client.get_customer_transactions(customer_id)
        except Exception as e:
            logging.error(f"Error getting transactions for customer {customer_id}: {e}")
            return []
    
    def get_customer_goals(self, customer_id: int) -> List[Dict[str, Any]]:
        """Get all goals for a customer.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            List[Dict[str, Any]]: List of goals
        """
        if not self.mcp_client:
            self.mcp_client = FinancialAdvisorMcpClient(host="localhost", port=8080)
        
        try:
            return self.mcp_client.get_customer_goals(customer_id)
        except Exception as e:
            logging.error(f"Error getting goals for customer {customer_id}: {e}")
            return []
    
    def get_customer_advice_history(self, customer_id: int) -> List[Dict[str, Any]]:
        """Get all advice history for a customer.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            List[Dict[str, Any]]: List of advice entries
        """
        if not self.mcp_client:
            self.mcp_client = FinancialAdvisorMcpClient(host="localhost", port=8080)
        
        try:
            return self.mcp_client.get_customer_advice_history(customer_id)
        except Exception as e:
            logging.error(f"Error getting advice history for customer {customer_id}: {e}")
            return []
