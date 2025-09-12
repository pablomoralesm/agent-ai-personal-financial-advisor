"""
Shared components for MCP Database Servers

This module contains shared business logic, database management, models, and configuration
that are used by both the standalone FastMCP server and the ADK-integrated STDIO server.

The shared components follow DRY principles while preserving the educational value
of having separate server implementations that demonstrate different MCP patterns.
"""

from .database_manager import DatabaseManager
from .business_logic import (
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
from .models import Customer, Transaction, FinancialGoal
from .config import get_database_config, setup_logging

__all__ = [
    'DatabaseManager',
    'get_customer_profile',
    'create_customer', 
    'add_transaction',
    'get_transactions_by_customer',
    'get_spending_summary',
    'create_financial_goal',
    'get_financial_goals',
    'update_goal_progress',
    'save_advice',
    'get_advice_history',
    'log_agent_interaction',
    'get_spending_categories',
    'Customer',
    'Transaction',
    'FinancialGoal',
    'get_database_config',
    'setup_logging'
]
