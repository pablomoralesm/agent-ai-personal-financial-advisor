"""
Agent Executor - Handles real agent execution using ADK

This module provides the functions to execute real agents through the ADK
framework, replacing placeholder functions with actual agent execution
using MCP tools and Gemini models.

Part of the Agentic AI Personal Financial Advisor application.
"""

import asyncio
import streamlit as st
from typing import Dict, Any, List, Optional
from datetime import datetime

from utils.adk_session_manager import ADKSessionManager
from utils.logging_config import get_logger

logger = get_logger(__name__)

class AgentExecutor:
    """
    Executes agents using the ADK framework for real financial analysis.
    
    This class replaces placeholder functions with actual agent execution,
    ensuring that all analysis is performed by real AI agents using
    MCP tools and Gemini models.
    """
    
    def __init__(self, mcp_server_path: str):
        """
        Initialize the Agent Executor.
        
        Args:
            mcp_server_path: Path to the MCP database server script
        """
        self.mcp_server_path = mcp_server_path
        self.session_manager = ADKSessionManager(mcp_server_path)
        
        logger.info("Agent Executor initialized")
    
    async def execute_full_analysis(self, customer_id: int) -> Dict[str, Any]:
        """
        Execute comprehensive financial analysis using the orchestrator agent.
        
        Args:
            customer_id: ID of the customer to analyze
            
        Returns:
            Dictionary containing analysis results and status
        """
        try:
            logger.info(f"Starting full analysis for customer {customer_id}")
            
            # Create ADK session
            session = await self.session_manager.create_session(customer_id, "full")
            if not session:
                return {
                    "status": "error",
                    "message": "Failed to create ADK session",
                    "customer_id": customer_id
                }
            
            # Get orchestrator agent
            orchestrator = self.session_manager.get_orchestrator()
            if not orchestrator:
                return {
                    "status": "error", 
                    "message": "Orchestrator agent not available",
                    "customer_id": customer_id
                }
            
            # Create Runner for agent execution
            from google.adk.runners import Runner
            from google.genai import types
            
            # Create content for the full analysis request
            content = types.Content(role='user', parts=[types.Part(text=f"Perform comprehensive financial analysis for customer {customer_id}")])
            
            # Create Runner with the orchestrator agent
            runner = Runner(
                app_name="financial_advisor",
                agent=orchestrator,
                session_service=self.session_manager.session_service
            )
            
            # Execute orchestrator using Runner
            results = []
            async def run_orchestrator():
                async for event in runner.run_async(
                    user_id=f"customer_{customer_id}",
                    session_id=str(session.id),
                    new_message=content
                ):
                    if hasattr(event, 'content') and event.content:
                        results.append({
                            'type': getattr(event, 'event_type', 'content'),
                            'content': str(event.content),
                            'timestamp': datetime.now().isoformat()
                        })
            
            # Run async execution in a separate thread to avoid event loop conflicts
            import concurrent.futures
            import threading
            
            def run_async_in_thread():
                """Run the async function in a new event loop in a separate thread"""
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    return loop.run_until_complete(run_orchestrator())
                finally:
                    loop.close()
            
            # Execute in a separate thread
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(run_async_in_thread)
                future.result()  # Wait for completion
            
            # Get final results from session state
            final_results = session.state.get('orchestration_status', 'unknown')
            
            logger.info(f"Full analysis completed for customer {customer_id}")
            
            return {
                "status": "success",
                "customer_id": customer_id,
                "analysis_type": "full",
                "results": results,
                "final_status": final_results,
                "session_id": str(session.id) if hasattr(session, 'id') else 'unknown'
            }
            
        except Exception as e:
            logger.error(f"Error in full analysis: {e}")
            return {
                "status": "error",
                "message": str(e),
                "customer_id": customer_id
            }
    
    async def execute_quick_analysis(self, customer_id: int) -> Dict[str, Any]:
        """
        Execute quick spending analysis using the SpendingAnalyzerAgent.
        
        Args:
            customer_id: ID of the customer to analyze
            
        Returns:
            Dictionary containing spending analysis results
        """
        try:
            logger.info(f"Starting quick analysis for customer {customer_id}")
            
            # Create ADK session
            session = await self.session_manager.create_session(customer_id, "quick")
            if not session:
                return {
                    "status": "error",
                    "message": "Failed to create ADK session",
                    "customer_id": customer_id
                }
            
            # Get spending analyzer agent
            spending_analyzer = self.session_manager.get_agent('spending_analyzer')
            if not spending_analyzer:
                return {
                    "status": "error",
                    "message": "SpendingAnalyzer agent not available",
                    "customer_id": customer_id
                }
            
            # Create Runner for agent execution
            from google.adk.runners import Runner
            from google.genai import types
            
            # Create content for the analysis request
            content = types.Content(role='user', parts=[types.Part(text=f"Analyze spending patterns for customer {customer_id}")])
            
            # Create Runner with the spending analyzer agent
            runner = Runner(
                app_name="financial_advisor",
                agent=spending_analyzer.agent,
                session_service=self.session_manager.session_service
            )
            
            # Execute spending analysis using Runner
            results = []
            async def run_spending_analysis():
                async for event in runner.run_async(
                    user_id=f"customer_{customer_id}",
                    session_id=str(session.id),
                    new_message=content
                ):
                    if hasattr(event, 'content') and event.content:
                        results.append({
                            'type': getattr(event, 'event_type', 'content'),
                            'content': str(event.content),
                            'timestamp': datetime.now().isoformat()
                        })
            
            # Run async execution in a separate thread to avoid event loop conflicts
            import concurrent.futures
            import threading
            
            def run_async_in_thread():
                """Run the async function in a new event loop in a separate thread"""
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    return loop.run_until_complete(run_spending_analysis())
                finally:
                    loop.close()
            
            # Execute in a separate thread
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(run_async_in_thread)
                future.result()  # Wait for completion
            
            # Get spending analysis results from session state
            spending_results = session.state.get('spending_analysis', {})
            
            logger.info(f"Quick analysis completed for customer {customer_id}")
            
            return {
                "status": "success",
                "customer_id": customer_id,
                "analysis_type": "quick",
                "results": results,
                "spending_analysis": spending_results,
                "session_id": str(session.id) if hasattr(session, 'id') else 'unknown'
            }
            
        except Exception as e:
            logger.error(f"Error in quick analysis: {e}")
            return {
                "status": "error",
                "message": str(e),
                "customer_id": customer_id
            }
    
    async def execute_goal_analysis(self, customer_id: int) -> Dict[str, Any]:
        """
        Execute goal-focused analysis using the GoalPlannerAgent.
        
        Args:
            customer_id: ID of the customer to analyze
            
        Returns:
            Dictionary containing goal analysis results
        """
        try:
            logger.info(f"Starting goal analysis for customer {customer_id}")
            
            # Create ADK session
            session = await self.session_manager.create_session(customer_id, "goal")
            if not session:
                return {
                    "status": "error",
                    "message": "Failed to create ADK session",
                    "customer_id": customer_id
                }
            
            # Get goal planner agent
            goal_planner = self.session_manager.get_agent('goal_planner')
            if not goal_planner:
                return {
                    "status": "error",
                    "message": "GoalPlanner agent not available",
                    "customer_id": customer_id
                }
            
            # Create Runner for agent execution
            from google.adk.runners import Runner
            from google.genai import types
            
            # Create content for the goal analysis request
            content = types.Content(role='user', parts=[types.Part(text=f"Analyze financial goals for customer {customer_id}")])
            
            # Create Runner with the goal planner agent
            runner = Runner(
                app_name="financial_advisor",
                agent=goal_planner.agent,
                session_service=self.session_manager.session_service
            )
            
            # Execute goal analysis using Runner
            results = []
            async def run_goal_analysis():
                async for event in runner.run_async(
                    user_id=f"customer_{customer_id}",
                    session_id=str(session.id),
                    new_message=content
                ):
                    if hasattr(event, 'content') and event.content:
                        results.append({
                            'type': getattr(event, 'event_type', 'content'),
                            'content': str(event.content),
                            'timestamp': datetime.now().isoformat()
                        })
            
            # Run async execution in a separate thread to avoid event loop conflicts
            import concurrent.futures
            import threading
            
            def run_async_in_thread():
                """Run the async function in a new event loop in a separate thread"""
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    return loop.run_until_complete(run_goal_analysis())
                finally:
                    loop.close()
            
            # Execute in a separate thread
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(run_async_in_thread)
                future.result()  # Wait for completion
            
            # Get goal analysis results from session state
            goal_results = session.state.get('goal_feasibility', {})
            savings_plan = session.state.get('savings_plan', {})
            
            logger.info(f"Goal analysis completed for customer {customer_id}")
            
            return {
                "status": "success",
                "customer_id": customer_id,
                "analysis_type": "goal",
                "results": results,
                "goal_feasibility": goal_results,
                "savings_plan": savings_plan,
                "session_id": str(session.id) if hasattr(session, 'id') else 'unknown'
            }
            
        except Exception as e:
            logger.error(f"Error in goal analysis: {e}")
            return {
                "status": "error",
                "message": str(e),
                "customer_id": customer_id
            }
    
    def get_execution_status(self) -> Dict[str, Any]:
        """
        Get the current status of the agent executor.
        
        Returns:
            Dictionary containing execution status information
        """
        return self.session_manager.get_session_status()
    
    async def execute_spending_analysis(self, customer_id: int) -> Dict[str, Any]:
        """
        Execute spending analysis using SpendingAnalyzerAgent.
        
        Args:
            customer_id: ID of the customer to analyze
            
        Returns:
            Dictionary containing spending analysis results
        """
        return await self.execute_quick_analysis(customer_id)
    
    async def execute_goal_analysis(self, customer_id: int) -> Dict[str, Any]:
        """
        Execute goal analysis using GoalPlannerAgent.
        
        Args:
            customer_id: ID of the customer to analyze
            
        Returns:
            Dictionary containing goal analysis results
        """
        try:
            logger.info(f"Starting goal analysis for customer {customer_id}")
            
            # Create ADK session
            session = await self.session_manager.create_session(customer_id, "goal")
            if not session:
                return {
                    "status": "error",
                    "message": "Failed to create ADK session",
                    "customer_id": customer_id
                }
            
            # Get orchestrator and run goal-focused analysis
            orchestrator = self.session_manager.get_orchestrator()
            if not orchestrator:
                return {
                    "status": "error",
                    "message": "Orchestrator agent not available",
                    "customer_id": customer_id
                }
            
            # Use orchestrator's goal-focused analysis
            result = await orchestrator.run_goal_focused_analysis(
                session, customer_id
            )
            
            return {
                "status": "completed",
                "customer_id": customer_id,
                "analysis_type": "goal_focused",
                **result
            }
            
        except Exception as e:
            logger.error(f"Error in goal analysis: {e}")
            return {
                "status": "error",
                "message": str(e),
                "customer_id": customer_id
            }

    def cleanup(self):
        """
        Clean up resources and stop all agents.
        """
        self.session_manager.cleanup()
        logger.info("Agent Executor cleanup completed")
