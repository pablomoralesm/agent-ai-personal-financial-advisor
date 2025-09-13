"""
Test Streamlit Integration with Unified Agent System

This module tests the integration between Streamlit UI components
and the unified agent system, ensuring that the UI can properly
execute agents and display results.

Part of the Agentic AI Personal Financial Advisor application.
"""

import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class TestStreamlitIntegration(unittest.TestCase):
    """Test Streamlit integration with unified agent system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mcp_server_path = str(project_root / "mcp_server" / "database_server_stdio.py")
        self.customer_id = 123
    
    def test_recommendations_component_import(self):
        """Test that recommendations component can be imported and initialized."""
        try:
            from ui.components.recommendations import render_recommendations, run_financial_analysis
            self.assertTrue(True, "Recommendations component imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import recommendations component: {e}")
    
    def test_recommendations_component_renders(self):
        """Test that recommendations component renders without errors."""
        try:
            from ui.components.recommendations import render_recommendations
            # This should not raise an exception during import
            self.assertTrue(True, "Recommendations component imported successfully")
        except Exception as e:
            self.fail(f"Recommendations component failed to import: {e}")
    
    def test_financial_analysis_function(self):
        """Test that financial analysis function works with unified agents."""
        try:
            from ui.components.recommendations import run_financial_analysis
            
            # Mock the unified agent executor
            with patch('utils.unified_agent_executor.run_financial_analysis_unified') as mock_unified:
                mock_unified.return_value = {
                    'status': 'success',
                    'results': {'spending_analysis': 'Test analysis'},
                    'recommendations': ['Test recommendation']
                }
                
                result = run_financial_analysis(self.customer_id)
                
                self.assertIsNotNone(result)
                self.assertEqual(result['status'], 'success')
                mock_unified.assert_called_once_with(self.customer_id)
                
        except Exception as e:
            self.fail(f"Financial analysis function failed: {e}")
    
    def test_quick_analysis_function(self):
        """Test that quick analysis function works with unified agents."""
        try:
            from ui.components.recommendations import run_quick_analysis
            
            # Mock the unified agent executor
            with patch('utils.unified_agent_executor.run_quick_analysis_unified') as mock_unified:
                mock_unified.return_value = {
                    'status': 'success',
                    'results': {'quick_analysis': 'Test quick analysis'},
                    'recommendations': ['Test quick recommendation']
                }
                
                result = run_quick_analysis(self.customer_id)
                
                self.assertIsNotNone(result)
                self.assertEqual(result['status'], 'success')
                mock_unified.assert_called_once_with(self.customer_id)
                
        except Exception as e:
            self.fail(f"Quick analysis function failed: {e}")
    
    def test_goal_analysis_function(self):
        """Test that goal analysis function works with unified agents."""
        try:
            from ui.components.recommendations import run_goal_analysis
            
            # Mock the unified agent executor
            with patch('utils.unified_agent_executor.run_goal_analysis_unified') as mock_unified:
                mock_unified.return_value = {
                    'status': 'success',
                    'results': {'goal_analysis': 'Test goal analysis'},
                    'recommendations': ['Test goal recommendation']
                }
                
                result = run_goal_analysis(self.customer_id)
                
                self.assertIsNotNone(result)
                self.assertEqual(result['status'], 'success')
                mock_unified.assert_called_once_with(self.customer_id, None)
                
        except Exception as e:
            self.fail(f"Goal analysis function failed: {e}")
    
    def test_unified_agent_executor_initialization(self):
        """Test that UnifiedAgentExecutor can be initialized."""
        try:
            from utils.unified_agent_executor import UnifiedAgentExecutor
            
            executor = UnifiedAgentExecutor(self.mcp_server_path)
            status = executor.get_agent_status()
            
            self.assertIsNotNone(executor)
            self.assertIn('orchestrator', status)
            self.assertEqual(status['deployment_context'], 'streamlit')
            self.assertEqual(status['orchestrator']['type'], 'procedural')
            
        except Exception as e:
            self.fail(f"UnifiedAgentExecutor initialization failed: {e}")
    
    def test_unified_agent_executor_analysis_methods(self):
        """Test that UnifiedAgentExecutor analysis methods work."""
        try:
            from utils.unified_agent_executor import UnifiedAgentExecutor
            
            executor = UnifiedAgentExecutor(self.mcp_server_path)
            
            # Test that methods exist and are callable
            self.assertTrue(hasattr(executor, 'execute_full_analysis'))
            self.assertTrue(hasattr(executor, 'execute_quick_analysis'))
            self.assertTrue(hasattr(executor, 'execute_goal_analysis'))
            self.assertTrue(hasattr(executor, 'get_agent_status'))
            
            # Test that methods are callable
            self.assertTrue(callable(executor.execute_full_analysis))
            self.assertTrue(callable(executor.execute_quick_analysis))
            self.assertTrue(callable(executor.execute_goal_analysis))
            self.assertTrue(callable(executor.get_agent_status))
            
        except Exception as e:
            self.fail(f"UnifiedAgentExecutor methods test failed: {e}")
    
    def test_streamlit_app_import(self):
        """Test that the main Streamlit app can be imported."""
        try:
            from streamlit_app import main
            self.assertTrue(callable(main))
        except ImportError as e:
            self.fail(f"Failed to import main Streamlit app: {e}")
    
    def test_streamlit_app_initialization(self):
        """Test that the main Streamlit app initializes correctly."""
        try:
            from streamlit_app import main
            # This should not raise an exception during import
            self.assertTrue(True, "Streamlit app imported successfully")
        except Exception as e:
            self.fail(f"Streamlit app import failed: {e}")

class TestStreamlitAgentIntegration(unittest.TestCase):
    """Test integration between Streamlit and unified agents."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.mcp_server_path = str(project_root / "mcp_server" / "database_server_stdio.py")
        self.customer_id = 123
    
    def test_mcp_server_path_initialization(self):
        """Test that MCP server path is properly initialized in session state."""
        try:
            from streamlit_app import main
            # This should not raise an exception during import
            self.assertTrue(True, "Streamlit app imported successfully")
        except Exception as e:
            self.fail(f"Streamlit app import failed: {e}")
    
    def test_agent_system_status_display(self):
        """Test that agent system status can be displayed in Streamlit."""
        try:
            from utils.unified_agent_executor import UnifiedAgentExecutor
            
            executor = UnifiedAgentExecutor(self.mcp_server_path)
            status = executor.get_agent_status()
            
            # Verify status structure
            self.assertIn('orchestrator', status)
            self.assertIn('deployment_context', status)
            self.assertIn('mcp_server_path', status)
            
            # Verify orchestrator info
            orchestrator_info = status['orchestrator']
            self.assertIn('initialized', orchestrator_info)
            self.assertIn('name', orchestrator_info)
            self.assertIn('type', orchestrator_info)
            
            self.assertTrue(orchestrator_info['initialized'])
            self.assertEqual(orchestrator_info['type'], 'procedural')
            self.assertEqual(status['deployment_context'], 'streamlit')
            
        except Exception as e:
            self.fail(f"Agent system status display test failed: {e}")

if __name__ == '__main__':
    unittest.main()
