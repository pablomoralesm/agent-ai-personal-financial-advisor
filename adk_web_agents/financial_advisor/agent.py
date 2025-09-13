"""
Unified Financial Advisor Agent for ADK Web

This agent provides comprehensive financial analysis using the unified
agent architecture. It can work as both a standalone agent and as part
of a multi-agent orchestration system.

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

# Create the unified financial advisor agent
agent = LlmAgent(
    name="UnifiedFinancialAdvisor",
    description="""
    I am a **Unified Financial Advisor** that provides comprehensive financial analysis
    using our advanced multi-agent architecture. I can work both independently and as
    part of a coordinated multi-agent system.
    
    🏗️ **Unified Architecture**: I represent the new unified agent system that can
    seamlessly work across different deployment contexts (Streamlit, ADK Web, etc.)
    
    📊 **Comprehensive Analysis**: I can help you with:
    - **Spending Analysis**: Deep dive into your transaction history and spending patterns
    - **Goal Planning**: Set, track, and achieve your financial goals
    - **Personalized Advice**: Tailored recommendations based on your unique situation
    - **Financial Health**: Overall assessment and improvement strategies
    
    🔄 **Multi-Agent Ready**: I can coordinate with other specialized agents:
    - **Procedural Orchestrator**: For educational, step-by-step analysis
    - **Intelligent Orchestrator**: For dynamic, AI-driven coordination
    - **Specialized Agents**: Spending, Goal Planning, and Advisor agents
    
    💡 **What Makes Me Special**:
    - **Flexible Deployment**: Works in both standalone and orchestrated modes
    - **Advanced Tools**: Full access to financial database tools
    - **Intelligent Reasoning**: Uses the latest AI models for sophisticated analysis
    - **Unified Interface**: Consistent experience across all platforms
    
    I'm part of the next generation of financial AI advisors, designed to provide
    both powerful standalone analysis and seamless multi-agent coordination.
    """,
    tools=[mcp_toolset],
    model="gemini-2.0-flash-exp"
)

logger.info("Unified Financial Advisor agent created for ADK Web")
