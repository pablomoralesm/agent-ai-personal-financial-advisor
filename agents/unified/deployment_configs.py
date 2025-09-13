"""
Deployment Configuration for Unified Multi-Agent System

This module provides configuration settings for different deployment contexts
(Streamlit and ADK Web) to ensure appropriate orchestration patterns.

Part of the Agentic AI Personal Financial Advisor application.
"""

from typing import Dict, Any
from enum import Enum

class DeploymentContext(Enum):
    """Deployment context enumeration."""
    STREAMLIT = "streamlit"
    ADK_WEB = "adk_web"

class OrchestratorType(Enum):
    """Orchestrator type enumeration."""
    PROCEDURAL = "procedural"
    INTELLIGENT = "intelligent"
    HYBRID = "hybrid"

class DeploymentConfig:
    """
    Configuration for different deployment contexts.
    
    Provides context-specific settings for orchestration, session management,
    and agent behavior across Streamlit and ADK Web platforms.
    """
    
    # Configuration for Streamlit (Educational Focus)
    STREAMLIT_CONFIG = {
        "orchestrator_type": OrchestratorType.PROCEDURAL,
        "use_runner": True,
        "session_service": "InMemorySessionService",
        "event_streaming": True,
        "educational_focus": True,
        "show_agent_collaboration": True,
        "step_by_step_workflow": True,
        "transparent_orchestration": True
    }
    
    # Configuration for ADK Web (Development Focus)
    ADK_WEB_CONFIG = {
        "orchestrator_type": OrchestratorType.HYBRID,  # Both available
        "use_runner": False,
        "session_service": "ADKWebSessionService",
        "event_streaming": False,
        "educational_focus": False,
        "show_agent_collaboration": False,
        "step_by_step_workflow": False,
        "transparent_orchestration": False,
        "orchestrator_selection": True
    }
    
    @classmethod
    def get_config(cls, context: str) -> Dict[str, Any]:
        """
        Get configuration for a specific deployment context.
        
        Args:
            context: Deployment context (streamlit, adk_web)
            
        Returns:
            Dictionary containing configuration settings
        """
        configs = {
            DeploymentContext.STREAMLIT.value: cls.STREAMLIT_CONFIG,
            DeploymentContext.ADK_WEB.value: cls.ADK_WEB_CONFIG
        }
        
        config = configs.get(context, cls.STREAMLIT_CONFIG)
        
        # Convert enums to values for easier use
        if isinstance(config.get("orchestrator_type"), OrchestratorType):
            config["orchestrator_type"] = config["orchestrator_type"].value
        
        return config
    
    @classmethod
    def is_educational_focus(cls, context: str) -> bool:
        """
        Check if the context has educational focus.
        
        Args:
            context: Deployment context
            
        Returns:
            True if educational focus, False otherwise
        """
        config = cls.get_config(context)
        return config.get("educational_focus", False)
    
    @classmethod
    def supports_orchestrator_type(cls, context: str, orchestrator_type: str) -> bool:
        """
        Check if a context supports a specific orchestrator type.
        
        Args:
            context: Deployment context
            orchestrator_type: Type of orchestrator
            
        Returns:
            True if supported, False otherwise
        """
        config = cls.get_config(context)
        context_orchestrator_type = config.get("orchestrator_type")
        
        if context_orchestrator_type == OrchestratorType.HYBRID.value:
            return orchestrator_type in [OrchestratorType.PROCEDURAL.value, OrchestratorType.INTELLIGENT.value]
        else:
            return context_orchestrator_type == orchestrator_type
    
    @classmethod
    def get_supported_orchestrator_types(cls, context: str) -> list:
        """
        Get supported orchestrator types for a context.
        
        Args:
            context: Deployment context
            
        Returns:
            List of supported orchestrator types
        """
        config = cls.get_config(context)
        context_orchestrator_type = config.get("orchestrator_type")
        
        if context_orchestrator_type == OrchestratorType.HYBRID.value:
            return [OrchestratorType.PROCEDURAL.value, OrchestratorType.INTELLIGENT.value]
        else:
            return [context_orchestrator_type]
