# MCP Database Servers - Student Guide

Welcome to the MCP (Model Context Protocol) Database Servers! This folder contains two different implementations of the same database server, demonstrating different approaches to building MCP servers while sharing common business logic.

## 🎯 **Learning Objectives**

By studying this code, you will learn:
- How to build MCP servers using different approaches
- How to apply DRY (Don't Repeat Yourself) principles in real projects
- How to structure shared components in Python
- How to maintain educational value while reducing code duplication
- Professional software engineering practices

## 📁 **Project Structure**

```
mcp_server/
├── shared/                    # 🆕 Shared components (DRY implementation)
│   ├── __init__.py           # Exports all shared functionality
│   ├── database_manager.py   # Unified database management
│   ├── business_logic.py     # All tool functions (shared logic)
│   ├── models.py            # Pydantic models for validation
│   └── config.py            # Configuration management
├── database_server.py        # FastMCP implementation (standalone)
├── database_server_stdio.py  # STDIO implementation (ADK-integrated)
└── README.md                # This file
```

## 🚀 **Two Server Implementations**

### 1. **FastMCP Server** (`database_server.py`)
- **Purpose**: Standalone MCP server using FastMCP framework
- **Use Case**: Independent server that can run on its own
- **Key Features**:
  - Uses `@mcp.tool()` decorators
  - Async server lifecycle with `await mcp.run()`
  - Pydantic models for type validation
  - Clean, modern Python async/await patterns

**How to run:**
```bash
cd mcp_server
python database_server.py
```

### 2. **STDIO Server** (`database_server_stdio.py`)
- **Purpose**: ADK-integrated server using stdin/stdout communication
- **Use Case**: Works with ADK's `StdioConnectionParams` (updated for latest ADK)
- **Key Features**:
  - Full JSON-RPC 2.0 protocol implementation
  - Manual MCP protocol handling (initialize, tools/list, tools/call)
  - Robust error handling with proper JSON-RPC error codes
  - Subprocess communication via stdin/stdout
  - Compatible with ADK agent framework
  - Uses modern ADK connection parameters
  - Import fallback mechanism for both module and direct execution

**How to run:**
```bash
cd mcp_server
python database_server_stdio.py
```

## 🔗 **ADK Integration (Updated)**

The STDIO server is designed to work with Google's ADK (Agent Development Kit) framework. The integration has been updated to use the latest ADK patterns:

### **Modern ADK Usage (Current)**

**In your agent files:**
```python
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams
from mcp.client.stdio import StdioServerParameters

# Updated configuration
mcp_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command='python3',
            args=[mcp_server_path]
        )
    )
)
```

### **What Changed?**

- **Old**: Direct use of `StdioServerParameters` (deprecated)
- **New**: `StdioConnectionParams` wrapping `StdioServerParameters`
- **Benefit**: Future-proof against ADK updates, no deprecation warnings

## 🔌 **JSON-RPC 2.0 Protocol Implementation**

The STDIO server implements the full JSON-RPC 2.0 protocol as required by the MCP specification. This is a crucial part of making the server work correctly with ADK agents.

### **Supported MCP Methods:**

#### **1. Initialize (`initialize`)**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {"name": "test", "version": "1.0.0"}
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {"tools": {}},
    "serverInfo": {
      "name": "financial-advisor-database-server",
      "version": "1.0.0"
    }
  }
}
```

#### **2. List Tools (`tools/list`)**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}
```

**Response:** Returns all 8 available tools with their schemas.

#### **3. Call Tool (`tools/call`)**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "get_spending_summary",
    "arguments": {"customer_id": 1, "months": 6}
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"success\": true, \"categories\": [...], \"totals\": {...}}"
      }
    ]
  }
}
```

### **Error Handling:**

The server implements proper JSON-RPC 2.0 error responses:

- **Parse Error** (`-32700`): Invalid JSON received
- **Method Not Found** (`-32601`): Unknown method requested
- **Internal Error** (`-32603`): Server-side execution error

### **Key Implementation Details:**

1. **Output Flushing**: All responses include `sys.stdout.flush()` for reliable communication
2. **Empty Line Handling**: Skips empty lines in stdin to prevent parsing errors
3. **Import Fallback**: Works both as a module and when run directly
4. **Error Logging**: Comprehensive logging for debugging and monitoring

## 🧩 **Shared Components Architecture**

The `shared/` folder contains all the common business logic that both servers use. This is a great example of the **DRY (Don't Repeat Yourself)** principle in action!

### **Why Shared Components?**

**Before DRY:**
- 1,220 lines of code across both files
- ~80% duplication of business logic
- Bug fixes needed in two places
- Hard to maintain consistency

**After DRY:**
- ~70% reduction in duplicated code
- Single source of truth for business logic
- Bug fixes apply everywhere automatically
- Easier to add new features

### **Shared Components Breakdown:**

#### **`shared/database_manager.py`**
```python
class DatabaseManager:
    """Unified database management for both server types."""
    def get_connection(self): ...
    def execute_query(self, query, params, fetch_all): ...
```
- Handles MySQL connections
- Provides error handling and connection management
- Used by both servers identically

#### **`shared/business_logic.py`**
```python
def get_customer_profile(customer_id: int, db_manager: DatabaseManager) -> Dict[str, Any]:
    """Shared implementation of get_customer_profile."""
    # All the business logic here
```
- Contains all 12 tool functions
- Pure business logic (no MCP protocol handling)
- Takes `db_manager` as parameter for flexibility

#### **`shared/models.py`**
```python
class Customer(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    # ... validation rules
```
- Pydantic models for data validation
- Type safety and serialization
- Used by both servers

#### **`shared/config.py`**
```python
def get_database_config() -> Dict[str, Any]:
    """Get database configuration from environment variables."""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        # ... other config
    }
```
- Centralized configuration management
- Environment variable handling
- Consistent settings across servers

## 🔄 **How the DRY Pattern Works**

### **Server Implementation Pattern:**

**FastMCP Server:**
```python
from .shared import get_customer_profile, DatabaseManager

@mcp.tool()
def get_customer_profile_tool(customer_id: int) -> Dict[str, Any]:
    """FastMCP wrapper around shared business logic."""
    return get_customer_profile(customer_id, db_manager)
```

**STDIO Server:**
```python
from .shared import get_customer_profile, DatabaseManager

def get_customer_profile_wrapper(customer_id: int) -> Dict[str, Any]:
    """STDIO wrapper around shared business logic."""
    result = get_customer_profile(customer_id, db_manager)
    if "error" in result:
        return {"success": False, "error": result["error"]}
    return {"success": True, "customer": result}
```

### **Key Benefits of This Pattern:**

1. **Single Source of Truth**: Business logic exists in one place
2. **Protocol Separation**: MCP handling remains distinct per server
3. **Easy Maintenance**: Add new tools by updating shared components
4. **Consistent Behavior**: Both servers behave identically
5. **Educational Value**: Students see both patterns clearly

## 🛠️ **Available Tools**

Both servers provide the same set of tools:

### **Customer Management**
- `get_customer_profile(customer_id)` - Retrieve customer information
- `create_customer(name, email, phone, date_of_birth)` - Create new customer

### **Transaction Management**
- `add_transaction(customer_id, amount, category, ...)` - Add new transaction
- `get_transactions_by_customer(customer_id, ...)` - Get customer transactions
- `get_spending_summary(customer_id, months)` - Get spending analysis

### **Financial Goals**
- `create_financial_goal(customer_id, goal_name, ...)` - Create new goal
- `get_financial_goals(customer_id, status)` - Get customer goals
- `update_goal_progress(goal_id, current_amount)` - Update goal progress

### **Advice & Logging**
- `save_advice(customer_id, agent_name, ...)` - Save agent advice
- `get_advice_history(customer_id, ...)` - Get advice history
- `log_agent_interaction(session_id, ...)` - Log agent interactions
- `get_spending_categories()` - Get available categories

## 🎓 **Learning Exercises**

### **Exercise 1: Understanding the Architecture**
1. Compare `database_server.py` and `database_server_stdio.py`
2. Identify what's different between them (MCP protocol handling)
3. Identify what's the same (business logic calls)
4. Explain why this separation is beneficial

### **Exercise 2: Adding a New Tool**
1. Add a new function to `shared/business_logic.py`
2. Add the corresponding tool to both servers
3. Test that both servers work with the new tool
4. Observe how DRY principles make this easy

### **Exercise 3: Exploring Shared Components**
1. Study the `shared/` folder structure
2. Understand how each component works
3. Identify the dependencies between components
4. Explain how this structure improves maintainability

### **Exercise 4: Protocol Differences**
1. Run both servers and compare their behavior
2. Understand the difference between FastMCP decorators and STDIO handling
3. Identify when you'd use each approach
4. Consider the trade-offs of each method

### **Exercise 5: ADK Integration Updates**
1. Study the ADK integration section above
2. Compare the old vs. new ADK usage patterns
3. Understand why `StdioConnectionParams` wraps `StdioServerParameters`
4. Learn how to adapt to library deprecations in real projects
5. Practice updating agent configurations to use the new pattern

## 🔧 **Development Workflow**

### **Adding New Features:**
1. **Add to shared components first** - Update `shared/business_logic.py`
2. **Update both servers** - Add wrapper functions to both files
3. **Test both implementations** - Ensure they work identically
4. **Update documentation** - Keep this README current

### **Fixing Bugs:**
1. **Fix in shared components** - The fix applies to both servers automatically
2. **Test both servers** - Verify the fix works everywhere
3. **No duplication** - You only need to fix it once!

## 📚 **Key Concepts Demonstrated**

### **1. DRY Principles**
- **Don't Repeat Yourself**: Business logic exists in one place
- **Single Source of Truth**: Changes apply everywhere automatically
- **Maintainability**: Easier to update and debug

### **2. Separation of Concerns**
- **Business Logic**: Pure functions in `shared/business_logic.py`
- **Protocol Handling**: Server-specific MCP implementation
- **Configuration**: Centralized in `shared/config.py`

### **3. Dependency Injection**
- **Flexible Design**: Functions take `db_manager` as parameter
- **Testability**: Easy to mock dependencies for testing
- **Reusability**: Same functions work in different contexts

### **4. Professional Code Organization**
- **Modular Structure**: Clear separation of responsibilities
- **Import Management**: Clean, organized imports
- **Documentation**: Comprehensive docstrings and comments

### **5. Library Evolution and Deprecation Handling**
- **Adapting to Changes**: How to update code when libraries evolve
- **Backward Compatibility**: Understanding deprecation warnings
- **Future-proofing**: Using current, non-deprecated APIs
- **Real-world Updates**: Practical experience with library updates

## 🚨 **Common Pitfalls to Avoid**

### **1. Don't Mix Protocol and Business Logic**
❌ **Bad:**
```python
@mcp.tool()
def get_customer_profile(customer_id: int):
    # Business logic mixed with MCP protocol
    query = "SELECT * FROM customers WHERE id = %s"
    # ... database code here
```

✅ **Good:**
```python
# In shared/business_logic.py
def get_customer_profile(customer_id: int, db_manager: DatabaseManager):
    # Pure business logic
    # ... database code here

# In database_server.py
@mcp.tool()
def get_customer_profile_tool(customer_id: int):
    return get_customer_profile(customer_id, db_manager)
```

### **2. Don't Duplicate Business Logic**
❌ **Bad:** Copy-paste the same function to both servers
✅ **Good:** Put it in shared components and import it

### **3. Don't Forget Error Handling**
❌ **Bad:** Let errors bubble up without proper handling
✅ **Good:** Handle errors consistently in shared components

### **4. Don't Use Deprecated APIs**
❌ **Bad:** Ignoring deprecation warnings and using old APIs
```python
# Old, deprecated approach
from google.adk.tools.mcp_tool.mcp_toolset import StdioServerParameters
MCPToolset(connection_params=StdioServerParameters(...))
```

✅ **Good:** Use current, non-deprecated APIs
```python
# New, current approach
from google.adk.tools.mcp_tool.mcp_toolset import StdioConnectionParams
from mcp.client.stdio import StdioServerParameters
MCPToolset(connection_params=StdioConnectionParams(
    server_params=StdioServerParameters(...)
))
```

## 🎯 **Next Steps**

1. **Study the Code**: Read through both server implementations
2. **Run the Servers**: Test both implementations
3. **Experiment**: Try adding new tools or modifying existing ones
4. **Understand DRY**: See how shared components reduce duplication
5. **Apply the Pattern**: Use these concepts in your own projects

## 💡 **Key Takeaways**

- **DRY principles** make code more maintainable and less error-prone
- **Separation of concerns** makes code easier to understand and test
- **Shared components** can preserve educational value while reducing duplication
- **Professional code organization** is essential for larger projects
- **Both approaches** (FastMCP and STDIO) have their place in different contexts
- **Library evolution** is a reality - learn to adapt to deprecations and updates
- **Future-proofing** your code saves time and prevents technical debt

This implementation demonstrates how to balance educational value with professional software engineering practices. You get to see both MCP patterns clearly while learning how to structure code for maintainability, reusability, and adaptability to library changes! 🚀

---

**Happy Learning!** 🎓

*Remember: The best way to understand this code is to read it, run it, and experiment with it. Don't just read the documentation - dive into the code and see how it works!*
