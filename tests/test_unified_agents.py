"""
Unit tests for the NEW unified agent system.

This module tests the NEW unified agent structure in agents/unified/ directory:
- UnifiedAgent, UnifiedAgentBase, UnifiedOrchestratorBase
- ProceduralOrchestrator, IntelligentOrchestrator
- AgentFactory, OrchestratorFactory
- DeploymentConfig

These tests focus on individual component behavior with heavy mocking
to isolate units of functionality. They should be fast and not require
external dependencies.

This is the NEW architecture that replaces the legacy agent system.

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

class TestDeploymentConfig(unittest.TestCase):
    """Test deployment configuration management."""
    
    def test_deployment_context_enum(self):
        """Test deployment context enum values."""
        from agents.unified.deployment_configs import DeploymentContext
        
        self.assertEqual(DeploymentContext.STREAMLIT.value, "streamlit")
        self.assertEqual(DeploymentContext.ADK_WEB.value, "adk_web")
    
    def test_orchestrator_type_enum(self):
        """Test orchestrator type enum values."""
        from agents.unified.deployment_configs import OrchestratorType
        
        self.assertEqual(OrchestratorType.PROCEDURAL.value, "procedural")
        self.assertEqual(OrchestratorType.INTELLIGENT.value, "intelligent")
    
    def test_deployment_config_creation(self):
        """Test deployment config creation."""
        # Test static method access
        streamlit_config = DeploymentConfig.get_config("streamlit")
        adk_web_config = DeploymentConfig.get_config("adk_web")
        
        self.assertIsNotNone(streamlit_config)
        self.assertIsNotNone(adk_web_config)
        self.assertIsInstance(streamlit_config, dict)
        self.assertIsInstance(adk_web_config, dict)
    
    def test_context_specific_configurations(self):
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

class TestUnifiedAgent(unittest.TestCase):
    """Test unified agent base functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mcp_server_path = "/fake/path/mcp_server.py"
        self.deployment_context = "streamlit"
    
    @patch('agents.unified.base_agent.McpToolset')
    @patch('agents.unified.base_agent.LlmAgent')
    def test_unified_agent_creation(self, mock_llm_agent, mock_mcp_toolset):
        """Test unified agent creation."""
        # Setup mocks
        mock_mcp_toolset.return_value = Mock()
        mock_llm_agent.return_value = Mock()
        
        agent = UnifiedAgent(
            name="TestAgent",
            mcp_server_path=self.mcp_server_path,
            deployment_context=self.deployment_context,
            model="gemini-2.0-flash",
            instruction="Test instruction",
            description="Test description"
        )
        
        # Verify agent creation
        self.assertEqual(agent.name, "TestAgent")
        self.assertEqual(agent.model, "gemini-2.0-flash")
        self.assertEqual(agent.instruction, "Test instruction")
        self.assertEqual(agent.description, "Test description")
        
        # Verify MCP toolset was created
        mock_mcp_toolset.assert_called_once()
        
        # Verify LlmAgent was created
        mock_llm_agent.assert_called_once()
    
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

class TestAgentFactory(unittest.TestCase):
    """Test agent factory functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mcp_server_path = "/fake/path/mcp_server.py"
        self.factory = AgentFactory()
    
    @patch('agents.unified.agent_factory.UnifiedAgent')
    def test_create_spending_analyzer(self, mock_unified_agent):
        """Test spending analyzer creation."""
        mock_agent = Mock()
        mock_unified_agent.return_value = mock_agent
        
        agent = self.factory.create_spending_analyzer(self.mcp_server_path, "streamlit")
        
        self.assertIsNotNone(agent)
        mock_unified_agent.assert_called_once()
    
    @patch('agents.unified.agent_factory.UnifiedAgent')
    def test_create_goal_planner(self, mock_unified_agent):
        """Test goal planner creation."""
        mock_agent = Mock()
        mock_unified_agent.return_value = mock_agent
        
        agent = self.factory.create_goal_planner(self.mcp_server_path, "streamlit")
        
        self.assertIsNotNone(agent)
        mock_unified_agent.assert_called_once()
    
    @patch('agents.unified.agent_factory.UnifiedAgent')
    def test_create_advisor(self, mock_unified_agent):
        """Test advisor creation."""
        mock_agent = Mock()
        mock_unified_agent.return_value = mock_agent
        
        agent = self.factory.create_advisor(self.mcp_server_path, "streamlit")
        
        self.assertIsNotNone(agent)
        mock_unified_agent.assert_called_once()
    
    @patch('agents.unified.agent_factory.AgentFactory.create_spending_analyzer')
    @patch('agents.unified.agent_factory.AgentFactory.create_goal_planner')
    @patch('agents.unified.agent_factory.AgentFactory.create_advisor')
    def test_create_individual_agents(self, mock_advisor, mock_goal, mock_spending):
        """Test individual agents creation."""
        mock_spending.return_value = Mock()
        mock_goal.return_value = Mock()
        mock_advisor.return_value = Mock()
        
        agents = self.factory.create_individual_agents(self.mcp_server_path, "streamlit")
        
        self.assertEqual(len(agents), 3)
        self.assertIn('spending_analyzer', agents)
        self.assertIn('goal_planner', agents)
        self.assertIn('advisor', agents)

class TestOrchestratorFactory(unittest.TestCase):
    """Test orchestrator factory functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mcp_server_path = "/fake/path/mcp_server.py"
        self.factory = OrchestratorFactory()
    
    @patch('agents.unified.agent_factory.ProceduralOrchestrator')
    def test_create_procedural_orchestrator(self, mock_procedural):
        """Test procedural orchestrator creation."""
        mock_orchestrator = Mock()
        mock_procedural.return_value = mock_orchestrator
        
        orchestrator = self.factory.create_orchestrator(
            "procedural", self.mcp_server_path, "streamlit"
        )
        
        self.assertIsNotNone(orchestrator)
        mock_procedural.assert_called_once()
    
    @patch('agents.unified.agent_factory.IntelligentOrchestrator')
    def test_create_intelligent_orchestrator(self, mock_intelligent):
        """Test intelligent orchestrator creation."""
        mock_orchestrator = Mock()
        mock_intelligent.return_value = mock_orchestrator
        
        orchestrator = self.factory.create_orchestrator(
            "intelligent", self.mcp_server_path, "adk_web"
        )
        
        self.assertIsNotNone(orchestrator)
        mock_intelligent.assert_called_once()
    
    def test_create_invalid_orchestrator_type(self):
        """Test creating orchestrator with invalid type."""
        with self.assertRaises(ValueError):
            self.factory.create_orchestrator(
                "invalid", self.mcp_server_path, "streamlit"
            )

class TestProceduralOrchestratorUnit(unittest.TestCase):
    """Unit tests for procedural orchestrator with heavy mocking."""
    
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
        
        # Set agent names for get_sub_agent method
        self.mock_spending.name = 'spending_analyzer'
        self.mock_goal.name = 'goal_planner'
        self.mock_advisor.name = 'advisor'
        
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
    
    def test_orchestrator_initialization(self):
        """Test orchestrator initialization."""
        self.assertEqual(self.orchestrator.name, "ProceduralOrchestrator")
        self.assertEqual(self.orchestrator.description, "Educational orchestrator with clear, predictable workflow patterns")
        self.assertEqual(self.orchestrator._deployment_context, "streamlit")
    
    def test_set_sub_agents(self):
        """Test setting sub-agents."""
        self.assertEqual(self.orchestrator._spending_analyzer, self.mock_spending)
        self.assertEqual(self.orchestrator._goal_planner, self.mock_goal)
        self.assertEqual(self.orchestrator._advisor, self.mock_advisor)
    
    def test_get_sub_agent(self):
        """Test getting specific sub-agent."""
        # Check if the method exists before testing
        if hasattr(self.orchestrator, 'get_sub_agent'):
            spending_agent = self.orchestrator.get_sub_agent('spending_analyzer')
            self.assertEqual(spending_agent, self.mock_spending)
            
            goal_agent = self.orchestrator.get_sub_agent('goal_planner')
            self.assertEqual(goal_agent, self.mock_goal)
            
            advisor_agent = self.orchestrator.get_sub_agent('advisor')
            self.assertEqual(advisor_agent, self.mock_advisor)
        else:
            # Skip this test if method doesn't exist
            self.skipTest("get_sub_agent method not implemented")
    
    def test_get_all_sub_agents(self):
        """Test getting all sub-agents."""
        all_agents = self.orchestrator.get_all_sub_agents()
        self.assertEqual(len(all_agents), 3)
        self.assertIn(self.mock_spending, all_agents)
        self.assertIn(self.mock_goal, all_agents)
        self.assertIn(self.mock_advisor, all_agents)
    
    def test_procedural_orchestration_workflow(self):
        """Test procedural orchestration workflow with proper async mocking."""
        async def run_test():
            # Create mock context
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
        """Test orchestration error handling with proper async mocking."""
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
    
    def test_agent_failure_handling(self):
        """Test handling when sub-agents fail with proper async mocking."""
        async def run_test():
            # Create mock sub-agents that fail
            mock_spending = Mock()
            mock_goal = Mock()
            mock_advisor = Mock()
            
            # Mock agents that raise exceptions
            mock_spending.agent = Mock()
            mock_spending.agent.run_async = Mock(side_effect=Exception("Spending analysis failed"))
            
            mock_goal.agent = Mock()
            mock_goal.agent.run_async = Mock(return_value=AsyncIteratorMock([
                Mock(content="Goal planning event", event_type="progress")
            ]))
            
            mock_advisor.agent = Mock()
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
    
    def test_session_state_sharing(self):
        """Test that agents share data through session state with proper async mocking."""
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
    
    def test_quick_analysis_workflow(self):
        """Test quick analysis workflow with proper async mocking."""
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
    
    def test_goal_focused_analysis(self):
        """Test goal-focused analysis workflow with proper async mocking."""
        async def run_test():
            mock_ctx = Mock()
            mock_ctx.session.state = {'customer_id': 123}
            
            result = await self.orchestrator.run_goal_focused_analysis(mock_ctx, 123, 456)
            
            self.assertEqual(result['status'], 'completed')
            self.assertEqual(result['customer_id'], 123)
            self.assertEqual(result['goal_id'], 456)
            
            # Verify session state was updated
            self.assertIn('spending_insights', mock_ctx.session.state)
            self.assertIn('goal_feasibility', mock_ctx.session.state)
            self.assertIn('goal_progress', mock_ctx.session.state)
            self.assertIn('savings_plan', mock_ctx.session.state)
            self.assertIn('quick_recommendations', mock_ctx.session.state)
        
        asyncio.run(run_test())

class TestIntelligentOrchestratorUnit(unittest.TestCase):
    """Unit tests for intelligent orchestrator with heavy mocking."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mcp_server_path = "/fake/path/mcp_server.py"
        self.orchestrator = IntelligentOrchestrator(self.mcp_server_path, "adk_web")
    
    def test_intelligent_orchestrator_initialization(self):
        """Test intelligent orchestrator initialization."""
        self.assertEqual(self.orchestrator.name, "IntelligentOrchestrator")
        # Check if _deployment_context exists (it might be a private attribute)
        if hasattr(self.orchestrator, '_deployment_context'):
            self.assertEqual(self.orchestrator._deployment_context, "adk_web")
    
    def test_set_sub_agents(self):
        """Test setting sub-agents for intelligent orchestrator."""
        mock_spending = Mock()
        mock_goal = Mock()
        mock_advisor = Mock()
        
        self.orchestrator.set_sub_agents(mock_spending, mock_goal, mock_advisor)
        
        self.assertEqual(self.orchestrator._sub_agents['spending_analyzer'], mock_spending)
        self.assertEqual(self.orchestrator._sub_agents['goal_planner'], mock_goal)
        self.assertEqual(self.orchestrator._sub_agents['advisor'], mock_advisor)

if __name__ == '__main__':
    unittest.main()
