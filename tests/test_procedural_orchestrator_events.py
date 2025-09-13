#!/usr/bin/env python3
"""
Unit tests for ProceduralOrchestrator Event creation patterns.

These tests ensure that the procedural orchestrator uses the correct ADK Event
creation pattern and doesn't fall back to the deprecated ctx.create_event() method.

Part of the Agentic AI Personal Financial Advisor application.
"""

import unittest
from unittest.mock import AsyncMock, MagicMock, patch
import asyncio
from types import SimpleNamespace

from agents.unified.procedural_orchestrator import ProceduralOrchestrator
from agents.unified.deployment_configs import DeploymentContext
from google.adk.events import Event
from google.genai.types import Content, Part


class TestProceduralOrchestratorEvents(unittest.TestCase):
    """Test Event creation patterns in ProceduralOrchestrator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mcp_server_path = "mcp_server/database_server_stdio.py"
        self.customer_id = 1
        
        # Create orchestrator
        self.orchestrator = ProceduralOrchestrator(
            mcp_server_path=self.mcp_server_path,
            deployment_context=DeploymentContext.STREAMLIT
        )
        
        # Create mock context
        self.ctx = SimpleNamespace()
        self.ctx.session = SimpleNamespace()
        self.ctx.session.state = {'customer_id': self.customer_id}
    
    def run_async_test(self, async_method):
        """Helper to run async test methods."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(async_method())
        finally:
            loop.close()
    
    def test_event_creation_patterns(self):
        """Test that all events use the correct ADK Event creation pattern."""
        # Mock the sub-agents to avoid real execution
        mock_spending = MagicMock()
        mock_goal = MagicMock()
        mock_advisor = MagicMock()
        
        # Set sub-agents using the proper method
        self.orchestrator.set_sub_agents(mock_spending, mock_goal, mock_advisor)
        
        # Mock the sub-agent run_async methods to return empty async generators
        async def empty_async_generator():
            return
            yield  # This makes it an async generator
        
        mock_spending.agent.run_async = AsyncMock(return_value=empty_async_generator())
        mock_goal.agent.run_async = AsyncMock(return_value=empty_async_generator())
        mock_advisor.agent.run_async = AsyncMock(return_value=empty_async_generator())
        
        # Run the orchestrator
        events = []
        async def collect_events():
            async for event in self.orchestrator._run_async_impl(self.ctx):
                events.append(event)
        
        self.run_async_test(collect_events)
        
        # Verify that all events are proper ADK Event objects
        self.assertGreater(len(events), 0, "Should generate at least one event")
        
        for event in events:
            self.assertIsInstance(event, Event, f"Event should be ADK Event, got {type(event)}")
            self.assertIsInstance(event.content, Content, f"Event content should be Content, got {type(event.content)}")
            self.assertIsInstance(event.content.parts, list, "Event content should have parts list")
            self.assertGreater(len(event.content.parts), 0, "Event content should have at least one part")
            self.assertIsInstance(event.content.parts[0], Part, f"Event content part should be Part, got {type(event.content.parts[0])}")
            self.assertIsInstance(event.content.parts[0].text, str, "Event content part should have text")
            self.assertEqual(event.author, self.orchestrator.name, "Event author should match orchestrator name")
    
    def test_no_ctx_create_event_calls(self):
        """Test that the orchestrator doesn't use ctx.create_event() method."""
        # This test ensures we catch any regression to ctx.create_event()
        
        # Mock the sub-agents
        mock_spending = MagicMock()
        mock_goal = MagicMock()
        mock_advisor = MagicMock()
        
        # Set sub-agents using the proper method
        self.orchestrator.set_sub_agents(mock_spending, mock_goal, mock_advisor)
        
        # Mock the sub-agent run_async methods
        async def empty_async_generator():
            return
            yield
        
        mock_spending.agent.run_async = AsyncMock(return_value=empty_async_generator())
        mock_goal.agent.run_async = AsyncMock(return_value=empty_async_generator())
        mock_advisor.agent.run_async = AsyncMock(return_value=empty_async_generator())
        
        # Add a create_event method to the context to catch if it's called
        create_event_called = []
        def mock_create_event(*args, **kwargs):
            create_event_called.append((args, kwargs))
            return Event(author="test", content=Content(parts=[Part(text="test")]))
        
        self.ctx.create_event = mock_create_event
        
        # Run the orchestrator
        events = []
        async def collect_events():
            async for event in self.orchestrator._run_async_impl(self.ctx):
                events.append(event)
        
        self.run_async_test(collect_events)
        
        # Verify that ctx.create_event was never called
        self.assertEqual(len(create_event_called), 0, 
                        f"ctx.create_event() should not be called, but was called {len(create_event_called)} times: {create_event_called}")
    
    def test_event_content_structure(self):
        """Test that event content follows the correct ADK structure."""
        # Mock the sub-agents
        mock_spending = MagicMock()
        mock_goal = MagicMock()
        mock_advisor = MagicMock()
        
        # Set sub-agents using the proper method
        self.orchestrator.set_sub_agents(mock_spending, mock_goal, mock_advisor)
        
        # Mock the sub-agent run_async methods
        async def empty_async_generator():
            return
            yield
        
        mock_spending.agent.run_async = AsyncMock(return_value=empty_async_generator())
        mock_goal.agent.run_async = AsyncMock(return_value=empty_async_generator())
        mock_advisor.agent.run_async = AsyncMock(return_value=empty_async_generator())
        
        # Run the orchestrator
        events = []
        async def collect_events():
            async for event in self.orchestrator._run_async_impl(self.ctx):
                events.append(event)
        
        self.run_async_test(collect_events)
        
        # Verify event structure
        for event in events:
            # Check Event structure
            self.assertIsInstance(event, Event)
            self.assertIsNotNone(event.author)
            self.assertIsNotNone(event.content)
            
            # Check Content structure
            self.assertIsInstance(event.content, Content)
            self.assertIsInstance(event.content.parts, list)
            self.assertGreater(len(event.content.parts), 0)
            
            # Check Part structure
            for part in event.content.parts:
                self.assertIsInstance(part, Part)
                self.assertIsInstance(part.text, str)
                self.assertGreater(len(part.text), 0)
    
    def test_error_event_creation(self):
        """Test that error events are created with proper ADK structure."""
        # Test with no customer ID to trigger error path
        self.ctx.session.state = {}
        
        events = []
        async def collect_events():
            async for event in self.orchestrator._run_async_impl(self.ctx):
                events.append(event)
        
        self.run_async_test(collect_events)
        
        # Should have at least one error event
        self.assertGreater(len(events), 0)
        
        # Check that error events follow proper structure
        for event in events:
            self.assertIsInstance(event, Event)
            self.assertIsInstance(event.content, Content)
            self.assertIsInstance(event.content.parts, list)
            self.assertGreater(len(event.content.parts), 0)
            self.assertIsInstance(event.content.parts[0], Part)
            self.assertIsInstance(event.content.parts[0].text, str)
    
    def test_imports_are_correct(self):
        """Test that the orchestrator imports the correct ADK types."""
        # Check that the required imports are present
        import agents.unified.procedural_orchestrator as module
        
        # Verify Event import
        self.assertTrue(hasattr(module, 'Event'), "Module should import Event")
        self.assertEqual(module.Event, Event, "Should import Event from google.adk.events")
        
        # Verify Content and Part imports
        self.assertTrue(hasattr(module, 'Content'), "Module should import Content")
        self.assertTrue(hasattr(module, 'Part'), "Module should import Part")
        self.assertEqual(module.Content, Content, "Should import Content from google.genai.types")
        self.assertEqual(module.Part, Part, "Should import Part from google.genai.types")


class TestProceduralOrchestratorRegression(unittest.TestCase):
    """Test to prevent regression to ctx.create_event() pattern."""
    
    def test_source_code_does_not_contain_create_event(self):
        """Test that the source code doesn't contain ctx.create_event() calls."""
        import os
        import re
        
        # Read the procedural orchestrator source code
        file_path = os.path.join(os.path.dirname(__file__), '..', 'agents', 'unified', 'procedural_orchestrator.py')
        
        with open(file_path, 'r') as f:
            source_code = f.read()
        
        # Check for ctx.create_event patterns
        create_event_patterns = [
            r'ctx\.create_event\(',
            r'\.create_event\(',
            r'create_event\('
        ]
        
        for pattern in create_event_patterns:
            matches = re.findall(pattern, source_code)
            self.assertEqual(len(matches), 0, 
                           f"Found {len(matches)} instances of '{pattern}' in source code. "
                           f"Should use proper ADK Event creation pattern instead. "
                           f"Matches: {matches}")
    
    def test_source_code_contains_proper_event_creation(self):
        """Test that the source code contains proper ADK Event creation patterns."""
        import os
        import re
        
        # Read the procedural orchestrator source code
        file_path = os.path.join(os.path.dirname(__file__), '..', 'agents', 'unified', 'procedural_orchestrator.py')
        
        with open(file_path, 'r') as f:
            source_code = f.read()
        
        # Check for proper Event creation patterns
        proper_patterns = [
            r'yield Event\(',
            r'Event\(',
            r'Content\(',
            r'Part\('
        ]
        
        for pattern in proper_patterns:
            matches = re.findall(pattern, source_code)
            self.assertGreater(len(matches), 0, 
                             f"Should find instances of '{pattern}' in source code for proper ADK Event creation")


if __name__ == '__main__':
    unittest.main()
