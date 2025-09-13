"""
OrchestratorAgent - Coordinates all financial advisor agents

This agent orchestrates the SpendingAnalyzer, GoalPlanner, and Advisor agents
using ADK's built-in multi-agent capabilities including session state sharing
and AgentTool delegation patterns.

Part of the Agentic AI Personal Financial Advisor application.
"""

from typing import List, Dict, Any, Optional
import json
from datetime import datetime
import os

from google.adk.agents import LlmAgent, BaseAgent
from google.adk.tools import agent_tool
from google.adk.events import Event
from google.genai.types import Content, Part

from agents.spending_analyzer import create_spending_analyzer_agent
from agents.goal_planner import create_goal_planner_agent
from agents.advisor import create_advisor_agent
from utils.logging_config import get_logger

logger = get_logger(__name__)

class FinancialAdvisorOrchestrator(BaseAgent):
    """
    Custom orchestrator agent that coordinates all financial advisor agents.
    
    Uses ADK's BaseAgent pattern for custom orchestration logic as described
    in the ADK documentation. Manages the workflow of:
    1. SpendingAnalyzerAgent - analyzes spending patterns
    2. GoalPlannerAgent - evaluates and plans financial goals  
    3. AdvisorAgent - synthesizes insights and provides recommendations
    
    Implements agent collaboration through session state sharing and
    direct agent delegation using AgentTool pattern.
    """
    
    def __init__(self, mcp_server_path: str):
        """
        Initialize the orchestrator with all sub-agents.
        
        Args:
            mcp_server_path: Path to the MCP database server script
        """
        # Create all sub-agents first
        spending_analyzer = create_spending_analyzer_agent(mcp_server_path)
        goal_planner = create_goal_planner_agent(mcp_server_path)
        advisor = create_advisor_agent(mcp_server_path, spending_analyzer, goal_planner)
        
        # Create list of sub-agents for ADK framework
        sub_agents = [
            spending_analyzer.agent,
            goal_planner.agent, 
            advisor.agent
        ]
        
        # Initialize BaseAgent with sub-agents first
        super().__init__(
            name="FinancialAdvisorOrchestrator",
            description="Orchestrates spending analysis, goal planning, and comprehensive financial advice",
            sub_agents=sub_agents
        )
        
        # Store references after parent initialization
        self._mcp_server_path = mcp_server_path
        self._spending_analyzer = spending_analyzer
        self._goal_planner = goal_planner
        self._advisor = advisor
        
        logger.info("FinancialAdvisorOrchestrator initialized successfully")
    
    async def _run_async_impl(self, ctx):
        """
        Custom orchestration logic implementing the financial advisor workflow.
        
        This method implements the core asynchronous execution logic as required
        by ADK's BaseAgent pattern. It coordinates the three agents to provide
        comprehensive financial advice.
        """
        try:
            # Get customer ID from context or session state
            customer_id = ctx.session.state.get('customer_id')
            if not customer_id:
                yield Event(author=self.name, content=Content(parts=[Part(text="Error: No customer ID provided. Please specify a customer ID to analyze.")]))
                return
            
            logger.info(f"Starting financial advisor orchestration for customer {customer_id}")
            
            # Initialize session state for orchestration
            ctx.session.state['orchestration_start_time'] = datetime.now().isoformat()
            ctx.session.state['current_step'] = 'initialization'
            
            yield Event(author=self.name, content=Content(parts=[Part(text=f"🏦 Starting comprehensive financial analysis for customer {customer_id}...")]))
            
            # Step 1: Spending Analysis
            ctx.session.state['current_step'] = 'spending_analysis'
            yield Event(author=self.name, content=Content(parts=[Part(text="📊 Analyzing spending patterns and habits...")]))
            
            # Run spending analysis through the SpendingAnalyzer
            async for event in self._spending_analyzer.agent.run_async(ctx):
                # Forward events from spending analyzer
                yield event
            
            spending_result = await self._spending_analyzer.analyze_customer_spending(ctx, customer_id)
            
            if spending_result.get('status') == 'error':
                yield Event(author=self.name, content=Content(parts=[Part(text=f"❌ Spending analysis failed: {spending_result.get('error')}")]))
                return
            
            yield Event(author=self.name, content=Content(parts=[Part(text="✅ Spending analysis completed successfully")]))
            
            # Step 2: Goal Planning and Feasibility Analysis
            ctx.session.state['current_step'] = 'goal_planning'
            yield Event(author=self.name, content=Content(parts=[Part(text="🎯 Evaluating financial goals and creating savings plans...")]))
            
            # Run goal feasibility analysis
            goal_result = await self._goal_planner.evaluate_goal_feasibility(ctx, customer_id)
            
            if goal_result.get('status') == 'error':
                yield Event(author=self.name, content=Content(parts=[Part(text=f"⚠️ Goal planning completed with warnings: {goal_result.get('error')}")]))
            else:
                yield Event(author=self.name, content=Content(parts=[Part(text="✅ Goal feasibility analysis completed successfully")]))
            
            # Step 3: Comprehensive Advice Generation
            ctx.session.state['current_step'] = 'advice_generation'
            yield Event(author=self.name, content=Content(parts=[Part(text="💡 Synthesizing insights and generating comprehensive recommendations...")]))
            
            # Run comprehensive advice generation
            advice_result = await self._advisor.provide_comprehensive_advice(ctx, customer_id)
            
            if advice_result.get('status') == 'error':
                yield Event(author=self.name, content=Content(parts=[Part(text=f"❌ Advice generation failed: {advice_result.get('error')}")]))
                return
            
            yield Event(author=self.name, content=Content(parts=[Part(text="✅ Comprehensive financial advice generated successfully")]))
            
            # Step 4: Final Summary and Next Steps
            ctx.session.state['current_step'] = 'completion'
            
            # Create final summary from session state data
            summary = self._create_orchestration_summary(ctx, customer_id)
            
            yield Event(author=self.name, content=Content(parts=[Part(text=f"""
🎉 **Financial Analysis Complete!**

**Summary for Customer {customer_id}:**

{summary}

**Next Steps:**
1. Review the detailed recommendations provided
2. Implement the top priority actions within 30 days
3. Set up automatic savings transfers for goal achievement
4. Schedule a follow-up review in 3 months

All analysis data and recommendations have been saved to your profile for future reference.
""")]))
            
            # Store final orchestration status
            ctx.session.state['orchestration_status'] = 'completed'
            ctx.session.state['completion_time'] = datetime.now().isoformat()
            
            logger.info(f"Financial advisor orchestration completed successfully for customer {customer_id}")
            
        except Exception as e:
            logger.error(f"Error in orchestration: {e}")
            yield Event(author=self.name, content=Content(parts=[Part(text=f"❌ Orchestration failed with error: {str(e)}")]))
            ctx.session.state['orchestration_status'] = 'failed'
            ctx.session.state['error'] = str(e)
    
    def _create_orchestration_summary(self, ctx, customer_id: int) -> str:
        """
        Create a summary of the orchestration results.
        
        Args:
            ctx: ADK invocation context
            customer_id: ID of the customer
            
        Returns:
            String summary of the analysis results
        """
        try:
            summary_parts = []
            
            # Spending Analysis Summary
            spending_analysis = ctx.session.state.get('spending_analysis', {})
            if spending_analysis:
                summary_parts.append("✅ **Spending Analysis:** Completed - patterns and optimization opportunities identified")
            else:
                summary_parts.append("⚠️ **Spending Analysis:** Limited data available")
            
            # Goal Planning Summary
            goal_feasibility = ctx.session.state.get('goal_feasibility', {})
            if goal_feasibility:
                summary_parts.append("✅ **Goal Planning:** Completed - feasibility assessed and savings plans created")
            else:
                summary_parts.append("⚠️ **Goal Planning:** Limited goal data available")
            
            # Comprehensive Advice Summary
            comprehensive_advice = ctx.session.state.get('comprehensive_advice', {})
            if comprehensive_advice:
                summary_parts.append("✅ **Financial Advice:** Comprehensive recommendations generated with priority actions")
            else:
                summary_parts.append("❌ **Financial Advice:** Generation failed or incomplete")
            
            return "\n".join(summary_parts)
            
        except Exception as e:
            logger.error(f"Error creating summary: {e}")
            return "⚠️ Summary generation encountered issues - please review individual analysis results"
    
    async def run_quick_analysis(self, ctx, customer_id: int, focus_area: Optional[str] = None) -> Dict[str, Any]:
        """
        Run a quick analysis focused on immediate actionable insights.
        
        Args:
            ctx: ADK invocation context
            customer_id: ID of the customer
            focus_area: Optional focus area (spending, goals, emergency)
            
        Returns:
            Dictionary containing quick analysis results
        """
        try:
            logger.info(f"Running quick analysis for customer {customer_id}")
            
            # Set customer ID in session state
            ctx.session.state['customer_id'] = customer_id
            ctx.session.state['analysis_type'] = 'quick'
            ctx.session.state['focus_area'] = focus_area
            
            # Run quick spending insights
            await self._spending_analyzer.get_spending_insights(ctx, customer_id)
            
            # Get quick recommendations from advisor
            result = await self._advisor.provide_quick_recommendations(ctx, customer_id, focus_area)
            
            return {
                'status': 'completed',
                'customer_id': customer_id,
                'focus_area': focus_area,
                'spending_insights': ctx.session.state.get('spending_insights', {}),
                'recommendations': ctx.session.state.get('quick_recommendations', {}),
                'analysis_type': 'quick'
            }
            
        except Exception as e:
            logger.error(f"Error in quick analysis: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'customer_id': customer_id
            }
    
    async def run_goal_focused_analysis(self, ctx, customer_id: int, goal_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Run analysis focused specifically on financial goals.
        
        Args:
            ctx: ADK invocation context
            customer_id: ID of the customer
            goal_id: Optional specific goal ID to focus on
            
        Returns:
            Dictionary containing goal-focused analysis results
        """
        try:
            logger.info(f"Running goal-focused analysis for customer {customer_id}")
            
            # Set context in session state
            ctx.session.state['customer_id'] = customer_id
            ctx.session.state['analysis_type'] = 'goal_focused'
            ctx.session.state['target_goal_id'] = goal_id
            
            # Run spending analysis to understand capacity
            await self._spending_analyzer.get_spending_insights(ctx, customer_id)
            
            # Run comprehensive goal analysis
            await self._goal_planner.evaluate_goal_feasibility(ctx, customer_id, goal_id)
            await self._goal_planner.track_goal_progress(ctx, customer_id)
            
            if goal_id:
                # Create specific savings plan for the goal
                await self._goal_planner.create_savings_plan(ctx, customer_id, goal_id)
            
            # Get goal-specific recommendations
            await self._advisor.provide_quick_recommendations(ctx, customer_id, 'goals')
            
            return {
                'status': 'completed',
                'customer_id': customer_id,
                'goal_id': goal_id,
                'goal_feasibility': ctx.session.state.get('goal_feasibility', {}),
                'goal_progress': ctx.session.state.get('goal_progress', {}),
                'savings_plan': ctx.session.state.get('savings_plan', {}),
                'recommendations': ctx.session.state.get('quick_recommendations', {}),
                'analysis_type': 'goal_focused'
            }
            
        except Exception as e:
            logger.error(f"Error in goal-focused analysis: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'customer_id': customer_id,
                'goal_id': goal_id
            }

def create_financial_advisor_orchestrator(mcp_server_path: str) -> FinancialAdvisorOrchestrator:
    """
    Factory function to create a FinancialAdvisorOrchestrator instance.
    
    Args:
        mcp_server_path: Path to the MCP database server script
        
    Returns:
        Configured FinancialAdvisorOrchestrator instance
    """
    return FinancialAdvisorOrchestrator(mcp_server_path)
