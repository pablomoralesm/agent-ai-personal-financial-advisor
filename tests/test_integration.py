"""Integration tests for the Financial Advisor app."""

import os
import sys
import unittest
import datetime
import time
import threading
import logging

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.mcp.mcp_server import FinancialAdvisorMcpServer
from src.mcp.mcp_client import FinancialAdvisorMcpClient
from src.agents.spending_analyzer_agent import SpendingAnalyzerAgent
from src.agents.goal_planner_agent import GoalPlannerAgent
from src.agents.advisor_agent import AdvisorAgent
from src.agents.a2a_server import (
    SpendingAnalyzerA2AServer,
    GoalPlannerA2AServer,
    AdvisorA2AServer
)
from src.db.init_db import init_database
from src.utils.config import GOOGLE_API_KEY

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class IntegrationTest(unittest.TestCase):
    """Integration tests for the Financial Advisor app."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        # Initialize database
        init_database()
        
        # Start MCP server
        cls.mcp_server = FinancialAdvisorMcpServer()
        cls.mcp_server_thread = threading.Thread(
            target=cls.mcp_server.start,
            args=("localhost", 8080),
            daemon=True
        )
        cls.mcp_server_thread.start()
        
        # Wait for server to start
        time.sleep(2)
        
        # Create MCP client
        cls.mcp_client = FinancialAdvisorMcpClient(host="localhost", port=8080)
        
        # Create agents
        cls.spending_analyzer_agent = SpendingAnalyzerAgent(
            mcp_client=cls.mcp_client,
            api_key=GOOGLE_API_KEY
        )
        
        cls.goal_planner_agent = GoalPlannerAgent(
            mcp_client=cls.mcp_client,
            api_key=GOOGLE_API_KEY
        )
        
        # Start A2A servers
        cls.spending_analyzer_a2a_server = SpendingAnalyzerA2AServer(
            agent=cls.spending_analyzer_agent,
            host="localhost",
            port=8081
        )
        cls.spending_analyzer_thread = threading.Thread(
            target=cls.spending_analyzer_a2a_server.start,
            daemon=True
        )
        cls.spending_analyzer_thread.start()
        
        cls.goal_planner_a2a_server = GoalPlannerA2AServer(
            agent=cls.goal_planner_agent,
            host="localhost",
            port=8082
        )
        cls.goal_planner_thread = threading.Thread(
            target=cls.goal_planner_a2a_server.start,
            daemon=True
        )
        cls.goal_planner_thread.start()
        
        # Wait for A2A servers to start
        time.sleep(2)
        
        # Create advisor agent
        cls.advisor_agent = AdvisorAgent(
            mcp_client=cls.mcp_client,
            api_key=GOOGLE_API_KEY,
            spending_analyzer_url="http://localhost:8081",
            goal_planner_url="http://localhost:8082"
        )
        
        # Create test customer
        cls.test_customer = cls.mcp_client.create_customer(
            name="Test Customer",
            email="test@example.com"
        )
        
        # Create test transactions
        today = datetime.date.today()
        
        # Add transactions for the past 3 months
        for i in range(90):
            date = today - datetime.timedelta(days=i)
            
            # Rent (monthly)
            if date.day == 1:
                cls.mcp_client.add_transaction(
                    customer_id=cls.test_customer["id"],
                    amount=1200.00,
                    category="Housing",
                    transaction_date=date.isoformat(),
                    description="Monthly rent"
                )
            
            # Groceries (weekly)
            if date.weekday() == 0:  # Monday
                cls.mcp_client.add_transaction(
                    customer_id=cls.test_customer["id"],
                    amount=120.00,
                    category="Food",
                    transaction_date=date.isoformat(),
                    description="Weekly groceries"
                )
            
            # Entertainment (random)
            if date.day % 10 == 0:
                cls.mcp_client.add_transaction(
                    customer_id=cls.test_customer["id"],
                    amount=50.00,
                    category="Entertainment",
                    transaction_date=date.isoformat(),
                    description="Movies and dining out"
                )
        
        # Create test goals
        cls.mcp_client.create_goal(
            customer_id=cls.test_customer["id"],
            goal_type="Emergency Fund",
            target_amount=10000.00,
            current_amount=2000.00,
            target_date=(today + datetime.timedelta(days=365)).isoformat(),
            description="Build emergency fund"
        )
        
        cls.mcp_client.create_goal(
            customer_id=cls.test_customer["id"],
            goal_type="Vacation",
            target_amount=3000.00,
            current_amount=500.00,
            target_date=(today + datetime.timedelta(days=180)).isoformat(),
            description="Summer vacation"
        )
    
    def test_spending_analyzer(self):
        """Test SpendingAnalyzerAgent."""
        result = self.spending_analyzer_agent.analyze_customer_spending(
            self.test_customer["id"],
            months=3
        )
        
        # Verify result structure
        self.assertIn("customer", result)
        self.assertIn("spending_patterns", result)
        self.assertIn("high_spending", result)
        self.assertIn("trends", result)
        
        # Verify spending patterns
        spending_patterns = result["spending_patterns"]
        self.assertIn("total_spending", spending_patterns)
        self.assertIn("avg_monthly_spending", spending_patterns)
        self.assertIn("spending_by_category", spending_patterns)
        
        # Verify high spending categories
        high_spending = result["high_spending"]
        self.assertIn("high_spending_categories", high_spending)
        
        # Verify trends
        trends = result["trends"]
        self.assertIn("trend", trends)
        self.assertIn("monthly_data", trends)
    
    def test_goal_planner(self):
        """Test GoalPlannerAgent."""
        result = self.goal_planner_agent.plan_customer_goals(
            self.test_customer["id"],
            avg_monthly_spending=2000.00
        )
        
        # Verify result structure
        self.assertIn("customer", result)
        self.assertIn("goals", result)
        self.assertIn("has_goals", result)
        self.assertTrue(result["has_goals"])
        self.assertIn("recommendations", result)
        self.assertIn("goal_analysis", result)
        
        # Verify recommendations
        recommendations = result["recommendations"]
        self.assertIn("goal_recommendations", recommendations)
        self.assertIn("total_monthly_contribution", recommendations)
        self.assertIn("estimated_savings_capacity", recommendations)
        self.assertIn("overall_realistic", recommendations)
        
        # Verify goal analysis
        goal_analysis = result["goal_analysis"]
        self.assertTrue(len(goal_analysis) > 0)
        for goal in goal_analysis:
            self.assertIn("goal", goal)
            self.assertIn("progress", goal)
            self.assertIn("monthly_contribution", goal)
            self.assertIn("is_realistic", goal)
            self.assertIn("months_remaining", goal)
            self.assertIn("feasibility", goal)
    
    def test_advisor_agent(self):
        """Test AdvisorAgent."""
        result = self.advisor_agent.provide_financial_advice(
            self.test_customer["id"],
            months=3
        )
        
        # Verify result structure
        self.assertIn("customer", result)
        self.assertIn("spending_analysis", result)
        self.assertIn("goal_planning", result)
        self.assertIn("advice", result)
        self.assertIn("next_steps", result)
        
        # Verify advice
        advice = result["advice"]
        self.assertIn("advice_text", advice)
        self.assertTrue(len(advice["advice_text"]) > 0)
        
        # Verify next steps
        next_steps = result["next_steps"]
        self.assertIn("next_steps", next_steps)
        self.assertTrue(len(next_steps["next_steps"]) > 0)
        
        # Check that advice was saved
        advice_history = self.mcp_client.get_customer_advice_history(self.test_customer["id"])
        self.assertTrue(len(advice_history) > 0)
        
        # Verify advice from all agents
        agent_names = [advice["agent_name"] for advice in advice_history]
        self.assertIn("SpendingAnalyzerAgent", agent_names)
        self.assertIn("GoalPlannerAgent", agent_names)
        self.assertIn("AdvisorAgent", agent_names)

if __name__ == "__main__":
    unittest.main()
