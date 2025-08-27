# Financial Advisor App Architecture

This document provides an overview of the Financial Advisor application architecture, explaining how the different components interact to provide personalized financial advice.

## System Architecture

The application follows a modular architecture with clear separation of concerns:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit UI  │◄──►│  Agent Manager   │◄──►│  MCP Server     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                         │
                    ┌───────────┼───────────┐            │
                    │           │           │            │
           ┌────────▼──┐ ┌─────▼─────┐ ┌────▼─────┐     │
           │Spending   │ │Goal       │ │Advisor   │     │
           │Analyzer   │ │Planner    │ │Agent     │     │
           │Agent      │ │Agent      │ │(+Gemini) │     │
           └───────────┘ └───────────┘ └──────────┘     │
                                                        │
                                              ┌─────────▼─────────┐
                                              │   MySQL Database │
                                              └───────────────────┘
```

## Key Components

### 1. Database Layer

The MySQL database stores all customer data, including:
- Customer profiles
- Financial transactions
- Financial goals
- Advice history

The database schema is designed to track customer financial activity and provide a foundation for analysis.

### 2. MCP (Model Context Protocol) Server

The MCP server acts as a secure interface between the agents and the database, implementing:
- Database operations as tools
- Data validation and security
- Structured data access patterns

This ensures agents can only access the database through well-defined tools, enhancing security and maintainability.

### 3. Agent System

The application uses three specialized agents built with Google ADK:

#### SpendingAnalyzerAgent
- Analyzes transaction patterns
- Identifies high spending categories
- Calculates spending trends over time
- Provides insights on spending habits

#### GoalPlannerAgent
- Evaluates financial goal feasibility
- Calculates required monthly contributions
- Recommends goal adjustments based on spending capacity
- Tracks progress toward goals

#### AdvisorAgent
- Integrates insights from other agents
- Uses Gemini LLM for personalized recommendations
- Generates actionable financial advice
- Prioritizes next steps for financial improvement

### 4. A2A (Agent-to-Agent) Communication

The agents communicate through the A2A protocol:
- Each agent exposes its capabilities as an A2A server
- Agents can call other agents' functions through A2A clients
- This enables collaborative intelligence and specialized roles

### 5. Agent Manager

The Agent Manager orchestrates the entire system:
- Initializes and configures all agents
- Starts the necessary servers
- Provides a unified interface for the UI
- Handles error conditions and retries

### 6. Streamlit UI

The user interface provides:
- Transaction entry and management
- Goal setting and tracking
- Agent execution controls
- Visualization of financial analysis and advice

## Data Flow

1. **User Input**:
   - User enters transactions and goals through the Streamlit UI
   - Data is sent to the Agent Manager

2. **Data Storage**:
   - Agent Manager uses the MCP client to store data
   - MCP server validates and persists data in the MySQL database

3. **Analysis Request**:
   - User requests financial advice
   - Agent Manager initiates the AdvisorAgent

4. **Agent Collaboration**:
   - AdvisorAgent calls SpendingAnalyzerAgent via A2A
   - AdvisorAgent calls GoalPlannerAgent via A2A
   - Each agent accesses data through MCP tools

5. **Advice Generation**:
   - AdvisorAgent integrates insights from other agents
   - Gemini LLM generates personalized advice
   - Recommendations are stored via MCP

6. **Results Presentation**:
   - Analysis and advice are displayed in the UI
   - User can view detailed breakdowns and recommendations

## Security Considerations

- **Database Access**: All database access is mediated through MCP tools
- **Input Validation**: Data is validated at multiple levels
- **Error Handling**: Robust error handling prevents system failures
- **API Key Security**: Sensitive credentials are stored in environment variables

## Educational Value

This architecture demonstrates:
1. **Agent Specialization**: Each agent has a clear, focused role
2. **Secure Data Access**: MCP provides controlled access to data
3. **A2A Communication**: Agents collaborate to solve complex problems
4. **LLM Integration**: Gemini enhances agent capabilities with natural language generation
5. **Modern UI**: Streamlit provides an interactive user experience
