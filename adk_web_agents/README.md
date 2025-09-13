# ADK Web Multi-Agent System

This directory contains the multi-agent system for ADK Web, implementing the hybrid orchestration approach from our unified architecture.

## 🏗️ **Architecture Overview**

The ADK Web system provides **three different agent types** to demonstrate different orchestration patterns:

### 1. **Unified Financial Advisor** (`financial_advisor/`)
- **Purpose**: Standalone comprehensive financial advisor
- **Pattern**: Direct agent with full MCP tool access
- **Use Case**: General financial analysis and advice
- **Deployment**: Works independently

### 2. **Procedural Orchestrator** (`procedural_orchestrator/`)
- **Purpose**: Educational, step-by-step multi-agent coordination
- **Pattern**: Procedural orchestration with transparent workflow
- **Use Case**: Learning how multi-agent systems work
- **Deployment**: Educational focus, clear process visibility

### 3. **Intelligent Orchestrator** (`intelligent_orchestrator/`)
- **Purpose**: Dynamic, AI-driven multi-agent coordination
- **Pattern**: Intelligent orchestration with adaptive decision-making
- **Use Case**: Production scenarios with complex financial analysis
- **Deployment**: Advanced reasoning, flexible coordination

## 🚀 **Getting Started**

### **Starting ADK Web**
```bash
# Navigate to project root
cd /path/to/agent-ai-personal-financial-advisor

# Activate virtual environment
source venv/bin/activate

# Start ADK Web
adk web
```

### **Agent Selection**
When you start ADK Web, you'll see three available agents:

1. **`financial_advisor`** - Unified Financial Advisor
2. **`procedural_orchestrator`** - Procedural Orchestrator  
3. **`intelligent_orchestrator`** - Intelligent Orchestrator

## 🎯 **Agent Capabilities**

### **Unified Financial Advisor**
- ✅ Direct financial analysis
- ✅ Full MCP tool access
- ✅ Comprehensive advice
- ✅ Standalone operation

### **Procedural Orchestrator**
- ✅ Step-by-step analysis process
- ✅ Transparent agent coordination
- ✅ Educational workflow visibility
- ✅ Predictable results

### **Intelligent Orchestrator**
- ✅ Dynamic agent selection
- ✅ Adaptive analysis approach
- ✅ Complex scenario handling
- ✅ Production-ready reasoning

## 🔧 **Technical Details**

### **MCP Integration**
All agents use the same MCP server configuration:
- **Server**: `mcp_server/database_server_stdio.py`
- **Protocol**: JSON-RPC 2.0
- **Tools**: 12 financial database tools

### **Model Configuration**
- **Model**: `gemini-2.0-flash-exp`
- **Context**: ADK Web deployment
- **Tools**: MCPToolset with StdioConnectionParams

### **Agent Discovery**
Each agent directory contains:
- `__init__.py` - Exports `root_agent` for ADK Web discovery
- `agent.py` - Main agent implementation

## 📚 **Usage Examples**

### **Basic Financial Analysis**
```
"Analyze my spending patterns for the last 3 months"
```

### **Goal Planning**
```
"Help me create a savings plan for a $50,000 house down payment"
```

### **Comprehensive Review**
```
"Give me a complete financial health assessment"
```

## 🔄 **Multi-Agent Coordination**

### **Procedural Orchestrator Workflow**
1. **Spending Analysis Agent** → Analyzes transactions
2. **Goal Planning Agent** → Evaluates goals
3. **Advisor Agent** → Synthesizes recommendations

### **Intelligent Orchestrator Workflow**
- **Dynamic**: AI decides agent sequence based on request
- **Adaptive**: Adjusts approach based on intermediate results
- **Flexible**: Can skip or repeat steps as needed

## 🎓 **Educational Value**

### **Procedural Orchestrator**
- **Learning**: See exactly how agents coordinate
- **Transparency**: Clear step-by-step process
- **Debugging**: Easy to understand and troubleshoot

### **Intelligent Orchestrator**
- **Advanced**: See AI-driven decision making
- **Production**: Real-world orchestration patterns
- **Flexibility**: Adaptive multi-agent coordination

## 🚀 **Next Steps**

1. **Test All Agents**: Try each agent with different financial scenarios
2. **Compare Approaches**: See how procedural vs intelligent orchestration differ
3. **Custom Scenarios**: Create your own financial analysis requests
4. **Integration**: Use agents in your own applications

## 📖 **Related Documentation**

- [Multi-Agent Architecture Plan](../MULTI_AGENT_ARCHITECTURE_PLAN.md)
- [Unified Agent System](../agents/unified/README.md)
- [MCP Server Documentation](../mcp_server/README.md)

---

**Part of the Agentic AI Personal Financial Advisor application.**
