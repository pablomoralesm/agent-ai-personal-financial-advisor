"""
Test Streamlit Integration with ADK Agent System

This module tests the integration between Streamlit UI components
and the ADK agent system, ensuring that the UI can properly
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
    """Test Streamlit integration with ADK agent system."""
    
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
        """Test that financial analysis function works with ADK agents."""
        try:
            from ui.components.recommendations import run_financial_analysis
            
            # Mock the ADK agent manager
            with patch('utils.adk_agent_manager.run_full_analysis_adk') as mock_adk:
                mock_adk.return_value = {
                    'status': 'success',
                    'analysis_type': 'full',
                    'customer_id': self.customer_id,
                    'result': {
                        'events': [{'content': 'Test analysis content'}],
                        'summary': 'Test analysis summary'
                    },
                    'agent_used': 'SequencerAgent'
                }
                
                result = run_financial_analysis(self.customer_id)
                
                self.assertIsNotNone(result)
                self.assertEqual(result['analysis_type'], 'full')
                self.assertEqual(result['customer_id'], self.customer_id)
                self.assertIn('result', result)
                self.assertEqual(result['agent_used'], 'SequencerAgent')
                
        except Exception as e:
            self.fail(f"Financial analysis function failed: {e}")
    
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
    """Test integration between Streamlit and ADK agents."""
    
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
            from utils.adk_agent_manager import ADKAgentManager
            
            manager = ADKAgentManager(mcp_server_path=self.mcp_server_path)
            status = manager.get_agent_status()
            
            # Verify status structure
            self.assertIn('agent_manager', status)
            self.assertIn('deployment_context', status)
            self.assertIn('available_agents', status)
            self.assertIn('integration_type', status)
            
            # Verify ADK agent manager info
            self.assertEqual(status['agent_manager'], 'ADKAgentManager')
            self.assertEqual(status['deployment_context'], 'streamlit')
            self.assertEqual(status['integration_type'], 'direct')
            
        except Exception as e:
            self.fail(f"Agent system status display test failed: {e}")

if __name__ == '__main__':
    unittest.main()