# Agent Design in Financial Advisor App

This document explains the design principles and implementation details of the agents in the Financial Advisor application.

## Agent Development Kit (ADK) Overview

The Google Agent Development Kit (ADK) provides a powerful framework for building intelligent agents. Key components used in this application include:

- **Agent**: The core class for implementing agents
- **AgentConfig**: Configuration for agent behavior and capabilities
- **Tool**: Functions that agents can use to perform actions
- **ToolConfig**: Configuration for tool behavior and parameters
- **LLM**: Large Language Model integration for intelligent reasoning
- **A2A Protocol**: Agent-to-Agent communication framework

## Agent Design Principles

The Financial Advisor app follows these agent design principles:

1. **Single Responsibility**: Each agent has a clear, focused responsibility
2. **Tool-Based Architecture**: Agents use tools to perform specific tasks
3. **Collaborative Intelligence**: Agents share insights to improve recommendations
4. **Data-Driven Decisions**: Analysis is based on customer financial data
5. **Explainable Results**: Advice includes reasoning and specific recommendations

## Agent Implementation

### Base Agent Structure

All agents in the system follow a similar structure:

```python
class FinancialAgent(Agent):
    def __init__(self, mcp_client, api_key):
        # Configure LLM
        llm_config = GeminiConfig(...)
        llm = GeminiLLM(llm_config)
        
        # Configure agent
        agent_config = AgentConfig(
            name="AgentName",
            description="Agent description",
            llm=llm,
            tools=self._create_tools()
        )
        
        super().__init__(agent_config)
    
    def _create_tools(self):
        # Define and return tools
        ...
    
    # Tool implementations
    def _tool_function(self, param1, param2):
        # Implement tool functionality
        ...
    
    # Main public method
    def main_function(self, customer_id):
        # Implement main agent functionality
        ...
```

### SpendingAnalyzerAgent

The SpendingAnalyzerAgent analyzes customer spending patterns:

#### Tools:
- `get_customer_transactions`: Retrieves all transactions for a customer
- `get_transactions_by_category`: Filters transactions by category
- `get_transactions_by_date_range`: Gets transactions within a date range
- `get_spending_by_category`: Calculates total spending by category
- `get_monthly_spending`: Calculates monthly spending totals
- `analyze_spending_patterns`: Performs comprehensive spending analysis
- `identify_high_spending_categories`: Finds categories with excessive spending
- `calculate_spending_trends`: Determines if spending is increasing/decreasing

#### Main Function:
`analyze_customer_spending(customer_id, months)`: Analyzes spending over a specified period and returns insights.

#### Key Algorithms:
- Percentage calculation for spending categories
- Trend analysis comparing first and second half of period
- High spending category identification using threshold

### GoalPlannerAgent

The GoalPlannerAgent helps set and evaluate financial goals:

#### Tools:
- `get_customer_goals`: Retrieves all goals for a customer
- `get_goal`: Gets a specific goal by ID
- `create_goal`: Creates a new financial goal
- `update_goal_progress`: Updates progress toward a goal
- `calculate_goal_progress`: Calculates percentage completion and time remaining
- `calculate_monthly_contribution`: Determines required monthly savings
- `recommend_goal_adjustments`: Suggests goal modifications based on capacity
- `evaluate_goal_feasibility`: Assesses if goals are realistic

#### Main Function:
`plan_customer_goals(customer_id, avg_monthly_spending)`: Evaluates goals against financial capacity.

#### Key Algorithms:
- Goal progress calculation (amount and time)
- Monthly contribution calculation based on remaining time
- Feasibility assessment comparing required vs. available savings
- Target date adjustment for unrealistic goals

### AdvisorAgent

The AdvisorAgent integrates insights and provides personalized advice:

#### Tools:
- `get_customer_advice_history`: Retrieves previous advice
- `add_advice`: Saves new advice to history
- `get_spending_analysis`: Gets analysis from SpendingAnalyzerAgent (A2A)
- `get_goal_planning`: Gets planning from GoalPlannerAgent (A2A)
- `generate_personalized_advice`: Creates tailored financial advice
- `recommend_next_steps`: Prioritizes actions for financial improvement

#### Main Function:
`provide_financial_advice(customer_id, months)`: Generates comprehensive financial advice.

#### Key Algorithms:
- A2A integration with other agents
- LLM prompt engineering for personalized advice
- Next steps prioritization based on financial situation
- Advice generation using Gemini LLM

## A2A Communication

Agents communicate using the A2A protocol:

1. **A2A Server Registration**:
   ```python
   server = A2AServer()
   server.register_function(
       "function_name",
       agent_instance.function,
       "Function description"
   )
   ```

2. **A2A Client Usage**:
   ```python
   client = A2AClient("http://localhost:8081")
   response = client.execute(
       "function_name",
       {"param1": value1, "param2": value2}
   )
   ```

This allows agents to:
- Call other agents' functions remotely
- Share data and insights
- Collaborate on complex problems

## Tool Design

Tools are designed to be:

1. **Focused**: Each tool performs a specific task
2. **Well-Documented**: Clear descriptions and parameter definitions
3. **Strongly Typed**: Parameters have defined types
4. **Error-Handling**: Tools handle errors gracefully

Example tool registration:

```python
Tool(
    ToolConfig(
        name="calculate_monthly_contribution",
        description="Calculate required monthly contribution to reach a goal",
        function=self._calculate_monthly_contribution,
        parameters=[
            ToolSpec.Parameter(
                name="goal_id",
                description="Goal ID",
                type="integer",
                required=True
            )
        ]
    )
)
```

## LLM Integration

The AdvisorAgent uses Gemini LLM to generate personalized advice:

1. **Context Preparation**:
   - Format financial data for the LLM
   - Include relevant customer information

2. **Prompt Engineering**:
   ```
   You are a financial advisor providing personalized advice to {customer_name}.
   
   Spending Analysis:
   - Total spending: ${total_spending}
   - Average monthly spending: ${avg_monthly_spending}
   - Spending trend: {spending_trend}
   - High spending categories: {high_spending_categories}
   
   Goal Assessment:
   - Has financial goals: {has_goals}
   - Overall goal assessment: {overall_goal_assessment}
   - Total monthly contribution needed: ${total_monthly_contribution}
   - Estimated monthly savings capacity: ${estimated_savings_capacity}
   
   Based on this information, provide personalized financial advice...
   ```

3. **Response Processing**:
   - Extract advice text from LLM response
   - Save to advice history
   - Return structured advice

## Educational Takeaways

Key lessons from this agent design:

1. **Modular Agent Design**: Breaking complex problems into specialized agents
2. **Tool-Based Architecture**: Using tools for structured functionality
3. **A2A Communication**: Enabling agent collaboration
4. **LLM Enhancement**: Using LLMs for natural language generation
5. **Data-Driven Advice**: Basing recommendations on actual financial data
