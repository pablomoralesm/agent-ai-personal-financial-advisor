# A2A Communication in Financial Advisor App

This document explains the Agent-to-Agent (A2A) communication implementation in the Financial Advisor application and how it enables collaborative intelligence between specialized agents.

## What is A2A Communication?

Agent-to-Agent (A2A) communication is a protocol in Google's Agent Development Kit (ADK) that allows agents to communicate with each other. It enables agents to:

1. Expose their functionality as services
2. Call functions on other agents
3. Share data and insights
4. Collaborate on complex tasks

## A2A Architecture in Financial Advisor App

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│ SpendingAnalyzer    │     │ GoalPlanner         │     │ Advisor             │
│ Agent               │     │ Agent               │     │ Agent               │
└──────────┬──────────┘     └──────────┬──────────┘     └──────────┬──────────┘
           │                           │                           │
           │                           │                           │
┌──────────▼──────────┐     ┌──────────▼──────────┐     ┌──────────▼──────────┐
│ SpendingAnalyzer    │     │ GoalPlanner         │     │ Advisor             │
│ A2A Server          │     │ A2A Server          │     │ A2A Server          │
└──────────┬──────────┘     └──────────┬──────────┘     └──────────┬──────────┘
           │                           │                           │
           │                           │                           │
           └───────────────────────────┼───────────────────────────┘
                                       │
                      ┌─────────────────▼─────────────────┐
                      │          HTTP/gRPC                │
                      └─────────────────┬─────────────────┘
                                        │
                      ┌─────────────────▼─────────────────┐
                      │          A2A Clients              │
                      └───────────────────────────────────┘
```

## A2A Server Implementation

Each agent exposes its functionality through an A2A server:

### SpendingAnalyzerA2AServer

```python
class SpendingAnalyzerA2AServer:
    def __init__(self, agent, host="localhost", port=8081):
        self.agent = agent
        self.host = host
        self.port = port
        self.server = A2AServer()
        self._register_functions()
    
    def _register_functions(self):
        self.server.register_function(
            "analyze_customer_spending",
            self.agent.analyze_customer_spending,
            "Analyze customer spending and provide insights"
        )
    
    def start(self):
        logging.info(f"Starting SpendingAnalyzerA2AServer at {self.host}:{self.port}")
        self.server.serve(host=self.host, port=self.port)
```

### GoalPlannerA2AServer

```python
class GoalPlannerA2AServer:
    def __init__(self, agent, host="localhost", port=8082):
        self.agent = agent
        self.host = host
        self.port = port
        self.server = A2AServer()
        self._register_functions()
    
    def _register_functions(self):
        self.server.register_function(
            "plan_customer_goals",
            self.agent.plan_customer_goals,
            "Plan and evaluate customer goals"
        )
    
    def start(self):
        logging.info(f"Starting GoalPlannerA2AServer at {self.host}:{self.port}")
        self.server.serve(host=self.host, port=self.port)
```

### AdvisorA2AServer

```python
class AdvisorA2AServer:
    def __init__(self, agent, host="localhost", port=8083):
        self.agent = agent
        self.host = host
        self.port = port
        self.server = A2AServer()
        self._register_functions()
    
    def _register_functions(self):
        self.server.register_function(
            "provide_financial_advice",
            self.agent.provide_financial_advice,
            "Provide comprehensive financial advice for a customer"
        )
    
    def start(self):
        logging.info(f"Starting AdvisorA2AServer at {self.host}:{self.port}")
        self.server.serve(host=self.host, port=self.port)
```

## A2A Client Usage

Agents use A2A clients to call functions on other agents:

```python
class AdvisorAgent(Agent):
    def __init__(self, mcp_client, api_key, spending_analyzer_url, goal_planner_url):
        self.mcp_client = mcp_client
        self.spending_analyzer_url = spending_analyzer_url
        self.goal_planner_url = goal_planner_url
        
        # Create A2A clients for other agents
        self.spending_analyzer_client = A2AClient(spending_analyzer_url)
        self.goal_planner_client = A2AClient(goal_planner_url)
        
        # ... rest of initialization
    
    def _get_spending_analysis(self, customer_id, months):
        try:
            # Use A2A to call the SpendingAnalyzerAgent
            response = self.spending_analyzer_client.execute(
                "analyze_customer_spending",
                {"customer_id": customer_id, "months": months}
            )
            return response
        except Exception as e:
            logging.error(f"Error getting spending analysis: {e}")
            return {"error": f"Failed to get spending analysis: {str(e)}"}
    
    def _get_goal_planning(self, customer_id, avg_monthly_spending):
        try:
            # Use A2A to call the GoalPlannerAgent
            response = self.goal_planner_client.execute(
                "plan_customer_goals",
                {"customer_id": customer_id, "avg_monthly_spending": avg_monthly_spending}
            )
            return response
        except Exception as e:
            logging.error(f"Error getting goal planning: {e}")
            return {"error": f"Failed to get goal planning: {str(e)}"}
```

## Agent Orchestration

The `AgentManager` class orchestrates the A2A communication:

```python
class AgentManager:
    def initialize_agents(self):
        # Create agents
        self.spending_analyzer_agent = SpendingAnalyzerAgent(
            mcp_client=self.mcp_client,
            api_key=GOOGLE_API_KEY
        )
        
        self.goal_planner_agent = GoalPlannerAgent(
            mcp_client=self.mcp_client,
            api_key=GOOGLE_API_KEY
        )
        
        self.advisor_agent = AdvisorAgent(
            mcp_client=self.mcp_client,
            api_key=GOOGLE_API_KEY,
            spending_analyzer_url="http://localhost:8081",
            goal_planner_url="http://localhost:8082"
        )
        
        # Create A2A servers
        self.spending_analyzer_a2a_server = SpendingAnalyzerA2AServer(
            agent=self.spending_analyzer_agent,
            host="localhost",
            port=8081
        )
        
        self.goal_planner_a2a_server = GoalPlannerA2AServer(
            agent=self.goal_planner_agent,
            host="localhost",
            port=8082
        )
        
        self.advisor_a2a_server = AdvisorA2AServer(
            agent=self.advisor_agent,
            host="localhost",
            port=8083
        )
    
    def start_servers(self):
        # Start A2A servers in threads
        spending_analyzer_thread = threading.Thread(
            target=self.spending_analyzer_a2a_server.start,
            daemon=True
        )
        spending_analyzer_thread.start()
        
        goal_planner_thread = threading.Thread(
            target=self.goal_planner_a2a_server.start,
            daemon=True
        )
        goal_planner_thread.start()
        
        advisor_thread = threading.Thread(
            target=self.advisor_a2a_server.start,
            daemon=True
        )
        advisor_thread.start()
```

## A2A Communication Flow

The A2A communication in the Financial Advisor app follows this flow:

1. **Server Registration**:
   - Each agent registers its functions with an A2A server
   - Servers run on different ports (8081, 8082, 8083)

2. **Client Connection**:
   - The AdvisorAgent creates A2A clients to connect to other agents
   - Clients are configured with the server URLs

3. **Function Execution**:
   - AdvisorAgent calls functions on other agents via A2A
   - Parameters are passed as JSON
   - Results are returned as JSON

4. **Result Integration**:
   - AdvisorAgent integrates results from other agents
   - Combined insights are used to generate advice

## Benefits of A2A Communication

### 1. Specialization
- Each agent can focus on a specific domain
- Agents can be developed and tested independently
- Expertise is encapsulated in dedicated agents

### 2. Modularity
- Agents can be replaced or upgraded individually
- New agents can be added without changing existing ones
- System can scale by adding more specialized agents

### 3. Distributed Processing
- Computation can be distributed across multiple agents
- Agents can run on different machines if needed
- Complex tasks can be broken down into manageable parts

### 4. Collaborative Intelligence
- Agents can combine their insights for better results
- Different perspectives lead to more comprehensive advice
- Specialized knowledge can be applied where most relevant

## A2A Error Handling

The A2A implementation includes error handling:

```python
try:
    response = self.spending_analyzer_client.execute(
        "analyze_customer_spending",
        {"customer_id": customer_id, "months": months}
    )
    return response
except Exception as e:
    logging.error(f"Error getting spending analysis: {e}")
    return {"error": f"Failed to get spending analysis: {str(e)}"}
```

This ensures that:
- Communication failures are detected
- Errors are logged for debugging
- The calling agent can handle failures gracefully

## Educational Takeaways

Key lessons from the A2A implementation:

1. **Agent Specialization**: Creating focused agents with specific expertise
2. **Function Exposure**: Exposing agent functions through A2A servers
3. **Remote Execution**: Calling functions on remote agents
4. **Result Integration**: Combining insights from multiple agents
5. **Distributed Intelligence**: Building systems with collaborative agents
