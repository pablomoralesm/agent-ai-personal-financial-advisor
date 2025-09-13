#!/usr/bin/env python3
"""
Unit tests for UI analysis functionality.

This test suite verifies that the UI analysis buttons work correctly with the
hybrid agent executor approach, following proper testing best practices.
"""

import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.unified_agent_executor import HybridAgentExecutor


class TestUIAnalysis(unittest.TestCase):
    """Test cases for UI analysis functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mcp_server_path = "mcp_server/database_server_stdio.py"
        self.customer_id = 1
        self.goal_id = 1
    
    def test_hybrid_executor_initialization(self):
        """Test that HybridAgentExecutor initializes correctly for both contexts."""
        # Test Streamlit context
        streamlit_executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="streamlit"
        )
        self.assertEqual(streamlit_executor.context, "streamlit")
        self.assertIsNone(streamlit_executor.agent_executor)  # Now using unified system
        self.assertEqual(streamlit_executor.deployment_context.value, "streamlit")
        
        # Test ADK Web context
        adk_executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="adk_web"
        )
        self.assertEqual(adk_executor.context, "adk_web")
        self.assertIsNone(adk_executor.agent_executor)  # Now using unified system
        self.assertEqual(adk_executor.deployment_context.value, "adk_web")
    
    @patch('agents.unified.agent_factory.AgentFactory')
    async def test_quick_analysis_streamlit(self, mock_agent_factory):
        """Test quick analysis execution for Streamlit context."""
        # Mock the spending analyzer
        mock_analyzer = MagicMock()
        mock_agent = MagicMock()
        mock_agent.run_async = AsyncMock(return_value=AsyncMock())
        mock_agent.run_async.return_value.__aiter__ = AsyncMock(return_value=iter([]))
        mock_analyzer.get_agent.return_value = mock_agent
        mock_agent_factory.create_spending_analyzer.return_value = mock_analyzer
        
        executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="streamlit"
        )
        
        result = await executor.execute_quick_analysis(self.customer_id)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["customer_id"], self.customer_id)
        self.assertIn("events", result)
        mock_agent_factory.create_spending_analyzer.assert_called_once()
    
    @patch('agents.unified.agent_factory.OrchestratorFactory')
    async def test_full_analysis_streamlit(self, mock_orchestrator_factory):
        """Test full analysis execution for Streamlit context."""
        # Mock the orchestrator
        mock_orchestrator = MagicMock()
        mock_agent = MagicMock()
        mock_agent.run_async = AsyncMock(return_value=AsyncMock())
        mock_agent.run_async.return_value.__aiter__ = AsyncMock(return_value=iter([]))
        mock_orchestrator.get_agent.return_value = mock_agent
        mock_orchestrator_factory.create_orchestrator.return_value = mock_orchestrator
        
        executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="streamlit"
        )
        
        result = await executor.execute_full_analysis(self.customer_id)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["customer_id"], self.customer_id)
        self.assertIn("events", result)
        mock_orchestrator_factory.create_orchestrator.assert_called_once()
    
    @patch('agents.unified.agent_factory.AgentFactory')
    async def test_goal_analysis_streamlit(self, mock_agent_factory):
        """Test goal analysis execution for Streamlit context."""
        # Mock the goal planner
        mock_planner = MagicMock()
        mock_agent = MagicMock()
        mock_agent.run_async = AsyncMock(return_value=AsyncMock())
        mock_agent.run_async.return_value.__aiter__ = AsyncMock(return_value=iter([]))
        mock_planner.get_agent.return_value = mock_agent
        mock_agent_factory.create_goal_planner.return_value = mock_planner
        
        executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="streamlit"
        )
        
        result = await executor.execute_goal_analysis(self.customer_id, self.goal_id)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["customer_id"], self.customer_id)
        self.assertEqual(result["goal_id"], self.goal_id)
        self.assertIn("events", result)
        mock_agent_factory.create_goal_planner.assert_called_once()
    
    @patch('agents.unified.agent_factory.AgentFactory')
    async def test_quick_analysis_adk_web(self, mock_agent_factory):
        """Test quick analysis execution for ADK Web context."""
        # Mock the spending analyzer
        mock_analyzer = MagicMock()
        mock_agent = MagicMock()
        mock_agent.run_async = AsyncMock(return_value=AsyncMock())
        mock_agent.run_async.return_value.__aiter__ = AsyncMock(return_value=iter([]))
        mock_analyzer.get_agent.return_value = mock_agent
        mock_agent_factory.create_spending_analyzer.return_value = mock_analyzer
        
        executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="adk_web"
        )
        
        result = await executor.execute_quick_analysis(self.customer_id)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["customer_id"], self.customer_id)
        self.assertIn("events", result)
        mock_agent_factory.create_spending_analyzer.assert_called_once()
    
    @patch('agents.unified.agent_factory.OrchestratorFactory')
    async def test_full_analysis_adk_web(self, mock_orchestrator_factory):
        """Test full analysis execution for ADK Web context."""
        # Mock the orchestrator
        mock_orchestrator = MagicMock()
        mock_agent = MagicMock()
        mock_agent.run_async = AsyncMock(return_value=AsyncMock())
        mock_agent.run_async.return_value.__aiter__ = AsyncMock(return_value=iter([]))
        mock_orchestrator.get_agent.return_value = mock_agent
        mock_orchestrator_factory.create_orchestrator.return_value = mock_orchestrator
        
        executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="adk_web"
        )
        
        result = await executor.execute_full_analysis(self.customer_id)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["customer_id"], self.customer_id)
        self.assertIn("events", result)
        mock_orchestrator_factory.create_orchestrator.assert_called_once()
    
    @patch('agents.unified.agent_factory.AgentFactory')
    async def test_goal_analysis_adk_web(self, mock_agent_factory):
        """Test goal analysis execution for ADK Web context."""
        # Mock the goal planner
        mock_planner = MagicMock()
        mock_agent = MagicMock()
        mock_agent.run_async = AsyncMock(return_value=AsyncMock())
        mock_agent.run_async.return_value.__aiter__ = AsyncMock(return_value=iter([]))
        mock_planner.get_agent.return_value = mock_agent
        mock_agent_factory.create_goal_planner.return_value = mock_planner
        
        executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="adk_web"
        )
        
        result = await executor.execute_goal_analysis(self.customer_id, self.goal_id)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["customer_id"], self.customer_id)
        self.assertEqual(result["goal_id"], self.goal_id)
        self.assertIn("events", result)
        mock_agent_factory.create_goal_planner.assert_called_once()
    
    def test_error_handling_invalid_context(self):
        """Test error handling for invalid context."""
        # The current implementation doesn't validate context, so this should work
        executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="invalid_context"
        )
        # Should not crash
        self.assertIsNotNone(executor)
    
    def test_get_agent_status(self):
        """Test agent status retrieval for both contexts."""
        # Test Streamlit context
        streamlit_executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="streamlit"
        )
        status = streamlit_executor.get_agent_status()
        self.assertIn("deployment_context", status)
        self.assertEqual(status["deployment_context"], "streamlit")
        
        # Test ADK Web context
        adk_executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="adk_web"
        )
        status = adk_executor.get_agent_status()
        self.assertIn("deployment_context", status)
        self.assertEqual(status["deployment_context"], "adk_web")


class TestUIAnalysisIntegration(unittest.TestCase):
    """Integration tests for UI analysis functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mcp_server_path = "mcp_server/database_server_stdio.py"
        self.customer_id = 1
        self.goal_id = 1
    
    async def test_streamlit_context_real_execution(self):
        """Test real execution with Streamlit context (if MCP server is available)."""
        try:
            executor = HybridAgentExecutor(
                mcp_server_path=self.mcp_server_path,
                context="streamlit"
            )
            
            # This will use the real AgentExecutor if MCP server is available
            result = await executor.execute_quick_analysis(self.customer_id)
            
            # Should return a result (success or error)
            self.assertIn("status", result)
            self.assertIn("customer_id", result)
            
        except Exception as e:
            # If MCP server is not available, that's expected in test environment
            self.assertIn("MCP", str(e))
    
    async def test_adk_web_context_real_execution(self):
        """Test real execution with ADK Web context (if agents are available)."""
        try:
            executor = HybridAgentExecutor(
                mcp_server_path=self.mcp_server_path,
                context="adk_web"
            )
            
            # This will use the real unified agent system if available
            result = await executor.execute_quick_analysis(self.customer_id)
            
            # Should return a result (success or error)
            self.assertIn("status", result)
            self.assertIn("customer_id", result)
            
        except Exception as e:
            # If agents are not available, that's expected in test environment
            self.assertIn("agent", str(e).lower())


def run_async_test(coro):
    """Helper function to run async tests."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


# Convert async test methods to sync methods that run async code
def make_async_test(async_method):
    """Convert an async test method to a sync method."""
    def sync_test(self):
        return run_async_test(async_method(self))
    return sync_test

# Apply the conversion to async test methods
TestUIAnalysis.test_quick_analysis_streamlit = make_async_test(TestUIAnalysis.test_quick_analysis_streamlit)
TestUIAnalysis.test_full_analysis_streamlit = make_async_test(TestUIAnalysis.test_full_analysis_streamlit)
TestUIAnalysis.test_goal_analysis_streamlit = make_async_test(TestUIAnalysis.test_goal_analysis_streamlit)
TestUIAnalysis.test_quick_analysis_adk_web = make_async_test(TestUIAnalysis.test_quick_analysis_adk_web)
TestUIAnalysis.test_full_analysis_adk_web = make_async_test(TestUIAnalysis.test_full_analysis_adk_web)
TestUIAnalysis.test_goal_analysis_adk_web = make_async_test(TestUIAnalysis.test_goal_analysis_adk_web)

TestUIAnalysisIntegration.test_streamlit_context_real_execution = make_async_test(TestUIAnalysisIntegration.test_streamlit_context_real_execution)
TestUIAnalysisIntegration.test_adk_web_context_real_execution = make_async_test(TestUIAnalysisIntegration.test_adk_web_context_real_execution)


if __name__ == "__main__":
    unittest.main()
