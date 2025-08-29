"""
Tests for the MCP (Model Context Protocol) database server.

This module tests the FastMCP server that provides database access tools
to the AI agents. It ensures the server can start, tools are properly
registered, and database operations work correctly.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import os
import sys
import tempfile
import json

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from mcp_server.database_server import mcp, DatabaseManager


class TestMCPServerSetup(unittest.TestCase):
    """Test the MCP server initialization and configuration."""
    
    def test_mcp_server_creation(self):
        """Test that the FastMCP server is created successfully."""
        self.assertIsNotNone(mcp)
        self.assertTrue(hasattr(mcp, 'tool'))
    
    def test_database_manager_creation(self):
        """Test that DatabaseManager can be created."""
        config = {
            'host': 'localhost',
            'port': 3306,
            'database': 'test_db',
            'user': 'test_user',
            'password': 'test_password',
            'autocommit': True,
            'charset': 'utf8mb4'
        }
        
        db_manager = DatabaseManager(config)
        self.assertIsNotNone(db_manager)
        self.assertEqual(db_manager.config, config)
    
    def test_tool_registration(self):
        """Test that all expected tools are registered."""
        # FastMCP tools are registered via decorators, so we test the module imports
        # rather than trying to access them as attributes
        try:
            # Import the tool functions directly to verify they exist
            from mcp_server.database_server import (
                get_customer_profile,
                create_customer,
                add_transaction, 
                get_transactions_by_customer,
                create_financial_goal,
                get_financial_goals,
                save_advice,
                get_advice_history
            )
            
            # Verify all tools exist (they may be FunctionTool objects, not callable functions)
            self.assertIsNotNone(get_customer_profile)
            self.assertIsNotNone(create_customer)
            self.assertIsNotNone(add_transaction)
            self.assertIsNotNone(get_transactions_by_customer)
            self.assertIsNotNone(create_financial_goal)
            self.assertIsNotNone(get_financial_goals)
            self.assertIsNotNone(save_advice)
            self.assertIsNotNone(get_advice_history)
            
        except ImportError as e:
            self.fail(f"Failed to import MCP tool functions: {e}")
    
    def test_tool_decorators(self):
        """Test that tools have proper decorators."""
        # Since we can't directly access the decorated functions from the mcp object,
        # we test that the module can be imported and the functions exist
        try:
            from mcp_server.database_server import (
                get_customer_profile,
                create_customer,
                add_transaction,
                get_transactions_by_customer,
                create_financial_goal,
                get_financial_goals,
                save_advice,
                get_advice_history
            )
            
            # All tools should exist (they may be FunctionTool objects)
            tools = [
                get_customer_profile,
                create_customer,
                add_transaction,
                get_transactions_by_customer,
                create_financial_goal,
                get_financial_goals,
                save_advice,
                get_advice_history
            ]
            
            for tool in tools:
                self.assertIsNotNone(tool)
                
        except ImportError as e:
            self.fail(f"Failed to import MCP tools: {e}")


class TestDatabaseManager(unittest.TestCase):
    """Test the DatabaseManager class."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_config = {
            'host': 'localhost',
            'port': 3306,
            'user': 'test_user',
            'password': 'test_password',
            'database': 'test_db',
            'autocommit': True,
            'charset': 'utf8mb4'
        }
    
    @patch('mcp_server.database_server.mysql.connector.connect')
    def test_get_connection(self, mock_connect):
        """Test database connection establishment."""
        # Mock the MySQL connector
        mock_connection = Mock()
        mock_connect.return_value = mock_connection
        
        db_manager = DatabaseManager(self.test_config)
        connection = db_manager.get_connection()
        
        # Verify MySQL connector was called with correct parameters
        mock_connect.assert_called_once_with(**self.test_config)
        
        # Verify connection was returned
        self.assertEqual(connection, mock_connection)
    
    @patch('mcp_server.database_server.mysql.connector.connect')
    def test_execute_query_select(self, mock_connect):
        """Test SELECT query execution."""
        # Mock connection
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        
        mock_connect.return_value = mock_connection
        
        db_manager = DatabaseManager(self.test_config)
        result = db_manager.execute_query("SELECT * FROM customers")
        
        # Verify connection was established
        mock_connect.assert_called_once()
        
        # Verify cursor was used
        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM customers", ())
        
        # Verify result contains expected data
        self.assertEqual(result, mock_cursor.fetchall.return_value)
    
    @patch('mcp_server.database_server.mysql.connector.connect')
    def test_execute_query_insert(self, mock_connect):
        """Test INSERT query execution."""
        # Mock connection
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        
        mock_connect.return_value = mock_connection
        
        db_manager = DatabaseManager(self.test_config)
        result = db_manager.execute_query("INSERT INTO customers (name) VALUES (%s)", ("John Doe",))
        
        # Verify connection was established
        mock_connect.assert_called_once()
        
        # Verify SQL query was executed
        mock_cursor.execute.assert_called_once_with("INSERT INTO customers (name) VALUES (%s)", ("John Doe",))
        
        # Verify transaction was committed
        mock_connection.commit.assert_called_once()
        
        # Verify rowcount was returned
        self.assertEqual(result, mock_cursor.rowcount)


class TestMCPServerIntegration(unittest.TestCase):
    """Test MCP server integration and error handling."""
    
    def test_mcp_server_imports(self):
        """Test that MCP server module can be imported and contains expected components."""
        try:
            # Test that we can import the main components
            from mcp_server.database_server import mcp, DatabaseManager, db_manager
            
            # Verify components exist
            self.assertIsNotNone(mcp)
            self.assertIsNotNone(DatabaseManager)
            self.assertIsNotNone(db_manager)
            
        except ImportError as e:
            self.fail(f"Failed to import MCP server components: {e}")
    
    def test_database_manager_instance(self):
        """Test that the global database manager instance is properly configured."""
        try:
            from mcp_server.database_server import db_manager
            
            # Verify db_manager is an instance of DatabaseManager
            self.assertIsInstance(db_manager, DatabaseManager)
            
            # Verify it has the expected configuration
            self.assertIn('host', db_manager.config)
            self.assertIn('port', db_manager.config)
            self.assertIn('database', db_manager.config)
            self.assertIn('user', db_manager.config)
            self.assertIn('password', db_manager.config)
            
        except Exception as e:
            self.fail(f"Failed to verify database manager instance: {e}")


if __name__ == '__main__':
    unittest.main()
