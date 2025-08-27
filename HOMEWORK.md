# 📚 HOMEWORK: Complete ADK+MCP Financial Advisor Implementation

## 🎯 Assignment Overview

Your task is to implement a **production-ready Financial Advisor AI system** using only **Google's Agent Development Kit (ADK)** and **Model Context Protocol (MCP)** for MySQL connectivity. This assignment eliminates all custom database code and simulations to create a fully framework-native application.

## 🏆 Learning Objectives

By completing this homework, you will:
- Master Google ADK for production agent development
- Implement real MCP protocol for database connectivity
- Understand enterprise-grade AI agent architecture
- Build scalable, framework-native applications
- Follow Google's recommended patterns and best practices

## 📋 Assignment Requirements

### ✅ **Must Have**
- **100% ADK-based**: All agents must use Google ADK framework
- **Real MCP Integration**: Use actual MCP toolset for MySQL (no simulations)
- **No Direct DB Access**: Remove all custom database code (`financial_mcp/`)
- **Production Ready**: Error handling, logging, monitoring
- **Framework Native**: Follow Google's patterns throughout

### ❌ **Not Allowed**
- Direct SQLAlchemy or MySQL connector usage
- Custom database managers or servers
- Simulated MCP tools or responses
- Direct imports from `financial_mcp/` module
- Custom orchestrators (use ADK's built-in coordination)

## 🏗️ Implementation Steps

### **Phase 1: MCP Server Setup** ⭐ **[25 points]**

#### 1.1 Install MCP Dependencies
```bash
# Install MCP toolbox for databases
pip install toolbox-core
pip install mcp-server-mysql  # If available

# Or install from source if needed
git clone https://github.com/google/mcp-toolbox-databases
cd mcp-toolbox-databases
pip install -e .
```

#### 1.2 Configure MCP MySQL Server
Create `mcp_server_config.json`:
```json
{
  "server": {
    "name": "financial-advisor-mcp",
    "version": "1.0.0"
  },
  "database": {
    "type": "mysql",
    "host": "localhost",
    "port": 3306,
    "database": "financial_advisor",
    "username": "root",
    "password": ""
  },
  "tools": [
    "get_customer_profile",
    "get_transactions",
    "get_goals", 
    "create_transaction",
    "update_goal",
    "execute_query"
  ]
}
```

#### 1.3 Create MCP Server Script
Create `financial_mcp_server.py`:
```python
#!/usr/bin/env python3
"""
Production MCP Server for Financial Advisor Database Access.
"""
from mcp import Server, Tool
import mysql.connector
import json
from typing import Dict, Any, List

# TODO: Implement complete MCP server with all financial tools
# - Customer management tools
# - Transaction management tools  
# - Goal management tools
# - Analysis and reporting tools
# - Schema introspection tools
```

📚 **Reference Implementation**: See `adk_agents_mcp/mcp_database_config.py` for:
- `ExampleMCPTools.get_customer_profile()` - Complete example implementation
- `ExampleMCPTools.get_mcp_tool_template()` - Code generation helper
- `ExampleMCPTools.get_all_tool_templates()` - Templates for all required tools

**Deliverable**: Working MCP server that provides all database operations

### **Phase 2: ADK Agent Implementation** ⭐ **[35 points]**

#### 2.1 Remove All Custom Database Code
```bash
# Delete custom database implementations
rm -rf financial_mcp/
rm -rf adk_agents/  # Keep only as reference
rm -rf adk_agents_mcp/  # Keep only as reference

# Create new ADK-only implementation
mkdir adk_production/
```

#### 2.2 Implement Pure ADK Agents
Create `adk_production/spending_agent.py`:
```python
from google.adk import Agent
from google.adk.tools import MCPToolset
from google.adk.tools.mcp_tool.mcp_toolset import StdioConnectionParams

class SpendingAnalyzerAgent:
    def __init__(self):
        # Real MCP toolset (no simulation)
        self.mcp_toolset = MCPToolset(
            connection_params=StdioConnectionParams(
                command='python',
                args=['financial_mcp_server.py']
            ),
            tool_filter=[
                'get_customer_profile',
                'get_transactions', 
                'execute_query'
            ]
        )
        
        # Pure ADK agent with MCP tools
        self.agent = Agent(
            name="spending_analyzer",
            model="gemini-1.5-flash",
            description="Analyzes spending patterns using MCP database tools",
            instruction=self._get_system_prompt(),
            tools=[self.mcp_toolset]
        )
    
    def _get_system_prompt(self) -> str:
        return """
        You are a Financial Spending Analyzer with access to MCP database tools.
        
        Available MCP Tools:
        - get_customer_profile(customer_id): Get customer information
        - get_transactions(customer_id, start_date, end_date): Get transaction data
        - execute_query(sql, params): Execute custom SQL queries
        
        Use these tools to analyze spending patterns and provide insights.
        """
    
    async def analyze_spending(self, customer_id: int) -> Dict[str, Any]:
        # TODO: Implement using only ADK agent with MCP tools
        # - Use agent.run() with MCP tool integration
        # - Let ADK handle all tool calling
        # - Return structured results
        pass
```

**Deliverable**: Three complete ADK agents (Spending, Goal, Advisor) using only MCP tools

#### 2.3 Implement ADK Orchestration
Create `adk_production/orchestrator.py`:
```python
from google.adk import Agent
from google.adk.agents import Sequential, Parallel
from .spending_agent import SpendingAnalyzerAgent
from .goal_agent import GoalPlannerAgent  
from .advisor_agent import AdvisorAgent

class FinancialAdvisorOrchestrator:
    def __init__(self):
        # Use ADK's built-in orchestration
        self.workflow = Sequential([
            Parallel([
                SpendingAnalyzerAgent(),
                GoalPlannerAgent()
            ]),
            AdvisorAgent()
        ])
    
    async def run_analysis(self, customer_id: int):
        # TODO: Use ADK orchestration patterns
        # - No custom workflow management
        # - Use ADK's Sequential/Parallel agents
        # - Let framework handle coordination
        pass
```

### **Phase 3: UI Integration** ⭐ **[20 points]**

#### 3.1 Update Streamlit UI
Modify `ui/main.py` to use only ADK agents:
```python
# Remove all imports from financial_mcp/
# Remove custom database server imports
# Import only ADK production agents

from adk_production.orchestrator import FinancialAdvisorOrchestrator

def render_ai_analysis(customer_id: int):
    # TODO: Update to use only ADK orchestrator
    # - Remove framework selection (ADK only)
    # - Use ADK async patterns with Streamlit
    # - Handle ADK responses properly
    pass
```

#### 3.2 Implement ADK-Native UI Patterns
```python
import asyncio
import streamlit as st

@st.cache_resource
def get_orchestrator():
    return FinancialAdvisorOrchestrator()

async def run_adk_analysis(customer_id: int):
    orchestrator = get_orchestrator()
    return await orchestrator.run_analysis(customer_id)

def display_adk_results(results):
    # TODO: Handle pure ADK results
    # - Parse ADK agent responses
    # - Display MCP tool outputs
    # - Show framework metadata
    pass
```

### **Phase 4: Testing & Validation** ⭐ **[15 points]**

#### 4.1 Create Comprehensive Test Suite
Create `test_production_adk.py`:
```python
import pytest
import asyncio
from adk_production.orchestrator import FinancialAdvisorOrchestrator

class TestProductionADK:
    def test_mcp_server_connection(self):
        """Test MCP server is running and accessible."""
        # TODO: Verify MCP server connectivity
        pass
    
    def test_adk_agents_initialization(self):
        """Test all ADK agents initialize properly."""
        # TODO: Test agent creation with MCP toolsets
        pass
    
    async def test_spending_analysis(self):
        """Test spending analysis through pure ADK."""
        # TODO: Test complete spending analysis workflow
        pass
    
    async def test_orchestrator_workflow(self):
        """Test full orchestrator workflow."""
        # TODO: Test end-to-end ADK orchestration
        pass
    
    def test_no_custom_db_imports(self):
        """Verify no custom database code is imported."""
        import sys
        assert 'financial_mcp' not in sys.modules
        # TODO: Add more import verification
```

#### 4.2 Performance & Load Testing
```python
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def test_adk_performance():
    """Test ADK performance with multiple concurrent requests."""
    # TODO: Implement performance benchmarks
    # - Test concurrent agent execution
    # - Measure MCP tool call latency
    # - Compare with baseline performance
    pass
```

### **Phase 5: Documentation** ⭐ **[5 points]**

#### 5.1 Create Deployment Guide
Create `DEPLOYMENT.md`:
```markdown
# Production ADK Deployment Guide

## Prerequisites
- Google Cloud account with ADK access
- MySQL database server
- MCP toolbox installation

## Setup Steps
1. Configure MCP server
2. Deploy ADK agents
3. Set up monitoring
4. Configure scaling

## Production Considerations
- Error handling and recovery
- Logging and monitoring
- Security and authentication
- Performance optimization
```

#### 5.2 Update Documentation
- Update `README.md` to reflect ADK-only approach
- Create API documentation for MCP tools
- Document performance characteristics
- Add troubleshooting guide

## 📊 Grading Rubric

| Component | Points | Criteria |
|-----------|--------|----------|
| **MCP Server** | 25 | Working MySQL MCP server with all tools |
| **ADK Agents** | 35 | Pure ADK implementation, no custom DB code |
| **UI Integration** | 20 | Streamlit UI using only ADK agents |
| **Testing** | 15 | Comprehensive test suite with validation |
| **Documentation** | 5 | Clear deployment and usage documentation |
| **TOTAL** | **100** | |

### **Bonus Points** ⭐ **[+10 points]**
- **Production Deployment**: Deploy to Google Cloud with real scaling
- **Advanced MCP Tools**: Custom MCP tools for complex financial analysis
- **Monitoring Integration**: Add observability and metrics
- **Security Implementation**: Authentication and authorization

## 🚀 Getting Started

### **Step 1: Environment Setup**
```bash
# Clone the repository
git clone https://github.com/pablomoralesm/agent-ai-personal-financial-advisor.git
cd agent-ai-personal-financial-advisor
git checkout feature/google-adk-implementation

# Create new branch for homework
git checkout -b homework/adk-mcp-production

# Set up environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Install additional MCP dependencies
pip install toolbox-core
```

### **Step 2: Study Existing Implementation**
Before starting, study the reference implementations:
- `adk_agents/` - ADK implementation patterns
- `adk_agents_mcp/` - MCP integration examples  
- `MCP_IMPLEMENTATION_GUIDE.md` - MCP documentation
- `ADK_COMPARISON.md` - Framework comparison

### **Step 3: Plan Your Implementation**
Create a detailed plan addressing:
- MCP server architecture
- ADK agent design
- Tool integration strategy
- Testing approach
- Deployment considerations

## 📚 Resources

### **Official Documentation**
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [MCP Toolbox for Databases](https://cloud.google.com/blog/products/ai-machine-learning/mcp-toolbox-for-databases)
- [ADK Tutorials](https://google.github.io/adk-docs/tutorials/)

### **Reference Implementations**
- `adk_agents_mcp/mcp_database_config.py` - **ExampleMCPTools** class with complete tool examples
- Current project's `adk_agents_mcp/` for MCP patterns
- Google's ADK samples repository
- MCP server examples

### **Code Templates Available**
```python
# Import the example tools for reference
from adk_agents_mcp.mcp_database_config import example_mcp_tools

# Get template code for all tools
templates = example_mcp_tools.get_all_tool_templates()

# Get specific tool template
customer_profile_template = templates['get_customer_profile']
print(customer_profile_template)  # Shows complete implementation
```

### **Tools & Libraries**
- `google-adk` - Google Agent Development Kit
- `toolbox-core` - MCP toolbox core functionality
- `mysql-connector-python` - For MCP server (not direct use)

## ⚠️ Common Pitfalls to Avoid

1. **Direct Database Access**: No SQLAlchemy or direct MySQL calls in agents
2. **Simulation Code**: Remove all simulated MCP responses
3. **Custom Orchestration**: Use ADK's built-in orchestration only
4. **Import Violations**: Don't import from `financial_mcp/` module
5. **Framework Mixing**: Keep implementation purely ADK-based

## 🎉 Success Criteria

Your implementation is successful when:
- ✅ MCP server provides all database operations
- ✅ ADK agents use only MCP tools (no direct DB access)
- ✅ Streamlit UI works with pure ADK implementation
- ✅ All tests pass without custom database code
- ✅ Application is production-ready and scalable

## 📞 Getting Help
- **Documentation**: Refer to `MCP_IMPLEMENTATION_GUIDE.md`
- **Examples**: Study the reference implementations in the repository

## 📅 Deliverables & Timeline

### **Week 1**: MCP Server & Basic ADK Setup
- Working MCP server with database connectivity
- Basic ADK agent with MCP integration
- Initial test framework

### **Week 2**: Complete ADK Implementation
- All three agents implemented
- ADK orchestration working
- UI integration complete

### **Week 3**: Testing & Documentation
- Comprehensive test suite
- Performance validation
- Documentation complete

### **Final goal**
- Complete working application
- All tests passing
- Deployment-ready code
- Comprehensive documentation

---

**Good luck!** This homework will give you hands-on experience with enterprise-grade AI agent development using industry-standard frameworks and protocols. 🚀
