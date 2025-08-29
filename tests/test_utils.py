"""
Tests for utility functions in the Personal Financial Advisor application.

This module tests:
- Database connection utilities
- Logging configuration
- Data formatting utilities
- Plotting utilities
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import os
import sys
import tempfile
import logging

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from utils.database import get_db_config, test_database_connection, create_database_if_not_exists
from utils.logging_config import setup_logging, get_logger


class TestDatabaseUtils(unittest.TestCase):
    """Test database utility functions."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_db_config = {
            'host': 'localhost',
            'port': 3306,
            'user': 'test_user',
            'password': 'test_password',
            'database': 'test_db'
        }
    
    @patch('utils.database.mysql.connector.connect')
    def test_get_db_config(self, mock_connect):
        """Test database configuration retrieval."""
        # Test that config is returned with expected structure
        config = get_db_config()
        
        # Verify config has all required keys
        required_keys = ['host', 'port', 'database', 'user', 'password', 'autocommit', 'charset']
        for key in required_keys:
            self.assertIn(key, config)
        
        # Verify port is an integer
        self.assertIsInstance(config['port'], int)
    
    @patch('utils.database.mysql.connector.connect')
    def test_test_database_connection_success(self, mock_connect):
        """Test successful database connection test."""
        # Mock successful connection
        mock_connection = Mock()
        mock_connect.return_value = mock_connection
        
        # Test connection
        result = test_database_connection()
        
        # Verify connection was established
        mock_connect.assert_called_once()
        
        # Verify connection was closed
        mock_connection.close.assert_called_once()
        
        # Verify result indicates success
        self.assertTrue(result)
    
    @patch('utils.database.mysql.connector.connect')
    def test_test_database_connection_failure(self, mock_connect):
        """Test database connection test failure handling."""
        # Mock connection failure
        mock_connect.side_effect = Exception("Connection failed")
        
        # Test connection
        result = test_database_connection()
        
        # Verify result indicates failure
        self.assertFalse(result)
    
    @patch('utils.database.mysql.connector.connect')
    def test_create_database_if_not_exists(self, mock_connect):
        """Test database creation function."""
        # Mock connection
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        
        mock_connect.return_value = mock_connection
        
        # Test database creation
        result = create_database_if_not_exists()
        
        # Verify connection was established
        mock_connect.assert_called()
        
        # Verify cursor was used
        mock_connection.cursor.assert_called()
        
        # Verify result indicates success
        self.assertTrue(result)


class TestLoggingConfig(unittest.TestCase):
    """Test logging configuration utilities."""
    
    def setUp(self):
        """Set up test environment."""
        # Clear any existing loggers
        logging.getLogger().handlers.clear()
    
    def test_setup_logging(self):
        """Test logging setup function."""
        # Test logging setup
        setup_logging()
        
        # Verify root logger has handlers
        root_logger = logging.getLogger()
        self.assertTrue(len(root_logger.handlers) > 0)
        
        # Verify log level is set
        self.assertGreaterEqual(root_logger.level, logging.INFO)
    
    def test_get_logger(self):
        """Test logger retrieval function."""
        # Setup logging first
        setup_logging()
        
        # Get a logger
        logger = get_logger(__name__)
        
        # Verify logger is properly configured
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, __name__)
        
        # Verify logger has handlers
        self.assertTrue(len(logger.handlers) > 0)
    
    def test_logger_levels(self):
        """Test that loggers respect configured levels."""
        # Setup logging with INFO level
        setup_logging()
        
        # Get logger
        logger = get_logger(__name__)
        
        # Test that DEBUG messages are not logged at INFO level
        with self.assertLogs(logger, level='INFO') as log_context:
            logger.debug("This debug message should not appear")
            logger.info("This info message should appear")
        
        # Verify only INFO message was logged
        self.assertEqual(len(log_context.records), 1)
        self.assertEqual(log_context.records[0].levelname, 'INFO')


class TestUIUtils(unittest.TestCase):
    """Test UI utility functions."""
    
    def test_formatting_utilities_import(self):
        """Test that UI formatting utilities can be imported."""
        try:
            from ui.utils.formatting import format_currency, format_date
            self.assertTrue(callable(format_currency))
            self.assertTrue(callable(format_date))
        except ImportError as e:
            self.fail(f"Failed to import UI formatting utilities: {e}")
    
    def test_plotting_utilities_import(self):
        """Test that UI plotting utilities can be imported."""
        try:
            from ui.utils.plotting import create_spending_chart, create_goal_progress_chart
            self.assertTrue(callable(create_spending_chart))
            self.assertTrue(callable(create_goal_progress_chart))
        except ImportError as e:
            self.fail(f"Failed to import UI plotting utilities: {e}")


class TestEnvironmentConfiguration(unittest.TestCase):
    """Test environment and configuration handling."""
    
    def test_environment_variables_handling(self):
        """Test that environment variables are properly handled."""
        # Test that the application can handle missing environment variables
        # without crashing
        try:
            # This should not raise an exception even if .env is missing
            from dotenv import load_dotenv
            load_dotenv()
        except Exception as e:
            self.fail(f"Environment loading should be graceful: {e}")
    
    def test_configuration_imports(self):
        """Test that configuration modules can be imported."""
        try:
            # Test that we can import the main configuration
            import os
            from dotenv import load_dotenv
            
            # Load environment variables
            load_dotenv()
            
            # Test that we can access configuration
            api_key = os.getenv('GOOGLE_API_KEY')
            db_host = os.getenv('DB_HOST')
            
            # These might be None in test environment, but shouldn't crash
            self.assertIsInstance(api_key, (str, type(None)))
            self.assertIsInstance(db_host, (str, type(None)))
            
        except Exception as e:
            self.fail(f"Configuration handling should not crash: {e}")


if __name__ == '__main__':
    unittest.main()
