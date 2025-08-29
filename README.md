# 🏦 AI Personal Financial Advisor

An educational Agentic AI application that provides personalized financial advice using Google's Agent Development Kit (ADK). This application demonstrates multi-agent collaboration, MCP (Model Context Protocol) integration, and modern AI-powered financial analysis.

## 🎯 Purpose

This application was built for an Agentic AI class to demonstrate:
- **Multi-agent systems** using Google ADK
- **MCP integration** for database operations
- **Agent-to-agent collaboration** through built-in ADK mechanisms
- **Real-world AI application** in financial advisory

## 📋 Current Implementation Status

✅ **Fully Implemented:**
- Complete agent architecture (SpendingAnalyzer, GoalPlanner, Advisor, Orchestrator)
- MCP database server with 10+ tools for MySQL operations
- Comprehensive Streamlit UI with 4 main sections
- Database schema with sample data
- Comprehensive test suite with 45+ test cases
- Project structure and documentation

🔄 **Functional but Mock Data:**
- UI displays sample customer data for demonstration
- Agent analysis results are simulated for UI testing
- Database integration is implemented but uses mock responses in UI

🎯 **Ready for Enhancement:**
- Connect UI directly to MCP database tools for live data
- Implement real-time agent execution in Streamlit
- Add actual Gemini API calls with proper error handling
- Expand test coverage with integration tests
- Add performance testing and load testing

## 🤖 AI Agents

### SpendingAnalyzerAgent
- Analyzes customer spending habits and patterns
- Categorizes expenses (fixed vs variable costs)
- Identifies spending trends and anomalies
- Provides spending optimization insights

### GoalPlannerAgent
- Evaluates financial goal feasibility
- Creates realistic savings/investment plans
- Tracks progress toward goals
- Suggests goal prioritization and adjustments

### AdvisorAgent
- Synthesizes insights from other agents
- Generates comprehensive financial recommendations
- Prioritizes advice based on urgency and impact
- Provides clear explanations and action steps

### OrchestratorAgent
- Coordinates all three agents using ADK's built-in capabilities
- Manages multi-agent workflows
- Handles agent collaboration through session state sharing
- Implements custom orchestration logic

## 🛠 Technology Stack

- **AI Framework**: Google Agent Development Kit (ADK) ≥1.13.0
- **Language**: Python 3.11
- **LLM**: Gemini 2.0 Flash (cost-effective, supports tool calling)
- **Database**: MySQL with MCP toolset integration
- **UI**: Streamlit ≥1.49.0
- **Agent Communication**: Built-in ADK multi-agent capabilities
- **Data Visualization**: Plotly ≥6.3.0

## 🏗 Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Streamlit UI    │    │ Orchestrator     │    │ MCP Database    │
│                 │    │ Agent            │    │ Server          │
│ - Dashboard     │◄──►│                  │◄──►│                 │
│ - Transactions  │    │ ┌──────────────┐ │    │ - MySQL Tools   │
│ - Goals         │    │ │ Spending     │ │    │ - CRUD Ops      │
│ - Recommendations│   │ │ Analyzer     │ │    │ - Query Engine  │
└─────────────────┘    │ └──────────────┘ │    └─────────────────┘
                       │ ┌──────────────┐ │
                       │ │ Goal         │ │
                       │ │ Planner      │ │
                       │ └──────────────┘ │
                       │ ┌──────────────┐ │
                       │ │ Advisor      │ │
                       │ │ Agent        │ │
                       │ └──────────────┘ │
                       └──────────────────┘
```

## 📋 Prerequisites

- **Python 3.11** (specific version required)
- **MySQL Server** (local or remote)
- **Google AI Studio API Key** (for Gemini model access)

## ⚡ Quick Start

```bash
# 1. Setup environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure .env file (already provided)
# Make sure your .env file has valid GOOGLE_API_KEY and DB credentials

# 3. Setup database (if using MySQL)
# Create database and run schema.sql

# 4. Run the application
streamlit run streamlit_app.py
```

## 🚀 Detailed Installation & Setup

### 1. Clone and Setup Environment

```bash
# Clone the repository
git clone <repository-url>
cd agent-ai-personal-financial-advisor

# Create Python 3.11 virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Start MySQL server
# Create database
mysql -u root -p
CREATE DATABASE financial_advisor;
USE financial_advisor;

# Run schema creation
mysql -u root -p financial_advisor < database/schema.sql

# Load sample data (optional)
mysql -u root -p financial_advisor < database/sample_data.sql
```

### 3. Environment Configuration

The `.env` file should contain:

```env
# Google AI Configuration
GOOGLE_API_KEY=your_google_ai_studio_api_key

# MySQL Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=financial_advisor
DB_USER=root
DB_PASSWORD=your_mysql_password

# Application Configuration
APP_DEBUG=True
APP_LOG_LEVEL=INFO
```

### 4. Test MCP Database Server

```bash
# Test the MCP server
python mcp_server/database_server.py
```

## 🎮 Running the Application

### Start the Streamlit UI

**Option 1: Direct Streamlit (Recommended)**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the Streamlit application
streamlit run streamlit_app.py
```

**Option 2: Using the Run Script**
```bash
# Alternative launcher with automatic path setup
source venv/bin/activate
python run_app.py
```

The application will be available at `http://localhost:8501`

### Using the Application

1. **Select a Customer** from the sidebar (Alice, Bob, or Carol)
2. **Run Analysis** using the AI agents:
   - 🔍 Full Analysis: Complete financial analysis
   - ⚡ Quick Insights: Fast spending insights
   - 🎯 Goal Focus: Goal-specific analysis
3. **View Results** in the Dashboard, Transactions, Goals, and Recommendations tabs
4. **Add Data** through the transaction and goal entry forms

## 🧪 Testing the Application

### System Status Check

The Streamlit app includes a system status checker in the sidebar that verifies:
- ✅ Database connection
- ✅ MCP server file availability

### Manual Testing

1. **Test Database Connection**:
   ```bash
   source venv/bin/activate
   python -c "from utils.database import test_database_connection; print('✅ Success' if test_database_connection() else '❌ Failed')"
   ```

2. **Test MCP Server**:
   ```bash
   python mcp_server/database_server.py
   ```

2. **Test Individual Agents**:
   ```python
   from agents.spending_analyzer import create_spending_analyzer_agent
   from agents.goal_planner import create_goal_planner_agent
   from agents.advisor import create_advisor_agent
   
   # Test agent creation
   mcp_path = "mcp_server/database_server.py"
   analyzer = create_spending_analyzer_agent(mcp_path)
   planner = create_goal_planner_agent(mcp_path)
   advisor = create_advisor_agent(mcp_path)
   ```

3. **Test Orchestrator**:
   ```python
   from agents.orchestrator import create_financial_advisor_orchestrator
   
   orchestrator = create_financial_advisor_orchestrator("mcp_server/database_server.py")
   ```

### Automated Tests

```bash
# Run unit tests
python -m pytest tests/ -v

# Run integration tests
python -m pytest tests/test_integration.py -v
```

## 📊 Features Demonstrated

### ADK Concepts
- ✅ **LlmAgent**: Core intelligent agents with Gemini 2.0 Flash
- ✅ **BaseAgent**: Custom orchestrator with `_run_async_impl`
- ✅ **MCPToolset**: Database operations via MCP protocol
- ✅ **AgentTool**: Agent-to-agent delegation
- ✅ **Session State**: Data sharing between agents
- ✅ **Multi-agent Coordination**: Hierarchical agent structure

### Financial Features
- ✅ **Spending Analysis**: Pattern recognition and optimization
- ✅ **Goal Planning**: Feasibility analysis and savings plans
- ✅ **Comprehensive Advice**: Prioritized recommendations
- ✅ **Progress Tracking**: Goal and savings monitoring
- ✅ **Data Visualization**: Interactive charts and dashboards

### Technical Features
- ✅ **MCP Integration**: Enterprise-grade database access
- ✅ **Modern UI**: Responsive Streamlit interface
- ✅ **Error Handling**: Comprehensive error management
- ✅ **Logging**: Detailed application logging
- ✅ **Type Safety**: Pydantic models and type hints

## 📁 Project Structure

```
agent-ai-personal-financial-advisor/
├── .env                          # Environment variables
├── requirements.txt             # Python dependencies
├── streamlit_app.py             # Main Streamlit application
├── run_app.py                   # Alternative application launcher
├── simple_app.py                # Simple test app for debugging
├── README.md                    # This file
├── ADK_INSIGHTS.md             # ADK implementation insights
├── IMPLEMENTATION_PLAN.md      # Detailed implementation plan
├── database/
│   ├── schema.sql              # Database schema
│   └── sample_data.sql         # Sample data for testing
├── mcp_server/
│   ├── database_server.py      # MCP database server
│   └── __init__.py
├── agents/
│   ├── spending_analyzer.py    # SpendingAnalyzerAgent
│   ├── goal_planner.py        # GoalPlannerAgent
│   ├── advisor.py             # AdvisorAgent
│   ├── orchestrator.py        # Main orchestration agent
│   └── __init__.py
├── ui/
│   ├── components/            # UI components
│   │   ├── customer_profile.py
│   │   ├── transaction_entry.py
│   │   ├── goal_management.py
│   │   └── recommendations.py
│   └── utils/
│       ├── plotting.py        # Plotly visualization utilities
│       └── formatting.py     # Data formatting utilities
├── utils/
│   ├── database.py           # Database connection utilities
│   └── logging_config.py     # Logging configuration
└── tests/                    # Comprehensive test suite
    ├── __init__.py
    ├── conftest.py           # Pytest configuration & fixtures
    ├── run_tests.py          # Test runner script
    ├── README.md             # Testing guide
    ├── test_agents.py        # Agent functionality tests
    ├── test_mcp_server.py    # MCP server tests
    ├── test_utils.py         # Utility function tests
    └── test_ui_components.py # UI component tests
```

## 🎓 Educational Value

This application demonstrates key concepts students need to master:

### ADK Core Concepts
1. **LlmAgent Creation**: How to create intelligent agents with Gemini models
2. **Custom BaseAgent**: Implementing custom orchestration with `_run_async_impl`
3. **Multi-Agent Systems**: Hierarchical agent structures with `sub_agents`
4. **Session State Management**: Data sharing between agents via `ctx.session.state`
5. **AgentTool Integration**: Using agents as tools for delegation

### MCP Integration Patterns
1. **MCPToolset Usage**: Connecting agents to external services via MCP protocol
2. **Database MCP Server**: Building enterprise-grade database access tools
3. **Tool Discovery**: How ADK automatically discovers and adapts MCP tools
4. **Connection Management**: Proper MCP server lifecycle management

### Real-World Implementation
1. **Financial Domain Modeling**: Practical AI application in finance
2. **Agent Specialization**: Designing agents with focused responsibilities
3. **Collaborative Workflows**: Agents working together to solve complex problems
4. **User Interface Integration**: Connecting AI agents to user-facing applications
5. **Error Handling & Logging**: Production-ready code practices

### Code Quality & Best Practices
1. **Type Safety**: Using Pydantic models and Python type hints
2. **Documentation**: Comprehensive code comments and docstrings
3. **Project Structure**: Modular, maintainable codebase organization
4. **Testing Strategies**: Unit and integration testing approaches

## 🧪 Testing

The project includes a comprehensive test suite designed to help students learn testing best practices:

### Running Tests

```bash
# Run all tests
python tests/run_tests.py

# Run specific test categories
pytest tests/test_agents.py -v
pytest tests/test_mcp_server.py -v
pytest tests/test_utils.py -v
pytest tests/test_ui_components.py -v

# Run with pytest directly
pytest tests/ -v
```

### Test Coverage

- **🤖 AI Agents**: Agent creation, configuration, and tool integration
- **🔌 MCP Server**: Database tools, error handling, and server setup
- **🛠️ Utilities**: Database connections, logging, and configuration
- **🎨 UI Components**: Streamlit components and visualization utilities
- **🔗 Integration**: End-to-end functionality and data flow

### Test Features

- **45+ Test Cases**: Comprehensive coverage of all major components
- **Mock Objects**: Proper isolation of external dependencies
- **Pytest Configuration**: Professional testing setup with fixtures
- **Educational Focus**: Tests demonstrate testing best practices
- **Detailed Documentation**: Complete testing guide in `tests/README.md`

## 🔧 Troubleshooting

### Common Issues

1. **Database Connection Failed**:
   - Check MySQL server is running
   - Verify credentials in `.env` file
   - Ensure database exists

2. **Google API Key Issues**:
   - Verify API key is valid
   - Check Google AI Studio quota
   - Ensure key has proper permissions

3. **MCP Server Not Found**:
   - Verify `mcp_server/database_server.py` exists
   - Check file permissions
   - Ensure FastMCP is installed correctly

4. **Import Errors**:
   - Ensure you're running from the project root directory
   - Verify virtual environment is activated
   - Check PYTHONPATH includes project root
   - Use `python run_app.py` if direct streamlit command fails

5. **Agent Initialization Failed**:
   - Ensure MCP server is accessible
   - Check network connectivity
   - Verify all required environment variables
   - Check Google API key is valid

6. **Streamlit Import Issues**:
   - Run `streamlit run streamlit_app.py` from project root
   - Avoid running from subdirectories
   - Ensure all `__init__.py` files exist in package directories

### Debug Mode

Enable debug logging by setting in `.env`:
```env
APP_DEBUG=True
APP_LOG_LEVEL=DEBUG
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Next Steps for Students

To enhance this application and deepen your ADK understanding:

### Beginner Enhancements
1. **Connect Live Data**: Replace mock data with actual MCP database calls
2. **Add More Categories**: Expand spending categories and subcategories  
3. **Improve UI**: Add more charts and better styling
4. **Add Validation**: Implement form validation and error handling

### Intermediate Enhancements
1. **Real Agent Execution**: Implement actual agent runs in Streamlit
2. **Advanced Analytics**: Add trend analysis and forecasting
3. **Goal Recommendations**: Implement AI-powered goal suggestions
4. **Export Features**: Add PDF reports and data export

### Advanced Enhancements
1. **Streaming Responses**: Implement real-time agent streaming
2. **Multi-User Support**: Add user authentication and multi-tenancy
3. **External Integrations**: Connect to bank APIs or financial services
4. **Deployment**: Deploy to Cloud Run or Vertex AI Agent Engine

### Learning Exercises
1. **Create New Agents**: Build specialized agents (e.g., InvestmentAdvisor, DebtManager)
2. **Custom Tools**: Develop new MCP tools for external APIs
3. **Workflow Agents**: Experiment with SequentialAgent, ParallelAgent patterns
4. **Advanced Orchestration**: Implement conditional agent execution logic

## 🤝 Contributing

This is an educational project. Contributions are welcome for:
- Additional agent capabilities
- UI improvements
- Test coverage
- Documentation enhancements

## 🙏 Acknowledgments

- **Google Agent Development Kit** for the AI agent framework
- **Google AI Studio** for Gemini model access
- **Streamlit** for the web application framework
- **FastMCP** for simplified MCP server implementation

---

**🤖 Powered by Google Agent Development Kit (ADK)** | Built for educational purposes
