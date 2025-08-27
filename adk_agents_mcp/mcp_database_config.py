"""
MCP Database Configuration for ADK Financial Advisor agents.

This module sets up the Model Context Protocol (MCP) toolset for database connectivity,
providing a framework-native approach to database access in ADK agents.
"""

import os
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class MCPDatabaseConfig:
    """Configuration for MCP database connectivity."""
    
    # Database connection details
    host: str = "localhost"
    port: int = 3306
    database: str = "financial_advisor"
    username: str = "root"
    password: str = ""
    
    # MCP server configuration
    mcp_server_port: int = 5000
    mcp_server_host: str = "localhost"
    
    @classmethod
    def from_env(cls) -> 'MCPDatabaseConfig':
        """Create configuration from environment variables."""
        return cls(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '3306')),
            database=os.getenv('DB_NAME', 'financial_advisor'),
            username=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            mcp_server_host=os.getenv('MCP_SERVER_HOST', 'localhost'),
            mcp_server_port=int(os.getenv('MCP_SERVER_PORT', '5000'))
        )
    
    def get_mysql_connection_string(self) -> str:
        """Get MySQL connection string."""
        return f"mysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
    
    def get_mcp_server_url(self) -> str:
        """Get MCP server URL."""
        return f"http://{self.mcp_server_host}:{self.mcp_server_port}"


class MCPDatabaseToolsetSetup:
    """
    Setup class for MCP database toolset configuration.
    
    This class provides the configuration needed to connect ADK agents
    to the database using Google's MCP framework instead of direct database access.
    """
    
    def __init__(self, config: Optional[MCPDatabaseConfig] = None):
        """Initialize MCP database setup."""
        self.config = config or MCPDatabaseConfig.from_env()
        self._available_tools = [
            "get_customer_by_id",
            "get_customer_transactions",
            "get_customer_goals",
            "create_customer",
            "create_transaction", 
            "create_goal",
            "update_goal",
            "list_customers",
            "get_transaction_summary",
            "get_goal_progress"
        ]
    
    def get_database_schema_prompt(self) -> str:
        """
        Get a prompt describing the database schema for MCP tools.
        
        This helps the MCP tools understand the database structure.
        """
        return """
Database Schema for Financial Advisor Application:

TABLES:
1. customers
   - id (INT, PRIMARY KEY, AUTO_INCREMENT)
   - name (VARCHAR(255), NOT NULL)
   - email (VARCHAR(255), UNIQUE, NOT NULL)
   - age (INT)
   - income (DECIMAL(15,2))
   - created_at (TIMESTAMP)
   - updated_at (TIMESTAMP)

2. transactions
   - id (INT, PRIMARY KEY, AUTO_INCREMENT)
   - customer_id (INT, FOREIGN KEY -> customers.id)
   - amount (DECIMAL(15,2), NOT NULL)
   - category (ENUM: food, transportation, entertainment, utilities, healthcare, shopping, travel, other)
   - description (TEXT)
   - date (DATE, NOT NULL)
   - created_at (TIMESTAMP)

3. goals
   - id (INT, PRIMARY KEY, AUTO_INCREMENT)
   - customer_id (INT, FOREIGN KEY -> customers.id)
   - title (VARCHAR(255), NOT NULL)
   - description (TEXT)
   - goal_type (ENUM: savings, investment, debt_payoff, emergency_fund, other)
   - target_amount (DECIMAL(15,2), NOT NULL)
   - current_amount (DECIMAL(15,2), DEFAULT 0)
   - target_date (DATE)
   - is_achieved (BOOLEAN, DEFAULT FALSE)
   - created_at (TIMESTAMP)
   - updated_at (TIMESTAMP)

4. advice
   - id (INT, PRIMARY KEY, AUTO_INCREMENT)  
   - customer_id (INT, FOREIGN KEY -> customers.id)
   - advice_text (LONGTEXT, NOT NULL)
   - confidence_score (DECIMAL(3,2))
   - recommendations (JSON)
   - created_at (TIMESTAMP)

COMMON QUERIES:
- Get customer spending by category over time period
- Calculate monthly income vs expenses
- Track goal progress and required savings
- Generate spending insights and recommendations
"""
    
    def get_financial_analysis_tools_config(self) -> Dict[str, Any]:
        """
        Get configuration for financial analysis tools that can be used via MCP.
        
        These tools would be implemented on the MCP server side to provide
        database access functionality to the ADK agents.
        """
        return {
            "tools": [
                {
                    "name": "get_customer_financial_profile",
                    "description": "Get comprehensive financial profile for a customer including transactions and goals",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "customer_id": {"type": "integer", "description": "Customer ID"},
                            "days_back": {"type": "integer", "description": "Number of days to look back", "default": 90}
                        },
                        "required": ["customer_id"]
                    }
                },
                {
                    "name": "get_spending_analysis_data",
                    "description": "Get spending analysis data for a customer",
                    "parameters": {
                        "type": "object", 
                        "properties": {
                            "customer_id": {"type": "integer", "description": "Customer ID"},
                            "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                            "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"}
                        },
                        "required": ["customer_id"]
                    }
                },
                {
                    "name": "get_goal_planning_data", 
                    "description": "Get goal planning data for a customer",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "customer_id": {"type": "integer", "description": "Customer ID"},
                            "goal_id": {"type": "integer", "description": "Specific goal ID (optional)"}
                        },
                        "required": ["customer_id"]
                    }
                },
                {
                    "name": "execute_financial_query",
                    "description": "Execute a custom SQL query for financial analysis",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "SQL query to execute"},
                            "parameters": {"type": "array", "description": "Query parameters"}
                        },
                        "required": ["query"]
                    }
                }
            ],
            "database_schema": self.get_database_schema_prompt()
        }
    
    def get_mcp_connection_params(self) -> Dict[str, Any]:
        """
        Get MCP connection parameters for ADK agents.
        
        This would typically connect to an MCP server that provides database tools.
        For this implementation, we'll simulate the MCP approach.
        """
        return {
            "server_url": self.config.get_mcp_server_url(),
            "connection_type": "http",  # or "stdio" for local server
            "tools_filter": self._available_tools,
            "database_config": {
                "type": "mysql",
                "connection_string": self.config.get_mysql_connection_string(),
                "schema": self.get_database_schema_prompt()
            }
        }
    
    def get_simulated_mcp_tools_config(self) -> str:
        """
        Get configuration for simulated MCP tools.
        
        Since setting up a full MCP server is complex, this provides a configuration
        that our agents can use to simulate MCP behavior while demonstrating the concepts.
        """
        config = {
            "mcp_server_config": {
                "host": self.config.mcp_server_host,
                "port": self.config.mcp_server_port,
                "database": {
                    "type": "mysql",
                    "connection": self.config.get_mysql_connection_string(),
                    "schema": self.get_database_schema_prompt()
                }
            },
            "available_tools": self.get_financial_analysis_tools_config(),
            "simulation_mode": True,
            "note": "This configuration simulates MCP behavior for educational purposes"
        }
        
        return json.dumps(config, indent=2)


# Global configuration instance
mcp_config = MCPDatabaseConfig.from_env()
mcp_setup = MCPDatabaseToolsetSetup(mcp_config)
