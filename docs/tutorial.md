# Financial Advisor App Tutorial

This tutorial will guide you through understanding, running, and extending the Financial Advisor application. It's designed for educational purposes to demonstrate agent development using Google ADK.

## Prerequisites

Before starting, ensure you have:

1. Python 3.11 installed
2. MySQL database server installed and running
3. Google API key for Gemini LLM

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd financial-advisor
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the application**:
   ```bash
   # Create a config.py file from the example
   cp config.example.py config.py
   
   # Edit the file with your database credentials and API key
   nano config.py
   ```

5. **Initialize the database**:
   ```bash
   python src/db/init_db.py
   ```

## Running the Application

1. **Start the application**:
   ```bash
   python src/main.py
   ```

   This will:
   - Initialize the database
   - Start the MCP server
   - Start the A2A servers for all agents
   - Launch the Streamlit UI

2. **Access the UI**:
   Open your browser and navigate to `http://localhost:8501`

## Using the Application

### 1. Create a Customer

1. In the sidebar, fill in the "Create New Customer" form
2. Enter a name and email
3. Click "Create Customer"
4. Select your new customer from the dropdown

### 2. Add Transactions

1. Go to the "Transactions" tab
2. Fill in the transaction details:
   - Amount
   - Category
   - Date
   - Description
3. Click "Add Transaction"
4. Repeat to add multiple transactions

### 3. Set Financial Goals

1. Go to the "Goals" tab
2. Fill in the goal details:
   - Goal Type
   - Target Amount
   - Current Amount
   - Target Date
   - Description
3. Click "Add Goal"
4. Repeat to add multiple goals

### 4. Generate Financial Advice

1. Go to the "Analysis & Advice" tab
2. Adjust the "Months to analyze" slider if needed
3. Click "Generate Financial Advice"
4. Wait for the analysis to complete
5. Review the spending analysis, goal assessment, and personalized advice

### 5. View Advice History

1. Go to the "Advice History" tab
2. Click on any entry to expand and view past advice
3. Compare advice from different agents and times

## Understanding the Code

### Project Structure

```
financial-advisor/
├── docs/                    # Documentation
├── src/                     # Source code
│   ├── agents/              # Agent implementations
│   │   ├── advisor_agent.py
│   │   ├── goal_planner_agent.py
│   │   ├── spending_analyzer_agent.py
│   │   ├── a2a_server.py
│   │   └── agent_manager.py
│   ├── db/                  # Database utilities
│   │   ├── db_utils.py
│   │   ├── init_db.py
│   │   └── schema.sql
│   ├── mcp/                 # MCP server and client
│   │   ├── mcp_client.py
│   │   └── mcp_server.py
│   ├── ui/                  # Streamlit UI
│   │   └── app.py
│   ├── utils/               # Utility functions
│   │   └── config.py
│   └── main.py              # Main entry point
├── tests/                   # Test code
│   └── test_integration.py
├── config.example.py        # Example configuration
├── requirements.txt         # Dependencies
└── README.md                # Project overview
```

### Key Components

1. **Agents**: The core intelligence of the application
   - `SpendingAnalyzerAgent`: Analyzes transaction patterns
   - `GoalPlannerAgent`: Evaluates financial goals
   - `AdvisorAgent`: Provides personalized advice

2. **MCP**: Database access layer
   - `FinancialAdvisorMcpServer`: Exposes database operations as tools
   - `FinancialAdvisorMcpClient`: Client for accessing MCP tools

3. **A2A Communication**: Agent collaboration
   - `SpendingAnalyzerA2AServer`: Exposes spending analysis functions
   - `GoalPlannerA2AServer`: Exposes goal planning functions
   - `AdvisorA2AServer`: Exposes financial advice functions

4. **Agent Manager**: Orchestration layer
   - Initializes and configures all agents
   - Starts necessary servers
   - Provides unified interface for the UI

5. **Streamlit UI**: User interface
   - Transaction entry and management
   - Goal setting and tracking
   - Financial advice generation and display

## Extending the Application

### Adding a New Agent

To add a new agent (e.g., `InvestmentAdvisorAgent`):

1. **Create the agent class**:
   ```python
   # src/agents/investment_advisor_agent.py
   from google.adk import Agent, AgentConfig, Tool, ToolConfig, ToolSpec
   from google.adk.llm import GeminiLLM
   from google.adk.llm.gemini import GeminiConfig

   class InvestmentAdvisorAgent(Agent):
       def __init__(self, mcp_client, api_key):
           # Initialize agent
           ...
   ```

2. **Create an A2A server**:
   ```python
   # src/agents/a2a_server.py (add to existing file)
   class InvestmentAdvisorA2AServer:
       def __init__(self, agent, host="localhost", port=8084):
           # Initialize A2A server
           ...
   ```

3. **Update the Agent Manager**:
   ```python
   # src/agents/agent_manager.py (modify)
   def initialize_agents(self):
       # Add new agent initialization
       self.investment_advisor_agent = InvestmentAdvisorAgent(...)
       self.investment_advisor_a2a_server = InvestmentAdvisorA2AServer(...)
   ```

4. **Update the UI**:
   ```python
   # src/ui/app.py (modify)
   # Add a new tab or section for investment advice
   ```

### Adding New MCP Tools

To add new database functionality:

1. **Update the schema**:
   ```sql
   -- src/db/schema.sql (add)
   CREATE TABLE IF NOT EXISTS investments (
       id INT AUTO_INCREMENT PRIMARY KEY,
       customer_id INT NOT NULL,
       -- other fields
       FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
   );
   ```

2. **Add MCP tools**:
   ```python
   # src/mcp/mcp_server.py (modify)
   def _register_tools(self):
       # Add new tools
       self._register_tool(
           "get_customer_investments",
           self._get_customer_investments,
           "Get all investments for a customer",
           {"customer_id": "int"}
       )
   ```

3. **Implement tool functions**:
   ```python
   # src/mcp/mcp_server.py (add)
   def _get_customer_investments(self, customer_id):
       """Get all investments for a customer."""
       return fetch_data(
           "SELECT * FROM investments WHERE customer_id = %s",
           (customer_id,)
       )
   ```

4. **Update the MCP client**:
   ```python
   # src/mcp/mcp_client.py (add)
   def get_customer_investments(self, customer_id):
       """Get all investments for a customer."""
       return self.client.execute_tool("get_customer_investments", {"customer_id": customer_id})
   ```

## Testing

Run the integration tests to verify your changes:

```bash
python -m unittest tests/test_integration.py
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**:
   - Verify MySQL is running
   - Check database credentials in `config.py`
   - Ensure database and tables exist

2. **MCP Server Errors**:
   - Check if port 8080 is available
   - Look for error messages in the console

3. **A2A Communication Errors**:
   - Verify all A2A servers are running
   - Check URLs and ports in the agent configuration

4. **LLM API Errors**:
   - Verify your Google API key is valid
   - Check for rate limiting or quota issues

### Logging

The application uses Python's logging module. To increase log verbosity:

```python
# src/main.py (modify)
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Learning Exercises

1. **Add a Budget Tracker**:
   - Create a new table for budget categories and limits
   - Add MCP tools to manage budgets
   - Create a BudgetAnalyzerAgent to track spending against budgets

2. **Implement Investment Recommendations**:
   - Create an InvestmentAdvisorAgent
   - Add tools to analyze risk tolerance and investment preferences
   - Generate personalized investment recommendations

3. **Enhance the UI**:
   - Add data visualizations for spending trends
   - Create interactive goal progress trackers
   - Implement a dashboard with key financial metrics

4. **Improve Agent Collaboration**:
   - Add more A2A communication patterns
   - Implement feedback loops between agents
   - Create a meta-agent that coordinates other agents

## Conclusion

This tutorial has guided you through using and extending the Financial Advisor application. By exploring the code and completing the learning exercises, you'll gain a deeper understanding of agent development with Google ADK, MCP tools, and A2A communication.

For more information, refer to the other documentation files and the Google ADK documentation at https://google.github.io/adk-docs/.
