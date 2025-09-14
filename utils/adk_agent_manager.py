"""
ADK Agent Manager - Direct integration of ADK Web agents into Streamlit

This module provides direct access to ADK Web agents without modifying them.
Uses the working adk_web_agents as-is for maximum stability.
"""

import asyncio
import streamlit as st
from typing import Dict, Any, Optional
from datetime import datetime
from utils.logging_config import get_logger

# Import ADK Web agents directly (NO MODIFICATIONS)
from adk_web_agents.sequencer.agent import agent as sequencer_agent
from adk_web_agents.standalone.agent import agent as standalone_agent

logger = get_logger(__name__)

class ADKAgentManager:
    """
    Manages direct integration of ADK Web agents into Streamlit.
    
    This class provides a clean interface to the working ADK Web agents
    without modifying them, ensuring maximum stability.
    """
    
    def __init__(self, mcp_server_path: str):
        self.mcp_server_path = mcp_server_path
        logger.info("ADK Agent Manager initialized with direct agent integration")
    
    async def run_full_analysis(self, customer_id: int) -> Dict[str, Any]:
        """
        Run comprehensive financial analysis using the SequencerAgent.
        
        The SequencerAgent provides step-by-step multi-agent coordination:
        1. Spending Analyzer Agent
        2. Goal Planner Agent  
        3. Advisor Agent
        
        Args:
            customer_id: ID of the customer to analyze
            
        Returns:
            Dictionary containing analysis results and status
        """
        try:
            logger.info(f"Starting full analysis for customer {customer_id}")
            
            # Import required ADK components
            from google.adk.runners import Runner
            from google.adk.sessions import InMemorySessionService
            from google.genai import types
            
            # Create session service and session
            session_service = InMemorySessionService()
            session = await session_service.create_session(
                app_name="financial_advisor",
                user_id=f"customer_{customer_id}",
                session_id=f"analysis_{customer_id}_{int(datetime.now().timestamp())}"
            )
            
            # Create content for the analysis request
            content = types.Content(
                role='user', 
                parts=[types.Part(text=f"Perform comprehensive financial analysis for customer {customer_id}")]
            )
            
            # Create Runner with the sequencer agent
            runner = Runner(
                app_name="financial_advisor",
                agent=sequencer_agent,
                session_service=session_service
            )
            
            # Execute sequencer agent using Runner
            results = []
            agent_summaries = {}
            agent_outputs = {}
            
            async for event in runner.run_async(
                user_id=f"customer_{customer_id}",
                session_id=str(session.id),
                new_message=content
            ):
                if hasattr(event, 'content') and event.content:
                    content_str = str(event.content)
                    results.append({
                        'type': getattr(event, 'event_type', 'content'),
                        'content': content_str,
                        'timestamp': datetime.now().isoformat()
                    })
                    
                    # Extract agent summaries from content
                    if hasattr(event, 'author') and event.author:
                        agent_name = event.author
                        if agent_name not in agent_summaries:
                            agent_summaries[agent_name] = []
                        agent_summaries[agent_name].append(content_str)
                        logger.info(f"Captured summary from {agent_name}: {len(content_str)} chars")
                
                # Extract structured outputs from agents
                if hasattr(event, 'agent_outputs') and event.agent_outputs:
                    for agent_name, output in event.agent_outputs.items():
                        agent_outputs[agent_name] = output
                        logger.info(f"Captured output from {agent_name}: {type(output)}")
            
            # Get the final session state to extract agent outputs
            try:
                final_session = await session_service.get_session(str(session.id))
                if hasattr(final_session, 'agent_outputs') and final_session.agent_outputs:
                    agent_outputs.update(final_session.agent_outputs)
                    logger.info(f"Final session agent outputs: {list(agent_outputs.keys())}")
            except Exception as e:
                logger.warning(f"Could not get final session state: {e}")
            
            # Extract specific agent outputs
            spending_analysis = agent_outputs.get('spending_analysis', {})
            goal_planning = agent_outputs.get('goal_planning', {})
            financial_advice = agent_outputs.get('financial_advice', {})
            
            # Create comprehensive result from agent outputs and summaries
            analysis_result = {
                "events": results,
                "agent_outputs": agent_outputs,
                "agent_summaries": agent_summaries,
                "spending_analysis": spending_analysis,
                "goal_planning": goal_planning,
                "financial_advice": financial_advice,
                "summary": self._create_analysis_summary(agent_summaries, agent_outputs, customer_id)
            }
            
            logger.info(f"Full analysis completed for customer {customer_id}")
            return {
                "status": "success",
                "analysis_type": "full",
                "customer_id": customer_id,
                "result": analysis_result,
                "agent_used": "SequencerAgent"
            }
            
        except Exception as e:
            logger.error(f"Error in full analysis for customer {customer_id}: {str(e)}")
            return {
                "status": "error",
                "analysis_type": "full", 
                "customer_id": customer_id,
                "error": str(e),
                "agent_used": "SequencerAgent"
            }
    
    async def run_quick_analysis(self, customer_id: int) -> Dict[str, Any]:
        """
        Run quick financial analysis using the StandaloneAgent.
        
        The StandaloneAgent provides pure MCP-only analysis without orchestration.
        
        Args:
            customer_id: ID of the customer to analyze
            
        Returns:
            Dictionary containing analysis results and status
        """
        try:
            logger.info(f"Starting quick analysis for customer {customer_id}")
            
            # Import required ADK components
            from google.adk.runners import Runner
            from google.adk.sessions import InMemorySessionService
            from google.genai import types
            
            # Create session service and session
            session_service = InMemorySessionService()
            session = await session_service.create_session(
                app_name="financial_advisor",
                user_id=f"customer_{customer_id}",
                session_id=f"quick_analysis_{customer_id}_{int(datetime.now().timestamp())}"
            )
            
            # Create content for the analysis request
            content = types.Content(
                role='user', 
                parts=[types.Part(text=f"Perform quick financial analysis for customer {customer_id}")]
            )
            
            # Create Runner with the standalone agent
            runner = Runner(
                app_name="financial_advisor",
                agent=standalone_agent,
                session_service=session_service
            )
            
            # Execute standalone agent using Runner
            results = []
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
            
            logger.info(f"Quick analysis completed for customer {customer_id}")
            return {
                "status": "success",
                "analysis_type": "quick",
                "customer_id": customer_id,
                "result": {
                    "events": results,
                    "summary": "Quick financial analysis completed using StandaloneAgent"
                },
                "agent_used": "StandaloneAgent"
            }
            
        except Exception as e:
            logger.error(f"Error in quick analysis for customer {customer_id}: {str(e)}")
            return {
                "status": "error",
                "analysis_type": "quick",
                "customer_id": customer_id,
                "error": str(e),
                "agent_used": "StandaloneAgent"
            }
    
    def _create_analysis_summary(self, agent_summaries: Dict[str, list], agent_outputs: Dict[str, Any], customer_id: int) -> str:
        """
        Create a comprehensive summary from agent summaries and outputs.
        
        Args:
            agent_summaries: Dictionary containing summaries from all agents
            agent_outputs: Dictionary containing structured outputs from all agents
            customer_id: ID of the customer being analyzed
            
        Returns:
            Formatted summary string
        """
        try:
            summary_parts = []
            
            # Use agent summaries first (these are the actual generated content)
            for agent_name, summaries in agent_summaries.items():
                if summaries:
                    # Join all summaries from this agent
                    agent_summary = "\n".join(summaries)
                    # Truncate if too long
                    if len(agent_summary) > 500:
                        agent_summary = agent_summary[:500] + "..."
                    summary_parts.append(f"**{agent_name}:**\n{agent_summary}")
            
            # If we have agent summaries, use them
            if summary_parts:
                return "\n\n".join(summary_parts)
            
            # Fallback to structured outputs
            if agent_outputs:
                for agent_name, output in agent_outputs.items():
                    if isinstance(output, dict) and output.get('summary'):
                        summary_parts.append(f"**{agent_name}:** {output['summary']}")
                    elif isinstance(output, str):
                        summary_parts.append(f"**{agent_name}:** {output[:200]}...")
            
            # If we have structured outputs, use them
            if summary_parts:
                return "\n\n".join(summary_parts)
            
            # Final fallback
            return f"Comprehensive financial analysis completed for customer {customer_id} using SequencerAgent."
            
        except Exception as e:
            logger.error(f"Error creating analysis summary: {e}")
            return f"Financial analysis completed for customer {customer_id} using SequencerAgent."

    def get_agent_status(self) -> Dict[str, Any]:
        """
        Get status information about available agents.
        
        Returns:
            Dictionary containing agent status information
        """
        return {
            "deployment_context": "streamlit",
            "agent_manager": "ADKAgentManager",
            "available_agents": [
                "SequencerAgent (Full Analysis)",
                "StandaloneAgent (Quick Analysis)"
            ],
            "integration_type": "direct",
            "mcp_server_path": self.mcp_server_path
        }

# Convenience functions for Streamlit UI
async def run_full_analysis_adk(customer_id: int) -> Dict[str, Any]:
    """
    Convenience function for Streamlit UI to run full analysis.
    
    Args:
        customer_id: ID of the customer to analyze
        
    Returns:
        Dictionary containing analysis results and status
    """
    manager = ADKAgentManager(mcp_server_path=st.session_state.mcp_server_path)
    return await manager.run_full_analysis(customer_id)

async def run_quick_analysis_adk(customer_id: int) -> Dict[str, Any]:
    """
    Convenience function for Streamlit UI to run quick analysis.
    
    Args:
        customer_id: ID of the customer to analyze
        
    Returns:
        Dictionary containing analysis results and status
    """
    manager = ADKAgentManager(mcp_server_path=st.session_state.mcp_server_path)
    return await manager.run_quick_analysis(customer_id)
