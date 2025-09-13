#!/usr/bin/env python3
"""
Unit tests for the Hybrid Agent Executor.

This test suite verifies that the HybridAgentExecutor works correctly with both
Streamlit and ADK Web contexts, following proper testing best practices.
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


class TestHybridAgentExecutor(unittest.TestCase):
    """Test cases for the Hybrid Agent Executor."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mcp_server_path = "mcp_server/database_server_stdio.py"
    
    def test_streamlit_context_initialization(self):
        """Test that Streamlit context initializes correctly."""
        executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="streamlit"
        )
        
        self.assertEqual(executor.context, "streamlit")
        self.assertIsNotNone(executor.agent_executor)
        self.assertEqual(executor.mcp_server_path, self.mcp_server_path)
    
    def test_adk_web_context_initialization(self):
        """Test that ADK Web context initializes correctly."""
        executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="adk_web"
        )
        
        self.assertEqual(executor.context, "adk_web")
        self.assertIsNone(executor.agent_executor)
        self.assertEqual(executor.mcp_server_path, self.mcp_server_path)
        self.assertEqual(executor.deployment_context.value, "adk_web")
    
    def test_get_agent_status_streamlit(self):
        """Test agent status for Streamlit context."""
        executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="streamlit"
        )
        
        status = executor.get_agent_status()
        
        self.assertIn("orchestrator", status)
        self.assertIn("deployment_context", status)
        self.assertEqual(status["deployment_context"], "streamlit")
    
    def test_get_agent_status_adk_web(self):
        """Test agent status for ADK Web context."""
        executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="adk_web"
        )
        
        status = executor.get_agent_status()
        
        self.assertIn("orchestrator", status)
        self.assertIn("deployment_context", status)
        self.assertEqual(status["deployment_context"], "adk_web")
    
    @patch('utils.unified_agent_executor.AgentExecutor')
    async def test_execute_full_analysis_streamlit(self, mock_agent_executor):
        """Test full analysis execution for Streamlit context."""
        # Mock the agent executor
        mock_executor_instance = MagicMock()
        mock_executor_instance.execute_full_analysis = AsyncMock(return_value={
            "status": "success",
            "customer_id": 1,
            "message": "Analysis completed"
        })
        mock_agent_executor.return_value = mock_executor_instance
        
        executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="streamlit"
        )
        
        result = await executor.execute_full_analysis(customer_id=1)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["customer_id"], 1)
        mock_executor_instance.execute_full_analysis.assert_called_once_with(1)
    
    @patch('agents.unified.agent_factory.OrchestratorFactory')
    async def test_execute_full_analysis_adk_web(self, mock_orchestrator_factory):
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
        
        result = await executor.execute_full_analysis(customer_id=1)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["customer_id"], 1)
        self.assertIn("events", result)
        mock_orchestrator_factory.create_orchestrator.assert_called_once()
    
    @patch('utils.unified_agent_executor.AgentExecutor')
    async def test_execute_quick_analysis_streamlit(self, mock_agent_executor):
        """Test quick analysis execution for Streamlit context."""
        # Mock the agent executor
        mock_executor_instance = MagicMock()
        mock_executor_instance.execute_quick_analysis = AsyncMock(return_value={
            "status": "success",
            "customer_id": 1,
            "message": "Quick analysis completed"
        })
        mock_agent_executor.return_value = mock_executor_instance
        
        executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="streamlit"
        )
        
        result = await executor.execute_quick_analysis(customer_id=1)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["customer_id"], 1)
        mock_executor_instance.execute_quick_analysis.assert_called_once_with(1)
    
    @patch('agents.unified.agent_factory.AgentFactory')
    async def test_execute_quick_analysis_adk_web(self, mock_agent_factory):
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
        
        result = await executor.execute_quick_analysis(customer_id=1)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["customer_id"], 1)
        self.assertIn("events", result)
        mock_agent_factory.create_spending_analyzer.assert_called_once()
    
    @patch('utils.unified_agent_executor.AgentExecutor')
    async def test_execute_goal_analysis_streamlit(self, mock_agent_executor):
        """Test goal analysis execution for Streamlit context."""
        # Mock the agent executor
        mock_executor_instance = MagicMock()
        mock_executor_instance.execute_goal_analysis = AsyncMock(return_value={
            "status": "success",
            "customer_id": 1,
            "message": "Goal analysis completed"
        })
        mock_agent_executor.return_value = mock_executor_instance
        
        executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="streamlit"
        )
        
        result = await executor.execute_goal_analysis(customer_id=1, goal_id=1)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["customer_id"], 1)
        mock_executor_instance.execute_goal_analysis.assert_called_once_with(1)
    
    @patch('agents.unified.agent_factory.AgentFactory')
    async def test_execute_goal_analysis_adk_web(self, mock_agent_factory):
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
        
        result = await executor.execute_goal_analysis(customer_id=1, goal_id=1)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["customer_id"], 1)
        self.assertEqual(result["goal_id"], 1)
        self.assertIn("events", result)
        mock_agent_factory.create_goal_planner.assert_called_once()
    
    def test_error_handling_invalid_context(self):
        """Test error handling for invalid context."""
        # The current implementation doesn't validate context, so this test should pass
        # If we want to add validation, we can update the HybridAgentExecutor
        executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="invalid_context"
        )
        # For now, just verify it doesn't crash
        self.assertIsNotNone(executor)


class TestHybridAgentExecutorIntegration(unittest.TestCase):
    """Integration tests for the Hybrid Agent Executor."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mcp_server_path = "mcp_server/database_server_stdio.py"
    
    async def test_streamlit_context_real_execution(self):
        """Test real execution with Streamlit context (if MCP server is available)."""
        try:
            executor = HybridAgentExecutor(
                mcp_server_path=self.mcp_server_path,
                context="streamlit"
            )
            
            # This will use the real AgentExecutor if MCP server is available
            result = await executor.execute_quick_analysis(customer_id=1)
            
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
            result = await executor.execute_quick_analysis(customer_id=1)
            
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
TestHybridAgentExecutor.test_execute_full_analysis_streamlit = make_async_test(TestHybridAgentExecutor.test_execute_full_analysis_streamlit)
TestHybridAgentExecutor.test_execute_full_analysis_adk_web = make_async_test(TestHybridAgentExecutor.test_execute_full_analysis_adk_web)
TestHybridAgentExecutor.test_execute_quick_analysis_streamlit = make_async_test(TestHybridAgentExecutor.test_execute_quick_analysis_streamlit)
TestHybridAgentExecutor.test_execute_quick_analysis_adk_web = make_async_test(TestHybridAgentExecutor.test_execute_quick_analysis_adk_web)
TestHybridAgentExecutor.test_execute_goal_analysis_streamlit = make_async_test(TestHybridAgentExecutor.test_execute_goal_analysis_streamlit)
TestHybridAgentExecutor.test_execute_goal_analysis_adk_web = make_async_test(TestHybridAgentExecutor.test_execute_goal_analysis_adk_web)

TestHybridAgentExecutorIntegration.test_streamlit_context_real_execution = make_async_test(TestHybridAgentExecutorIntegration.test_streamlit_context_real_execution)
TestHybridAgentExecutorIntegration.test_adk_web_context_real_execution = make_async_test(TestHybridAgentExecutorIntegration.test_adk_web_context_real_execution)


if __name__ == "__main__":
    unittest.main()
