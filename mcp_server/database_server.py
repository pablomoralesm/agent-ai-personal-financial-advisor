#!/usr/bin/env python3
"""
MCP Database Server for Financial Advisor Application

This server provides MCP tools for database interactions, allowing ADK agents
to access customer data, transactions, goals, and advice history through
the Model Context Protocol.

Uses FastMCP for simplified MCP server implementation as recommended in ADK docs.
"""

import asyncio
import logging
import sys
from typing import Dict, Any

from fastmcp import FastMCP

# Import shared components
try:
    # Try relative import first (when used as module)
    from .shared import (
        DatabaseManager, 
        get_database_config,
        setup_logging,
        get_customer_profile,
        create_customer,
        add_transaction,
        get_transactions_by_customer,
        get_spending_summary,
        create_financial_goal,
        get_financial_goals,
        update_goal_progress,
        save_advice,
        get_advice_history,
        log_agent_interaction,
        get_spending_categories
    )
except ImportError:
    # Fall back to absolute import (when run directly)
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from mcp_server.shared import (
        DatabaseManager, 
        get_database_config,
        setup_logging,
        get_customer_profile,
        create_customer,
        add_transaction,
        get_transactions_by_customer,
        get_spending_summary,
        create_financial_goal,
        get_financial_goals,
        update_goal_progress,
        save_advice,
        get_advice_history,
        log_agent_interaction,
        get_spending_categories
    )

# Configure logging
logger = setup_logging()

# Get database configuration
DB_CONFIG = get_database_config()

# Initialize FastMCP server
mcp = FastMCP("Financial Advisor Database Server")

# Global database manager instance
db_manager = DatabaseManager(DB_CONFIG)

# ============================================================================
# CUSTOMER MANAGEMENT TOOLS
# ============================================================================

@mcp.tool()
def get_customer_profile_tool(customer_id: int) -> Dict[str, Any]:
    """
    Retrieve complete customer profile information.
    
    Args:
        customer_id: The ID of the customer to retrieve
        
    Returns:
        Dictionary containing customer profile data
    """
    return get_customer_profile(customer_id, db_manager)

@mcp.tool()
def create_customer_tool(name: str, email: str, phone: str = None, date_of_birth: str = None) -> Dict[str, Any]:
    """
    Create a new customer profile.
    
    Args:
        name: Customer's full name
        email: Customer's email address
        phone: Optional phone number
        date_of_birth: Optional date of birth in YYYY-MM-DD format
        
    Returns:
        Dictionary containing the created customer's information
    """
    return create_customer(name, email, phone, date_of_birth, db_manager)

# ============================================================================
# TRANSACTION MANAGEMENT TOOLS
# ============================================================================

@mcp.tool()
def add_transaction_tool(
    customer_id: int,
    amount: float,
    category: str,
    transaction_date: str,
    transaction_type: str,
    subcategory: str = None,
    description: str = None,
    payment_method: str = None
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
        
    Returns:
        Dictionary containing transaction creation result
    """
    return add_transaction(
        customer_id, amount, category, transaction_date, transaction_type,
        subcategory, description, payment_method, db_manager
    )

@mcp.tool()
def get_transactions_by_customer_tool(
    customer_id: int,
    start_date: str = None,
    end_date: str = None,
    category: str = None,
    transaction_type: str = None,
    limit: int = 100
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
        
    Returns:
        Dictionary containing list of transactions
    """
    return get_transactions_by_customer(
        customer_id, start_date, end_date, category, transaction_type, limit, None, db_manager
    )

@mcp.tool()
def get_spending_summary_tool(customer_id: int, months: int = 6) -> Dict[str, Any]:
    """
    Get spending summary and analysis for a customer over specified months.
    
    Args:
        customer_id: ID of the customer
        months: Number of months to analyze (default 6)
        
    Returns:
        Dictionary containing spending analysis data
    """
    return get_spending_summary(customer_id, months, db_manager)

# ============================================================================
# FINANCIAL GOALS MANAGEMENT TOOLS
# ============================================================================

@mcp.tool()
def create_financial_goal_tool(
    customer_id: int,
    goal_name: str,
    goal_type: str,
    target_amount: float,
    target_date: str = None,
    priority: str = 'medium',
    description: str = None
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
        
    Returns:
        Dictionary containing goal creation result
    """
    return create_financial_goal(
        customer_id, goal_name, goal_type, target_amount, target_date, priority, description, db_manager
    )

@mcp.tool()
def get_financial_goals_tool(customer_id: int, status: str = None) -> Dict[str, Any]:
    """
    Retrieve financial goals for a customer.
    
    Args:
        customer_id: ID of the customer
        status: Optional status filter (active, completed, paused, cancelled)
        
    Returns:
        Dictionary containing list of financial goals
    """
    return get_financial_goals(customer_id, status, db_manager)

@mcp.tool()
def update_goal_progress_tool(goal_id: int, current_amount: float) -> Dict[str, Any]:
    """
    Update the current amount for a financial goal.
    
    Args:
        goal_id: ID of the goal to update
        current_amount: New current amount
        
    Returns:
        Dictionary containing update result
    """
    return update_goal_progress(goal_id, current_amount, db_manager)

# ============================================================================
# ADVICE HISTORY TOOLS
# ============================================================================

@mcp.tool()
def save_advice_tool(
    customer_id: int,
    agent_name: str,
    advice_type: str,
    advice_content: str,
    confidence_score: float = None,
    metadata: Dict[str, Any] = None
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
        
    Returns:
        Dictionary containing save result
    """
    return save_advice(
        customer_id, agent_name, advice_type, advice_content, confidence_score, metadata, db_manager
    )

@mcp.tool()
def get_advice_history_tool(
    customer_id: int,
    agent_name: str = None,
    advice_type: str = None,
    limit: int = 50
) -> Dict[str, Any]:
    """
    Retrieve advice history for a customer.
    
    Args:
        customer_id: ID of the customer
        agent_name: Optional filter by agent name
        advice_type: Optional filter by advice type
        limit: Maximum number of records to return
        
    Returns:
        Dictionary containing advice history
    """
    return get_advice_history(
        customer_id, agent_name, advice_type, limit, db_manager
    )

# ============================================================================
# AGENT INTERACTION LOGGING TOOLS
# ============================================================================

@mcp.tool()
def log_agent_interaction_tool(
    session_id: str,
    from_agent: str,
    interaction_type: str,
    message_content: str,
    customer_id: int = None,
    to_agent: str = None,
    context_data: Dict[str, Any] = None
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
        
    Returns:
        Dictionary containing logging result
    """
    return log_agent_interaction(
        session_id, from_agent, interaction_type, message_content, 
        customer_id, to_agent, context_data, db_manager
    )

# ============================================================================
# UTILITY TOOLS
# ============================================================================

@mcp.tool()
def get_spending_categories_tool() -> Dict[str, Any]:
    """
    Get all available spending categories.
    
    Returns:
        Dictionary containing list of spending categories
    """
    return get_spending_categories(db_manager)

# ============================================================================
# SERVER STARTUP
# ============================================================================

async def main():
    """Main function to run the MCP server."""
    try:
        # Test database connection
        db_manager.get_connection().close()
        logger.info("Database connection successful")
        
        # Start the MCP server
        logger.info("Starting Financial Advisor MCP Database Server...")
        await mcp.run()
        
    except Exception as e:
        logger.error(f"Failed to start MCP server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
