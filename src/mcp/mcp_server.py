"""MCP Server implementation for the Financial Advisor app.

This module implements an MCP server that provides database access tools
for agents to interact with the MySQL database.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Callable

from google.adk.mcp import McpServer, McpTool, McpToolSpec
from google.adk.mcp.errors import McpToolExecutionError

from src.db.db_utils import (
    fetch_data,
    fetch_one,
    insert_data,
    update_data,
    delete_data
)

class FinancialAdvisorMcpServer:
    """MCP Server for the Financial Advisor app."""
    
    def __init__(self):
        """Initialize the MCP server with database tools."""
        self.server = McpServer()
        self._register_tools()
        
    def _register_tools(self):
        """Register all MCP tools with the server."""
        # Customer tools
        self._register_tool(
            "get_customer",
            self._get_customer,
            "Get customer by ID",
            {"customer_id": "int"}
        )
        self._register_tool(
            "get_customers",
            self._get_customers,
            "Get all customers",
            {}
        )
        self._register_tool(
            "create_customer",
            self._create_customer,
            "Create a new customer",
            {"name": "string", "email": "string"}
        )
        
        # Transaction tools
        self._register_tool(
            "get_customer_transactions",
            self._get_customer_transactions,
            "Get all transactions for a customer",
            {"customer_id": "int"}
        )
        self._register_tool(
            "get_transactions_by_category",
            self._get_transactions_by_category,
            "Get transactions by category for a customer",
            {"customer_id": "int", "category": "string"}
        )
        self._register_tool(
            "get_transactions_by_date_range",
            self._get_transactions_by_date_range,
            "Get transactions within a date range for a customer",
            {"customer_id": "int", "start_date": "string", "end_date": "string"}
        )
        self._register_tool(
            "add_transaction",
            self._add_transaction,
            "Add a new transaction for a customer",
            {
                "customer_id": "int",
                "amount": "float",
                "category": "string",
                "transaction_date": "string",
                "description": "string"
            }
        )
        
        # Goal tools
        self._register_tool(
            "get_customer_goals",
            self._get_customer_goals,
            "Get all goals for a customer",
            {"customer_id": "int"}
        )
        self._register_tool(
            "get_goal",
            self._get_goal,
            "Get a specific goal by ID",
            {"goal_id": "int"}
        )
        self._register_tool(
            "create_goal",
            self._create_goal,
            "Create a new goal for a customer",
            {
                "customer_id": "int",
                "goal_type": "string",
                "target_amount": "float",
                "current_amount": "float",
                "target_date": "string",
                "description": "string"
            }
        )
        self._register_tool(
            "update_goal_progress",
            self._update_goal_progress,
            "Update the current amount for a goal",
            {"goal_id": "int", "current_amount": "float"}
        )
        
        # Advice tools
        self._register_tool(
            "get_customer_advice_history",
            self._get_customer_advice_history,
            "Get all advice history for a customer",
            {"customer_id": "int"}
        )
        self._register_tool(
            "add_advice",
            self._add_advice,
            "Add new advice to the history",
            {"customer_id": "int", "agent_name": "string", "advice_text": "string"}
        )
        
        # Analysis tools
        self._register_tool(
            "get_spending_by_category",
            self._get_spending_by_category,
            "Get total spending by category for a customer",
            {"customer_id": "int", "start_date": "string", "end_date": "string"}
        )
        self._register_tool(
            "get_monthly_spending",
            self._get_monthly_spending,
            "Get monthly spending totals for a customer",
            {"customer_id": "int", "year": "int"}
        )
    
    def _register_tool(self, name: str, func: Callable, description: str, params: Dict[str, str]):
        """Register a tool with the MCP server.
        
        Args:
            name: Tool name
            func: Function to execute
            description: Tool description
            params: Parameter definitions
        """
        param_specs = {}
        for param_name, param_type in params.items():
            param_specs[param_name] = McpToolSpec.Parameter(
                description=f"{param_name} parameter",
                type=param_type
            )
        
        tool_spec = McpToolSpec(
            name=name,
            description=description,
            parameters=param_specs
        )
        
        self.server.register_tool(McpTool(tool_spec, func))
    
    def start(self, host: str = "localhost", port: int = 8080):
        """Start the MCP server.
        
        Args:
            host: Host address
            port: Port number
        """
        logging.info(f"Starting MCP server at {host}:{port}")
        self.server.serve(host=host, port=port)
    
    # Tool implementations
    
    def _get_customer(self, customer_id: int) -> Dict[str, Any]:
        """Get customer by ID."""
        customer = fetch_one("SELECT * FROM customers WHERE id = %s", (customer_id,))
        if not customer:
            raise McpToolExecutionError(f"Customer with ID {customer_id} not found")
        return customer
    
    def _get_customers(self) -> List[Dict[str, Any]]:
        """Get all customers."""
        return fetch_data("SELECT * FROM customers")
    
    def _create_customer(self, name: str, email: str) -> Dict[str, Any]:
        """Create a new customer."""
        customer_id = insert_data("customers", {"name": name, "email": email})
        if not customer_id:
            raise McpToolExecutionError("Failed to create customer")
        return {"id": customer_id, "name": name, "email": email}
    
    def _get_customer_transactions(self, customer_id: int) -> List[Dict[str, Any]]:
        """Get all transactions for a customer."""
        return fetch_data(
            "SELECT * FROM transactions WHERE customer_id = %s ORDER BY transaction_date DESC",
            (customer_id,)
        )
    
    def _get_transactions_by_category(self, customer_id: int, category: str) -> List[Dict[str, Any]]:
        """Get transactions by category for a customer."""
        return fetch_data(
            "SELECT * FROM transactions WHERE customer_id = %s AND category = %s ORDER BY transaction_date DESC",
            (customer_id, category)
        )
    
    def _get_transactions_by_date_range(self, customer_id: int, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get transactions within a date range for a customer."""
        return fetch_data(
            """
            SELECT * FROM transactions 
            WHERE customer_id = %s 
            AND transaction_date BETWEEN %s AND %s 
            ORDER BY transaction_date DESC
            """,
            (customer_id, start_date, end_date)
        )
    
    def _add_transaction(self, customer_id: int, amount: float, category: str, 
                        transaction_date: str, description: str) -> Dict[str, Any]:
        """Add a new transaction for a customer."""
        transaction_data = {
            "customer_id": customer_id,
            "amount": amount,
            "category": category,
            "transaction_date": transaction_date,
            "description": description
        }
        transaction_id = insert_data("transactions", transaction_data)
        if not transaction_id:
            raise McpToolExecutionError("Failed to add transaction")
        
        transaction_data["id"] = transaction_id
        return transaction_data
    
    def _get_customer_goals(self, customer_id: int) -> List[Dict[str, Any]]:
        """Get all goals for a customer."""
        return fetch_data(
            "SELECT * FROM goals WHERE customer_id = %s ORDER BY target_date",
            (customer_id,)
        )
    
    def _get_goal(self, goal_id: int) -> Dict[str, Any]:
        """Get a specific goal by ID."""
        goal = fetch_one("SELECT * FROM goals WHERE id = %s", (goal_id,))
        if not goal:
            raise McpToolExecutionError(f"Goal with ID {goal_id} not found")
        return goal
    
    def _create_goal(self, customer_id: int, goal_type: str, target_amount: float,
                    current_amount: float, target_date: str, description: str) -> Dict[str, Any]:
        """Create a new goal for a customer."""
        goal_data = {
            "customer_id": customer_id,
            "goal_type": goal_type,
            "target_amount": target_amount,
            "current_amount": current_amount,
            "target_date": target_date,
            "description": description
        }
        goal_id = insert_data("goals", goal_data)
        if not goal_id:
            raise McpToolExecutionError("Failed to create goal")
        
        goal_data["id"] = goal_id
        return goal_data
    
    def _update_goal_progress(self, goal_id: int, current_amount: float) -> Dict[str, Any]:
        """Update the current amount for a goal."""
        success = update_data(
            "goals",
            {"current_amount": current_amount},
            "id = %s",
            (goal_id,)
        )
        if not success:
            raise McpToolExecutionError(f"Failed to update goal {goal_id}")
        
        return self._get_goal(goal_id)
    
    def _get_customer_advice_history(self, customer_id: int) -> List[Dict[str, Any]]:
        """Get all advice history for a customer."""
        return fetch_data(
            "SELECT * FROM advice_history WHERE customer_id = %s ORDER BY created_at DESC",
            (customer_id,)
        )
    
    def _add_advice(self, customer_id: int, agent_name: str, advice_text: str) -> Dict[str, Any]:
        """Add new advice to the history."""
        advice_data = {
            "customer_id": customer_id,
            "agent_name": agent_name,
            "advice_text": advice_text
        }
        advice_id = insert_data("advice_history", advice_data)
        if not advice_id:
            raise McpToolExecutionError("Failed to add advice")
        
        advice_data["id"] = advice_id
        return advice_data
    
    def _get_spending_by_category(self, customer_id: int, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get total spending by category for a customer."""
        return fetch_data(
            """
            SELECT category, SUM(amount) as total_amount
            FROM transactions
            WHERE customer_id = %s AND transaction_date BETWEEN %s AND %s
            GROUP BY category
            ORDER BY total_amount DESC
            """,
            (customer_id, start_date, end_date)
        )
    
    def _get_monthly_spending(self, customer_id: int, year: int) -> List[Dict[str, Any]]:
        """Get monthly spending totals for a customer."""
        return fetch_data(
            """
            SELECT 
                MONTH(transaction_date) as month,
                SUM(amount) as total_amount
            FROM transactions
            WHERE customer_id = %s AND YEAR(transaction_date) = %s
            GROUP BY MONTH(transaction_date)
            ORDER BY month
            """,
            (customer_id, year)
        )

def main():
    """Start the MCP server."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    server = FinancialAdvisorMcpServer()
    server.start()

if __name__ == "__main__":
    main()
