"""
Base Agent Classes for Unified Multi-Agent System

This module provides base classes that extract common patterns from existing
agents, providing a unified foundation for both Streamlit and ADK Web contexts.

Part of the Agentic AI Personal Financial Advisor application.
"""

from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from pathlib import Path

from google.adk.agents import LlmAgent, BaseAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StdioConnectionParams
from mcp.client.stdio import StdioServerParameters

from utils.logging_config import get_logger

logger = get_logger(__name__)

class UnifiedAgentBase(ABC):
    """
    Abstract base class for unified agents.
    
    Provides common initialization patterns, MCP setup, and error handling
    that work across both Streamlit and ADK Web contexts.
    """
    
    def __init__(self, name: str, mcp_server_path: str, deployment_context: str):
        """
        Initialize the unified agent base.
        
        Args:
            name: Name of the agent
            mcp_server_path: Path to the MCP database server script
            deployment_context: Context (streamlit, adk_web)
        """
        self.name = name
        self.mcp_server_path = Path(mcp_server_path)
        self.deployment_context = deployment_context
        self.agent = self._create_agent()
        
        logger.info(f"UnifiedAgentBase '{name}' initialized for {deployment_context}")
    
    def _create_agent(self) -> LlmAgent:
        """
        Create the LLM agent with common configuration.
        
        Returns:
            Configured LlmAgent instance
        """
        # Create MCP toolset for database access
        mcp_toolset = McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='python3',
                    args=[str(self.mcp_server_path)]
                )
            )
        )
        
        # Get agent-specific configuration
        config = self._get_agent_config()
        
        # Create the LLM agent
        agent = LlmAgent(
            name=config['name'],
            model=config['model'],
            instruction=config['instruction'],
            description=config['description'],
            tools=[mcp_toolset] + config.get('additional_tools', [])
        )
        
        return agent
    
    @abstractmethod
    def _get_agent_config(self) -> Dict[str, Any]:
        """
        Get agent-specific configuration.
        
        Returns:
            Dictionary containing agent configuration
        """
        pass
    
    def get_agent(self) -> LlmAgent:
        """
        Get the underlying LLM agent.
        
        Returns:
            The LLM agent instance
        """
        return self.agent

class UnifiedAgent(UnifiedAgentBase):
    """
    Concrete implementation of unified agent.
    
    Provides a standard agent implementation that can be used across
    different deployment contexts with consistent behavior.
    """
    
    def __init__(self, name: str, mcp_server_path: str, deployment_context: str, 
                 model: str = "gemini-2.0-flash", instruction: str = "", 
                 description: str = "", additional_tools: List = None):
        """
        Initialize the unified agent.
        
        Args:
            name: Name of the agent
            mcp_server_path: Path to the MCP database server script
            deployment_context: Context (streamlit, adk_web)
            model: LLM model to use
            instruction: Agent instruction text
            description: Agent description
            additional_tools: Additional tools beyond MCP
        """
        self.model = model
        self.instruction = instruction
        self.description = description
        self.additional_tools = additional_tools or []
        
        super().__init__(name, mcp_server_path, deployment_context)
    
    def _get_agent_config(self) -> Dict[str, Any]:
        """
        Get agent configuration.
        
        Returns:
            Dictionary containing agent configuration
        """
        return {
            'name': self.name,
            'model': self.model,
            'instruction': self.instruction,
            'description': self.description,
            'additional_tools': self.additional_tools
        }

class UnifiedOrchestratorBase(BaseAgent):
    """
    Base class for unified orchestrators.
    
    Provides common orchestration patterns that work across both
    Streamlit and ADK Web contexts.
    """
    
    def __init__(self, name: str, description: str, mcp_server_path: str, 
                 deployment_context: str, sub_agents: List = None):
        """
        Initialize the unified orchestrator base.
        
        Args:
            name: Name of the orchestrator
            description: Description of the orchestrator
            mcp_server_path: Path to the MCP database server script
            deployment_context: Context (streamlit, adk_web)
            sub_agents: List of sub-agents to orchestrate
        """
        # Initialize BaseAgent with sub-agents first
        super().__init__(
            name=name,
            description=description,
            sub_agents=[agent.agent if hasattr(agent, 'agent') else agent 
                       for agent in (sub_agents or [])]
        )
        
        # Store attributes after super().__init__ using object.__setattr__
        object.__setattr__(self, '_mcp_server_path', Path(mcp_server_path))
        object.__setattr__(self, '_deployment_context', deployment_context)
        object.__setattr__(self, '_sub_agents', sub_agents or [])
        
        logger.info(f"UnifiedOrchestratorBase '{name}' initialized for {deployment_context}")
    
    @property
    def mcp_server_path(self):
        """Get MCP server path."""
        return self._mcp_server_path
    
    @property
    def deployment_context(self):
        """Get deployment context."""
        return self._deployment_context
    
    @property
    def sub_agents(self):
        """Get sub-agents list."""
        return self._sub_agents
    
    def get_sub_agent(self, agent_name: str):
        """
        Get a sub-agent by name.
        
        Args:
            agent_name: Name of the sub-agent
            
        Returns:
            Sub-agent instance if found, None otherwise
        """
        for agent in self._sub_agents:
            if hasattr(agent, 'name') and agent.name == agent_name:
                return agent
            elif hasattr(agent, 'agent') and hasattr(agent.agent, 'name') and agent.agent.name == agent_name:
                return agent
        return None
    
    def get_all_sub_agents(self) -> List:
        """
        Get all sub-agents.
        
        Returns:
            List of all sub-agents
        """
        return self._sub_agents
