"""
Procedural Orchestrator Agent for ADK Web

This agent demonstrates the educational procedural orchestration pattern
with clear, step-by-step multi-agent coordination. Perfect for learning
how agents work together in a predictable, transparent manner.

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

# Create the procedural orchestrator agent
agent = LlmAgent(
    name="ProceduralOrchestrator",
    description="""
    I am a **Procedural Financial Orchestrator** that demonstrates educational, 
    step-by-step multi-agent coordination for financial analysis.
    
    🎓 **Educational Focus**: I show you exactly how different AI agents work together
    in a clear, predictable sequence to analyze your financial situation.
    
    📋 **Step-by-Step Process**:
    1. **Spending Analysis Agent**: Analyzes your transaction history and spending patterns
    2. **Goal Planning Agent**: Evaluates your financial goals and feasibility
    3. **Advisor Agent**: Synthesizes insights and provides comprehensive recommendations
    
    🔍 **Transparent Workflow**: You can see each step of the analysis process,
    making it perfect for learning how multi-agent systems work.
    
    💡 **What I Can Help With**:
    - Complete financial health analysis with visible agent collaboration
    - Step-by-step spending pattern analysis
    - Goal feasibility assessment with clear reasoning
    - Comprehensive financial advice with transparent decision-making
    
    This is the **educational version** of our financial advisor system,
    designed to help you understand how AI agents coordinate to provide
    comprehensive financial insights.
    """,
    tools=[mcp_toolset],
    model="gemini-2.0-flash-exp"
)

logger.info("Procedural Orchestrator agent created for ADK Web")
