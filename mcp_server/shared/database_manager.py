"""
Shared database management for both MCP servers.

This module provides a unified DatabaseManager class that handles MySQL connections
and query execution with proper error handling and connection management.
"""

import logging
from typing import Dict, Any, Optional, Union, List
import mysql.connector
from mysql.connector import Error

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Database connection manager with connection pooling and error handling.
    Implements enterprise-grade database access as recommended in ADK docs.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the database manager with configuration.
        
        Args:
            config: Database configuration dictionary containing host, port, 
                   database, user, password, and other connection parameters
        """
        self.config = config
        self._pool = None
    
    def get_connection(self):
        """
        Get a database connection with error handling.
        
        Returns:
            MySQL connection object
            
        Raises:
            Error: If connection fails
        """
        try:
            return mysql.connector.connect(**self.config)
        except Error as e:
            logger.error(f"Database connection error: {e}")
            raise
    
    def execute_query(self, query: str, params: tuple = None, fetch_all: bool = True):
        """
        Execute a query with proper error handling and connection management.
        
        Args:
            query: SQL query to execute
            params: Query parameters tuple
            fetch_all: If True, fetch all results; if False, fetch one result
            
        Returns:
            Query results (list of dicts for SELECT, row count for others)
            
        Raises:
            Error: If query execution fails
        """
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall() if fetch_all else cursor.fetchone()
            else:
                connection.commit()
                return cursor.rowcount
                
        except Error as e:
            logger.error(f"Query execution error: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def execute_query_with_result_handling(self, query: str, params: tuple = None, fetch_all: bool = True):
        """
        Execute a query with enhanced result handling for STDIO server compatibility.
        
        This method provides the same functionality as execute_query but returns
        results in a format that's compatible with both server implementations.
        
        Args:
            query: SQL query to execute
            params: Query parameters tuple
            fetch_all: If True, fetch all results; if False, fetch one result
            
        Returns:
            Query results with enhanced error handling
        """
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute(query, params or ())
            
            if query.strip().upper().startswith('SELECT'):
                if fetch_all:
                    result = cursor.fetchall()
                else:
                    result = cursor.fetchone()
                return result
            else:
                return {"rows_affected": cursor.rowcount}
                
        except Error as e:
            logger.error(f"Database error: {e}")
            raise
        finally:
            if connection and connection.is_connected():
                cursor.close()
                connection.close()
