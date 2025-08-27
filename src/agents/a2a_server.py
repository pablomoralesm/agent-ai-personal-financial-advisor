"""A2A server implementation for the Financial Advisor app.

This module implements A2A servers for each agent to expose their functionality
to other agents.
"""

import logging
from typing import Dict, Any

from google.adk.a2a import A2AServer

from src.agents.spending_analyzer_agent import SpendingAnalyzerAgent
from src.agents.goal_planner_agent import GoalPlannerAgent
from src.agents.advisor_agent import AdvisorAgent

class SpendingAnalyzerA2AServer:
    """A2A server for the SpendingAnalyzerAgent."""
    
    def __init__(self, agent: SpendingAnalyzerAgent, host: str = "localhost", port: int = 8081):
        """Initialize the A2A server.
        
        Args:
            agent: SpendingAnalyzerAgent instance
            host: Host address
            port: Port number
        """
        self.agent = agent
        self.host = host
        self.port = port
        self.server = A2AServer()
        self._register_functions()
    
    def _register_functions(self):
        """Register agent functions with the A2A server."""
        self.server.register_function(
            "analyze_customer_spending",
            self.agent.analyze_customer_spending,
            "Analyze customer spending and provide insights"
        )
    
    def start(self):
        """Start the A2A server."""
        logging.info(f"Starting SpendingAnalyzerA2AServer at {self.host}:{self.port}")
        self.server.serve(host=self.host, port=self.port)

class GoalPlannerA2AServer:
    """A2A server for the GoalPlannerAgent."""
    
    def __init__(self, agent: GoalPlannerAgent, host: str = "localhost", port: int = 8082):
        """Initialize the A2A server.
        
        Args:
            agent: GoalPlannerAgent instance
            host: Host address
            port: Port number
        """
        self.agent = agent
        self.host = host
        self.port = port
        self.server = A2AServer()
        self._register_functions()
    
    def _register_functions(self):
        """Register agent functions with the A2A server."""
        self.server.register_function(
            "plan_customer_goals",
            self.agent.plan_customer_goals,
            "Plan and evaluate customer goals"
        )
    
    def start(self):
        """Start the A2A server."""
        logging.info(f"Starting GoalPlannerA2AServer at {self.host}:{self.port}")
        self.server.serve(host=self.host, port=self.port)

class AdvisorA2AServer:
    """A2A server for the AdvisorAgent."""
    
    def __init__(self, agent: AdvisorAgent, host: str = "localhost", port: int = 8083):
        """Initialize the A2A server.
        
        Args:
            agent: AdvisorAgent instance
            host: Host address
            port: Port number
        """
        self.agent = agent
        self.host = host
        self.port = port
        self.server = A2AServer()
        self._register_functions()
    
    def _register_functions(self):
        """Register agent functions with the A2A server."""
        self.server.register_function(
            "provide_financial_advice",
            self.agent.provide_financial_advice,
            "Provide comprehensive financial advice for a customer"
        )
    
    def start(self):
        """Start the A2A server."""
        logging.info(f"Starting AdvisorA2AServer at {self.host}:{self.port}")
        self.server.serve(host=self.host, port=self.port)
