"""
Sequencer Agent for ADK Web

This agent provides step-by-step sequential execution of financial analysis
using specialized agents. It demonstrates procedural orchestration patterns
with clear, predictable workflow execution using the ADK SequentialAgent.

Part of the Agentic AI Personal Financial Advisor application.
"""

import os
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from google.adk.agents import SequentialAgent
from utils.logging_config import get_logger

logger = get_logger(__name__)

# Import the specialized agents
from agents.spending_analyzer.agent import agent as spending_analyzer_agent
from agents.goal_planner.agent import agent as goal_planner_agent
from agents.advisor.agent import agent as advisor_agent

# Create the SequentialAgent with the specialized agents as sub-agents
agent = SequentialAgent(
    name="SequencerAgent",
    description="""Sequential Financial Analysis Orchestrator

Executes financial analysis in a predictable, step-by-step sequence:
1. Spending Analysis - Analyzes spending patterns and categories
2. Goal Planning - Reviews and suggests financial goals  
3. Advisory Services - Provides personalized recommendations

This agent demonstrates procedural orchestration with clear workflow execution.
Perfect for when you need predictable, sequential analysis steps.

The SequentialAgent automatically runs sub-agents in order and shares session state
between them, allowing each agent to build upon the previous agent's results.

Input Format: JSON with customer_id field
Example: {"customer_id": "1"}
""",
    sub_agents=[spending_analyzer_agent, goal_planner_agent, advisor_agent]
)

logger.info("Sequencer agent created for ADK Web using SequentialAgent")