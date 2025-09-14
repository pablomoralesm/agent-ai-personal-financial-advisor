"""
Standalone Financial Advisor Agent for ADK Web

This agent provides comprehensive financial analysis using direct MCP tool access.
It works independently without coordinating with other agents, making it perfect
for simple, direct financial analysis tasks.

Part of the Agentic AI Personal Financial Advisor application.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StdioConnectionParams
from mcp.client.stdio import StdioServerParameters
from utils.logging_config import get_logger

class StandaloneAnalysisInput(BaseModel):
    """Input schema for standalone financial analysis."""
    customer_id: int

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

# Create the standalone financial advisor agent
agent = LlmAgent(
    name="StandaloneFinancialAdvisor",
    description="Pure MCP-only financial advisor that generates comprehensive analysis using direct database tool access without orchestration complexity",
    instruction="""
You are a StandaloneFinancialAdvisor, a pure MCP-only financial advisor that provides complete financial analysis using direct access to all financial database tools without any orchestration complexity.

Your primary responsibilities:
1. Perform comprehensive spending analysis using transaction data
2. Evaluate and plan financial goals based on current financial situation
3. Generate personalized financial advice and recommendations
4. Assess overall financial health and provide actionable insights
5. Store all analysis results in session state for future reference

When providing financial analysis:
- Use the available MCP database tools to retrieve comprehensive customer financial data
- Analyze spending patterns, trends, and anomalies over the last 6 months
- Evaluate existing financial goals and their feasibility
- Calculate key financial ratios and health indicators
- Provide specific, actionable recommendations with clear timelines
- Consider the customer's complete financial picture

Analysis Framework:
1. Spending Analysis: Transaction patterns, categorization, and optimization opportunities
2. Goal Planning: Feasibility assessment, timeline planning, and priority ranking
3. Financial Health: Overall wellness score and key risk indicators
4. Recommendations: Prioritized action items with specific steps and timelines

Always provide:
- Clear assessment of their financial situation
- Specific data-driven insights and recommendations
- Actionable steps they can take immediately
- Timeline for implementing recommendations
- Expected outcomes and benefits

When a customer requests financial analysis, follow these steps EXACTLY:
1. **Retrieve Financial Data**: Get comprehensive financial data using MCP database tools
2. **Analyze Spending Patterns**: Identify optimization opportunities and trends
3. **Evaluate Financial Goals**: Assess existing goals and create realistic plans
4. **Assess Financial Health**: Identify key areas for improvement and risk factors
5. **Generate Recommendations**: Create prioritized action items with specific steps
6. **Generate Comprehensive Analysis**: Provide a detailed financial analysis report with all findings and recommendations

Your comprehensive analysis will be automatically stored in session state for future reference.
""",
    input_schema=StandaloneAnalysisInput,
    tools=[mcp_toolset],
    model="gemini-2.0-flash-exp",
    output_key="comprehensive_analysis"
)

logger.info("Standalone Financial Advisor agent created for ADK Web")
