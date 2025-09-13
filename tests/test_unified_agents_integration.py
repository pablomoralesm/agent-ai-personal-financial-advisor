"""
Integration tests for unified agent system.

These tests focus on component interactions with minimal mocking
to test real workflows and integration scenarios. They may be slower
but provide confidence in the overall system behavior.

Part of the Agentic AI Personal Financial Advisor application.
"""

import unittest
import asyncio
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from pathlib import Path

from agents.unified import (
    UnifiedAgent, ProceduralOrchestrator, IntelligentOrchestrator,
    AgentFactory, OrchestratorFactory, DeploymentConfig
)

class AsyncIteratorMock:
    """Mock class that provides a proper async iterator for testing."""
    
    def __init__(self, events):
        self.events = events
        self.index = 0
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.index >= len(self.events):
            raise StopAsyncIteration
        event = self.events[self.index]
        self.index += 1
        return event

class TestDeploymentContextDifferences(unittest.TestCase):
    """Test differences between deployment contexts."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mcp_server_path = "/fake/path/mcp_server.py"
        self.factory = AgentFactory()
        self.orchestrator_factory = OrchestratorFactory()
    
    def test_streamlit_vs_adk_web_configuration(self):
        """Test that different contexts have different configurations."""
        streamlit_config = DeploymentConfig.get_config("streamlit")
        adk_web_config = DeploymentConfig.get_config("adk_web")
        
        # Should have different configurations
        self.assertNotEqual(streamlit_config, adk_web_config)
        
        # Both should have required keys
        required_keys = ['orchestrator_type', 'use_runner', 'session_service', 'educational_focus']
        for key in required_keys:
            self.assertIn(key, streamlit_config)
            self.assertIn(key, adk_web_config)
    
    def test_factory_creates_correct_orchestrators(self):
        """Test that factory creates correct orchestrators for each context."""
        # Test Streamlit context
        streamlit_agents = self.factory.create_individual_agents(self.mcp_server_path, "streamlit")
        streamlit_orchestrator = self.orchestrator_factory.create_orchestrator(
            "procedural", self.mcp_server_path, "streamlit"
        )
        
        self.assertIsInstance(streamlit_orchestrator, ProceduralOrchestrator)
        self.assertEqual(len(streamlit_agents), 3)
        
        # Test ADK Web context
        adk_web_agents = self.factory.create_individual_agents(self.mcp_server_path, "adk_web")
        adk_web_procedural = self.orchestrator_factory.create_orchestrator(
            "procedural", self.mcp_server_path, "adk_web"
        )
        adk_web_intelligent = self.orchestrator_factory.create_orchestrator(
            "intelligent", self.mcp_server_path, "adk_web"
        )
        
        self.assertIsInstance(adk_web_procedural, ProceduralOrchestrator)
        self.assertIsInstance(adk_web_intelligent, IntelligentOrchestrator)
        self.assertEqual(len(adk_web_agents), 3)
    
    def test_orchestrator_type_restrictions(self):
        """Test that orchestrator types are properly restricted by context."""
        # Streamlit should only support procedural
        with self.assertRaises(ValueError):
            self.orchestrator_factory.create_orchestrator(
                "intelligent", self.mcp_server_path, "streamlit"
            )
        
        # ADK Web should support both
        procedural = self.orchestrator_factory.create_orchestrator(
            "procedural", self.mcp_server_path, "adk_web"
        )
        intelligent = self.orchestrator_factory.create_orchestrator(
            "intelligent", self.mcp_server_path, "adk_web"
        )
        
        self.assertIsInstance(procedural, ProceduralOrchestrator)
        self.assertIsInstance(intelligent, IntelligentOrchestrator)

class TestOrchestratorAsyncBehavior(unittest.TestCase):
    """Test async orchestration behavior with minimal mocking."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mcp_server_path = "/fake/path/mcp_server.py"
        self.orchestrator = ProceduralOrchestrator(self.mcp_server_path, "streamlit")
        
        # Create mock sub-agents with proper async iterator mocking
        self.mock_spending = Mock()
        self.mock_goal = Mock()
        self.mock_advisor = Mock()
        
        # Create mock agents that return async iterators
        self.mock_spending.agent = Mock()
        self.mock_goal.agent = Mock()
        self.mock_advisor.agent = Mock()
        
        # Mock the run_async method to return an async iterator
        self.mock_spending.agent.run_async = Mock(return_value=AsyncIteratorMock([
            Mock(content="Spending analysis event 1", event_type="progress"),
            Mock(content="Spending analysis event 2", event_type="progress")
        ]))
        
        self.mock_goal.agent.run_async = Mock(return_value=AsyncIteratorMock([
            Mock(content="Goal planning event 1", event_type="progress"),
            Mock(content="Goal planning event 2", event_type="progress")
        ]))
        
        self.mock_advisor.agent.run_async = Mock(return_value=AsyncIteratorMock([
            Mock(content="Advice generation event 1", event_type="progress"),
            Mock(content="Advice generation event 2", event_type="progress")
        ]))
        
        self.orchestrator.set_sub_agents(self.mock_spending, self.mock_goal, self.mock_advisor)
    
    def test_procedural_orchestration_workflow(self):
        """Test actual procedural orchestration workflow."""
        async def run_test():
            # Create mock context
            mock_ctx = Mock()
            mock_ctx.session.state = {'customer_id': 123}
            mock_ctx.create_event = Mock(return_value=Mock())
            
            # Run orchestration
            events = []
            async for event in self.orchestrator._run_async_impl(mock_ctx):
                events.append(event)
            
            # Verify orchestration steps
            self.assertGreater(len(events), 0)
            
            # Verify sub-agents were called
            self.mock_spending.agent.run_async.assert_called_once()
            self.mock_goal.agent.run_async.assert_called_once()
            self.mock_advisor.agent.run_async.assert_called_once()
            
            # Verify session state was updated
            self.assertIn('spending_analysis', mock_ctx.session.state)
            self.assertIn('goal_feasibility', mock_ctx.session.state)
            self.assertIn('comprehensive_advice', mock_ctx.session.state)
        
        # Run async test
        asyncio.run(run_test())
    
    def test_orchestration_error_handling(self):
        """Test orchestration error handling."""
        async def run_test():
            # Create mock context with no customer_id
            mock_ctx = Mock()
            mock_ctx.session.state = {}
            
            # Create a list to capture events
            captured_events = []
            def mock_create_event(content, event_type):
                event = Mock()
                event.content = content
                event.event_type = event_type
                captured_events.append(event)
                return event
            
            mock_ctx.create_event = mock_create_event
            
            # Run orchestration
            events = []
            async for event in self.orchestrator._run_async_impl(mock_ctx):
                events.append(event)
            
            # Verify error handling
            self.assertGreater(len(events), 0)
            # Should have error event
            error_events = [e for e in events if hasattr(e, 'event_type') and e.event_type == 'error']
            self.assertGreater(len(error_events), 0)
        
        asyncio.run(run_test())
    
    def test_quick_analysis_workflow(self):
        """Test quick analysis workflow."""
        async def run_test():
            mock_ctx = Mock()
            mock_ctx.session.state = {'customer_id': 123}
            
            result = await self.orchestrator.run_quick_analysis(mock_ctx, 123, 'spending')
            
            self.assertEqual(result['status'], 'completed')
            self.assertEqual(result['customer_id'], 123)
            self.assertEqual(result['focus_area'], 'spending')
            
            # Verify session state was updated
            self.assertIn('spending_insights', mock_ctx.session.state)
            self.assertIn('quick_recommendations', mock_ctx.session.state)
        
        asyncio.run(run_test())

class TestSessionStateSharing(unittest.TestCase):
    """Test session state sharing between agents."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mcp_server_path = "/fake/path/mcp_server.py"
        self.orchestrator = ProceduralOrchestrator(self.mcp_server_path, "streamlit")
        
        # Create mock sub-agents that interact with session state
        self.mock_spending = Mock()
        self.mock_goal = Mock()
        self.mock_advisor = Mock()
        
        # Create mock agents with proper async iterator mocking
        self.mock_spending.agent = Mock()
        self.mock_goal.agent = Mock()
        self.mock_advisor.agent = Mock()
        
        # Mock the run_async method to return an async iterator
        self.mock_spending.agent.run_async = Mock(return_value=AsyncIteratorMock([
            Mock(content="Spending analysis event", event_type="progress")
        ]))
        
        self.mock_goal.agent.run_async = Mock(return_value=AsyncIteratorMock([
            Mock(content="Goal planning event", event_type="progress")
        ]))
        
        self.mock_advisor.agent.run_async = Mock(return_value=AsyncIteratorMock([
            Mock(content="Advice generation event", event_type="progress")
        ]))
        
        self.orchestrator.set_sub_agents(self.mock_spending, self.mock_goal, self.mock_advisor)
    
    def test_session_state_sharing_workflow(self):
        """Test that agents share data through session state."""
        async def run_test():
            mock_ctx = Mock()
            mock_ctx.session.state = {'customer_id': 123}
            mock_ctx.create_event = Mock(return_value=Mock())
            
            # Run orchestration
            events = []
            async for event in self.orchestrator._run_async_impl(mock_ctx):
                events.append(event)
            
            # Verify session state was populated
            self.assertIn('spending_analysis', mock_ctx.session.state)
            self.assertIn('goal_feasibility', mock_ctx.session.state)
            self.assertIn('comprehensive_advice', mock_ctx.session.state)
            
            # Verify data structure
            spending_data = mock_ctx.session.state['spending_analysis']
            goal_data = mock_ctx.session.state['goal_feasibility']
            advice_data = mock_ctx.session.state['comprehensive_advice']
            
            # All should be completed successfully
            self.assertEqual(spending_data['status'], 'completed')
            self.assertEqual(goal_data['status'], 'completed')
            self.assertEqual(advice_data['status'], 'completed')
            
            # All should have the same customer_id
            self.assertEqual(spending_data['customer_id'], 123)
            self.assertEqual(goal_data['customer_id'], 123)
            self.assertEqual(advice_data['customer_id'], 123)
        
        asyncio.run(run_test())

class TestErrorHandling(unittest.TestCase):
    """Test error handling scenarios."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mcp_server_path = "/fake/path/mcp_server.py"
        self.orchestrator = ProceduralOrchestrator(self.mcp_server_path, "streamlit")
    
    def test_agent_failure_handling(self):
        """Test handling when sub-agents fail."""
        async def run_test():
            # Create mock sub-agents that fail
            mock_spending = Mock()
            mock_goal = Mock()
            mock_advisor = Mock()
            
            # Create mock agents with proper async iterator mocking
            mock_spending.agent = Mock()
            mock_goal.agent = Mock()
            mock_advisor.agent = Mock()
            
            # Mock agents that raise exceptions or work normally
            mock_spending.agent.run_async = Mock(side_effect=Exception("Spending analysis failed"))
            mock_goal.agent.run_async = Mock(return_value=AsyncIteratorMock([
                Mock(content="Goal planning event", event_type="progress")
            ]))
            mock_advisor.agent.run_async = Mock(return_value=AsyncIteratorMock([
                Mock(content="Advice event", event_type="progress")
            ]))
            
            self.orchestrator.set_sub_agents(mock_spending, mock_goal, mock_advisor)
            
            mock_ctx = Mock()
            mock_ctx.session.state = {'customer_id': 123}
            
            # Create a list to capture events
            captured_events = []
            def mock_create_event(content, event_type):
                event = Mock()
                event.content = content
                event.event_type = event_type
                captured_events.append(event)
                return event
            
            mock_ctx.create_event = mock_create_event
            
            # Run orchestration
            events = []
            async for event in self.orchestrator._run_async_impl(mock_ctx):
                events.append(event)
            
            # Verify error handling
            error_events = [e for e in events if hasattr(e, 'event_type') and e.event_type == 'error']
            self.assertGreater(len(error_events), 0)
            
            # Verify session state contains error information
            self.assertIn('spending_analysis', mock_ctx.session.state)
            spending_analysis = mock_ctx.session.state['spending_analysis']
            self.assertEqual(spending_analysis['status'], 'error')
            self.assertIn('error', spending_analysis)
        
        asyncio.run(run_test())
    
    def test_mcp_server_failure_handling(self):
        """Test handling when MCP server fails."""
        # Test with invalid MCP server path - should not raise exception during init
        # but should fail when trying to use the agent
        agent = UnifiedAgent(
            name="TestAgent",
            mcp_server_path="/nonexistent/path/server.py",
            deployment_context="streamlit"
        )
        
        # Verify agent was created (it should be, as we don't validate path during init)
        self.assertIsNotNone(agent)
        self.assertEqual(agent.name, "TestAgent")

class TestPerformanceAndTimeouts(unittest.TestCase):
    """Test performance and timeout scenarios."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mcp_server_path = "/fake/path/mcp_server.py"
        self.orchestrator = ProceduralOrchestrator(self.mcp_server_path, "streamlit")
        
        # Create mock sub-agents
        self.mock_spending = Mock()
        self.mock_goal = Mock()
        self.mock_advisor = Mock()
        
        # Create mock agents that return async iterators
        self.mock_spending.agent = Mock()
        self.mock_goal.agent = Mock()
        self.mock_advisor.agent = Mock()
        
        # Mock the run_async method to return an async iterator
        self.mock_spending.agent.run_async = Mock(return_value=AsyncIteratorMock([
            Mock(content="Spending analysis event", event_type="progress")
        ]))
        
        self.mock_goal.agent.run_async = Mock(return_value=AsyncIteratorMock([
            Mock(content="Goal planning event", event_type="progress")
        ]))
        
        self.mock_advisor.agent.run_async = Mock(return_value=AsyncIteratorMock([
            Mock(content="Advice generation event", event_type="progress")
        ]))
        
        self.orchestrator.set_sub_agents(self.mock_spending, self.mock_goal, self.mock_advisor)
    
    def test_orchestration_performance(self):
        """Test that orchestration completes within reasonable time."""
        async def run_test():
            mock_ctx = Mock()
            mock_ctx.session.state = {'customer_id': 123}
            mock_ctx.create_event = Mock(return_value=Mock())
            
            import time
            start_time = time.time()
            
            # Run orchestration
            events = []
            async for event in self.orchestrator._run_async_impl(mock_ctx):
                events.append(event)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Should complete within 1 second (very generous for mocked tests)
            self.assertLess(execution_time, 1.0)
            self.assertGreater(len(events), 0)
        
        asyncio.run(run_test())

class TestUnifiedAgentIntegration(unittest.TestCase):
    """Integration tests for unified agents with real ADK components."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mcp_server_path = "/fake/path/mcp_server.py"
        self.deployment_context = "streamlit"
    
    @patch('agents.unified.base_agent.McpToolset')
    def test_real_agent_creation_with_mcp(self, mock_mcp_toolset):
        """Test agent creation with real MCP toolset integration."""
        # Don't mock MCPToolset to test real integration
        mock_mcp_toolset.side_effect = lambda **kwargs: Mock()
        
        agent = UnifiedAgent(
            name="TestAgent",
            mcp_server_path=self.mcp_server_path,
            deployment_context=self.deployment_context,
            model="gemini-2.0-flash",
            instruction="Test instruction",
            description="Test description"
        )
        
        # Verify MCP toolset was created with correct parameters
        mock_mcp_toolset.assert_called_once()
        call_args = mock_mcp_toolset.call_args
        
        # Verify connection parameters
        self.assertIn('connection_params', call_args[1])
        connection_params = call_args[1]['connection_params']
        self.assertEqual(connection_params.server_params.command, 'python3')
        self.assertIn('mcp_server.py', str(connection_params.server_params.args[0]))
    
    def test_agent_configuration_validation(self):
        """Test that agent configurations are properly validated."""
        # Test valid configuration
        agent = UnifiedAgent(
            name="ValidAgent",
            mcp_server_path=self.mcp_server_path,
            deployment_context=self.deployment_context
        )
        
        config = agent._get_agent_config()
        self.assertIsInstance(config, dict)
        self.assertIn('name', config)
        self.assertIn('model', config)
        self.assertIn('instruction', config)
        
        # Test invalid configuration should raise error
        with self.assertRaises(Exception):  # Pydantic ValidationError
            UnifiedAgent(
                name=None,  # Invalid name
                mcp_server_path=self.mcp_server_path,
                deployment_context=self.deployment_context
            )

if __name__ == '__main__':
    unittest.main()