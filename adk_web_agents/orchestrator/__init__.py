"""
Intelligent Orchestrator Agent for ADK Web

This agent provides intelligent, LLM-based financial analysis using
the intelligent orchestration pattern. Perfect for production scenarios
where the AI decides the best approach dynamically.

Part of the Agentic AI Personal Financial Advisor application.
"""

from .agent import agent as intelligent_orchestrator_agent

# Export the main agent for ADK Web discovery
root_agent = intelligent_orchestrator_agent

__all__ = ['intelligent_orchestrator_agent', 'root_agent']
