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


class ExampleMCPTools:
    """
    Example MCP tool implementations for students to reference.
    
    This class demonstrates how to implement MCP tools that will be used
    by the production MCP server. Students can use these as templates
    for implementing the complete set of financial analysis tools.
    """
    
    def __init__(self, database_config: MCPDatabaseConfig):
        """Initialize with database configuration."""
        self.config = database_config
        
    def get_customer_profile(self, customer_id: int) -> dict:
        """
        Example MCP tool: Get customer profile by ID.
        
        This is a reference implementation showing how to structure
        an MCP tool that students should implement in their MCP server.
        
        Args:
            customer_id: The ID of the customer to retrieve
            
        Returns:
            Dictionary with customer profile data in MCP format
            
        MCP Tool Specification:
        {
            "name": "get_customer_profile",
            "description": "Retrieve customer profile information by customer ID",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "integer",
                        "description": "The unique identifier for the customer"
                    }
                },
                "required": ["customer_id"]
            }
        }
        """
        try:
            # This is pseudo-code showing the structure
            # Students should implement actual database connectivity in their MCP server
            
            # Example SQL query (students will implement this in MCP server)
            query = """
                SELECT id, name, email, age, income, created_at, updated_at
                FROM customers 
                WHERE id = %s
            """
            
            # Example result structure (what the MCP server should return)
            example_result = {
                "tool_name": "get_customer_profile",
                "success": True,
                "data": {
                    "customer_id": customer_id,
                    "name": "John Doe",
                    "email": "john.doe@example.com", 
                    "age": 35,
                    "income": 75000.00,
                    "created_at": "2024-01-15T10:30:00Z",
                    "updated_at": "2024-01-15T10:30:00Z"
                },
                "metadata": {
                    "query_executed": query,
                    "execution_time_ms": 25,
                    "mcp_version": "1.0.0"
                }
            }
            
            return example_result
            
        except Exception as e:
            # Error response format for MCP tools
            return {
                "tool_name": "get_customer_profile",
                "success": False,
                "error": {
                    "type": "database_error",
                    "message": str(e),
                    "customer_id": customer_id
                },
                "metadata": {
                    "mcp_version": "1.0.0"
                }
            }
    
    def get_mcp_tool_template(self, tool_name: str, description: str, 
                            parameters: dict, sql_query: str) -> str:
        """
        Generate MCP tool template code for students.
        
        This helper method shows students how to structure their MCP tools
        following the standard pattern.
        
        Args:
            tool_name: Name of the MCP tool
            description: Description of what the tool does
            parameters: Input parameters schema
            sql_query: SQL query the tool will execute
            
        Returns:
            Python code template as string
        """
        
        template = f'''
@server.tool()
async def {tool_name}({", ".join(f"{k}: {v.get('type', 'str')}" for k, v in parameters.get('properties', {}).items())}):
    """
    {description}
    
    MCP Tool Implementation for Financial Advisor Database.
    """
    try:
        # Connect to database
        connection = mysql.connector.connect(
            host="{self.config.host}",
            port={self.config.port},
            database="{self.config.database}",
            user="{self.config.username}",
            password="{self.config.password}"
        )
        
        cursor = connection.cursor(dictionary=True)
        
        # Execute query
        query = """{sql_query}"""
        cursor.execute(query, ({", ".join(parameters.get('properties', {}).keys())},))
        
        # Fetch results
        results = cursor.fetchall()
        
        # Close connections
        cursor.close()
        connection.close()
        
        # Return MCP-formatted response
        return {{
            "tool_name": "{tool_name}",
            "success": True,
            "data": results,
            "metadata": {{
                "query": query,
                "result_count": len(results),
                "mcp_version": "1.0.0"
            }}
        }}
        
    except Exception as e:
        return {{
            "tool_name": "{tool_name}",
            "success": False,
            "error": {{
                "type": "database_error",
                "message": str(e)
            }},
            "metadata": {{
                "mcp_version": "1.0.0"
            }}
        }}
'''
        return template
    
    def get_all_tool_templates(self) -> dict:
        """
        Get templates for all required MCP tools.
        
        Students can use these templates to implement their complete MCP server.
        """
        
        tools = {
            "get_customer_profile": {
                "description": "Retrieve customer profile information by customer ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "customer_id": {"type": "integer", "description": "Customer ID"}
                    },
                    "required": ["customer_id"]
                },
                "sql": "SELECT id, name, email, age, income, created_at, updated_at FROM customers WHERE id = %s"
            },
            
            "get_customer_transactions": {
                "description": "Retrieve transactions for a customer within a date range",
                "parameters": {
                    "type": "object", 
                    "properties": {
                        "customer_id": {"type": "integer", "description": "Customer ID"},
                        "start_date": {"type": "string", "description": "Start date (YYYY-MM-DD)"},
                        "end_date": {"type": "string", "description": "End date (YYYY-MM-DD)"}
                    },
                    "required": ["customer_id"]
                },
                "sql": "SELECT * FROM transactions WHERE customer_id = %s AND date BETWEEN %s AND %s ORDER BY date DESC"
            },
            
            "get_customer_goals": {
                "description": "Retrieve financial goals for a customer",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "customer_id": {"type": "integer", "description": "Customer ID"},
                        "active_only": {"type": "boolean", "description": "Return only active goals", "default": False}
                    },
                    "required": ["customer_id"]
                },
                "sql": "SELECT * FROM goals WHERE customer_id = %s AND (is_achieved = FALSE OR %s = FALSE)"
            },
            
            "create_transaction": {
                "description": "Create a new transaction record",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "customer_id": {"type": "integer", "description": "Customer ID"},
                        "amount": {"type": "number", "description": "Transaction amount"},
                        "category": {"type": "string", "description": "Transaction category"},
                        "description": {"type": "string", "description": "Transaction description"},
                        "date": {"type": "string", "description": "Transaction date (YYYY-MM-DD)"}
                    },
                    "required": ["customer_id", "amount", "category", "description", "date"]
                },
                "sql": "INSERT INTO transactions (customer_id, amount, category, description, date) VALUES (%s, %s, %s, %s, %s)"
            }
        }
        
        # Generate templates for each tool
        templates = {}
        for tool_name, tool_config in tools.items():
            templates[tool_name] = self.get_mcp_tool_template(
                tool_name=tool_name,
                description=tool_config["description"],
                parameters=tool_config["parameters"],
                sql_query=tool_config["sql"]
            )
        
        return templates


# Global configuration instance
mcp_config = MCPDatabaseConfig.from_env()
mcp_setup = MCPDatabaseToolsetSetup(mcp_config)

# Example tools for student reference
example_mcp_tools = ExampleMCPTools(mcp_config)
