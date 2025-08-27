"""Database utility functions for the Financial Advisor app."""

import mysql.connector
from mysql.connector import Error
from typing import Dict, List, Any, Optional, Tuple
import logging

from src.utils.config import DB_CONFIG

def get_connection():
    """Create and return a connection to the database.
    
    Returns:
        mysql.connector.connection.MySQLConnection: Database connection
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        logging.error(f"Error connecting to MySQL database: {e}")
        raise

def execute_query(query: str, params: Tuple = None) -> bool:
    """Execute a query that doesn't return data.
    
    Args:
        query (str): SQL query to execute
        params (tuple, optional): Parameters for the query
        
    Returns:
        bool: True if successful, False otherwise
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
        return True
    except Error as e:
        logging.error(f"Error executing query: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def fetch_data(query: str, params: Tuple = None) -> List[Dict[str, Any]]:
    """Execute a query and return the results as a list of dictionaries.
    
    Args:
        query (str): SQL query to execute
        params (tuple, optional): Parameters for the query
        
    Returns:
        List[Dict[str, Any]]: Query results
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        logging.error(f"Error fetching data: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def fetch_one(query: str, params: Tuple = None) -> Optional[Dict[str, Any]]:
    """Execute a query and return a single result as a dictionary.
    
    Args:
        query (str): SQL query to execute
        params (tuple, optional): Parameters for the query
        
    Returns:
        Optional[Dict[str, Any]]: Query result or None if no result
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchone()
    except Error as e:
        logging.error(f"Error fetching data: {e}")
        return None
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def insert_data(table: str, data: Dict[str, Any]) -> Optional[int]:
    """Insert data into a table and return the ID of the inserted row.
    
    Args:
        table (str): Table name
        data (Dict[str, Any]): Data to insert
        
    Returns:
        Optional[int]: ID of the inserted row, or None if insert failed
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        cursor.execute(query, list(data.values()))
        connection.commit()
        
        return cursor.lastrowid
    except Error as e:
        logging.error(f"Error inserting data: {e}")
        return None
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def update_data(table: str, data: Dict[str, Any], condition: str, params: Tuple) -> bool:
    """Update data in a table.
    
    Args:
        table (str): Table name
        data (Dict[str, Any]): Data to update
        condition (str): WHERE condition
        params (Tuple): Parameters for the condition
        
    Returns:
        bool: True if successful, False otherwise
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        
        # Combine data values and condition params
        all_params = list(data.values()) + list(params)
        
        cursor.execute(query, all_params)
        connection.commit()
        
        return True
    except Error as e:
        logging.error(f"Error updating data: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def delete_data(table: str, condition: str, params: Tuple) -> bool:
    """Delete data from a table.
    
    Args:
        table (str): Table name
        condition (str): WHERE condition
        params (Tuple): Parameters for the condition
        
    Returns:
        bool: True if successful, False otherwise
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        query = f"DELETE FROM {table} WHERE {condition}"
        cursor.execute(query, params)
        connection.commit()
        
        return True
    except Error as e:
        logging.error(f"Error deleting data: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
