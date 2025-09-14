"""
Procedural Orchestrator Agent for ADK Web

This agent provides educational, step-by-step financial analysis using
the procedural orchestration pattern. Perfect for learning how multi-agent
systems work with clear, predictable workflows.

Part of the Agentic AI Personal Financial Advisor application.
"""

from .agent import agent as procedural_orchestrator_agent

# Export the main agent for ADK Web discovery
root_agent = procedural_orchestrator_agent

__all__ = ['procedural_orchestrator_agent', 'root_agent']
