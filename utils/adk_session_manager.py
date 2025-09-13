"""
ADK Session Manager - Manages ADK sessions and agent execution

This module provides the core functionality for creating ADK sessions,
initializing agents, and managing MCP server connections for real
agent execution in the Personal Financial Advisor application.

Part of the Agentic AI Personal Financial Advisor application.
"""

import os
import asyncio
import subprocess
import time
from typing import Dict, Any, Optional, List
from pathlib import Path

from google.adk.sessions import Session, InMemorySessionService

from agents.spending_analyzer import SpendingAnalyzerAgent
from agents.goal_planner import GoalPlannerAgent
from agents.advisor import AdvisorAgent
from agents.orchestrator import FinancialAdvisorOrchestrator

from utils.logging_config import get_logger

logger = get_logger(__name__)

class ADKSessionManager:
    """
    Manages ADK sessions and agent execution for the financial advisor application.
    
    Responsibilities:
    - Create and manage ADK sessions
    - Initialize agent instances with proper configuration
    - Ensure MCP server is running and healthy
    - Provide session context for agent execution
    - Manage agent lifecycle and cleanup
    """
    
    def __init__(self, mcp_server_path: str):
        """
        Initialize the ADK Session Manager.
        
        Args:
            mcp_server_path: Path to the MCP database server script
        """
        self.mcp_server_path = Path(mcp_server_path)
        self.session_service = InMemorySessionService()
        self._agents = {}
        self._mcp_process = None
        
        logger.info(f"ADK Session Manager initialized with MCP server: {mcp_server_path}")
    
    def ensure_mcp_server_running(self) -> bool:
        """
        Ensure MCP server is running and healthy.
        
        Returns:
            True if MCP server is running and accessible, False otherwise
        """
        try:
            # Check if MCP server file exists
            if not self.mcp_server_path.exists():
                logger.error(f"MCP server file not found: {self.mcp_server_path}")
                return False
            
            # Check if MCP server process is already running
            if self._mcp_process and self._mcp_process.poll() is None:
                logger.info("MCP server is already running")
                return True
            
            # Start MCP server
            logger.info("Starting MCP server...")
            self._mcp_process = subprocess.Popen(
                ['python3', str(self.mcp_server_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait a moment for server to start
            time.sleep(2)
            
            # Check if process is running
            if self._mcp_process.poll() is None:
                logger.info("MCP server started successfully")
                return True
            else:
                logger.error("MCP server failed to start")
                return False
                
        except Exception as e:
            logger.error(f"Error starting MCP server: {e}")
            return False
    
    def verify_mcp_tools_available(self) -> bool:
        """
        Verify that all required MCP tools are accessible.
        
        Returns:
            True if all tools are available, False otherwise
        """
        try:
            # This is a basic check - in a real implementation, we would
            # test actual tool connectivity through the MCP protocol
            if not self.ensure_mcp_server_running():
                return False
            
            # For now, we'll assume tools are available if server is running
            # In a production system, we would test each tool individually
            logger.info("MCP tools verification completed (basic check)")
            return True
            
        except Exception as e:
            logger.error(f"MCP tools verification failed: {e}")
            return False
    
    def initialize_agents(self) -> bool:
        """
        Initialize all agent instances.
        
        Returns:
            True if all agents initialized successfully, False otherwise
        """
        try:
            logger.info("Initializing agents...")
            
            # Verify MCP server is running
            if not self.verify_mcp_tools_available():
                logger.error("Cannot initialize agents: MCP server not available")
                return False
            
            # Initialize individual agents
            self._agents['spending_analyzer'] = SpendingAnalyzerAgent(str(self.mcp_server_path))
            self._agents['goal_planner'] = GoalPlannerAgent(str(self.mcp_server_path))
            self._agents['advisor'] = AdvisorAgent(str(self.mcp_server_path))
            
            # Initialize orchestrator
            self._agents['orchestrator'] = FinancialAdvisorOrchestrator(str(self.mcp_server_path))
            
            logger.info("All agents initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing agents: {e}")
            return False
    
    async def create_session(self, customer_id: int, analysis_type: str = "full") -> Optional[Session]:
        """
        Create a new ADK session for agent execution.
        
        Args:
            customer_id: ID of the customer to analyze
            analysis_type: Type of analysis to perform
            
        Returns:
            ADK Session object if successful, None otherwise
        """
        try:
            # Ensure agents are initialized
            if not self._agents:
                if not self.initialize_agents():
                    logger.error("Cannot create session: agents not initialized")
                    return None
            
            # Create session with proper parameters
            session = await self.session_service.create_session(
                app_name="financial_advisor",
                user_id=f"customer_{customer_id}",
                state={
                    "customer_id": customer_id,
                    "analysis_type": analysis_type,
                    "created_at": time.time(),
                    "status": "initialized"
                }
            )
            
            logger.info(f"Created ADK session for customer {customer_id}, type: {analysis_type}")
            return session
            
        except Exception as e:
            logger.error(f"Error creating ADK session: {e}")
            return None
    
    def get_agent(self, agent_name: str):
        """
        Get an agent instance by name.
        
        Args:
            agent_name: Name of the agent to retrieve
            
        Returns:
            Agent instance if found, None otherwise
        """
        return self._agents.get(agent_name)
    
    def get_orchestrator(self):
        """
        Get the orchestrator agent instance.
        
        Returns:
            FinancialAdvisorOrchestrator instance if available, None otherwise
        """
        return self._agents.get('orchestrator')
    
    def cleanup(self):
        """
        Clean up resources and stop MCP server.
        """
        try:
            if self._mcp_process and self._mcp_process.poll() is None:
                logger.info("Stopping MCP server...")
                self._mcp_process.terminate()
                self._mcp_process.wait(timeout=5)
                logger.info("MCP server stopped")
            
            # Clear agent references
            self._agents.clear()
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def get_session_status(self) -> Dict[str, Any]:
        """
        Get the current status of the session manager.
        
        Returns:
            Dictionary containing status information
        """
        mcp_running = False
        if self._mcp_process:
            mcp_running = self._mcp_process.poll() is None
        
        return {
            "mcp_server_running": mcp_running,
            "agents_initialized": len(self._agents) > 0,
            "agent_count": len(self._agents),
            "mcp_server_path": str(self.mcp_server_path),
            "session_service_available": self.session_service is not None
        }
