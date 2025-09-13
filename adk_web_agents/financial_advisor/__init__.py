"""
Financial Advisor Agent for ADK Web

This agent provides comprehensive financial analysis and advice using
the MCP database server tools.
"""

from .agent import agent

# ADK Web expects the agent to be exposed as 'root_agent'
root_agent = agent

__all__ = ['agent', 'root_agent']
