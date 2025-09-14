"""
Advisor Agent for ADK Web

This agent provides comprehensive financial advice and recommendations.
It can be used both standalone and as a tool by orchestrators.

Part of the Agentic AI Personal Financial Advisor application.
"""

from .agent import agent

# Export the agent for ADK Web discovery
root_agent = agent

__all__ = ['agent', 'root_agent']
