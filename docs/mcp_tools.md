# MCP Tools in Financial Advisor App

This document explains the Model Context Protocol (MCP) implementation in the Financial Advisor application and how it's used to provide secure database access for agents.

## What is MCP?

The Model Context Protocol (MCP) is a component of Google's Agent Development Kit (ADK) that allows agents to interact with external systems through well-defined tools. In this application, MCP is used to provide a secure and structured interface between agents and the MySQL database.

## MCP Architecture

```
┌───────────┐     ┌───────────┐     ┌───────────┐
│  Agent 1  │     │  Agent 2  │     │  Agent 3  │
└─────┬─────┘     └─────┬─────┘     └─────┬─────┘
      │                 │                 │
      └─────────┬───────┴─────────┬───────┘
                │                 │
        ┌───────▼─────────────────▼───────┐
        │          MCP Client             │
        └───────────────┬─────────────────┘
                        │
                        │ HTTP/gRPC
                        │
        ┌───────────────▼─────────────────┐
        │          MCP Server             │
        └───────────────┬─────────────────┘
                        │
                ┌───────▼───────┐
                │   Database    │
                └───────────────┘
```

## MCP Server Implementation

The `FinancialAdvisorMcpServer` class implements the MCP server:

```python
class FinancialAdvisorMcpServer:
    def __init__(self):
        self.server = McpServer()
        self._register_tools()
    
    def _register_tools(self):
        # Register all MCP tools
        ...
    
    def _register_tool(self, name, func, description, params):
        # Register a single tool
        ...
    
    def start(self, host="localhost", port=8080):
        # Start the MCP server
        self.server.serve(host=host, port=port)
    
    # Tool implementations
    def _tool_function(self, param1, param2):
        # Implement tool functionality
        ...
```

## MCP Tool Categories

The MCP server provides tools in several categories:

### 1. Customer Tools
- `get_customer`: Get customer by ID
- `get_customers`: Get all customers
- `create_customer`: Create a new customer

### 2. Transaction Tools
- `get_customer_transactions`: Get all transactions for a customer
- `get_transactions_by_category`: Get transactions by category
- `get_transactions_by_date_range`: Get transactions within a date range
- `add_transaction`: Add a new transaction

### 3. Goal Tools
- `get_customer_goals`: Get all goals for a customer
- `get_goal`: Get a specific goal by ID
- `create_goal`: Create a new goal
- `update_goal_progress`: Update the current amount for a goal

### 4. Advice Tools
- `get_customer_advice_history`: Get all advice history for a customer
- `add_advice`: Add new advice to the history

### 5. Analysis Tools
- `get_spending_by_category`: Get total spending by category
- `get_monthly_spending`: Get monthly spending totals

## MCP Tool Registration

Each tool is registered with the MCP server using a specification:

```python
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
```

This specification defines:
- Tool name
- Tool description
- Parameter names, types, and descriptions

## MCP Client Implementation

The `FinancialAdvisorMcpClient` class provides a client interface to the MCP server:

```python
class FinancialAdvisorMcpClient:
    def __init__(self, host="localhost", port=8080):
        self.client = McpClient(f"http://{host}:{port}")
    
    # Customer methods
    def get_customer(self, customer_id):
        return self.client.execute_tool("get_customer", {"customer_id": customer_id})
    
    def get_customers(self):
        return self.client.execute_tool("get_customers", {})
    
    # ... other methods for each tool
```

## Benefits of MCP in this Application

### 1. Security
- Agents cannot directly access the database
- Access is mediated through well-defined tools
- Input validation happens at the MCP server level

### 2. Abstraction
- Agents don't need to know database details
- Database schema changes don't affect agent code
- Complex queries are hidden behind simple tool interfaces

### 3. Consistency
- All agents use the same tools for data access
- Data validation is centralized
- Error handling is standardized

### 4. Modularity
- Database implementation can be changed without affecting agents
- New tools can be added without modifying existing code
- Tools can be versioned and deprecated safely

## MCP Tool Error Handling

MCP tools use the `McpToolExecutionError` to handle errors:

```python
def _get_customer(self, customer_id):
    """Get customer by ID."""
    customer = fetch_one("SELECT * FROM customers WHERE id = %s", (customer_id,))
    if not customer:
        raise McpToolExecutionError(f"Customer with ID {customer_id} not found")
    return customer
```

This ensures that:
- Errors are properly communicated to the client
- Agents can handle errors gracefully
- The system remains robust even when data is missing

## MCP Tool Implementation Example

Here's an example of a tool implementation:

```python
def _get_spending_by_category(self, customer_id, start_date, end_date):
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
```

This tool:
1. Takes parameters from the MCP client
2. Executes a SQL query using the database utility
3. Returns the results to the client

## Educational Takeaways

Key lessons from the MCP implementation:

1. **Secure Data Access**: Using MCP to mediate database access
2. **Tool-Based Architecture**: Breaking functionality into discrete tools
3. **Client-Server Model**: Separating tool execution from tool usage
4. **Structured Error Handling**: Using McpToolExecutionError for robust error handling
5. **Parameter Validation**: Ensuring tools receive valid inputs
