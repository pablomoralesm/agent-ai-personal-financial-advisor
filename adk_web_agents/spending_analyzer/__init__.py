"""
Spending Analyzer Agent for ADK Web

This agent specializes in analyzing customer spending patterns and habits.
It can be used both standalone and as a tool by orchestrators.

Part of the Agentic AI Personal Financial Advisor application.
"""

from .agent import agent

# Export the agent for ADK Web discovery
root_agent = agent

__all__ = ['agent', 'root_agent']
