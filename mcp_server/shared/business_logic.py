"""
Shared business logic functions for MCP Database Servers.

This module contains all the business logic functions that are shared between
the standalone FastMCP server and the ADK-integrated STDIO server.
"""

import json
import logging
from datetime import datetime, date
from decimal import Decimal
from typing import Dict, Any, List, Optional, Union

from .database_manager import DatabaseManager

logger = logging.getLogger(__name__)


# ============================================================================
# CUSTOMER MANAGEMENT FUNCTIONS
# ============================================================================

def get_customer_profile(customer_id: int, db_manager: DatabaseManager) -> Dict[str, Any]:
    """
    Retrieve complete customer profile information.
    
    Args:
        customer_id: The ID of the customer to retrieve
        db_manager: Database manager instance
        
    Returns:
        Dictionary containing customer profile data
    """
    try:
        query = """
        SELECT id, name, email, phone, date_of_birth, created_at, updated_at
        FROM customers 
        WHERE id = %s
        """
        result = db_manager.execute_query(query, (customer_id,), fetch_all=False)
        
        if not result:
            return {"error": f"Customer with ID {customer_id} not found"}
        
        # Convert datetime objects to strings for JSON serialization
        if result.get('date_of_birth'):
            result['date_of_birth'] = result['date_of_birth'].isoformat()
        if result.get('created_at'):
            result['created_at'] = result['created_at'].isoformat()
        if result.get('updated_at'):
            result['updated_at'] = result['updated_at'].isoformat()
            
        return result
        
    except Exception as e:
        logger.error(f"Error retrieving customer profile: {e}")
        return {"error": str(e)}


def create_customer(name: str, email: str, phone: str = None, date_of_birth: str = None, 
                   db_manager: DatabaseManager = None) -> Dict[str, Any]:
    """
    Create a new customer profile.
    
    Args:
        name: Customer's full name
        email: Customer's email address
        phone: Optional phone number
        date_of_birth: Optional date of birth in YYYY-MM-DD format
        db_manager: Database manager instance
        
    Returns:
        Dictionary containing the created customer's information
    """
    try:
        # Parse date if provided
        dob = None
        if date_of_birth:
            try:
                dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            except ValueError:
                return {"error": "Invalid date format. Use YYYY-MM-DD"}
        
        query = """
        INSERT INTO customers (name, email, phone, date_of_birth)
        VALUES (%s, %s, %s, %s)
        """
        
        db_manager.execute_query(query, (name, email, phone, dob))
        
        # Get the created customer
        get_query = "SELECT * FROM customers WHERE email = %s ORDER BY id DESC LIMIT 1"
        result = db_manager.execute_query(get_query, (email,), fetch_all=False)
        
        # Convert datetime objects for JSON serialization
        if result.get('date_of_birth'):
            result['date_of_birth'] = result['date_of_birth'].isoformat()
        if result.get('created_at'):
            result['created_at'] = result['created_at'].isoformat()
        if result.get('updated_at'):
            result['updated_at'] = result['updated_at'].isoformat()
            
        return {"success": True, "customer": result}
        
    except Exception as e:
        logger.error(f"Error creating customer: {e}")
        return {"error": str(e)}


# ============================================================================
# TRANSACTION MANAGEMENT FUNCTIONS
# ============================================================================

def add_transaction(
    customer_id: int,
    amount: float,
    category: str,
    transaction_date: str,
    transaction_type: str,
    subcategory: str = None,
    description: str = None,
    payment_method: str = None,
    db_manager: DatabaseManager = None
) -> Dict[str, Any]:
    """
    Add a new financial transaction for a customer.
    
    Args:
        customer_id: ID of the customer
        amount: Transaction amount (positive for income, expenses)
        category: Transaction category
        transaction_date: Date in YYYY-MM-DD format
        transaction_type: 'income' or 'expense'
        subcategory: Optional subcategory
        description: Optional description
        payment_method: Optional payment method
        db_manager: Database manager instance
        
    Returns:
        Dictionary containing transaction creation result
    """
    try:
        # Validate transaction type
        if transaction_type not in ['income', 'expense']:
            return {"error": "transaction_type must be 'income' or 'expense'"}
        
        # Parse date
        try:
            trans_date = datetime.strptime(transaction_date, '%Y-%m-%d').date()
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD"}
        
        # Validate amount
        if amount <= 0:
            return {"error": "Amount must be positive"}
        
        query = """
        INSERT INTO transactions (customer_id, amount, category, subcategory, 
                                description, transaction_date, transaction_type, payment_method)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        db_manager.execute_query(query, (
            customer_id, amount, category, subcategory, 
            description, trans_date, transaction_type, payment_method
        ))
        
        return {"success": True, "message": "Transaction added successfully"}
        
    except Exception as e:
        logger.error(f"Error adding transaction: {e}")
        return {"error": str(e)}


def get_transactions_by_customer(
    customer_id: int,
    start_date: str = None,
    end_date: str = None,
    category: str = None,
    transaction_type: str = None,
    limit: int = 100,
    months: int = None,
    db_manager: DatabaseManager = None
) -> Dict[str, Any]:
    """
    Retrieve transactions for a customer with optional filtering.
    
    Args:
        customer_id: ID of the customer
        start_date: Optional start date filter (YYYY-MM-DD)
        end_date: Optional end date filter (YYYY-MM-DD)
        category: Optional category filter
        transaction_type: Optional type filter ('income' or 'expense')
        limit: Maximum number of transactions to return (default 100)
        months: Optional months filter (alternative to start_date/end_date)
        db_manager: Database manager instance
        
    Returns:
        Dictionary containing list of transactions
    """
    try:
        # Build dynamic query based on filters
        query = """
        SELECT id, customer_id, amount, category, subcategory, description,
               transaction_date, transaction_type, payment_method, created_at
        FROM transactions 
        WHERE customer_id = %s
        """
        params = [customer_id]
        
        # Handle months filter (for STDIO compatibility)
        if months and not start_date and not end_date:
            query += " AND transaction_date >= DATE_SUB(CURDATE(), INTERVAL %s MONTH)"
            params.append(months)
        else:
            if start_date:
                query += " AND transaction_date >= %s"
                params.append(start_date)
            
            if end_date:
                query += " AND transaction_date <= %s"
                params.append(end_date)
        
        if category:
            query += " AND category = %s"
            params.append(category)
            
        if transaction_type:
            query += " AND transaction_type = %s"
            params.append(transaction_type)
        
        query += " ORDER BY transaction_date DESC LIMIT %s"
        params.append(limit)
        
        results = db_manager.execute_query(query, tuple(params))
        
        # Convert dates for JSON serialization
        for result in results:
            if result.get('transaction_date'):
                result['transaction_date'] = result['transaction_date'].isoformat()
            if result.get('created_at'):
                result['created_at'] = result['created_at'].isoformat()
            # Convert Decimal to float for JSON serialization
            if result.get('amount'):
                result['amount'] = float(result['amount'])
        
        return {"success": True, "transactions": results, "count": len(results)}
        
    except Exception as e:
        logger.error(f"Error retrieving transactions: {e}")
        return {"error": str(e)}


def get_spending_summary(customer_id: int, months: int = 6, db_manager: DatabaseManager = None) -> Dict[str, Any]:
    """
    Get spending summary and analysis for a customer over specified months.
    
    Args:
        customer_id: ID of the customer
        months: Number of months to analyze (default 6)
        db_manager: Database manager instance
        
    Returns:
        Dictionary containing spending analysis data
    """
    try:
        # Get spending by category
        category_query = """
        SELECT category, 
               SUM(amount) as total_amount,
               COUNT(*) as transaction_count,
               AVG(amount) as avg_amount
        FROM transactions 
        WHERE customer_id = %s 
          AND transaction_type = 'expense'
          AND transaction_date >= DATE_SUB(CURDATE(), INTERVAL %s MONTH)
        GROUP BY category
        ORDER BY total_amount DESC
        """
        
        categories = db_manager.execute_query(category_query, (customer_id, months))
        
        # Get monthly totals
        monthly_query = """
        SELECT DATE_FORMAT(transaction_date, '%%Y-%%m') as month,
               SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END) as income,
               SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) as expenses
        FROM transactions 
        WHERE customer_id = %s
          AND transaction_date >= DATE_SUB(CURDATE(), INTERVAL %s MONTH)
        GROUP BY DATE_FORMAT(transaction_date, '%%Y-%%m')
        ORDER BY month DESC
        """
        
        monthly = db_manager.execute_query(monthly_query, (customer_id, months))
        
        # Convert Decimal to float for JSON serialization
        for cat in categories:
            cat['total_amount'] = float(cat['total_amount'])
            cat['avg_amount'] = float(cat['avg_amount'])
            
        for month in monthly:
            month['income'] = float(month['income'])
            month['expenses'] = float(month['expenses'])
            month['net'] = month['income'] - month['expenses']
        
        # Calculate totals
        total_income = sum(m['income'] for m in monthly)
        total_expenses = sum(m['expenses'] for m in monthly)
        
        return {
            "success": True,
            "period_months": months,
            "categories": categories,
            "monthly_summary": monthly,
            "totals": {
                "income": total_income,
                "expenses": total_expenses,
                "net": total_income - total_expenses,
                "avg_monthly_income": total_income / len(monthly) if monthly else 0,
                "avg_monthly_expenses": total_expenses / len(monthly) if monthly else 0
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting spending summary: {e}")
        return {"error": str(e)}


# ============================================================================
# FINANCIAL GOALS MANAGEMENT FUNCTIONS
# ============================================================================

def create_financial_goal(
    customer_id: int,
    goal_name: str,
    goal_type: str,
    target_amount: float,
    target_date: str = None,
    priority: str = 'medium',
    description: str = None,
    db_manager: DatabaseManager = None
) -> Dict[str, Any]:
    """
    Create a new financial goal for a customer.
    
    Args:
        customer_id: ID of the customer
        goal_name: Name of the financial goal
        goal_type: Type of goal (savings, investment, debt_payoff, purchase)
        target_amount: Target amount for the goal
        target_date: Optional target date (YYYY-MM-DD)
        priority: Priority level (low, medium, high)
        description: Optional description
        db_manager: Database manager instance
        
    Returns:
        Dictionary containing goal creation result
    """
    try:
        # Validate goal type
        valid_types = ['savings', 'investment', 'debt_payoff', 'purchase']
        if goal_type not in valid_types:
            return {"error": f"goal_type must be one of: {', '.join(valid_types)}"}
        
        # Validate priority
        if priority not in ['low', 'medium', 'high']:
            return {"error": "priority must be 'low', 'medium', or 'high'"}
        
        # Parse target date if provided
        parsed_date = None
        if target_date:
            try:
                parsed_date = datetime.strptime(target_date, '%Y-%m-%d').date()
            except ValueError:
                return {"error": "Invalid date format. Use YYYY-MM-DD"}
        
        query = """
        INSERT INTO financial_goals (customer_id, goal_name, goal_type, target_amount,
                                   target_date, priority, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        db_manager.execute_query(query, (
            customer_id, goal_name, goal_type, target_amount,
            parsed_date, priority, description
        ))
        
        return {"success": True, "message": "Financial goal created successfully"}
        
    except Exception as e:
        logger.error(f"Error creating financial goal: {e}")
        return {"error": str(e)}


def get_financial_goals(customer_id: int, status: str = None, db_manager: DatabaseManager = None) -> Dict[str, Any]:
    """
    Retrieve financial goals for a customer.
    
    Args:
        customer_id: ID of the customer
        status: Optional status filter (active, completed, paused, cancelled)
        db_manager: Database manager instance
        
    Returns:
        Dictionary containing list of financial goals
    """
    try:
        query = """
        SELECT id, customer_id, goal_name, goal_type, target_amount, current_amount,
               target_date, priority, status, description, created_at, updated_at
        FROM financial_goals 
        WHERE customer_id = %s
        """
        params = [customer_id]
        
        if status:
            query += " AND status = %s"
            params.append(status)
        
        query += " ORDER BY priority DESC, target_date ASC"
        
        results = db_manager.execute_query(query, tuple(params))
        
        # Convert dates and decimals for JSON serialization
        for result in results:
            if result.get('target_date'):
                result['target_date'] = result['target_date'].isoformat()
            if result.get('created_at'):
                result['created_at'] = result['created_at'].isoformat()
            if result.get('updated_at'):
                result['updated_at'] = result['updated_at'].isoformat()
            if result.get('target_amount'):
                result['target_amount'] = float(result['target_amount'])
            if result.get('current_amount'):
                result['current_amount'] = float(result['current_amount'])
            
            # Calculate progress percentage
            if result['target_amount'] > 0:
                result['progress_percentage'] = (result['current_amount'] / result['target_amount']) * 100
            else:
                result['progress_percentage'] = 0
        
        return {"success": True, "goals": results, "count": len(results)}
        
    except Exception as e:
        logger.error(f"Error retrieving financial goals: {e}")
        return {"error": str(e)}


def update_goal_progress(goal_id: int, current_amount: float, db_manager: DatabaseManager = None) -> Dict[str, Any]:
    """
    Update the current amount for a financial goal.
    
    Args:
        goal_id: ID of the goal to update
        current_amount: New current amount
        db_manager: Database manager instance
        
    Returns:
        Dictionary containing update result
    """
    try:
        query = """
        UPDATE financial_goals 
        SET current_amount = %s, updated_at = NOW()
        WHERE id = %s
        """
        
        rows_affected = db_manager.execute_query(query, (current_amount, goal_id))
        
        if rows_affected == 0:
            return {"error": f"Goal with ID {goal_id} not found"}
        
        # Check if goal is now completed
        check_query = """
        SELECT target_amount, current_amount, status
        FROM financial_goals 
        WHERE id = %s
        """
        
        result = db_manager.execute_query(check_query, (goal_id,), fetch_all=False)
        
        if result and float(result['current_amount']) >= float(result['target_amount']) and result['status'] == 'active':
            # Mark as completed
            complete_query = "UPDATE financial_goals SET status = 'completed' WHERE id = %s"
            db_manager.execute_query(complete_query, (goal_id,))
            return {"success": True, "message": "Goal progress updated and marked as completed!"}
        
        return {"success": True, "message": "Goal progress updated successfully"}
        
    except Exception as e:
        logger.error(f"Error updating goal progress: {e}")
        return {"error": str(e)}


# ============================================================================
# ADVICE HISTORY FUNCTIONS
# ============================================================================

def save_advice(
    customer_id: int,
    agent_name: str,
    advice_type: str,
    advice_content: str,
    confidence_score: float = None,
    metadata: Dict[str, Any] = None,
    db_manager: DatabaseManager = None
) -> Dict[str, Any]:
    """
    Save advice from an agent to the database.
    
    Args:
        customer_id: ID of the customer
        agent_name: Name of the agent providing advice
        advice_type: Type of advice (spending_analysis, goal_planning, general_advice)
        advice_content: The advice content
        confidence_score: Optional confidence score (0.0 to 1.0)
        metadata: Optional metadata dictionary
        db_manager: Database manager instance
        
    Returns:
        Dictionary containing save result
    """
    try:
        # Validate confidence score
        if confidence_score is not None and (confidence_score < 0 or confidence_score > 1):
            return {"error": "confidence_score must be between 0.0 and 1.0"}
        
        query = """
        INSERT INTO advice_history (customer_id, agent_name, advice_type, advice_content,
                                  confidence_score, metadata)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        metadata_json = json.dumps(metadata) if metadata else None
        
        result = db_manager.execute_query(query, (
            customer_id, agent_name, advice_type, advice_content,
            confidence_score, metadata_json
        ))
        
        return {"success": True, "message": "Advice saved successfully"}
        
    except Exception as e:
        logger.error(f"Error saving advice: {e}")
        return {"error": str(e)}


def get_advice_history(
    customer_id: int,
    agent_name: str = None,
    advice_type: str = None,
    limit: int = 50,
    db_manager: DatabaseManager = None
) -> Dict[str, Any]:
    """
    Retrieve advice history for a customer.
    
    Args:
        customer_id: ID of the customer
        agent_name: Optional filter by agent name
        advice_type: Optional filter by advice type
        limit: Maximum number of records to return
        db_manager: Database manager instance
        
    Returns:
        Dictionary containing advice history
    """
    try:
        query = """
        SELECT id, customer_id, agent_name, advice_type, advice_content,
               confidence_score, metadata, created_at
        FROM advice_history 
        WHERE customer_id = %s
        """
        params = [customer_id]
        
        if agent_name:
            query += " AND agent_name = %s"
            params.append(agent_name)
            
        if advice_type:
            query += " AND advice_type = %s"
            params.append(advice_type)
        
        query += " ORDER BY created_at DESC LIMIT %s"
        params.append(limit)
        
        results = db_manager.execute_query(query, tuple(params))
        
        # Convert dates and parse metadata for JSON serialization
        for result in results:
            if result.get('created_at'):
                result['created_at'] = result['created_at'].isoformat()
            if result.get('confidence_score'):
                result['confidence_score'] = float(result['confidence_score'])
            if result.get('metadata'):
                try:
                    result['metadata'] = json.loads(result['metadata'])
                except (json.JSONDecodeError, TypeError):
                    result['metadata'] = None
        
        return {"success": True, "advice_history": results, "count": len(results)}
        
    except Exception as e:
        logger.error(f"Error retrieving advice history: {e}")
        return {"error": str(e)}


# ============================================================================
# AGENT INTERACTION LOGGING FUNCTIONS
# ============================================================================

def log_agent_interaction(
    session_id: str,
    from_agent: str,
    interaction_type: str,
    message_content: str,
    customer_id: int = None,
    to_agent: str = None,
    context_data: Dict[str, Any] = None,
    db_manager: DatabaseManager = None
) -> Dict[str, Any]:
    """
    Log an interaction between agents or agent activities.
    
    Args:
        session_id: Session identifier
        from_agent: Name of the agent initiating the interaction
        interaction_type: Type of interaction (analysis, collaboration, recommendation)
        message_content: Content of the interaction
        customer_id: Optional customer ID
        to_agent: Optional target agent name
        context_data: Optional context data
        db_manager: Database manager instance
        
    Returns:
        Dictionary containing logging result
    """
    try:
        query = """
        INSERT INTO agent_interactions (session_id, customer_id, from_agent, to_agent,
                                      interaction_type, message_content, context_data)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        context_json = json.dumps(context_data) if context_data else None
        
        db_manager.execute_query(query, (
            session_id, customer_id, from_agent, to_agent,
            interaction_type, message_content, context_json
        ))
        
        return {"success": True, "message": "Agent interaction logged successfully"}
        
    except Exception as e:
        logger.error(f"Error logging agent interaction: {e}")
        return {"error": str(e)}


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_spending_categories(db_manager: DatabaseManager = None) -> Dict[str, Any]:
    """
    Get all available spending categories.
    
    Args:
        db_manager: Database manager instance
        
    Returns:
        Dictionary containing list of spending categories
    """
    try:
        query = """
        SELECT category_name, parent_category, description, is_income, is_active
        FROM spending_categories 
        WHERE is_active = TRUE
        ORDER BY is_income DESC, category_name ASC
        """
        
        results = db_manager.execute_query(query)
        
        # Convert boolean values for JSON serialization
        for result in results:
            result['is_income'] = bool(result['is_income'])
            result['is_active'] = bool(result['is_active'])
        
        return {"success": True, "categories": results, "count": len(results)}
        
    except Exception as e:
        logger.error(f"Error retrieving spending categories: {e}")
        return {"error": str(e)}
