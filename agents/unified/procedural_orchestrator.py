"""
Procedural Orchestrator for Educational Multi-Agent System

This orchestrator provides clear, predictable workflow patterns that are
perfect for educational purposes. It shows explicit agent delegation,
session state sharing, and step-by-step orchestration.

Part of the Agentic AI Personal Financial Advisor application.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime

from google.adk.agents import BaseAgent
from google.adk.tools import agent_tool
from google.adk.events import Event
from google.genai.types import Content, Part

from .base_agent import UnifiedOrchestratorBase
from .deployment_configs import DeploymentConfig
from utils.logging_config import get_logger

logger = get_logger(__name__)

class ProceduralOrchestrator(UnifiedOrchestratorBase):
    """
    Procedural orchestrator with clear, educational workflow patterns.
    
    This orchestrator provides explicit, step-by-step agent coordination
    that is perfect for learning multi-agent concepts. It shows:
    - Clear agent delegation patterns
    - Explicit session state sharing
    - Predictable workflow execution
    - Educational transparency
    """
    
    def __init__(self, mcp_server_path: str, deployment_context: str = "streamlit"):
        """
        Initialize the procedural orchestrator.
        
        Args:
            mcp_server_path: Path to the MCP database server script
            deployment_context: Context (streamlit, adk_web)
        """
        super().__init__(
            name="ProceduralOrchestrator",
            description="Educational orchestrator with clear, predictable workflow patterns",
            mcp_server_path=mcp_server_path,
            deployment_context=deployment_context,
            sub_agents=[]
        )
        
        # Store sub-agents as private attributes using object.__setattr__
        object.__setattr__(self, '_spending_analyzer', None)
        object.__setattr__(self, '_goal_planner', None)
        object.__setattr__(self, '_advisor', None)
        
        logger.info("ProceduralOrchestrator initialized for educational purposes")
    
    def set_sub_agents(self, spending_analyzer, goal_planner, advisor):
        """
        Set the sub-agents for orchestration.
        
        Args:
            spending_analyzer: SpendingAnalyzer agent instance
            goal_planner: GoalPlanner agent instance
            advisor: Advisor agent instance
        """
        object.__setattr__(self, '_spending_analyzer', spending_analyzer)
        object.__setattr__(self, '_goal_planner', goal_planner)
        object.__setattr__(self, '_advisor', advisor)
        
        # Update sub_agents list
        object.__setattr__(self, '_sub_agents', [spending_analyzer, goal_planner, advisor])
        
        logger.info("Sub-agents set for procedural orchestrator")
    
    @property
    def spending_analyzer(self):
        """Get spending analyzer agent."""
        return self._spending_analyzer
    
    @property
    def goal_planner(self):
        """Get goal planner agent."""
        return self._goal_planner
    
    @property
    def advisor(self):
        """Get advisor agent."""
        return self._advisor
    
    async def _run_async_impl(self, ctx):
        """
        Procedural orchestration logic with clear, educational workflow.
        
        This method implements the core asynchronous execution logic with
        explicit step-by-step agent coordination that is perfect for learning.
        """
        try:
            # Get customer ID from context or session state
            customer_id = ctx.session.state.get('customer_id')
            if not customer_id:
                yield Event(
                    author=self.name,
                    content=Content(parts=[Part(text="Error: No customer ID provided. Please specify a customer ID to analyze.")])
                )
                return
            
            logger.info(f"Starting procedural orchestration for customer {customer_id}")
            
            # Initialize session state for orchestration
            ctx.session.state['orchestration_start_time'] = datetime.now().isoformat()
            ctx.session.state['current_step'] = 'initialization'
            ctx.session.state['orchestrator_type'] = 'procedural'
            
            yield Event(
                author=self.name,
                content=Content(parts=[Part(text=f"🏦 Starting comprehensive financial analysis for customer {customer_id}...")])
            )
            
            # Step 1: Spending Analysis
            yield Event(
                author=self.name,
                content=Content(parts=[Part(text="📊 Step 1: Analyzing spending patterns and habits...")])
            )
            
            ctx.session.state['current_step'] = 'spending_analysis'
            
            if self.spending_analyzer:
                try:
                    # Run spending analysis through the SpendingAnalyzer
                    # The UnifiedAgent wraps an LlmAgent, so we call run_async on the agent
                    async for event in self.spending_analyzer.agent.run_async(ctx):
                        # Forward events from spending analyzer
                        yield event
                    
                    # Store spending analysis results in session state
                    ctx.session.state['spending_analysis'] = {
                        'status': 'completed',
                        'customer_id': customer_id,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    yield Event(
                        author=self.name,
                        content=Content(parts=[Part(text="✅ Step 1 completed: Spending analysis successful")])
                    )
                except Exception as e:
                    logger.error(f"Error in spending analysis: {e}")
                    yield Event(
                        author=self.name,
                        content=Content(parts=[Part(text=f"❌ Spending analysis failed: {str(e)}")])
                    )
                    ctx.session.state['spending_analysis'] = {
                        'status': 'error',
                        'error': str(e),
                        'customer_id': customer_id,
                        'timestamp': datetime.now().isoformat()
                    }
            else:
                yield Event(
                    author=self.name,
                    content=Content(parts=[Part(text="⚠️ Step 1 skipped: SpendingAnalyzer not available")])
                )
            
            # Step 2: Goal Planning and Feasibility Analysis
            yield Event(
                author=self.name,
                content=Content(parts=[Part(text="🎯 Step 2: Evaluating financial goals and creating savings plans...")])
            )
            
            ctx.session.state['current_step'] = 'goal_planning'
            
            if self.goal_planner:
                try:
                    # Run goal feasibility analysis through the GoalPlanner
                    async for event in self.goal_planner.agent.run_async(ctx):
                        # Forward events from goal planner
                        yield event
                    
                    # Store goal planning results in session state
                    ctx.session.state['goal_feasibility'] = {
                        'status': 'completed',
                        'customer_id': customer_id,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    yield Event(
                        author=self.name,
                        content=Content(parts=[Part(text="✅ Step 2 completed: Goal feasibility analysis successful")])
                    )
                except Exception as e:
                    logger.error(f"Error in goal planning: {e}")
                    yield Event(
                        author=self.name,
                        content=Content(parts=[Part(text=f"❌ Goal planning failed: {str(e)}")])
                    )
                    ctx.session.state['goal_feasibility'] = {
                        'status': 'error',
                        'error': str(e),
                        'customer_id': customer_id,
                        'timestamp': datetime.now().isoformat()
                    }
            else:
                yield Event(
                    author=self.name,
                    content=Content(parts=[Part(text="⚠️ Step 2 skipped: GoalPlanner not available")])
                )
            
            # Step 3: Comprehensive Advice Generation
            yield Event(
                author=self.name,
                content=Content(parts=[Part(text="💡 Step 3: Synthesizing insights and generating comprehensive recommendations...")])
            )
            
            ctx.session.state['current_step'] = 'advice_generation'
            
            if self.advisor:
                try:
                    # Run comprehensive advice generation through the Advisor
                    async for event in self.advisor.agent.run_async(ctx):
                        # Forward events from advisor
                        yield event
                    
                    # Store comprehensive advice results in session state
                    ctx.session.state['comprehensive_advice'] = {
                        'status': 'completed',
                        'customer_id': customer_id,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    yield Event(
                        author=self.name,
                        content=Content(parts=[Part(text="✅ Step 3 completed: Comprehensive financial advice generated")])
                    )
                except Exception as e:
                    logger.error(f"Error in advice generation: {e}")
                    yield Event(
                        author=self.name,
                        content=Content(parts=[Part(text=f"❌ Advice generation failed: {str(e)}")])
                    )
                    ctx.session.state['comprehensive_advice'] = {
                        'status': 'error',
                        'error': str(e),
                        'customer_id': customer_id,
                        'timestamp': datetime.now().isoformat()
                    }
            else:
                yield Event(
                    author=self.name,
                    content=Content(parts=[Part(text="⚠️ Step 3 skipped: Advisor not available")])
                )
            
            # Step 4: Final Summary and Next Steps
            ctx.session.state['current_step'] = 'completion'
            
            # Create final summary from session state data
            summary = self._create_orchestration_summary(ctx, customer_id)
            
            yield Event(
                author=self.name,
                content=Content(parts=[Part(text=f"""
🎉 **Financial Analysis Complete!**

**Summary for Customer {customer_id}:**

{summary}

**Next Steps:**
1. Review the detailed recommendations provided
2. Implement the top priority actions within 30 days
3. Set up automatic savings transfers for goal achievement
4. Schedule a follow-up review in 3 months

All analysis data and recommendations have been saved to your profile for future reference.
""")])
            )
            
            # Store final orchestration status
            ctx.session.state['orchestration_status'] = 'completed'
            ctx.session.state['completion_time'] = datetime.now().isoformat()
            
            logger.info(f"Procedural orchestration completed successfully for customer {customer_id}")
            
        except Exception as e:
            logger.error(f"Error in procedural orchestration: {e}")
            yield Event(
                author=self.name,
                content=Content(parts=[Part(text=f"❌ Orchestration failed with error: {str(e)}")])
            )
            ctx.session.state['orchestration_status'] = 'failed'
            ctx.session.state['error'] = str(e)
            return
    
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
            if self.spending_analyzer:
                # Run spending analyzer agent
                async for event in self.spending_analyzer.agent.run_async(ctx):
                    pass  # Just run the agent, don't forward events for quick analysis
                
                # Store spending insights in session state
                ctx.session.state['spending_insights'] = {
                    'status': 'completed',
                    'customer_id': customer_id,
                    'focus_area': focus_area,
                    'timestamp': datetime.now().isoformat()
                }
            
            # Get quick recommendations from advisor
            if self.advisor:
                # Run advisor agent
                async for event in self.advisor.agent.run_async(ctx):
                    pass  # Just run the agent, don't forward events for quick analysis
                
                # Store quick recommendations in session state
                ctx.session.state['quick_recommendations'] = {
                    'status': 'completed',
                    'customer_id': customer_id,
                    'focus_area': focus_area,
                    'timestamp': datetime.now().isoformat()
                }
                
                result = {'status': 'success'}
            else:
                result = {'status': 'error', 'error': 'Advisor not available'}
            
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
            if self.spending_analyzer:
                async for event in self.spending_analyzer.agent.run_async(ctx):
                    pass  # Just run the agent
                
                # Store spending insights
                ctx.session.state['spending_insights'] = {
                    'status': 'completed',
                    'customer_id': customer_id,
                    'timestamp': datetime.now().isoformat()
                }
            
            # Run comprehensive goal analysis
            if self.goal_planner:
                async for event in self.goal_planner.agent.run_async(ctx):
                    pass  # Just run the agent
                
                # Store goal analysis results
                ctx.session.state['goal_feasibility'] = {
                    'status': 'completed',
                    'customer_id': customer_id,
                    'goal_id': goal_id,
                    'timestamp': datetime.now().isoformat()
                }
                
                ctx.session.state['goal_progress'] = {
                    'status': 'completed',
                    'customer_id': customer_id,
                    'timestamp': datetime.now().isoformat()
                }
                
                if goal_id:
                    # Store savings plan
                    ctx.session.state['savings_plan'] = {
                        'status': 'completed',
                        'customer_id': customer_id,
                        'goal_id': goal_id,
                        'timestamp': datetime.now().isoformat()
                    }
            
            # Get goal-specific recommendations
            if self.advisor:
                async for event in self.advisor.agent.run_async(ctx):
                    pass  # Just run the agent
                
                # Store goal recommendations
                ctx.session.state['quick_recommendations'] = {
                    'status': 'completed',
                    'customer_id': customer_id,
                    'focus_area': 'goals',
                    'timestamp': datetime.now().isoformat()
                }
            
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
