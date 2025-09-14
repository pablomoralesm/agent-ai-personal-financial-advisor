# ADK Web Multi-Agent System

This directory contains the multi-agent system for ADK Web, implementing a comprehensive financial advisory system with specialized agents and intelligent orchestration.

## 🏗️ **Architecture Overview**

The ADK Web system provides **six specialized agents** that work together to provide comprehensive financial advisory services:

### 1. **Standalone Financial Advisor** (`standalone/`)
- **Purpose**: Pure MCP-only financial advisor with direct database access
- **Pattern**: Direct agent with full MCP tool access, no orchestration complexity
- **Use Case**: Complete financial analysis and advice generation in one step
- **Deployment**: Works independently, demonstrates pure MCP tool usage

### 2. **Orchestrator Agent** (`orchestrator/`)
- **Purpose**: Intelligent coordination of specialized agents
- **Pattern**: LLM-driven orchestration with adaptive decision-making
- **Use Case**: Complex financial scenarios requiring multiple specialized analyses
- **Deployment**: Production scenarios with intelligent agent selection

### 3. **Sequencer Agent** (`sequencer/`)
- **Purpose**: Step-by-step multi-agent coordination
- **Pattern**: Sequential execution of specialized agents
- **Use Case**: Educational and systematic financial analysis workflow
- **Deployment**: Transparent process with clear step-by-step execution

### 4. **Spending Analyzer Agent** (`spending_analyzer/`)
- **Purpose**: Specialized spending pattern analysis
- **Pattern**: Focused analysis with MCP database tools
- **Use Case**: Detailed transaction analysis and spending optimization
- **Deployment**: Part of multi-agent workflows

### 5. **Goal Planner Agent** (`goal_planner/`)
- **Purpose**: Financial goal planning and feasibility analysis
- **Pattern**: Goal-focused analysis with database integration
- **Use Case**: Savings planning and goal prioritization
- **Deployment**: Part of multi-agent workflows

### 6. **Advisor Agent** (`advisor/`)
- **Purpose**: Financial advice synthesis and recommendations
- **Pattern**: Advice generation with comprehensive analysis
- **Use Case**: Final recommendations and action items
- **Deployment**: Part of multi-agent workflows

## 🚀 **Getting Started**

### **Starting ADK Web**
```bash
# Navigate to project root
cd /path/to/agent-ai-personal-financial-advisor

# Activate virtual environment
source venv/bin/activate

# Start ADK Web with the agents directory
adk web adk_web_agents
```

### **Agent Selection**
When you start ADK Web, you'll see six available agents:

1. **`standalone`** - Pure MCP-only Financial Advisor (complete analysis in one step)
2. **`orchestrator`** - Intelligent Orchestrator (AI-driven multi-agent coordination)
3. **`sequencer`** - Sequential Orchestrator (step-by-step multi-agent workflow)
4. **`spending_analyzer`** - Spending Analysis Specialist
5. **`goal_planner`** - Financial Goal Planning Specialist
6. **`advisor`** - Financial Advice Synthesis Specialist

## 🎯 **Agent Capabilities**

### **Standalone Financial Advisor**
- ✅ Complete financial analysis in one step
- ✅ Direct MCP database tool access
- ✅ Comprehensive advice generation
- ✅ Independent operation
- ✅ Pure MCP-only implementation (no orchestration complexity)

### **Orchestrator Agent**
- ✅ Intelligent multi-agent coordination
- ✅ Dynamic agent selection based on request
- ✅ Adaptive analysis approach
- ✅ Complex scenario handling
- ✅ Production-ready reasoning

### **Sequencer Agent**
- ✅ Step-by-step multi-agent execution
- ✅ Transparent workflow visibility
- ✅ Educational process demonstration
- ✅ Predictable sequential results
- ✅ Specialized agent delegation

### **Specialized Agents**
- ✅ **Spending Analyzer**: Transaction analysis, spending patterns, optimization
- ✅ **Goal Planner**: Financial goal evaluation, savings planning, feasibility
- ✅ **Advisor**: Advice synthesis, recommendations, action items
- ✅ All agents automatically save their analysis to the database
- ✅ Seamless integration with MCP database tools

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

### **Sequencer Agent Workflow**
1. **Spending Analyzer Agent** → Analyzes transactions and spending patterns
2. **Goal Planner Agent** → Evaluates financial goals and creates savings plans
3. **Advisor Agent** → Synthesizes comprehensive recommendations
4. **Results Collection** → Aggregates all analysis results

### **Orchestrator Agent Workflow**
- **Dynamic**: AI decides which agents to use based on request
- **Adaptive**: Adjusts approach based on intermediate results
- **Flexible**: Can skip or repeat steps as needed
- **Intelligent**: Uses LLM reasoning to coordinate specialized agents

### **Specialized Agent Integration**
- **Database Access**: All agents use MCP tools for data retrieval
- **Automatic Saving**: Each agent saves its analysis using `save_advice`
- **Data Sharing**: Agents can reference previous analysis results
- **Session State**: Results stored automatically for future reference

## 🎓 **Educational Value**

### **Sequencer Agent**
- **Learning**: See exactly how agents coordinate step-by-step
- **Transparency**: Clear sequential process with visible agent execution
- **Debugging**: Easy to understand and troubleshoot each step
- **Educational**: Perfect for learning multi-agent system fundamentals

### **Orchestrator Agent**
- **Advanced**: See AI-driven decision making in action
- **Production**: Real-world intelligent orchestration patterns
- **Flexibility**: Adaptive multi-agent coordination based on context
- **LLM Integration**: Learn how LLMs can coordinate specialized agents

### **Specialized Agents**
- **Focused Learning**: Understand single-purpose agent design
- **Tool Integration**: Learn MCP tool usage patterns
- **Database Interaction**: See how agents interact with data sources
- **Modular Design**: Understand composable agent architecture

## 🚀 **Next Steps**

1. **Test All Agents**: Try each agent with different financial scenarios
2. **Compare Approaches**: See how standalone vs multi-agent approaches differ
3. **Multi-Agent Workflows**: Test the Sequencer and Orchestrator agents
4. **Specialized Analysis**: Use individual specialized agents for focused analysis
5. **Custom Scenarios**: Create your own financial analysis requests
6. **Integration**: Use agents in your own applications

## 🆕 **Recent Improvements**

### **Enhanced Agent Instructions**
- **Tool Discovery**: Agents now rely on ADK framework for automatic tool discovery
- **Atomic Operations**: Advice generation and saving combined into single `save_advice` calls
- **Cleaner Instructions**: Removed explicit tool listings, letting ADK handle tool management
- **Mandatory Saving**: All agents automatically save their analysis to the database

### **Improved Architecture**
- **Specialized Agents**: Clear separation of concerns with focused agent responsibilities
- **Intelligent Orchestration**: LLM-driven coordination with adaptive decision-making
- **Sequential Execution**: Step-by-step multi-agent workflows for educational purposes
- **Database Integration**: Seamless MCP tool usage for all database operations

### **Better User Experience**
- **Automatic Saving**: No need to manually save analysis results
- **Session State**: Results automatically stored for future reference
- **Clear Workflows**: Transparent agent execution with visible progress
- **Comprehensive Analysis**: Multi-agent collaboration for thorough financial advice

## 📖 **Related Documentation**

- [MCP Server Documentation](../mcp_server/README.md)
- [Main Project README](../README.md)

---

**Part of the Agentic AI Personal Financial Advisor application.**
