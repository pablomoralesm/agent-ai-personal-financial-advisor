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
        # Get all registered tools from the mcp server
        tools = []
        for attr_name in dir(mcp):
            attr = getattr(mcp, attr_name)
            if hasattr(attr, '_is_tool'):
                tools.append(attr_name)
        
        # Verify essential tools are present
        expected_tools = [
            'get_customer_by_id',
            'add_transaction', 
            'get_transactions_by_customer',
            'add_goal',
            'get_goals_by_customer',
            'add_advice',
            'get_advice_history'
        ]
        
        for tool_name in expected_tools:
            self.assertIn(tool_name, tools, f"Tool {tool_name} not found")
    
    def test_tool_decorators(self):
        """Test that tools have proper decorators."""
        # Check that the main database tools exist and are callable
        self.assertTrue(callable(mcp.get_customer_by_id))
        self.assertTrue(callable(mcp.add_transaction))
        self.assertTrue(callable(mcp.get_transactions_by_customer))
        self.assertTrue(callable(mcp.add_goal))
        self.assertTrue(callable(mcp.get_goals_by_customer))
        self.assertTrue(callable(mcp.add_advice))
        self.assertTrue(callable(mcp.get_advice_history))


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
        # Mock database connection and cursor
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        
        # Mock cursor fetchall to return data
        mock_cursor.fetchall.return_value = [{'id': 1, 'name': 'John Doe'}]
        
        mock_connect.return_value = mock_connection
        
        db_manager = DatabaseManager(self.test_config)
        result = db_manager.execute_query("SELECT * FROM customers")
        
        # Verify connection was established
        mock_connect.assert_called_once()
        
        # Verify SQL query was executed
        mock_cursor.execute.assert_called_once_with("SELECT * FROM customers", None)
        
        # Verify result contains expected data
        self.assertEqual(result, [{'id': 1, 'name': 'John Doe'}])
    
    @patch('mcp_server.database_server.mysql.connector.connect')
    def test_execute_query_insert(self, mock_connect):
        """Test INSERT query execution."""
        # Mock database connection and cursor
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


class TestDatabaseTools(unittest.TestCase):
    """Test individual database tool functions."""
    
    def setUp(self):
        """Set up test environment."""
        self.mock_customer_data = {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30,
            "income": 75000
        }
        
        self.mock_transaction_data = {
            "customer_id": 1,
            "amount": 150.50,
            "category": "Food",
            "description": "Grocery shopping",
            "date": "2025-08-26"
        }
        
        self.mock_goal_data = {
            "customer_id": 1,
            "goal_type": "savings",
            "target_amount": 10000,
            "current_amount": 2500,
            "target_date": "2026-12-31"
        }
    
    @patch('mcp_server.database_server.db_manager')
    def test_get_customer_by_id(self, mock_db_manager):
        """Test get_customer_by_id tool function."""
        # Mock database manager
        mock_db_manager.execute_query.return_value = [self.mock_customer_data]
        
        # Call the tool function
        result = mcp.get_customer_by_id(1)
        
        # Verify database query was executed
        mock_db_manager.execute_query.assert_called_once()
        
        # Verify result contains expected data
        self.assertIsInstance(result, dict)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "John Doe")
    
    @patch('mcp_server.database_server.db_manager')
    def test_add_transaction(self, mock_db_manager):
        """Test add_transaction tool function."""
        # Mock database manager
        mock_db_manager.execute_query.return_value = 1
        
        # Call the tool function
        result = mcp.add_transaction(
            customer_id=1,
            amount=150.50,
            category="Food",
            description="Grocery shopping",
            date="2025-08-26"
        )
        
        # Verify database query was executed
        mock_db_manager.execute_query.assert_called_once()
        
        # Verify result indicates success
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)
    
    @patch('mcp_server.database_server.db_manager')
    def test_get_transactions_by_customer(self, mock_db_manager):
        """Test get_transactions_by_customer tool function."""
        # Mock database manager
        mock_db_manager.execute_query.return_value = [
            {"id": 1, "amount": 150.50, "category": "Food", "date": "2025-08-26"},
            {"id": 2, "amount": 75.25, "category": "Transportation", "date": "2025-08-25"}
        ]
        
        # Call the tool function
        result = mcp.get_transactions_by_customer(1)
        
        # Verify database query was executed
        mock_db_manager.execute_query.assert_called_once()
        
        # Verify result contains expected data
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["amount"], 150.50)
        self.assertEqual(result[0]["category"], "Food")
    
    @patch('mcp_server.database_server.db_manager')
    def test_add_goal(self, mock_db_manager):
        """Test add_goal tool function."""
        # Mock database manager
        mock_db_manager.execute_query.return_value = 1
        
        # Call the tool function
        result = mcp.add_goal(
            customer_id=1,
            goal_type="savings",
            target_amount=10000,
            current_amount=2500,
            target_date="2026-12-31"
        )
        
        # Verify database query was executed
        mock_db_manager.execute_query.assert_called_once()
        
        # Verify result indicates success
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)


class TestMCPServerIntegration(unittest.TestCase):
    """Test MCP server integration and error handling."""
    
    @patch('mcp_server.database_server.db_manager')
    def test_database_connection_error_handling(self, mock_db_manager):
        """Test that database connection errors are handled gracefully."""
        # Mock database manager to raise an exception
        mock_db_manager.execute_query.side_effect = Exception("Database connection failed")
        
        # Test that the tool function handles errors gracefully
        try:
            result = mcp.get_customer_by_id(1)
            # If we get here, the function should return an error message
            self.assertIsInstance(result, dict)
            self.assertIn("error", result)
        except Exception as e:
            # The function should not raise exceptions
            self.fail(f"Tool function should handle database errors gracefully: {e}")
    
    def test_tool_parameter_validation(self):
        """Test that tool functions validate their parameters."""
        # Test with invalid customer ID
        result = mcp.get_customer_by_id("invalid_id")
        self.assertIsInstance(result, dict)
        
        # Test with missing required parameters
        result = mcp.add_transaction(
            customer_id=1,
            amount="invalid_amount",
            category="Food",
            description="Test",
            date="2025-08-26"
        )
        self.assertIsInstance(result, dict)


if __name__ == '__main__':
    unittest.main()
