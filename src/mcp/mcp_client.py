"""MCP Client for the Financial Advisor app.

This module provides a client to interact with the MCP server.
"""

from typing import Dict, List, Any, Optional

from google.adk.mcp import McpClient

class FinancialAdvisorMcpClient:
    """MCP Client for the Financial Advisor app."""
    
    def __init__(self, host: str = "localhost", port: int = 8080):
        """Initialize the MCP client.
        
        Args:
            host: MCP server host
            port: MCP server port
        """
        self.client = McpClient(f"http://{host}:{port}")
    
    # Customer methods
    
    def get_customer(self, customer_id: int) -> Dict[str, Any]:
        """Get customer by ID.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            Dict[str, Any]: Customer data
        """
        return self.client.execute_tool("get_customer", {"customer_id": customer_id})
    
    def get_customers(self) -> List[Dict[str, Any]]:
        """Get all customers.
        
        Returns:
            List[Dict[str, Any]]: List of customers
        """
        return self.client.execute_tool("get_customers", {})
    
    def create_customer(self, name: str, email: str) -> Dict[str, Any]:
        """Create a new customer.
        
        Args:
            name: Customer name
            email: Customer email
            
        Returns:
            Dict[str, Any]: Created customer data
        """
        return self.client.execute_tool("create_customer", {"name": name, "email": email})
    
    # Transaction methods
    
    def get_customer_transactions(self, customer_id: int) -> List[Dict[str, Any]]:
        """Get all transactions for a customer.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            List[Dict[str, Any]]: List of transactions
        """
        return self.client.execute_tool("get_customer_transactions", {"customer_id": customer_id})
    
    def get_transactions_by_category(self, customer_id: int, category: str) -> List[Dict[str, Any]]:
        """Get transactions by category for a customer.
        
        Args:
            customer_id: Customer ID
            category: Transaction category
            
        Returns:
            List[Dict[str, Any]]: List of transactions
        """
        return self.client.execute_tool(
            "get_transactions_by_category", 
            {"customer_id": customer_id, "category": category}
        )
    
    def get_transactions_by_date_range(self, customer_id: int, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get transactions within a date range for a customer.
        
        Args:
            customer_id: Customer ID
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            List[Dict[str, Any]]: List of transactions
        """
        return self.client.execute_tool(
            "get_transactions_by_date_range", 
            {"customer_id": customer_id, "start_date": start_date, "end_date": end_date}
        )
    
    def add_transaction(self, customer_id: int, amount: float, category: str, 
                       transaction_date: str, description: str) -> Dict[str, Any]:
        """Add a new transaction for a customer.
        
        Args:
            customer_id: Customer ID
            amount: Transaction amount
            category: Transaction category
            transaction_date: Transaction date (YYYY-MM-DD)
            description: Transaction description
            
        Returns:
            Dict[str, Any]: Created transaction data
        """
        return self.client.execute_tool(
            "add_transaction", 
            {
                "customer_id": customer_id,
                "amount": amount,
                "category": category,
                "transaction_date": transaction_date,
                "description": description
            }
        )
    
    # Goal methods
    
    def get_customer_goals(self, customer_id: int) -> List[Dict[str, Any]]:
        """Get all goals for a customer.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            List[Dict[str, Any]]: List of goals
        """
        return self.client.execute_tool("get_customer_goals", {"customer_id": customer_id})
    
    def get_goal(self, goal_id: int) -> Dict[str, Any]:
        """Get a specific goal by ID.
        
        Args:
            goal_id: Goal ID
            
        Returns:
            Dict[str, Any]: Goal data
        """
        return self.client.execute_tool("get_goal", {"goal_id": goal_id})
    
    def create_goal(self, customer_id: int, goal_type: str, target_amount: float,
                   current_amount: float, target_date: str, description: str) -> Dict[str, Any]:
        """Create a new goal for a customer.
        
        Args:
            customer_id: Customer ID
            goal_type: Goal type
            target_amount: Target amount
            current_amount: Current amount
            target_date: Target date (YYYY-MM-DD)
            description: Goal description
            
        Returns:
            Dict[str, Any]: Created goal data
        """
        return self.client.execute_tool(
            "create_goal", 
            {
                "customer_id": customer_id,
                "goal_type": goal_type,
                "target_amount": target_amount,
                "current_amount": current_amount,
                "target_date": target_date,
                "description": description
            }
        )
    
    def update_goal_progress(self, goal_id: int, current_amount: float) -> Dict[str, Any]:
        """Update the current amount for a goal.
        
        Args:
            goal_id: Goal ID
            current_amount: Current amount
            
        Returns:
            Dict[str, Any]: Updated goal data
        """
        return self.client.execute_tool(
            "update_goal_progress", 
            {"goal_id": goal_id, "current_amount": current_amount}
        )
    
    # Advice methods
    
    def get_customer_advice_history(self, customer_id: int) -> List[Dict[str, Any]]:
        """Get all advice history for a customer.
        
        Args:
            customer_id: Customer ID
            
        Returns:
            List[Dict[str, Any]]: List of advice entries
        """
        return self.client.execute_tool("get_customer_advice_history", {"customer_id": customer_id})
    
    def add_advice(self, customer_id: int, agent_name: str, advice_text: str) -> Dict[str, Any]:
        """Add new advice to the history.
        
        Args:
            customer_id: Customer ID
            agent_name: Name of the agent providing the advice
            advice_text: Advice text
            
        Returns:
            Dict[str, Any]: Created advice data
        """
        return self.client.execute_tool(
            "add_advice", 
            {"customer_id": customer_id, "agent_name": agent_name, "advice_text": advice_text}
        )
    
    # Analysis methods
    
    def get_spending_by_category(self, customer_id: int, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get total spending by category for a customer.
        
        Args:
            customer_id: Customer ID
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            List[Dict[str, Any]]: Spending by category
        """
        return self.client.execute_tool(
            "get_spending_by_category", 
            {"customer_id": customer_id, "start_date": start_date, "end_date": end_date}
        )
    
    def get_monthly_spending(self, customer_id: int, year: int) -> List[Dict[str, Any]]:
        """Get monthly spending totals for a customer.
        
        Args:
            customer_id: Customer ID
            year: Year
            
        Returns:
            List[Dict[str, Any]]: Monthly spending totals
        """
        return self.client.execute_tool(
            "get_monthly_spending", 
            {"customer_id": customer_id, "year": year}
        )
