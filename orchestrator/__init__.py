"""
Orchestrator module for Agent-to-Agent (A2A) communication.

This module coordinates the collaboration between different agents,
managing the flow of information and ensuring proper sequencing
of agent operations.
"""

from .agent_coordinator import AgentCoordinator

__all__ = ["AgentCoordinator"]
