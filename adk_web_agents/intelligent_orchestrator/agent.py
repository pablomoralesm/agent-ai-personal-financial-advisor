"""
Intelligent Orchestrator Agent for ADK Web

This agent demonstrates the intelligent orchestration pattern where the LLM
dynamically decides how to coordinate multiple specialized agents based on
the specific financial analysis request. Perfect for production scenarios.

Part of the Agentic AI Personal Financial Advisor application.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from google.adk.agents import LlmAgent
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

# Create the intelligent orchestrator agent
agent = LlmAgent(
    name="IntelligentOrchestrator",
    description="""
    I am an **Intelligent Financial Orchestrator** that uses advanced AI reasoning
    to dynamically coordinate multiple specialized agents for optimal financial analysis.
    
    🧠 **Intelligent Coordination**: I analyze your request and intelligently decide
    which specialized agents to involve and in what order for the best results.
    
    🎯 **Adaptive Approach**: Unlike fixed workflows, I adapt my strategy based on:
    - Your specific financial questions
    - The complexity of your situation
    - The most effective analysis sequence
    - Real-time insights from each step
    
    🔄 **Dynamic Agent Selection**: I can coordinate:
    - **Spending Analysis Agent**: For transaction and spending pattern analysis
    - **Goal Planning Agent**: For financial goal setting and tracking
    - **Advisor Agent**: For comprehensive financial advice and recommendations
    - **Custom Analysis**: Tailored approaches for unique situations
    
    💡 **What I Can Help With**:
    - Complex financial scenarios requiring adaptive analysis
    - Multi-faceted financial questions with dynamic agent coordination
    - Production-level financial advice with intelligent reasoning
    - Advanced financial planning with AI-driven orchestration
    
    This is the **intelligent version** of our financial advisor system,
    designed for sophisticated financial analysis where the AI dynamically
    determines the best approach for your specific needs.
    """,
    tools=[mcp_toolset],
    model="gemini-2.0-flash-exp"
)

logger.info("Intelligent Orchestrator agent created for ADK Web")
