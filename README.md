# 💰 Agentic AI Financial Advisor

A comprehensive sample application demonstrating Agentic AI principles for financial advisory services. This educational project showcases how multiple AI agents can collaborate to provide personalized financial advice.

## 🎯 Project Overview

This application demonstrates three key Agentic AI concepts:

### 🤖 **Agents**
- **SpendingAnalyzerAgent**: Reviews spending habits and identifies patterns
- **GoalPlannerAgent**: Helps set realistic savings/investment goals
- **AdvisorAgent**: Synthesizes analysis to provide comprehensive recommendations

### 🔗 **MCP (Model Context Protocol)**
- Persistent storage of customer profiles, transactions, goals, and advice history
- MySQL database integration for reliable data management
- RESTful API interface for agent-database communication

### 🤝 **A2A (Agent-to-Agent Collaboration)**
- Coordinated workflow execution
- Inter-agent message passing
- Collaborative recommendation refinement

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ SpendingAnalyzer│    │  GoalPlanner    │    │    Advisor      │
│     Agent       │    │     Agent       │    │     Agent       │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────┴──────────────┐
                    │   Agent Coordinator        │
                    │   (A2A Orchestration)      │
                    └─────────────┬──────────────┘
                                  │
                    ┌─────────────┴──────────────┐
                    │      MCP Server            │
                    │   (Database Interface)     │
                    └─────────────┬──────────────┘
                                  │
                    ┌─────────────┴──────────────┐
                    │     MySQL Database         │
                    └────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- MySQL 8.0 or higher
- Google API Key (for Gemini LLM)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd agent-ai-personal-financial-advisor
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Configure your `.env` file**
   ```env
   # Google AI Configuration
   GOOGLE_API_KEY=your_google_api_key_here
   
   # MySQL Database Configuration
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=financial_advisor
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   
   # Application Configuration
   APP_DEBUG=True
   APP_LOG_LEVEL=INFO
   ```

### Database Setup

1. **Create MySQL database**
   ```sql
   CREATE DATABASE financial_advisor;
   ```

2. **Initialize database tables**
   ```bash
   python -c "
   from financial_mcp.database import db_manager
   db_manager.create_tables()
   print('Database tables created successfully!')
   "
   ```

### Running the Application

1. **Start the Streamlit application**
   ```bash
   streamlit run ui/main.py
   ```

2. **Open your browser** to `http://localhost:8501`

## 📚 Usage Guide

### 1. Customer Profile Setup
- Create a new customer profile or select an existing one
- Provide basic information: name, email, age, and income

### 2. Transaction Management
- Add income and expense transactions
- Categorize transactions for better analysis
- View transaction history and trends

### 3. Goal Setting
- Create financial goals (savings, investment, debt payoff, etc.)
- Set target amounts and dates
- Track progress towards goals

### 4. AI Analysis
- **Spending Analysis**: Get insights on spending patterns and habits
- **Goal Planning**: Receive recommendations for achieving financial goals
- **Comprehensive Analysis**: Complete financial health assessment with prioritized recommendations

## 🧩 Component Details

### Agents

#### SpendingAnalyzerAgent
- **Purpose**: Analyzes spending patterns and identifies optimization opportunities
- **Input**: Customer transaction history and profile
- **Output**: Spending insights, trend analysis, and recommendations
- **AI Model**: Uses Gemini LLM for pattern recognition and advice generation

#### GoalPlannerAgent
- **Purpose**: Creates realistic financial goal plans
- **Input**: Customer goals, financial capacity, and spending patterns
- **Output**: Feasibility assessment, timeline recommendations, and action steps
- **AI Model**: Uses Gemini LLM for goal analysis and planning

#### AdvisorAgent
- **Purpose**: Synthesizes all analysis into comprehensive financial advice
- **Input**: Results from other agents plus customer context
- **Output**: Prioritized recommendations, risk assessment, and action plan
- **AI Model**: Uses Gemini LLM for holistic financial advisory

### MCP Server
- **Database Models**: Customer, Transaction, Goal, Advice
- **API Interface**: RESTful methods for data operations
- **Data Validation**: Pydantic models for type safety
- **Connection Management**: SQLAlchemy ORM with connection pooling

### Agent Coordinator
- **Workflow Management**: Orchestrates multi-agent execution
- **Dependency Handling**: Manages agent execution order
- **A2A Communication**: Facilitates inter-agent message passing
- **Progress Tracking**: Real-time workflow status monitoring

## 🔧 Configuration

### Database Configuration
Located in `config/database.py`:
- Connection string management
- Connection pooling settings
- Environment variable integration

### AI Model Configuration
Located in `config/gemini.py`:
- Google API key management
- Model parameter settings
- Generation configuration

### Agent Configuration
Each agent has configurable:
- System prompts
- Confidence thresholds
- Analysis parameters

## 📊 Data Models

### Customer
```python
{
    "id": int,
    "name": str,
    "email": str,
    "age": int,
    "income": decimal,
    "created_at": datetime,
    "updated_at": datetime
}
```

### Transaction
```python
{
    "id": int,
    "customer_id": int,
    "amount": decimal,
    "category": str,
    "description": str,
    "transaction_date": date,
    "is_income": bool,
    "created_at": datetime
}
```

### Goal
```python
{
    "id": int,
    "customer_id": int,
    "title": str,
    "description": str,
    "goal_type": str,
    "target_amount": decimal,
    "current_amount": decimal,
    "target_date": date,
    "status": str,
    "created_at": datetime,
    "updated_at": datetime
}
```

### Advice
```python
{
    "id": int,
    "customer_id": int,
    "advice_type": str,
    "content": str,
    "agent_source": str,
    "confidence_score": decimal,
    "created_at": datetime
}
```

## 🧪 Testing

### Manual Testing

1. **Database Connection Test**
   ```bash
   python -c "
   from financial_mcp.server import mcp_server
   health = mcp_server.health_check()
   print(f'Database Status: {health}')
   "
   ```

2. **Agent Testing**
   ```bash
   python -c "
   from agents.spending_analyzer import spending_analyzer
   print(f'Agent: {spending_analyzer.agent_name}')
   print(f'Model Available: {spending_analyzer.model is not None}')
   "
   ```

3. **Workflow Testing**
   ```bash
   python -c "
   from orchestrator.agent_coordinator import agent_coordinator
   agents = agent_coordinator.get_agent_info()
   print(f'Available Agents: {list(agents.keys())}')
   "
   ```

### Integration Testing

Run the complete workflow:
1. Create a test customer
2. Add sample transactions
3. Create a financial goal
4. Run comprehensive analysis
5. Verify results in database

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Verify MySQL is running
   - Check database credentials in `.env`
   - Ensure database exists

2. **Google API Key Error**
   - Verify API key is valid
   - Check API quotas and limits
   - Ensure Gemini API is enabled

3. **Import Errors**
   - Verify virtual environment is activated
   - Check all dependencies are installed
   - Ensure Python path includes project directory

4. **Streamlit Not Starting**
   - Check port 8501 is available
   - Verify Streamlit is installed
   - Check for syntax errors in UI code

### Debug Mode

Enable debug logging by setting in `.env`:
```env
APP_DEBUG=True
APP_LOG_LEVEL=DEBUG
```

## 🎓 Educational Concepts

### Agentic AI Principles Demonstrated

1. **Autonomous Agents**: Each agent operates independently with its own reasoning
2. **Collaborative Intelligence**: Agents work together to provide better results
3. **Persistent Memory**: MCP provides shared memory across agent interactions
4. **Goal-Oriented Behavior**: Agents work towards specific financial objectives
5. **Adaptive Responses**: Agents adjust recommendations based on customer data

### Design Patterns

1. **Agent Pattern**: Encapsulated AI agents with specific responsibilities
2. **Observer Pattern**: Workflow progress monitoring and callbacks
3. **Factory Pattern**: Dynamic workflow creation based on requirements
4. **Repository Pattern**: Data access abstraction through MCP server
5. **Command Pattern**: Agent message passing and execution

## 🛠️ Development

### Project Structure
```
agent-ai-personal-financial-advisor/
├── agents/                 # AI agent implementations
├── mcp/                   # Model Context Protocol server
├── orchestrator/          # Agent coordination system
├── ui/                    # Streamlit user interface
├── config/                # Configuration management
├── requirements.txt       # Python dependencies
├── setup.py              # Package setup
└── README.md             # This file
```

### Adding New Agents

1. Inherit from `BaseAgent`
2. Implement required methods
3. Add to agent coordinator
4. Update UI for new capabilities

### Extending Functionality

- Add new transaction categories
- Implement additional goal types
- Create specialized analysis agents
- Add more sophisticated A2A communication

## 📈 Future Enhancements

- Real-time notifications
- Mobile app interface
- Advanced machine learning models
- Integration with banking APIs
- Multi-language support
- Advanced visualization dashboards

## 📄 License

This project is for educational purposes. Please refer to the license file for usage terms.

## 🤝 Contributing

This is an educational project. Contributions are welcome for:
- Bug fixes
- Documentation improvements
- Additional agent implementations
- Enhanced UI features

## 📞 Support

For questions about this educational project:
1. Check the troubleshooting section
2. Review the code documentation
3. Create an issue for bugs or feature requests

---

## 📎 Appendix

### MySQL Installation on macOS

For macOS users, here are detailed instructions to install MySQL using Homebrew:

#### Prerequisites
- macOS system
- Homebrew package manager installed

#### Installation Steps

1. **Install Homebrew** (if not already installed)
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install MySQL using Homebrew**
   ```bash
   brew install mysql
   ```

3. **Start MySQL service**
   ```bash
   brew services start mysql
   ```

4. **Secure the MySQL installation**
   ```bash
   mysql_secure_installation
   ```
   
   During this process, you'll be prompted to:
   - Set up password validation (optional - press 'n' for basic setup)
   - Set a root password (choose a strong password)
   - Remove anonymous users (press 'y')
   - Disallow root login remotely (press 'y')
   - Remove test database (press 'y')
   - Reload privilege tables (press 'y')

5. **Test the installation**
   ```bash
   mysql -u root -p --execute="SELECT VERSION();"
   ```
   
   Enter your root password when prompted. You should see the MySQL version displayed.

#### Common MySQL Commands for macOS

**Connect to MySQL:**
```bash
mysql -u root -p
```

**Check MySQL service status:**
```bash
brew services list | grep mysql
```

**Stop/Start/Restart MySQL:**
```bash
brew services stop mysql
brew services start mysql
brew services restart mysql
```

**Create the application database:**
```sql
mysql -u root -p
CREATE DATABASE financial_advisor;
EXIT;
```

#### Troubleshooting on macOS

- **MySQL service won't start**: Check if port 3306 is already in use
- **Permission denied**: Ensure your user has proper permissions
- **Connection refused**: Verify MySQL service is running with `brew services list`

---

*Built with ❤️ for the AgenticAI class to demonstrate practical implementation of multi-agent AI systems.*
