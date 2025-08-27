# Financial Advisor - Agentic AI Sample App

A sample application for an Agentic AI class demonstrating how to build intelligent financial advisor agents using Google's Agent Development Kit (ADK).

## Overview

This application demonstrates:

- **Agents**: Three specialized AI agents working together to provide financial advice
  - **SpendingAnalyzerAgent**: Reviews spending habits and identifies patterns
  - **GoalPlannerAgent**: Helps set realistic savings/investment goals
  - **AdvisorAgent**: Provides tailored financial recommendations

- **MCP (Model Context Protocol)**: Secure database access for agents
- **A2A Communication**: Agent collaboration to refine recommendations
- **Streamlit UI**: User-friendly interface for entering financial data and viewing advice

## Architecture

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

## Requirements

- Python 3.11
- MySQL database
- Google ADK
- Gemini API key

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   ```
   cp .env.example .env
   # Edit .env with your database credentials and API keys
   ```
5. Initialize the database:
   ```
   python src/db/init_db.py
   ```

## Usage

1. Start the Streamlit app:
   ```
   streamlit run src/ui/app.py
   ```
2. Open your browser at `http://localhost:8501`
3. Enter your financial transactions and goals
4. Run the agents to get personalized financial advice

## Educational Focus

This sample app demonstrates:

1. How to build specialized agents with Google ADK
2. Secure database access through MCP tools
3. Agent-to-agent communication for collaborative intelligence
4. Integration of Gemini LLM for enhanced recommendations
5. Building a user-friendly interface with Streamlit

## License

MIT
