"""
Shared configuration for MCP Database Servers.

This module provides centralized configuration management for database connections,
logging, and other shared settings used by both server implementations.
"""

import os
import logging
from typing import Dict, Any
import dotenv

# Load environment variables
dotenv.load_dotenv()


def get_database_config() -> Dict[str, Any]:
    """
    Get database configuration from environment variables.
    
    Returns:
        Dictionary containing database connection parameters
    """
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': int(os.getenv('DB_PORT', 3306)),
        'database': os.getenv('DB_NAME', 'financial_advisor'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'autocommit': True,
        'charset': 'utf8mb4'
    }


def setup_logging(level: str = 'INFO', format_string: str = None) -> logging.Logger:
    """
    Set up logging configuration for MCP servers.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Custom log format string
        
    Returns:
        Configured logger instance
    """
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=format_string
    )
    
    return logging.getLogger(__name__)


def get_server_config() -> Dict[str, Any]:
    """
    Get general server configuration.
    
    Returns:
        Dictionary containing server configuration parameters
    """
    return {
        'server_name': 'Financial Advisor Database Server',
        'max_connections': int(os.getenv('MAX_DB_CONNECTIONS', 10)),
        'connection_timeout': int(os.getenv('DB_TIMEOUT', 30)),
        'log_level': os.getenv('LOG_LEVEL', 'INFO')
    }
