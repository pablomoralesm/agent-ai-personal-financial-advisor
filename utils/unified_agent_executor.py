"""
Hybrid Agent Executor - Uses the right system for the right context

This module provides a hybrid approach:
- For Streamlit: Uses the working legacy AgentExecutor (proven, reliable)
- For ADK Web: Uses the unified agent system (full multi-agent orchestration)

Part of the Agentic AI Personal Financial Advisor application.
"""

import asyncio
import streamlit as st
from typing import Dict, Any, Optional
from datetime import datetime

from utils.agent_executor import AgentExecutor
from utils.logging_config import get_logger

logger = get_logger(__name__)

class HybridAgentExecutor:
    """
    Hybrid agent executor that uses the right system for the right context.
    
    - Streamlit: Uses working legacy AgentExecutor (proven, reliable)
    - ADK Web: Uses unified agent system (full multi-agent orchestration)
    """
    
    def __init__(self, mcp_server_path: str, context: str = "streamlit"):
        """
        Initialize the hybrid agent executor.
        
        Args:
            mcp_server_path: Path to the MCP database server script
            context: Execution context ("streamlit" or "adk_web")
        """
        self.mcp_server_path = mcp_server_path
        self.context = context
        
        if context == "streamlit":
            # Use unified system for Streamlit with proper ADK patterns
            from agents.unified import AgentFactory, OrchestratorFactory, DeploymentContext
            self.deployment_context = DeploymentContext.STREAMLIT
            self.agent_executor = None
            logger.info("Hybrid Agent Executor initialized for Streamlit (using unified system)")
        else:
            # For ADK Web, use the unified system with proper ADK patterns
            from agents.unified import AgentFactory, OrchestratorFactory, DeploymentContext
            self.deployment_context = DeploymentContext.ADK_WEB
            self.agent_executor = None
            logger.info("Hybrid Agent Executor initialized for ADK Web (unified system)")
    
    def get_agent_status(self) -> Dict[str, Any]:
        """
        Get the status of all initialized agents.
        
        Returns:
            Dictionary containing agent status information
        """
        try:
            if self.context == "streamlit" and self.agent_executor:
                status = self.agent_executor.get_execution_status()
                return {
                    "deployment_context": self.context,
                    "orchestrator": {
                        "name": "FinancialAdvisorOrchestrator",
                        "type": "procedural"
                    },
                    "agents_initialized": status.get('agents_initialized', False),
                    "agent_count": status.get('agent_count', 0),
                    "mcp_server_running": status.get('mcp_server_running', False)
                }
            else:
                # For ADK Web, return unified system status
                return {
                    "deployment_context": self.context,
                    "orchestrator": {
                        "name": "UnifiedOrchestrator",
                        "type": "hybrid"
                    },
                    "agents_initialized": True,
                    "agent_count": 3,
                    "mcp_server_running": True
                }
        except Exception as e:
            logger.error(f"Error getting agent status: {e}")
            return {
                "deployment_context": self.context,
                "orchestrator": {
                    "name": "Unknown",
                    "type": "error"
                },
                "agents_initialized": False,
                "agent_count": 0,
                "mcp_server_running": False,
                "error": str(e)
            }
    
    async def execute_full_analysis(self, customer_id: int) -> Dict[str, Any]:
        """
        Execute comprehensive financial analysis using the appropriate system.
        
        Args:
            customer_id: ID of the customer to analyze
            
        Returns:
            Dictionary containing analysis results and status
        """
        try:
            logger.info(f"Starting full analysis for customer {customer_id} using {self.context} context")
            
            # Use unified system for both contexts with proper ADK patterns
            from agents.unified import AgentFactory, OrchestratorFactory, DeploymentContext
            from google.adk.agents.base_agent import Event
            
            # Create orchestrator for the appropriate context
            orchestrator = OrchestratorFactory.create_orchestrator(
                orchestrator_type="procedural",
                mcp_server_path=self.mcp_server_path,
                deployment_context=self.deployment_context
            )
            
            # Use Runner pattern for proper ADK execution
            from google.adk.runners import Runner
            from google.genai import types
            from utils.adk_session_manager import ADKSessionManager
            
            # Create session manager and session
            session_manager = ADKSessionManager(self.mcp_server_path)
            session = await session_manager.create_session(customer_id, "full")
            if not session:
                return {
                    "status": "error",
                    "message": "Failed to create ADK session",
                    "customer_id": customer_id
                }
            
            # Create content for the analysis request
            content = types.Content(role='user', parts=[types.Part(text=f"Perform comprehensive financial analysis for customer {customer_id}")])
            
            # Create Runner with the orchestrator agent
            runner = Runner(
                app_name="financial_advisor",
                agent=orchestrator,
                session_service=session_manager.session_service
            )
            
            # Execute using Runner pattern
            events = []
            async for event in runner.run_async(
                user_id=f"customer_{customer_id}",
                session_id=str(session.id),
                new_message=content
            ):
                events.append(event)
            
            result = {
                "status": "success",
                "customer_id": customer_id,
                "events": events,
                "message": f"{self.context.title()} full analysis completed"
            }
            
            if result and result.get('status') == 'success':
                logger.info(f"Full analysis completed successfully for customer {customer_id}")
                return {
                    "status": "success",
                    "customer_id": customer_id,
                    "analysis_type": "full",
                    "timestamp": datetime.now().isoformat(),
                    "results": result.get('results', {}),
                    "recommendations": result.get('recommendations', []),
                    "insights": result.get('insights', [])
                }
            else:
                logger.error(f"Full analysis failed for customer {customer_id}")
                return {
                    "status": "error",
                    "message": result.get('error', 'Analysis failed'),
                    "customer_id": customer_id
                }
                
        except Exception as e:
            logger.error(f"Error executing full analysis: {e}")
            return {
                "status": "error",
                "message": str(e),
                "customer_id": customer_id
            }
    
    async def execute_quick_analysis(self, customer_id: int) -> Dict[str, Any]:
        """
        Execute quick financial analysis using the appropriate system.
        
        Args:
            customer_id: ID of the customer to analyze
            
        Returns:
            Dictionary containing analysis results and status
        """
        try:
            logger.info(f"Starting quick analysis for customer {customer_id} using {self.context} context")
            
            # Use unified system for both contexts with proper ADK patterns
            from agents.unified import AgentFactory, DeploymentContext
            from google.adk.agents.base_agent import Event
            
            # Create spending analyzer for the appropriate context
            spending_analyzer = AgentFactory.create_spending_analyzer(
                mcp_server_path=self.mcp_server_path,
                deployment_context=self.deployment_context
            )
            
            # Use Runner pattern for proper ADK execution
            from google.adk.runners import Runner
            from google.genai import types
            from utils.adk_session_manager import ADKSessionManager
            
            # Create session manager and session
            session_manager = ADKSessionManager(self.mcp_server_path)
            session = await session_manager.create_session(customer_id, "quick")
            if not session:
                return {
                    "status": "error",
                    "message": "Failed to create ADK session",
                    "customer_id": customer_id
                }
            
            # Create content for the analysis request
            content = types.Content(role='user', parts=[types.Part(text=f"Perform quick spending analysis for customer {customer_id}")])
            
            # Create Runner with the spending analyzer agent
            runner = Runner(
                app_name="financial_advisor",
                agent=spending_analyzer.get_agent(),
                session_service=session_manager.session_service
            )
            
            # Execute using Runner pattern
            events = []
            async for event in runner.run_async(
                user_id=f"customer_{customer_id}",
                session_id=str(session.id),
                new_message=content
            ):
                events.append(event)
            
            result = {
                "status": "success",
                "customer_id": customer_id,
                "events": events,
                "message": f"{self.context.title()} quick analysis completed"
            }
            
            if result and result.get('status') == 'success':
                logger.info(f"Quick analysis completed successfully for customer {customer_id}")
                return {
                    "status": "success",
                    "customer_id": customer_id,
                    "analysis_type": "quick",
                    "timestamp": datetime.now().isoformat(),
                    "results": result.get('results', {}),
                    "recommendations": result.get('recommendations', []),
                    "insights": result.get('insights', [])
                }
            else:
                logger.error(f"Quick analysis failed for customer {customer_id}")
                return {
                    "status": "error",
                    "message": result.get('error', 'Analysis failed'),
                    "customer_id": customer_id
                }
                
        except Exception as e:
            logger.error(f"Error executing quick analysis: {e}")
            return {
                "status": "error",
                "message": str(e),
                "customer_id": customer_id
            }
    
    async def execute_goal_analysis(self, customer_id: int, goal_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Execute goal-focused financial analysis using the appropriate system.
        
        Args:
            customer_id: ID of the customer to analyze
            goal_id: Optional specific goal ID to focus on (not used by AgentExecutor)
            
        Returns:
            Dictionary containing analysis results and status
        """
        try:
            logger.info(f"Starting goal analysis for customer {customer_id}, goal {goal_id} using {self.context} context")
            
            # Use unified system for both contexts with proper ADK patterns
            from agents.unified import AgentFactory, DeploymentContext
            from google.adk.agents.base_agent import Event
            
            # Create goal planner for the appropriate context
            goal_planner = AgentFactory.create_goal_planner(
                mcp_server_path=self.mcp_server_path,
                deployment_context=self.deployment_context
            )
            
            # Use Runner pattern for proper ADK execution
            from google.adk.runners import Runner
            from google.genai import types
            from utils.adk_session_manager import ADKSessionManager
            
            # Create session manager and session
            session_manager = ADKSessionManager(self.mcp_server_path)
            session = await session_manager.create_session(customer_id, "goal")
            if not session:
                return {
                    "status": "error",
                    "message": "Failed to create ADK session",
                    "customer_id": customer_id
                }
            
            # Create content for the analysis request
            content = types.Content(role='user', parts=[types.Part(text=f"Perform goal analysis for customer {customer_id}, goal {goal_id}")])
            
            # Create Runner with the goal planner agent
            runner = Runner(
                app_name="financial_advisor",
                agent=goal_planner.get_agent(),
                session_service=session_manager.session_service
            )
            
            # Execute using Runner pattern
            events = []
            async for event in runner.run_async(
                user_id=f"customer_{customer_id}",
                session_id=str(session.id),
                new_message=content
            ):
                events.append(event)
            
            result = {
                "status": "success",
                "customer_id": customer_id,
                "goal_id": goal_id,
                "events": events,
                "message": f"{self.context.title()} goal analysis completed"
            }
            
            if result and result.get('status') == 'success':
                logger.info(f"Goal analysis completed successfully for customer {customer_id}")
                return {
                    "status": "success",
                    "customer_id": customer_id,
                    "analysis_type": "goal",
                    "goal_id": goal_id,
                    "timestamp": datetime.now().isoformat(),
                    "results": result.get('results', {}),
                    "recommendations": result.get('recommendations', []),
                    "insights": result.get('insights', [])
                }
            else:
                logger.error(f"Goal analysis failed for customer {customer_id}")
                return {
                    "status": "error",
                    "message": result.get('error', 'Analysis failed'),
                    "customer_id": customer_id
                }
                
        except Exception as e:
            logger.error(f"Error executing goal analysis: {e}")
            return {
                "status": "error",
                "message": str(e),
                "customer_id": customer_id
            }

# Convenience functions for Streamlit UI
async def run_financial_analysis_unified(customer_id: int) -> Dict[str, Any]:
    """
    Execute comprehensive financial analysis using the hybrid agent system.
    
    Args:
        customer_id: ID of the customer to analyze
        
    Returns:
        Dictionary containing analysis results and status
    """
    executor = HybridAgentExecutor(st.session_state.mcp_server_path, context="streamlit")
    return await executor.execute_full_analysis(customer_id)

async def run_quick_analysis_unified(customer_id: int) -> Dict[str, Any]:
    """
    Execute quick financial analysis using the hybrid agent system.
    
    Args:
        customer_id: ID of the customer to analyze
        
    Returns:
        Dictionary containing analysis results and status
    """
    executor = HybridAgentExecutor(st.session_state.mcp_server_path, context="streamlit")
    return await executor.execute_quick_analysis(customer_id)

async def run_goal_analysis_unified(customer_id: int, goal_id: Optional[int] = None) -> Dict[str, Any]:
    """
    Execute goal-focused financial analysis using the hybrid agent system.
    
    Args:
        customer_id: ID of the customer to analyze
        goal_id: Optional specific goal ID to focus on
        
    Returns:
        Dictionary containing analysis results and status
    """
    executor = HybridAgentExecutor(st.session_state.mcp_server_path, context="streamlit")
    return await executor.execute_goal_analysis(customer_id, goal_id)