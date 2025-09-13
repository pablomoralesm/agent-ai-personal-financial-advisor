"""
Multi-Agent Interaction Tests

This module tests the multi-agent workflow components and verifies that the unified system
works correctly across both deployment contexts. These tests focus on the core functionality
without complex ADK execution mocking.
"""

import unittest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from types import SimpleNamespace

# Import the unified agent system
from agents.unified import (
    ProceduralOrchestrator, 
    IntelligentOrchestrator,
    AgentFactory,
    OrchestratorFactory,
    DeploymentContext,
    DeploymentConfig
)
from utils.unified_agent_executor import HybridAgentExecutor
from utils.adk_session_manager import ADKSessionManager


class AsyncIteratorMock:
    """Mock that can be used in async for loops"""
    def __init__(self, items):
        self.items = items
        self.index = 0
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.index >= len(self.items):
            raise StopAsyncIteration
        item = self.items[self.index]
        self.index += 1
        return item


class TestMultiAgentInteractions(unittest.TestCase):
    """Test multi-agent interactions in both Streamlit and ADK Web contexts"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mcp_server_path = "/path/to/mcp_server"
        self.customer_id = "test_customer_123"
        self.goal_id = "test_goal_456"
        
        # Mock MCP tools
        self.mock_mcp_tools = {
            'get_customer_profile': AsyncMock(return_value={'customer_id': self.customer_id}),
            'analyze_customer_spending': AsyncMock(return_value={'spending_analysis': 'mock_data'}),
            'get_customer_goals': AsyncMock(return_value={'goals': ['goal1', 'goal2']}),
            'generate_financial_advice': AsyncMock(return_value={'advice': 'mock_advice'})
        }
    
    def create_mock_event(self, content, author="test_agent"):
        """Create a mock ADK Event"""
        from google.adk.events import Event
        from google.genai.types import Content, Part
        
        return Event(
            author=author,
            content=Content(parts=[Part(text=content)])
        )
    
    def create_mock_agent(self, name, analysis_type="spending"):
        """Create a mock agent with proper async behavior"""
        mock_agent = Mock()
        mock_agent.name = name
        mock_agent.run_async = AsyncMock()
        
        # Create mock events for different analysis types
        if analysis_type == "spending":
            events = [
                self.create_mock_event(f"{name}: Starting spending analysis", name),
                self.create_mock_event(f"{name}: Analysis complete", name)
            ]
        elif analysis_type == "goal":
            events = [
                self.create_mock_event(f"{name}: Starting goal analysis", name),
                self.create_mock_event(f"{name}: Goal analysis complete", name)
            ]
        else:  # advisor
            events = [
                self.create_mock_event(f"{name}: Starting advice generation", name),
                self.create_mock_event(f"{name}: Advice generated", name)
            ]
        
        mock_agent.run_async.return_value = AsyncIteratorMock(events)
        return mock_agent


class TestStreamlitMultiAgentInteractions(TestMultiAgentInteractions):
    """Test multi-agent interactions in Streamlit context"""
    
    def test_streamlit_executor_initialization(self):
        """Test that Streamlit executor initializes correctly"""
        executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="streamlit"
        )
        
        # Verify initialization
        self.assertEqual(executor.context, "streamlit")
        self.assertEqual(executor.deployment_context, DeploymentContext.STREAMLIT)
        self.assertIsNone(executor.agent_executor)  # Uses unified system
    
    def test_streamlit_agent_status(self):
        """Test that Streamlit agent status is correct"""
        executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="streamlit"
        )
        
        status = executor.get_agent_status()
        
        # Verify status structure
        self.assertIn('deployment_context', status)
        self.assertIn('orchestrator', status)
        self.assertIn('agents_initialized', status)
        self.assertEqual(status['deployment_context'], 'streamlit')
    
    def test_streamlit_agent_factory_integration(self):
        """Test that Streamlit can create agents through the factory"""
        # Test agent factory for Streamlit context
        spending_agent = AgentFactory.create_spending_analyzer(
            mcp_server_path=self.mcp_server_path,
            deployment_context=DeploymentContext.STREAMLIT.value
        )
        
        # Verify agent creation
        self.assertIsNotNone(spending_agent)
        self.assertEqual(spending_agent.name, "SpendingAnalyzerAgent")
        
        # Test orchestrator factory for Streamlit context
        orchestrator = OrchestratorFactory.create_orchestrator(
            orchestrator_type="procedural",
            mcp_server_path=self.mcp_server_path,
            deployment_context=DeploymentContext.STREAMLIT.value
        )
        
        # Verify orchestrator creation
        self.assertIsNotNone(orchestrator)
        self.assertEqual(orchestrator.name, "ProceduralOrchestrator")


class TestADKWebMultiAgentInteractions(TestMultiAgentInteractions):
    """Test multi-agent interactions in ADK Web context"""
    
    def test_adk_web_executor_initialization(self):
        """Test that ADK Web executor initializes correctly"""
        executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="adk_web"
        )
        
        # Verify initialization
        self.assertEqual(executor.context, "adk_web")
        self.assertEqual(executor.deployment_context, DeploymentContext.ADK_WEB)
        self.assertIsNone(executor.agent_executor)  # Uses unified system
    
    def test_adk_web_agent_status(self):
        """Test that ADK Web agent status is correct"""
        executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="adk_web"
        )
        
        status = executor.get_agent_status()
        
        # Verify status structure
        self.assertIn('deployment_context', status)
        self.assertIn('orchestrator', status)
        self.assertIn('agents_initialized', status)
        self.assertEqual(status['deployment_context'], 'adk_web')
    
    def test_adk_web_agent_factory_integration(self):
        """Test that ADK Web can create agents through the factory"""
        # Test agent factory for ADK Web context
        spending_agent = AgentFactory.create_spending_analyzer(
            mcp_server_path=self.mcp_server_path,
            deployment_context=DeploymentContext.ADK_WEB.value
        )
        
        # Verify agent creation
        self.assertIsNotNone(spending_agent)
        self.assertEqual(spending_agent.name, "SpendingAnalyzerAgent")
        
        # Test orchestrator factory for ADK Web context
        orchestrator = OrchestratorFactory.create_orchestrator(
            orchestrator_type="procedural",
            mcp_server_path=self.mcp_server_path,
            deployment_context=DeploymentContext.ADK_WEB.value
        )
        
        # Verify orchestrator creation
        self.assertIsNotNone(orchestrator)
        self.assertEqual(orchestrator.name, "ProceduralOrchestrator")


class TestCrossPlatformConsistency(TestMultiAgentInteractions):
    """Test that both platforms use the same underlying system"""
    
    def test_deployment_context_consistency(self):
        """Test that both contexts use the same deployment configuration"""
        # Test Streamlit context
        streamlit_executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="streamlit"
        )
        
        # Test ADK Web context
        adk_web_executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="adk_web"
        )
        
        # Both should use unified system (agent_executor should be None)
        self.assertIsNone(streamlit_executor.agent_executor)
        self.assertIsNone(adk_web_executor.agent_executor)
        
        # Both should have deployment contexts
        self.assertIsNotNone(streamlit_executor.deployment_context)
        self.assertIsNotNone(adk_web_executor.deployment_context)
    
    def test_agent_factory_consistency(self):
        """Test that both contexts use the same agent factory"""
        from agents.unified.agent_factory import AgentFactory, OrchestratorFactory
        
        # Test that factory methods work for both contexts
        streamlit_config = DeploymentConfig.get_config(DeploymentContext.STREAMLIT)
        adk_web_config = DeploymentConfig.get_config(DeploymentContext.ADK_WEB)
        
        # Both should return valid configurations (dictionaries)
        self.assertIsNotNone(streamlit_config)
        self.assertIsNotNone(adk_web_config)
        self.assertIsInstance(streamlit_config, dict)
        self.assertIsInstance(adk_web_config, dict)
        
        # Both should have the same configuration keys
        self.assertIn('orchestrator_type', streamlit_config)
        self.assertIn('orchestrator_type', adk_web_config)
        self.assertIn('use_runner', streamlit_config)
        self.assertIn('use_runner', adk_web_config)


class TestErrorHandling(TestMultiAgentInteractions):
    """Test error handling in multi-agent interactions"""
    
    def test_invalid_context_handling(self):
        """Test error handling for invalid context"""
        # The HybridAgentExecutor doesn't validate context, it just defaults to streamlit behavior
        executor = HybridAgentExecutor(
            mcp_server_path=self.mcp_server_path,
            context="invalid_context"
        )
        
        # Should still initialize but with default behavior
        self.assertEqual(executor.context, "invalid_context")
        # The deployment_context will be set based on the if/else logic
        self.assertIsNotNone(executor.deployment_context)
    
    def test_missing_mcp_server_path(self):
        """Test error handling for missing MCP server path"""
        with self.assertRaises(TypeError):
            HybridAgentExecutor(context="streamlit")


class TestEventFlow(TestMultiAgentInteractions):
    """Test event flow between agents"""
    
    def test_event_author_consistency(self):
        """Test that events have consistent author information"""
        # Create mock events from different agents
        spending_event = self.create_mock_event("Spending analysis", "SpendingAnalyzer")
        goal_event = self.create_mock_event("Goal analysis", "GoalPlanner")
        advisor_event = self.create_mock_event("Advice generation", "Advisor")
        
        # Verify event structure
        self.assertEqual(spending_event.author, "SpendingAnalyzer")
        self.assertEqual(goal_event.author, "GoalPlanner")
        self.assertEqual(advisor_event.author, "Advisor")
        
        # Verify content structure
        self.assertIsNotNone(spending_event.content)
        self.assertIsNotNone(goal_event.content)
        self.assertIsNotNone(advisor_event.content)
    
    def test_event_content_structure(self):
        """Test that events have proper content structure"""
        event = self.create_mock_event("Test message", "TestAgent")
        
        # Verify content structure matches ADK pattern
        self.assertIsNotNone(event.content)
        self.assertIsNotNone(event.content.parts)
        self.assertEqual(len(event.content.parts), 1)
        self.assertEqual(event.content.parts[0].text, "Test message")


if __name__ == '__main__':
    unittest.main()
