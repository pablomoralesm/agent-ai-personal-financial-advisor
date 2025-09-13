# Fix StdioServerParameters Warning Plan

## 🎯 **Objective**
Update all agent configurations to use the new `StdioConnectionParams` instead of the deprecated `StdioServerParameters` to eliminate ADK warnings.

## 🔍 **Root Cause**
ADK library has been updated and `StdioServerParameters` is now deprecated. The new approach uses `StdioConnectionParams` which wraps the old parameters.

## 📋 **Files to Update**

### 1. **Agent Files** (4 files)
- `agents/spending_analyzer.py`
- `agents/goal_planner.py` 
- `agents/advisor.py`
- `agents/orchestrator.py` (if it has direct MCP usage)

### 2. **Documentation Files** (2 files)
- `ADK_INSIGHTS.md`
- `TDR_HIGH_PRIORITY_ENHANCEMENTS.md`

### 3. **Test Files** (1 file)
- `tests/conftest.py`

## 🔧 **Implementation Steps**

### **Step 1: Update Import Statements**

**Old:**
```python
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
```

**New:**
```python
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams
from mcp.client.stdio import StdioServerParameters
```

### **Step 2: Update MCPToolset Configuration**

**Old:**
```python
MCPToolset(
    connection_params=StdioServerParameters(
        command='python3',
        args=[mcp_server_path]
    )
)
```

**New:**
```python
MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command='python3',
            args=[mcp_server_path]
        )
    )
)
```

### **Step 3: Update Documentation**

Update all documentation to reflect the new usage pattern.

### **Step 4: Update Tests**

Update mock configurations in test files.

## ✅ **Verification Steps**

1. **Run Agent Tests**: Verify all agents still initialize correctly
2. **Check Warnings**: Confirm no more StdioServerParameters warnings
3. **Test MCP Connection**: Verify database tools still work
4. **Run Full Test Suite**: Ensure no regressions

## 🚀 **Expected Outcome**

- ✅ No more deprecation warnings
- ✅ All agents continue to work correctly
- ✅ MCP database tools remain functional
- ✅ Code uses current ADK best practices
- ✅ Future-proof against ADK updates

## 📊 **Impact Assessment**

- **Risk Level**: LOW - This is a straightforward parameter update
- **Breaking Changes**: NONE - Functionality remains identical
- **Testing Required**: Basic smoke tests to verify functionality
- **Rollback Plan**: Simple - revert import and parameter changes

## 🎯 **Success Criteria**

1. All agent initialization warnings eliminated
2. All agents continue to function correctly
3. MCP database tools remain accessible
4. No new errors introduced
5. Documentation updated to reflect new patterns
