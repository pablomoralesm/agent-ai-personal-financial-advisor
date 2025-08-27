"""
Database utilities for the Financial Advisor application.

Provides shared database connection and configuration utilities.
"""

import os
import logging
from typing import Dict, Any
import mysql.connector
from mysql.connector import Error
import dotenv

# Load environment variables
dotenv.load_dotenv()

logger = logging.getLogger(__name__)

def get_db_config() -> Dict[str, Any]:
    """
    Get database configuration from environment variables.
    
    Returns:
        Dictionary containing database configuration
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

def test_database_connection() -> bool:
    """
    Test database connection.
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        config = get_db_config()
        connection = mysql.connector.connect(**config)
        connection.close()
        logger.info("Database connection test successful")
        return True
    except Error as e:
        logger.error(f"Database connection test failed: {e}")
        return False

def create_database_if_not_exists() -> bool:
    """
    Create the database if it doesn't exist.
    
    Returns:
        True if database exists or was created successfully, False otherwise
    """
    try:
        config = get_db_config()
        db_name = config.pop('database')
        
        # Connect without specifying database
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.execute(f"USE {db_name}")
        
        cursor.close()
        connection.close()
        
        logger.info(f"Database '{db_name}' is ready")
        return True
        
    except Error as e:
        logger.error(f"Error creating database: {e}")
        return False
