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
        
    @patch('agents.spending_analyzer.LlmAgent')
    @patch('agents.spending_analyzer.MCPToolset')
    @patch('agents.spending_analyzer.StdioServerParameters')
    def test_create_spending_analyzer_agent(self, mock_stdio, mock_mcp, mock_llm):
        """Test that SpendingAnalyzerAgent is created with correct configuration."""
        # Mock the MCPToolset and LlmAgent
        mock_mcp_instance = Mock()
        mock_mcp.return_value = mock_mcp_instance
        
        mock_llm_instance = Mock()
        mock_llm.return_value = mock_llm_instance
        
        # Create the agent
        agent = create_spending_analyzer_agent(self.mock_mcp_server_path)
        
        # Verify MCPToolset was created with correct parameters
        mock_mcp.assert_called_once()
        mock_stdio.assert_called_once_with(
            command="python3",  # Updated to match actual implementation
            args=[self.mock_mcp_server_path]
        )
        
        # Verify LlmAgent was created with correct configuration
        mock_llm.assert_called_once()
        call_args = mock_llm.call_args
        
        # Check that the agent has the expected name and description
        self.assertIn("SpendingAnalyzerAgent", str(call_args))
        self.assertIn("spending habits", str(call_args).lower())
        
        # Verify the agent was returned
        self.assertEqual(agent, mock_llm_instance)


class TestGoalPlannerAgent(unittest.TestCase):
    """Test the GoalPlannerAgent creation and configuration."""
    
    def setUp(self):
        """Set up test environment."""
        self.mock_mcp_server_path = "/mock/path/to/mcp_server.py"
        
    @patch('agents.goal_planner.LlmAgent')
    @patch('agents.goal_planner.MCPToolset')
    @patch('agents.goal_planner.StdioServerParameters')
    def test_create_goal_planner_agent(self, mock_stdio, mock_mcp, mock_llm):
        """Test that GoalPlannerAgent is created with correct configuration."""
        # Mock the MCPToolset and LlmAgent
        mock_mcp_instance = Mock()
        mock_mcp.return_value = mock_mcp_instance
        
        mock_llm_instance = Mock()
        mock_llm.return_value = mock_llm_instance
        
        # Create the agent
        agent = create_goal_planner_agent(self.mock_mcp_server_path)
        
        # Verify MCPToolset was created with correct parameters
        mock_mcp.assert_called_once()
        mock_stdio.assert_called_once_with(
            command="python3",  # Updated to match actual implementation
            args=[self.mock_mcp_server_path]
        )
        
        # Verify LlmAgent was created with correct configuration
        mock_llm.assert_called_once()
        call_args = mock_llm.call_args
        
        # Check that the agent has the expected name and description
        self.assertIn("GoalPlannerAgent", str(call_args))
        self.assertIn("financial goals", str(call_args).lower())
        
        # Verify the agent was returned
        self.assertEqual(agent, mock_llm_instance)


class TestAdvisorAgent(unittest.TestCase):
    """Test the AdvisorAgent creation and configuration."""
    
    def setUp(self):
        """Set up test environment."""
        self.mock_mcp_server_path = "/mock/path/to/mcp_server.py"
        
    @patch('agents.advisor.LlmAgent')
    @patch('agents.advisor.MCPToolset')
    @patch('agents.advisor.agent_tool.AgentTool')
    @patch('agents.advisor.StdioServerParameters')
    def test_create_advisor_agent(self, mock_stdio, mock_mcp, mock_agent_tool, mock_llm):
        """Test that AdvisorAgent is created with correct configuration."""
        # Mock the dependencies
        mock_mcp_instance = Mock()
        mock_mcp.return_value = mock_mcp_instance
        
        mock_agent_tool_instance = Mock()
        mock_agent_tool.return_value = mock_agent_tool_instance
        
        mock_llm_instance = Mock()
        mock_llm.return_value = mock_llm_instance
        
        # Create the agent
        agent = create_advisor_agent(self.mock_mcp_server_path)
        
        # Verify MCPToolset was created
        mock_mcp.assert_called_once()
        
        # Verify LlmAgent was created with correct configuration
        mock_llm.assert_called_once()
        call_args = mock_llm.call_args
        
        # Check that the agent has the expected name and description
        self.assertIn("AdvisorAgent", str(call_args))
        self.assertIn("financial advice", str(call_args).lower())
        
        # Verify the agent was returned
        self.assertEqual(agent, mock_llm_instance)


class TestFinancialAdvisorOrchestrator(unittest.TestCase):
    """Test the FinancialAdvisorOrchestrator creation and configuration."""
    
    def setUp(self):
        """Set up test environment."""
        self.mock_mcp_server_path = "/mock/path/to/mcp_server.py"
        
    @patch('agents.orchestrator.create_spending_analyzer_agent')
    @patch('agents.orchestrator.create_goal_planner_agent')
    @patch('agents.orchestrator.create_advisor_agent')
    @patch('agents.orchestrator.FinancialAdvisorOrchestrator')
    def test_create_financial_advisor_orchestrator(self, mock_orchestrator_class, 
                                                  mock_create_advisor, 
                                                  mock_create_goal_planner,
                                                  mock_create_spending_analyzer):
        """Test that FinancialAdvisorOrchestrator is created with correct configuration."""
        # Mock the agent creation functions
        mock_spending_agent = Mock()
        mock_create_spending_analyzer.return_value = mock_spending_agent
        
        mock_goal_agent = Mock()
        mock_create_goal_planner.return_value = mock_goal_agent
        
        mock_advisor_agent = Mock()
        mock_create_advisor.return_value = mock_advisor_agent
        
        # Mock the orchestrator class
        mock_orchestrator_instance = Mock()
        mock_orchestrator_class.return_value = mock_orchestrator_instance
        
        # Create the orchestrator
        orchestrator = create_financial_advisor_orchestrator(self.mock_mcp_server_path)
        
        # Verify all agent creation functions were called
        mock_create_spending_analyzer.assert_called_once_with(self.mock_mcp_server_path)
        mock_create_goal_planner.assert_called_once_with(self.mock_mcp_server_path)
        mock_create_advisor.assert_called_once_with(self.mock_mcp_server_path)
        
        # Verify the orchestrator class was instantiated with correct parameters
        mock_orchestrator_class.assert_called_once_with(
            sub_agents=[mock_spending_agent, mock_goal_agent, mock_advisor_agent]
        )
        
        # Verify the orchestrator was returned
        self.assertEqual(orchestrator, mock_orchestrator_instance)


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


if __name__ == '__main__':
    unittest.main()
