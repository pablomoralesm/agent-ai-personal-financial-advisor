"""
Database Client for UI Components

Provides direct database access functions for UI components,
bypassing the MCP layer since UI components don't need to go through agents.
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime, date
from typing import List, Dict, Any, Optional
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'database': os.getenv('DB_NAME', 'financial_advisor'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'autocommit': True,
    'charset': 'utf8mb4'
}

class DatabaseClient:
    """Database client for UI components."""
    
    def __init__(self):
        self.config = DB_CONFIG
    
    def get_connection(self):
        """Get a database connection."""
        try:
            return mysql.connector.connect(**self.config)
        except Error as e:
            logger.error(f"Database connection error: {e}")
            raise
    
    def execute_query(self, query: str, params: tuple = None, fetch_all: bool = True):
        """Execute a query with proper error handling."""
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

# Global database client instance
db_client = DatabaseClient()

def get_customer_profile(customer_id: int) -> Dict[str, Any]:
    """Get customer profile from database."""
    try:
        query = """
        SELECT id, name, email, phone, age, monthly_income, credit_score, 
               created_at, updated_at
        FROM customers 
        WHERE id = %s
        """
        result = db_client.execute_query(query, (customer_id,), fetch_all=False)
        return result if result else {}
    except Exception as e:
        logger.error(f"Error getting customer profile: {e}")
        return {}

def get_transactions_by_customer(customer_id: int, limit: int = 100) -> List[Dict[str, Any]]:
    """Get transactions for a customer."""
    try:
        query = """
        SELECT id, customer_id, amount, category, subcategory, description,
               transaction_date, transaction_type, payment_method, created_at
        FROM transactions 
        WHERE customer_id = %s 
        ORDER BY transaction_date DESC 
        LIMIT %s
        """
        result = db_client.execute_query(query, (customer_id, limit))
        return result if result else []
    except Exception as e:
        logger.error(f"Error getting transactions: {e}")
        return []

def add_transaction(
    customer_id: int,
    amount: float,
    category: str,
    transaction_date: str,
    transaction_type: str,
    subcategory: Optional[str] = None,
    description: Optional[str] = None,
    payment_method: Optional[str] = None
) -> bool:
    """Add a new transaction to database."""
    try:
        query = """
        INSERT INTO transactions 
        (customer_id, amount, category, subcategory, description, 
         transaction_date, transaction_type, payment_method, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            customer_id, amount, category, subcategory, description,
            transaction_date, transaction_type, payment_method, datetime.now()
        )
        
        result = db_client.execute_query(query, params, fetch_all=False)
        return result > 0
    except Exception as e:
        logger.error(f"Error adding transaction: {e}")
        return False

def get_financial_goals(customer_id: int) -> List[Dict[str, Any]]:
    """Get financial goals for a customer."""
    try:
        query = """
        SELECT id, customer_id, goal_name, goal_type, target_amount, 
               current_amount, target_date, priority, description, 
               status, created_at, updated_at
        FROM financial_goals 
        WHERE customer_id = %s 
        ORDER BY priority DESC, created_at DESC
        """
        result = db_client.execute_query(query, (customer_id,))
        return result if result else []
    except Exception as e:
        logger.error(f"Error getting financial goals: {e}")
        return []

def create_financial_goal(
    customer_id: int,
    goal_name: str,
    goal_type: str,
    target_amount: float,
    current_amount: float,
    target_date: str,
    priority: str,
    description: Optional[str] = None
) -> bool:
    """Create a new financial goal."""
    try:
        query = """
        INSERT INTO financial_goals 
        (customer_id, goal_name, goal_type, target_amount, current_amount,
         target_date, priority, description, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            customer_id, goal_name, goal_type, target_amount, current_amount,
            target_date, priority, description, 'active', datetime.now(), datetime.now()
        )
        
        result = db_client.execute_query(query, params, fetch_all=False)
        return result > 0
    except Exception as e:
        logger.error(f"Error creating financial goal: {e}")
        return False

def update_goal_progress(goal_id: int, current_amount: float) -> bool:
    """Update goal progress."""
    try:
        query = """
        UPDATE financial_goals 
        SET current_amount = %s, updated_at = %s
        WHERE id = %s
        """
        params = (current_amount, datetime.now(), goal_id)
        
        result = db_client.execute_query(query, params, fetch_all=False)
        return result > 0
    except Exception as e:
        logger.error(f"Error updating goal progress: {e}")
        return False

def get_advice_history(customer_id: int) -> List[Dict[str, Any]]:
    """Get advice history for a customer."""
    try:
        query = """
        SELECT id, customer_id, advice_type, advice_content, agent_name,
               confidence_score, created_at
        FROM advice_history 
        WHERE customer_id = %s 
        ORDER BY created_at DESC
        """
        result = db_client.execute_query(query, (customer_id,))
        
        if not result:
            logger.info(f"No advice history found for customer {customer_id}")
            return []
        
        # Convert datetime objects to ISO format strings for JSON serialization
        for record in result:
            if record.get('created_at'):
                if hasattr(record['created_at'], 'isoformat'):
                    record['created_at'] = record['created_at'].isoformat()
                else:
                    record['created_at'] = str(record['created_at'])
            
            # Convert confidence_score to float if it exists
            if record.get('confidence_score') is not None:
                record['confidence_score'] = float(record['confidence_score'])
            
            # Ensure advice_content is a string
            if record.get('advice_content') is None:
                record['advice_content'] = ""
        
        logger.info(f"Retrieved {len(result)} advice records for customer {customer_id}")
        return result
        
    except Exception as e:
        logger.error(f"Error getting advice history for customer {customer_id}: {e}")
        return []

def save_advice(
    customer_id: int,
    advice_type: str,
    advice_content: str,
    agent_name: str,
    confidence_score: float
) -> bool:
    """Save advice to database."""
    try:
        query = """
        INSERT INTO advice_history 
        (customer_id, advice_type, advice_content, agent_name, 
         confidence_score, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            customer_id, advice_type, advice_content, agent_name,
            confidence_score, datetime.now()
        )
        
        result = db_client.execute_query(query, params, fetch_all=False)
        return result > 0
    except Exception as e:
        logger.error(f"Error saving advice: {e}")
        return False

def get_spending_summary(customer_id: int) -> Dict[str, Any]:
    """Get spending summary for a customer."""
    try:
        # Get current month spending by category
        current_month = datetime.now().strftime('%Y-%m')
        query = """
        SELECT category, SUM(amount) as total_amount
        FROM transactions
        WHERE customer_id = %s
        AND transaction_type = 'expense'
        AND DATE_FORMAT(transaction_date, '%%Y-%%m') = %s
        GROUP BY category
        ORDER BY total_amount DESC
        """
        result = db_client.execute_query(query, (customer_id, current_month))

        # Calculate total expenses
        total_query = """
        SELECT SUM(amount) as total_expenses
        FROM transactions
        WHERE customer_id = %s
        AND transaction_type = 'expense'
        AND DATE_FORMAT(transaction_date, '%%Y-%%m') = %s
        """
        total_result = db_client.execute_query(total_query, (customer_id, current_month), fetch_all=False)
        total_expenses = total_result['total_expenses'] if total_result else 0

        return {
            'categories': result if result else [],
            'total_expenses': total_expenses,
            'month': current_month
        }
    except Exception as e:
        logger.error(f"Error getting spending summary: {e}")
        return {'categories': [], 'total_expenses': 0, 'month': ''}

def get_all_customers() -> List[Dict[str, Any]]:
    """Get all customers from database."""
    try:
        query = """
        SELECT id, name, email, phone, age, monthly_income, credit_score,
               created_at, updated_at
        FROM customers
        ORDER BY name ASC
        """
        result = db_client.execute_query(query)
        return result if result else []
    except Exception as e:
        logger.error(f"Error getting all customers: {e}")
        return []

def clear_old_advice_records(customer_id: int, days_old: int = 30) -> bool:
    """Clear advice records older than specified days."""
    try:
        query = """
        DELETE FROM advice_history 
        WHERE customer_id = %s 
        AND created_at < DATE_SUB(NOW(), INTERVAL %s DAY)
        """
        result = db_client.execute_query(query, (customer_id, days_old), fetch_all=False)
        logger.info(f"Cleared {result} old advice records for customer {customer_id}")
        return result > 0
    except Exception as e:
        logger.error(f"Error clearing old advice records: {e}")
        return False

def clear_all_advice_records(customer_id: int) -> bool:
    """Clear all advice records for a customer."""
    try:
        query = "DELETE FROM advice_history WHERE customer_id = %s"
        result = db_client.execute_query(query, (customer_id,), fetch_all=False)
        logger.info(f"Cleared all {result} advice records for customer {customer_id}")
        return True
    except Exception as e:
        logger.error(f"Error clearing all advice records: {e}")
        return False
