# Google Agent Development Kit (ADK) - Implementation Insights

This document contains essential information extracted from the ADK documentation for implementing the Personal Financial Advisor app.

## Core ADK Concepts

### 1. Agent Types
- **LlmAgent/Agent**: Core intelligent agent powered by LLMs (like Gemini)
- **BaseAgent**: Foundation class for custom agents with arbitrary orchestration logic
- **Workflow Agents**: SequentialAgent, ParallelAgent, LoopAgent for structured processes

### 2. Agent Development Kit Architecture
- **Model-agnostic**: Works with various LLMs but optimized for Gemini
- **Deployment-agnostic**: Can deploy anywhere (Cloud Run, Vertex AI, etc.)
- **Framework-compatible**: Built for compatibility with other frameworks

## Key Implementation Patterns

### 1. Basic Agent Creation
```python
from google.adk.agents import LlmAgent, BaseAgent

# Simple LLM Agent
agent = LlmAgent(
    name="agent_name",
    model="gemini-2.0-flash",  # Cost-effective Gemini model
    instruction="Agent instructions here",
    description="Agent description",
    tools=[...],  # List of tools
    sub_agents=[...]  # List of sub-agents for multi-agent systems
)
```

### 2. Custom Agent Implementation
```python
class CustomAgent(BaseAgent):
    def __init__(self, sub_agents, **kwargs):
        super().__init__(sub_agents=sub_agents, **kwargs)
        # Store sub-agents as instance attributes
        
    async def _run_async_impl(self, ctx):
        # Custom orchestration logic
        # Access state via ctx.session.state
        # Call sub-agents via self.sub_agent.run_async(ctx)
        pass
```

### 3. Multi-Agent Systems
- Agents can have `sub_agents` for hierarchical organization
- Use `ctx.session.state` for sharing data between agents
- Agents can communicate through state management

## MCP (Model Context Protocol) Integration

### 1. MCPToolset Class
```python
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams
from mcp.client.stdio import StdioServerParameters

# Using MCP tools in agents
agent = LlmAgent(
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='python3',
                    args=['path/to/mcp_server.py']
                )
            )
        )
    ]
)
```

### 2. MCP Server Implementation
- MCP servers expose tools to agents via the MCP protocol
- Agents use MCPToolset to connect to MCP servers
- MCP handles database interactions, external APIs, etc.

### 3. Database MCP Integration
- Use MCP Toolbox for Databases for enterprise-grade database access
- Handles connection pooling, authentication, security
- Supports MySQL, PostgreSQL, SQLite, and other databases

## Multi-Agent Communication (Built-in ADK Capabilities)

### 1. Session State Sharing
```python
# Agents share data through session state
ctx.session.state["key"] = value
data = ctx.session.state.get("key")
```

### 2. AgentTool for Direct Delegation
```python
from google.adk.tools import agent_tool

# One agent can call another as a tool
advisor = LlmAgent(
    tools=[agent_tool.AgentTool(agent=other_agent)]
)
```

### 3. Hierarchical Agent Structure
```python
# Parent-child agent relationships
coordinator = LlmAgent(
    sub_agents=[agent1, agent2, agent3]
)
```

### 4. When A2A is Needed
- **A2A is only for remote/distributed agents** across different processes/servers
- **For local multi-agent systems**, use built-in ADK capabilities
- Our educational app uses local agents, so A2A is not required

## Recommended Gemini Models

### 1. Cost-Effective Options
- **gemini-2.0-flash**: Best for most use cases, cost-effective
- **gemini-1.5-flash**: Alternative flash model
- **gemini-1.5-pro**: For more complex reasoning (higher cost)

### 2. Model Selection Criteria
- Flash models: Fast, cost-effective, good for most tasks
- Pro models: Better reasoning, higher cost
- All support tool calling (required for our use case)

## Tools and Toolsets

### 1. Tool Types
- **FunctionTool**: Wraps Python functions
- **BaseTool**: Custom tool implementation
- **AgentTool**: Enables agent-to-agent delegation
- **MCPToolset**: Connects to MCP servers

### 2. Tool Integration
```python
# Adding tools to agents
agent = LlmAgent(
    tools=[
        my_function,  # Auto-wrapped as FunctionTool
        CustomTool(),  # BaseTool instance
        MCPToolset(...),  # MCP server connection
        AgentTool(other_agent)  # Agent delegation
    ]
)
```

## Session and State Management

### 1. Session State
```python
# Accessing shared state
ctx.session.state["key"] = value
data = ctx.session.state.get("key")
```

### 2. State Persistence
- InMemorySessionService: For development/testing
- Database-backed sessions: For production
- State survives across agent interactions

## Installation and Setup

### 1. Required Packages
```bash
pip install google-adk>=1.13.0
# Note: a2a package not needed for local multi-agent systems
```

### 2. Environment Configuration
- GOOGLE_API_KEY: For Gemini model access
- Database connection parameters
- Other service credentials as needed

## Development Best Practices

### 1. Agent Design
- Keep agents focused on specific tasks
- Use clear instructions and descriptions
- Implement proper error handling
- Use structured data exchange (input_schema, output_schema)

### 2. Multi-Agent Coordination
- Use hierarchical agent structures
- Share data through session state
- Implement proper agent lifecycle management
- Use A2A only for distributed/remote scenarios (not needed for local agents)

### 3. Tool Development
- Implement tools as MCP servers for reusability
- Use proper authentication and authorization
- Handle database connections through MCP toolsets
- Implement comprehensive logging

## Security Considerations

### 1. Agent Authentication
- Use service account identities for agents
- Implement proper IAM policies
- Constrain agent permissions (read-only when appropriate)
- Maintain audit logs for all actions

### 2. Database Access
- Use MCP servers for database interactions
- Implement connection pooling and security
- Never use direct database calls in agents
- Use proper SQL injection prevention

## Deployment Options

### 1. Development
- Use `adk web` for development and testing
- Local MCP servers for development
- In-memory session storage

### 2. Production
- Deploy on Cloud Run or Vertex AI
- Use persistent database storage
- Implement proper monitoring and logging
- Use A2A communication only for distributed agent architectures
