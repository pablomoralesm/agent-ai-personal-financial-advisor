"""
Orchestrator Agent for ADK Web

This agent demonstrates intelligent orchestration patterns where the LLM
dynamically decides how to coordinate agents based on the specific financial
analysis request. It can choose between individual agents or use the sequencer
for comprehensive analysis.

Part of the Agentic AI Personal Financial Advisor application.
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StdioConnectionParams
from mcp.client.stdio import StdioServerParameters
from utils.logging_config import get_logger

logger = get_logger(__name__)

# Get MCP server path
mcp_server_path = str(project_root / "mcp_server" / "database_server_stdio.py")

# Create MCP toolset for database access
mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=[mcp_server_path]
        )
    )
)

# Import the specialized agents
from agents.spending_analyzer.agent import agent as spending_analyzer_agent
from agents.goal_planner.agent import agent as goal_planner_agent
from agents.advisor.agent import agent as advisor_agent
from agents.sequencer.agent import agent as sequencer_agent

# Create agent tools for delegation
agent_tools = [
    agent_tool.AgentTool(agent=spending_analyzer_agent),
    agent_tool.AgentTool(agent=goal_planner_agent),
    agent_tool.AgentTool(agent=advisor_agent),
    agent_tool.AgentTool(agent=sequencer_agent)
]

# Combine agent tools with MCP tools
all_tools = agent_tools + [mcp_toolset]

# Create the orchestrator agent
agent = LlmAgent(
    name="OrchestratorAgent",
    description="""
    I am an **Intelligent Financial Orchestrator** that uses advanced AI reasoning
    to dynamically coordinate agents for optimal financial analysis.

    🧠 **Intelligent Coordination**: I analyze your request and intelligently decide
    which approach to use for the best results.

    🎯 **Adaptive Approach**: I can choose between:
    - **Individual Agents**: For specific, focused analysis
    - **Sequencer Agent**: For comprehensive, step-by-step analysis
    - **Direct Database Access**: For quick data queries and insights
    - **Custom Workflows**: Tailored approaches for unique situations

    🔄 **Available Agents**:
    - **SpendingAnalyzerAgent**: For transaction and spending pattern analysis
    - **GoalPlannerAgent**: For financial goal setting and tracking
    - **AdvisorAgent**: For financial advice and recommendations
    - **SequencerAgent**: For comprehensive step-by-step analysis

    💡 **What I Can Help With**:
    - **Quick Analysis**: "Analyze spending for customer 1" → Uses SpendingAnalyzerAgent
    - **Goal Planning**: "Plan goals for customer 2" → Uses GoalPlannerAgent
    - **Full Analysis**: "Complete analysis for customer 3" → Uses SequencerAgent
    - **Direct Queries**: "Show me customer 1's transactions" → Direct database access
    - **Custom Requests**: I'll choose the best combination of agents and tools

    **Examples:**
    - "Analyze customer 1's spending" → I'll use SpendingAnalyzerAgent
    - "Do a full financial analysis for customer 2" → I'll use SequencerAgent
    - "Help with goals for customer 3" → I'll use GoalPlannerAgent

    **IMPORTANT**: When delegating to other agents, always provide clear context
    and include the customer ID in your requests. For example:
    - "Please analyze spending patterns for customer 1"
    - "Create a goal plan for customer 2 based on their financial situation"
    - "Provide comprehensive financial advice for customer 3"
    
    **For SequencerAgent**: When calling the SequencerAgent for full analysis,
    pass the customer ID in JSON format: {"customer_id": "1"}

    **SAVE ALL RESULTS**: Always use `save_advice` to record any analysis results
    or recommendations in the database before displaying them to the user.
    This ensures all financial advice is properly stored for future reference.

    I'm the **intelligent coordinator** that decides the best approach
    for your specific financial analysis needs.
    """,
    tools=all_tools,
    model="gemini-2.0-flash-exp"
)

logger.info("Intelligent Orchestrator agent created for ADK Web")
