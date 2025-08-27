"""
MCP (Model Context Protocol) module for database operations.

This module handles persistent storage of customer data, transactions,
goals, and advice history using MySQL database.
"""

from .database import DatabaseManager
from .models import Customer, Transaction, Goal, Advice
from .server import MCPServer

__all__ = [
    "DatabaseManager",
    "Customer",
    "Transaction", 
    "Goal",
    "Advice",
    "MCPServer"
]
