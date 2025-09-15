# 🏦 AI Personal Financial Advisor

An educational Agentic AI application that provides personalized financial advice using Google's Agent Development Kit (ADK). This application demonstrates multi-agent collaboration, MCP (Model Context Protocol) integration, and modern AI-powered financial analysis.

## 🎯 Purpose

This application was built for an Agentic AI class to demonstrate:
- **Multi-agent systems** using Google ADK
- **MCP integration** for database operations
- **Agent-to-agent collaboration** through built-in ADK mechanisms
- **Real-world AI application** in financial advisory

## 📋 Current Implementation Status

✅ **Fully Implemented & Functional:**
- **ADK Web Agent System** - 6 specialized agents working in both Streamlit and ADK Web
- **Sequential Multi-Agent Analysis** - Full analysis using SequencerAgent with step-by-step coordination
- **MCP database server** with 8 tools for MySQL operations and JSON-RPC 2.0 protocol
- **Comprehensive Streamlit UI** with 4 main tabs and real-time data
- **Real database integration** - All UI components use live MySQL data
- **Dynamic customer selection** from database
- **Comprehensive test suite** with 6 test files and 128 test methods covering all components
- **Production-ready framework** with robust error handling and logging

✅ **Database Integration Complete:**
- Customer profiles loaded dynamically from database
- Real transaction data with 6-table schema (customers, transactions, goals, advice, interactions, categories)
- Live financial goals and progress tracking
- Advice history from AI agents
- Savings trend charts with real monthly data
- Multi-customer support with seamless switching

✅ **AI Agent System Complete:**
- **ADK Web Agents** - 6 specialized agents working in both Streamlit and ADK Web
- **Sequential Multi-Agent Analysis** - Full analysis using SequencerAgent with step-by-step coordination
- **Direct ADK Integration** - Streamlit UI uses ADK Web agents directly without modification
- **LLM Integration** - Gemini 2.0 Flash API fully connected and working
- **Event-Driven Architecture** - Proper ADK Event creation and handling
- **Session State Management** - Data sharing between agents via ADK session state
- **MCP Tool Integration** - Agents use database tools via MCP protocol

## 🤖 AI Agents

The application uses 6 specialized ADK Web agents that work in both Streamlit and ADK Web environments:

### StandaloneAgent
- Pure MCP-only financial advisor
- Provides quick financial analysis without orchestration
- Direct database access via MCP tools
- Ideal for simple, fast analysis requests

### SequencerAgent
- Step-by-step multi-agent coordination
- Orchestrates Spending Analyzer → Goal Planner → Advisor
- Sequential workflow for comprehensive analysis
- Used for full financial analysis in Streamlit UI

### OrchestratorAgent
- Intelligent LLM-driven coordination
- Advanced multi-agent orchestration
- Dynamic agent selection and coordination
- Handles complex analysis workflows

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

## 🛠 Technology Stack

- **AI Framework**: Google Agent Development Kit (ADK) ≥1.13.0
- **Language**: Python 3.11
- **LLM**: Gemini 2.0 Flash Experimental (cost-effective, supports tool calling)
- **Database**: MySQL with MCP toolset integration
- **UI**: Streamlit ≥1.49.0
- **Agent Communication**: Built-in ADK multi-agent capabilities
- **Data Visualization**: Plotly ≥6.3.0

## 🏗 Architecture

### Unified ADK Agent System

The application uses a unified architecture where the same ADK Web agents work in both Streamlit and ADK Web environments:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Streamlit UI    │    │ ADK Web Agents   │    │ MCP Database    │
│                 │    │ (Unified)        │    │ Server          │
│ - Dashboard     │◄──►│                  │◄──►│                 │
│ - Transactions  │    │ ┌──────────────┐ │    │ - MySQL Tools   │
│ - Goals         │    │ │ Sequencer    │ │    │ - JSON-RPC 2.0  │
│ - Recommendations│   │ │ Agent        │ │    │ - CRUD Ops      │
└─────────────────┘    │ └──────────────┘ │    └─────────────────┘
                       │ ┌──────────────┐ │
                       │ │ Standalone   │ │
                       │ │ Agent        │ │
                       │ └──────────────┘ │
                       │ ┌──────────────┐ │
                       │ │ Orchestrator │ │
                       │ │ Agent        │ │
                       │ └──────────────┘ │
                       │ ┌──────────────┐ │
                       │ │ Spending     │ │
                       │ │ Analyzer     │ │
                       │ └──────────────┘ │
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

### Option 1: Streamlit UI (Educational Focus)
```bash
# 1. Setup environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure .env file
# Make sure your .env file has valid GOOGLE_API_KEY and DB credentials

# 3. Setup database (if using MySQL)
# Create database and run schema.sql

# 4. Run Streamlit UI
streamlit run streamlit_app.py
# Access at http://localhost:8501
```

### Option 2: ADK Web (Multi-Agent Focus)
```bash
# 1. Setup environment (same as above)
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure .env file (same as above)

# 3. Setup database (same as above)

# 4. Run ADK Web
adk web agents
# Access at http://localhost:8080
# Select an agent and start chatting!
```

### Option 3: Both (Recommended for Learning)
```bash
# Terminal 1: Streamlit UI
source venv/bin/activate
streamlit run streamlit_app.py

# Terminal 2: ADK Web
source venv/bin/activate
adk web agents

# Access both:
# Streamlit: http://localhost:8501
# ADK Web: http://localhost:8080
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

### Option 1: Streamlit UI (Educational Focus)

**Start the Streamlit Application**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the Streamlit application
streamlit run streamlit_app.py
```

The application will be available at `http://localhost:8501`

### Option 2: ADK Web (Advanced Multi-Agent)

**Start ADK Web for Multi-Agent Interactions**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Start ADK Web with the agents directory
adk web agents
```

ADK Web will be available at `http://localhost:8080`

**Available ADK Web Agents:**
1. **Standalone** - Pure MCP-only financial analysis in one step with direct database access
2. **Orchestrator** - Intelligent LLM-driven coordination of specialized agents
3. **Sequencer** - Step-by-step sequential execution of all specialized agents
4. **Spending Analyzer** - Specialized spending pattern analysis and optimization
5. **Goal Planner** - Specialized financial goal planning and feasibility analysis
6. **Advisor** - Financial advice synthesis and recommendation generation

**Using ADK Web:**
1. Navigate to `http://localhost:8080`
2. Select an agent from the dropdown
3. Start a conversation with the agent
4. Agents will use MCP tools to access the database
5. Experience real multi-agent interactions and orchestration

### Using the Application

#### Streamlit UI (Educational Focus)
1. **Select a Customer** from the sidebar (dynamically loaded from database)
2. **Explore Financial Data** across 4 main tabs:
   - 📊 **Profile & Overview**: Financial health score, savings trends, spending analysis
   - 💰 **Transactions**: Add, view, and filter financial transactions
   - 🎯 **Goals**: Set, track, and update financial goals with progress bars
   - 🤖 **AI Recommendations**: View advice history and run AI analysis
3. **Run AI Analysis** using the analysis button:
   - 🚀 **Full Analysis**: Complete financial analysis with real AI agents
4. **Real-time Data**: All data is loaded live from MySQL database
5. **Multi-Customer Support**: Switch between different customer profiles seamlessly

#### ADK Web (Advanced Multi-Agent)
1. **Choose Your Agent** from the dropdown:
   - **Financial Advisor**: Direct conversation with comprehensive financial advisor
   - **Procedural Orchestrator**: Watch step-by-step multi-agent coordination
   - **Intelligent Orchestrator**: Experience AI-driven dynamic orchestration
2. **Start Conversations**: Chat directly with agents using natural language
3. **Multi-Agent Interactions**: See agents collaborate and delegate tasks
4. **Real Database Access**: Agents use MCP tools to query and update data
5. **Advanced Orchestration**: Experience different orchestration patterns

### 🎯 Choosing Your Approach

**Use Streamlit UI when:**
- Learning about financial data visualization
- Understanding database integration patterns
- Exploring UI/UX design with real data
- Educational demonstrations and presentations

**Use ADK Web when:**
- Learning about multi-agent systems
- Understanding agent orchestration patterns
- Exploring conversational AI interfaces
- Advanced multi-agent interactions and coordination

## 🧪 Testing the Application

### System Status Check

The Streamlit app includes a system status checker in the sidebar that verifies:
- ✅ Database connection
- ✅ MCP server file availability
- ✅ Agent system status

### Testing Both Approaches

**Test Streamlit UI:**
```bash
# Start Streamlit
source venv/bin/activate
streamlit run streamlit_app.py

# Test analysis buttons
# 1. Navigate to http://localhost:8501
# 2. Select a customer
# 3. Go to "AI Recommendations" tab
# 4. Click "Full Analysis"
# 5. Verify agents execute and provide real recommendations
```

**Test ADK Web:**
```bash
# Start ADK Web
source venv/bin/activate
adk web agents

# Test multi-agent interactions
# 1. Navigate to http://localhost:8080
# 2. Select "Procedural Orchestrator" from dropdown
# 3. Ask: "Analyze customer 1's spending patterns"
# 4. Watch agents collaborate and use MCP tools
# 5. Try "Intelligent Orchestrator" for dynamic coordination
```

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

3. **Test ADK Web Agents**:
   ```python
   from agents.standalone.agent import agent as standalone_agent
   from agents.sequencer.agent import agent as sequencer_agent
   from agents.orchestrator.agent import agent as orchestrator_agent
   
   # Test agent creation
   mcp_path = "mcp_server/database_server_stdio.py"
   # Agents are already configured and ready to use
   ```

4. **Test ADK Agent Manager**:
   ```python
   from utils.adk_agent_manager import ADKAgentManager
   
   manager = ADKAgentManager(mcp_server_path="mcp_server/database_server_stdio.py")
   status = manager.get_agent_status()
   ```

### Automated Tests

```bash
# Run unit tests
python -m pytest tests/ -v

# Run specific test files
python -m pytest tests/test_streamlit_integration.py -v
```

## 📊 Features Demonstrated

### ADK Concepts
- ✅ **LlmAgent**: Core intelligent agents with Gemini 2.0 Flash Experimental
- ✅ **SequentialAgent**: Built-in ADK orchestration for step-by-step execution
- ✅ **MCPToolset**: Database operations via MCP protocol
- ✅ **AgentTool**: Agent-to-agent delegation
- ✅ **Session State**: Data sharing between agents
- ✅ **Multi-agent Coordination**: Hierarchical agent structure

### Financial Features
- ✅ **Spending Analysis**: Pattern recognition and optimization with real transaction data
- ✅ **Goal Planning**: Feasibility analysis and savings plans with live progress tracking
- ✅ **Comprehensive Advice**: Prioritized recommendations from AI agents
- ✅ **Progress Tracking**: Real-time goal and savings monitoring
- ✅ **Data Visualization**: Interactive charts and dashboards with live data
- ✅ **Multi-Customer Support**: Seamless switching between different customer profiles
- ✅ **Dynamic Data Loading**: All financial data loaded from MySQL database in real-time

### Technical Features
- ✅ **MCP Integration**: Enterprise-grade database access via FastMCP
- ✅ **Modern UI**: Responsive Streamlit interface with real-time data
- ✅ **Error Handling**: Comprehensive error management and user feedback
- ✅ **Logging**: Detailed application logging with configurable levels
- ✅ **Type Safety**: Pydantic models and Python type hints throughout
- ✅ **Database Client**: Direct database access for UI components
- ✅ **Data Persistence**: Full CRUD operations for all financial data
- ✅ **Real-time Updates**: Live data refresh and dynamic UI updates

## 📁 Project Structure

```
agent-ai-personal-financial-advisor/
├── .env                          # Environment variables
├── requirements.txt             # Python dependencies
├── streamlit_app.py             # Main Streamlit application
├── README.md                    # This file
├── LICENSE                      # MIT License
├── database/
│   ├── schema.sql              # Database schema with all tables
│   └── sample_data.sql         # Sample data for testing
├── mcp_server/                 # MCP Database Server
│   ├── database_server.py      # FastMCP server
│   ├── database_server_stdio.py # STDIO server with JSON-RPC 2.0
│   ├── shared/                 # DRY shared components
│   │   ├── __init__.py
│   │   ├── business_logic.py   # Business logic functions
│   │   ├── config.py          # Configuration management
│   │   ├── database_manager.py # Database operations
│   │   └── models.py          # Data models
│   └── README.md              # MCP server documentation
├── agents/                    # ADK Web Agent System
│   ├── standalone/            # Standalone financial advisor agent
│   ├── sequencer/             # Sequential multi-agent orchestrator
│   ├── orchestrator/          # Intelligent multi-agent orchestrator
│   ├── spending_analyzer/     # Spending analysis specialist
│   ├── goal_planner/          # Financial goal planning specialist
│   ├── advisor/               # Financial advice synthesis specialist
│   └── README.md              # ADK Web documentation
├── ui/
│   └── components/            # UI components
│       ├── customer_profile.py # Customer profile & financial overview
│       ├── transaction_entry.py # Transaction management
│       ├── goal_management.py  # Goal setting & tracking
│       └── recommendations.py  # AI recommendations & analysis
├── utils/
│   ├── database.py            # Database connection utilities
│   ├── database_client.py     # Direct database access for UI
│   ├── logging_config.py     # Logging configuration
│   └── adk_agent_manager.py  # ADK agent management for Streamlit
└── tests/                     # Comprehensive test suite
    ├── __init__.py
    ├── README.md              # Testing documentation
    ├── test_agents.py         # ADK Web agent tests
    ├── test_adk_agent_manager.py # ADK agent manager tests
    ├── test_mcp_server.py     # MCP server tests
    ├── test_utils.py          # Utility function tests
    ├── test_ui_components.py  # UI component tests
    ├── test_streamlit_integration.py # Streamlit integration tests
    ├── run_tests.py           # Test runner script
    └── README.md              # Testing documentation
```

## 🎓 Educational Value

This application demonstrates key concepts students need to master:

### ADK Core Concepts
1. **LlmAgent Creation**: How to create intelligent agents with Gemini 2.0 Flash Experimental
2. **SequentialAgent**: Built-in ADK orchestration for step-by-step agent execution
3. **Multi-Agent Systems**: Hierarchical agent structures with `sub_agents`
4. **Session State Management**: Data sharing between agents via ADK session state
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
   - All imports are now working correctly with proper path setup

5. **Agent Initialization Failed**:
   - Ensure MCP server is accessible
   - Check network connectivity
   - Verify all required environment variables
   - Check Google API key is valid

6. **Streamlit Import Issues**:
   - Run `streamlit run streamlit_app.py` from project root
   - Avoid running from subdirectories
   - Ensure all `__init__.py` files exist in package directories
   - **Fixed**: All import issues resolved with proper path configuration

7. **Database Integration Issues**:
   - **Fixed**: All UI components now use real database data
   - **Fixed**: Customer list dynamically loaded from database
   - **Fixed**: Savings trend charts show real monthly data
   - **Fixed**: Date parsing and Decimal type issues resolved

8. **ADK Web Issues**:
   - **Agents Not Showing**: Make sure to run `adk web agents` (with the agents directory parameter)
   - **Agent Not Found**: Ensure you're in the project root directory when running `adk web`
   - **MCP Server Timeout**: Check that `mcp_server/database_server_stdio.py` is accessible
   - **Agent Import Errors**: Verify virtual environment is activated and all dependencies installed
   - **Database Connection**: Ensure MySQL server is running and credentials are correct
   - **Agent Selection**: Use the dropdown to select from available agents (Financial Advisor, Procedural Orchestrator, Intelligent Orchestrator)

### Debug Mode

Enable debug logging by setting in `.env`:
```env
APP_DEBUG=True
APP_LOG_LEVEL=DEBUG
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Application Status

The Personal Financial Advisor application is a **fully functional AI-powered financial advisor** ready for advanced features like streaming responses, additional specialized agents, and deployment to production environments.

## 🚀 Future Enhancement Ideas

This application provides a solid foundation for students to explore advanced AI concepts:

### Beginner Enhancements
1. **Add More Categories**: Expand spending categories and subcategories  
2. **Improve UI**: Add more charts and better styling
3. **Add Validation**: Implement form validation and error handling
4. **Custom Dashboards**: Create personalized financial dashboards

### Intermediate Enhancements
1. **Goal Recommendations**: Implement AI-powered goal suggestions
2. **Export Features**: Add PDF reports and data export
3. **Advanced Analytics**: Add more sophisticated financial metrics
4. **Notification System**: Implement alerts for spending limits and goal milestones

### Advanced Enhancements
1. **Streaming Responses**: Implement real-time agent streaming
2. **Multi-User Support**: Add user authentication and multi-tenancy
3. **External Integrations**: Connect to bank APIs or financial services
4. **Deployment**: Deploy to Cloud Run or Vertex AI Agent Engine
5. **Additional Agents**: Create specialized agents (Investment, Debt Management)
6. **Performance Optimization**: Add caching and performance monitoring

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