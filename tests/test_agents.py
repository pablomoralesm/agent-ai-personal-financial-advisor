"""
Tests for the AI agents in the Personal Financial Advisor application.

This module tests the core functionality of:
- SpendingAnalyzerAgent
- GoalPlannerAgent  
- AdvisorAgent
- FinancialAdvisorOrchestrator

These tests ensure the agents can be created, have proper tools, and follow ADK patterns.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import os
import sys

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from agents.spending_analyzer import create_spending_analyzer_agent
from agents.goal_planner import create_goal_planner_agent
from agents.advisor import create_advisor_agent
from agents.orchestrator import create_financial_advisor_orchestrator


class TestSpendingAnalyzerAgent(unittest.TestCase):
    """Test the SpendingAnalyzerAgent creation and configuration."""
    
    def setUp(self):
        """Set up test environment."""
        self.mock_mcp_server_path = "/mock/path/to/mcp_server.py"
    
    def test_create_spending_analyzer_agent_import(self):
        """Test that SpendingAnalyzerAgent can be imported and created."""
        try:
            # Test that the agent can be created without errors
            agent = create_spending_analyzer_agent(self.mock_mcp_server_path)
            
            # Verify agent was created
            self.assertIsNotNone(agent)
            
            # Verify it's the expected type
            from agents.spending_analyzer import SpendingAnalyzerAgent
            self.assertIsInstance(agent, SpendingAnalyzerAgent)
            
        except Exception as e:
            self.fail(f"Failed to create SpendingAnalyzerAgent: {e}")
    
    def test_spending_analyzer_agent_attributes(self):
        """Test that SpendingAnalyzerAgent has expected attributes."""
        try:
            agent = create_spending_analyzer_agent(self.mock_mcp_server_path)
            
            # Verify agent has expected attributes
            self.assertTrue(hasattr(agent, 'mcp_server_path'))
            self.assertTrue(hasattr(agent, 'agent'))
            
            # Verify MCP server path was set correctly
            self.assertEqual(agent.mcp_server_path, self.mock_mcp_server_path)
            
        except Exception as e:
            self.fail(f"Failed to verify SpendingAnalyzerAgent attributes: {e}")


class TestGoalPlannerAgent(unittest.TestCase):
    """Test the GoalPlannerAgent creation and configuration."""
    
    def setUp(self):
        """Set up test environment."""
        self.mock_mcp_server_path = "/mock/path/to/mcp_server.py"
    
    def test_create_goal_planner_agent_import(self):
        """Test that GoalPlannerAgent can be imported and created."""
        try:
            # Test that the agent can be created without errors
            agent = create_goal_planner_agent(self.mock_mcp_server_path)
            
            # Verify agent was created
            self.assertIsNotNone(agent)
            
            # Verify it's the expected type
            from agents.goal_planner import GoalPlannerAgent
            self.assertIsInstance(agent, GoalPlannerAgent)
            
        except Exception as e:
            self.fail(f"Failed to create GoalPlannerAgent: {e}")
    
    def test_goal_planner_agent_attributes(self):
        """Test that GoalPlannerAgent has expected attributes."""
        try:
            agent = create_goal_planner_agent(self.mock_mcp_server_path)
            
            # Verify agent has expected attributes
            self.assertTrue(hasattr(agent, 'mcp_server_path'))
            self.assertTrue(hasattr(agent, 'agent'))
            
            # Verify MCP server path was set correctly
            self.assertEqual(agent.mcp_server_path, self.mock_mcp_server_path)
            
        except Exception as e:
            self.fail(f"Failed to verify GoalPlannerAgent attributes: {e}")


class TestAdvisorAgent(unittest.TestCase):
    """Test the AdvisorAgent creation and configuration."""
    
    def setUp(self):
        """Set up test environment."""
        self.mock_mcp_server_path = "/mock/path/to/mcp_server.py"
    
    def test_create_advisor_agent_import(self):
        """Test that AdvisorAgent can be imported and created."""
        try:
            # Test that the agent can be created without errors
            agent = create_advisor_agent(self.mock_mcp_server_path)
            
            # Verify agent was created
            self.assertIsNotNone(agent)
            
            # Verify it's the expected type
            from agents.advisor import AdvisorAgent
            self.assertIsInstance(agent, AdvisorAgent)
            
        except Exception as e:
            self.fail(f"Failed to create AdvisorAgent: {e}")
    
    def test_advisor_agent_attributes(self):
        """Test that AdvisorAgent has expected attributes."""
        try:
            agent = create_advisor_agent(self.mock_mcp_server_path)
            
            # Verify agent has expected attributes
            self.assertTrue(hasattr(agent, 'mcp_server_path'))
            self.assertTrue(hasattr(agent, 'agent'))
            
            # Verify MCP server path was set correctly
            self.assertEqual(agent.mcp_server_path, self.mock_mcp_server_path)
            
        except Exception as e:
            self.fail(f"Failed to verify AdvisorAgent attributes: {e}")


class TestFinancialAdvisorOrchestrator(unittest.TestCase):
    """Test the FinancialAdvisorOrchestrator creation and configuration."""
    
    def setUp(self):
        """Set up test environment."""
        self.mock_mcp_server_path = "/mock/path/to/mcp_server_path"
    
    def test_create_financial_advisor_orchestrator_import(self):
        """Test that FinancialAdvisorOrchestrator can be imported and created."""
        try:
            # Test that the orchestrator can be created without errors
            orchestrator = create_financial_advisor_orchestrator(self.mock_mcp_server_path)
            
            # Verify orchestrator was created
            self.assertIsNotNone(orchestrator)
            
            # Verify it's the expected type
            from agents.orchestrator import FinancialAdvisorOrchestrator
            self.assertIsInstance(orchestrator, FinancialAdvisorOrchestrator)
            
        except Exception as e:
            self.fail(f"Failed to create FinancialAdvisorOrchestrator: {e}")
    
    def test_orchestrator_agent_attributes(self):
        """Test that FinancialAdvisorOrchestrator has expected attributes."""
        try:
            orchestrator = create_financial_advisor_orchestrator(self.mock_mcp_server_path)
            
            # Verify orchestrator has expected attributes
            self.assertTrue(hasattr(orchestrator, '_mcp_server_path'))
            self.assertTrue(hasattr(orchestrator, '_spending_analyzer'))
            self.assertTrue(hasattr(orchestrator, '_goal_planner'))
            self.assertTrue(hasattr(orchestrator, '_advisor'))
            
            # Verify MCP server path was set correctly
            self.assertEqual(orchestrator._mcp_server_path, self.mock_mcp_server_path)
            
        except Exception as e:
            self.fail(f"Failed to verify FinancialAdvisorOrchestrator attributes: {e}")


class TestAgentIntegration(unittest.TestCase):
    """Test that agents can work together properly."""
    
    def test_agent_imports(self):
        """Test that all agent modules can be imported without errors."""
        try:
            from agents.spending_analyzer import SpendingAnalyzerAgent
            from agents.goal_planner import GoalPlannerAgent
            from agents.advisor import AdvisorAgent
            from agents.orchestrator import FinancialAdvisorOrchestrator
        except ImportError as e:
            self.fail(f"Failed to import agent classes: {e}")
    
    def test_agent_class_definitions(self):
        """Test that agent classes are properly defined."""
        from agents.spending_analyzer import SpendingAnalyzerAgent
        from agents.goal_planner import GoalPlannerAgent
        from agents.advisor import AdvisorAgent
        from agents.orchestrator import FinancialAdvisorOrchestrator
        
        # Verify classes exist and are callable
        self.assertTrue(callable(SpendingAnalyzerAgent))
        self.assertTrue(callable(GoalPlannerAgent))
        self.assertTrue(callable(AdvisorAgent))
        self.assertTrue(callable(FinancialAdvisorOrchestrator))
    
    def test_agent_creation_functions(self):
        """Test that all agent creation functions work."""
        mock_path = "/mock/path/to/mcp_server.py"
        
        try:
            # Test all agent creation functions
            spending_agent = create_spending_analyzer_agent(mock_path)
            goal_agent = create_goal_planner_agent(mock_path)
            advisor_agent = create_advisor_agent(mock_path)
            orchestrator = create_financial_advisor_orchestrator(mock_path)
            
            # Verify all agents were created
            self.assertIsNotNone(spending_agent)
            self.assertIsNotNone(goal_agent)
            self.assertIsNotNone(advisor_agent)
            self.assertIsNotNone(orchestrator)
            
        except Exception as e:
            self.fail(f"Failed to create agents: {e}")


if __name__ == '__main__':
    unittest.main()
