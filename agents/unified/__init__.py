"""
Unified Agent Components

This module provides shared components for multi-agent systems that work
across both Streamlit and ADK Web contexts. It includes base classes,
factory functions, and both procedural and intelligent orchestrators.

Part of the Agentic AI Personal Financial Advisor application.
"""

from .base_agent import UnifiedAgent, UnifiedAgentBase, UnifiedOrchestratorBase
from .agent_factory import AgentFactory, OrchestratorFactory
from .procedural_orchestrator import ProceduralOrchestrator
from .intelligent_orchestrator import IntelligentOrchestrator
from .deployment_configs import DeploymentConfig, DeploymentContext, OrchestratorType

__all__ = [
    'UnifiedAgent',
    'UnifiedAgentBase',
    'UnifiedOrchestratorBase',
    'AgentFactory',
    'OrchestratorFactory',
    'ProceduralOrchestrator',
    'IntelligentOrchestrator',
    'DeploymentConfig',
    'DeploymentContext',
    'OrchestratorType'
]
