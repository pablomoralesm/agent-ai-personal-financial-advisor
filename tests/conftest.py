"""
Pytest configuration and common fixtures for the Personal Financial Advisor tests.

This file provides shared test fixtures and configuration that can be used
across all test modules.
"""

import pytest
import os
import sys
import tempfile
import logging
from unittest.mock import Mock, patch

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


@pytest.fixture(scope="session")
def project_root_path():
    """Provide the project root path for tests."""
    return project_root


@pytest.fixture(scope="session")
def test_data_dir():
    """Provide a temporary directory for test data."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture(scope="function")
def mock_db_connection():
    """Provide a mock database connection for testing."""
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor


@pytest.fixture(scope="function")
def mock_mcp_server_path():
    """Provide a mock MCP server path for testing."""
    return "/mock/path/to/mcp_server.py"


@pytest.fixture(scope="function")
def sample_customer_data():
    """Provide sample customer data for testing."""
    return {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
        "income": 75000
    }


@pytest.fixture(scope="function")
def sample_transaction_data():
    """Provide sample transaction data for testing."""
    return {
        "customer_id": 1,
        "amount": 150.50,
        "category": "Food",
        "description": "Grocery shopping",
        "date": "2025-08-26"
    }


@pytest.fixture(scope="function")
def sample_goal_data():
    """Provide sample financial goal data for testing."""
    return {
        "customer_id": 1,
        "goal_type": "savings",
        "target_amount": 10000,
        "current_amount": 2500,
        "target_date": "2026-12-31"
    }


@pytest.fixture(scope="function")
def mock_google_adk_components():
    """Mock Google ADK components for testing."""
    with patch('agents.spending_analyzer.LlmAgent') as mock_llm, \
         patch('agents.spending_analyzer.MCPToolset') as mock_mcp, \
         patch('agents.spending_analyzer.StdioServerParameters') as mock_stdio:
        
        yield {
            'LlmAgent': mock_llm,
            'MCPToolset': mock_mcp,
            'StdioServerParameters': mock_stdio
        }


@pytest.fixture(scope="function")
def setup_logging_for_tests():
    """Setup logging for test execution."""
    # Clear existing handlers
    logging.getLogger().handlers.clear()
    
    # Setup basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    yield
    
    # Cleanup
    logging.getLogger().handlers.clear()


@pytest.fixture(scope="function")
def mock_environment_variables():
    """Mock environment variables for testing."""
    test_env = {
        'GOOGLE_API_KEY': 'test_api_key_12345',
        'DB_HOST': 'localhost',
        'DB_PORT': '3306',
        'DB_NAME': 'test_financial_advisor',
        'DB_USER': 'test_user',
        'DB_PASSWORD': 'test_password',
        'APP_DEBUG': 'True',
        'APP_LOG_LEVEL': 'INFO'
    }
    
    with patch.dict(os.environ, test_env):
        yield test_env


def pytest_configure(config):
    """Configure pytest with custom markers and options."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on their names."""
    for item in items:
        # Mark tests based on naming conventions
        if "test_agent" in item.name.lower():
            item.add_marker(pytest.mark.unit)
        elif "test_mcp" in item.name.lower():
            item.add_marker(pytest.mark.integration)
        elif "test_ui" in item.name.lower():
            item.add_marker(pytest.mark.integration)
        else:
            item.add_marker(pytest.mark.unit)


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Automatically setup test environment for each test."""
    # Ensure we're in a clean state
    original_cwd = os.getcwd()
    
    yield
    
    # Cleanup after test
    os.chdir(original_cwd)
