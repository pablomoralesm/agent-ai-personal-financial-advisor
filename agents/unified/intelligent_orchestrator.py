"""
Intelligent Orchestrator for Production Multi-Agent System

This orchestrator uses LLM-powered decision making to dynamically select
and coordinate agents based on user requests. It demonstrates production
patterns for intelligent agent orchestration.

Part of the Agentic AI Personal Financial Advisor application.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime

from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool

from .base_agent import UnifiedAgentBase
from .deployment_configs import DeploymentConfig
from utils.logging_config import get_logger

logger = get_logger(__name__)

class IntelligentOrchestrator(UnifiedAgentBase):
    """
    Intelligent orchestrator with LLM-powered decision making.
    
    This orchestrator uses AI to dynamically decide which agents to call
    and in what order based on user requests. It demonstrates:
    - Dynamic agent selection
    - Intelligent workflow orchestration
    - Production-ready patterns
    - Adaptive behavior
    """
    
    def __init__(self, mcp_server_path: str, deployment_context: str = "adk_web"):
        """
        Initialize the intelligent orchestrator.
        
        Args:
            mcp_server_path: Path to the MCP database server script
            deployment_context: Context (streamlit, adk_web)
        """
        # Create the LLM agent with agent delegation tools
        super().__init__(
            name="IntelligentOrchestrator",
            mcp_server_path=mcp_server_path,
            deployment_context=deployment_context
        )
        
        # Store sub-agents for delegation using object.__setattr__
        object.__setattr__(self, '_sub_agents', {})
        
        logger.info("IntelligentOrchestrator initialized for production use")
    
    def _get_agent_config(self) -> Dict[str, Any]:
        """
        Get agent configuration for the intelligent orchestrator.
        
        Returns:
            Dictionary containing agent configuration
        """
        return {
            'name': 'IntelligentOrchestrator',
            'model': 'gemini-2.0-flash-exp',  # Use more capable model for orchestration
            'instruction': self._get_orchestrator_instruction(),
            'description': 'Intelligent orchestrator that dynamically coordinates financial advisor agents based on user requests',
            'additional_tools': []  # Will be populated with agent tools
        }
    
    def _get_orchestrator_instruction(self) -> str:
        """
        Get the orchestrator instruction text.
        
        Returns:
            Instruction text for the orchestrator
        """
        return """
You are an IntelligentOrchestrator, an AI-powered coordinator for financial advisor agents.

Your primary responsibilities:
1. Analyze user requests to understand what financial analysis is needed
2. Dynamically select which agents to call based on the request
3. Coordinate agent execution in the optimal order
4. Synthesize results from multiple agents
5. Provide comprehensive financial guidance

Available Agents:
- SpendingAnalyzerAgent: Analyzes spending patterns, categorizes expenses, identifies trends
- GoalPlannerAgent: Evaluates goal feasibility, creates savings plans, tracks progress
- AdvisorAgent: Provides comprehensive financial advice and recommendations

Decision Framework:
1. **Spending Analysis Requests**: Use SpendingAnalyzerAgent
2. **Goal Planning Requests**: Use GoalPlannerAgent + SpendingAnalyzerAgent (for capacity analysis)
3. **General Financial Advice**: Use AdvisorAgent + other agents as needed
4. **Comprehensive Analysis**: Use all agents in logical sequence

Workflow Patterns:
- **Quick Insights**: Single agent focused on immediate needs
- **Goal-Focused**: GoalPlanner + SpendingAnalyzer for capacity
- **Comprehensive**: All agents with proper sequencing
- **Custom**: Based on specific user requirements

Always:
- Provide reasoning for your agent selection
- Coordinate agents to avoid redundant work
- Synthesize results into actionable recommendations
- Consider the user's specific financial situation
- Store analysis results in session state for future reference

When orchestrating:
- Start with data gathering (spending analysis if needed)
- Move to planning (goal analysis if relevant)
- End with advice synthesis (advisor recommendations)
- Provide clear progress updates throughout
- Handle errors gracefully and suggest alternatives
"""
    
    def set_sub_agents(self, spending_analyzer, goal_planner, advisor):
        """
        Set the sub-agents for orchestration.
        
        Args:
            spending_analyzer: SpendingAnalyzer agent instance
            goal_planner: GoalPlanner agent instance
            advisor: Advisor agent instance
        """
        object.__setattr__(self, '_sub_agents', {
            'spending_analyzer': spending_analyzer,
            'goal_planner': goal_planner,
            'advisor': advisor
        })
        
        # Add agent tools to the orchestrator
        agent_tools = []
        if spending_analyzer:
            agent_tools.append(agent_tool.AgentTool(agent=spending_analyzer.agent))
        if goal_planner:
            agent_tools.append(agent_tool.AgentTool(agent=goal_planner.agent))
        if advisor:
            agent_tools.append(agent_tool.AgentTool(agent=advisor.agent))
        
        # Update the agent with new tools
        self.agent.tools.extend(agent_tools)
        
        logger.info("Sub-agents set for intelligent orchestrator")
    
    @property
    def sub_agents(self):
        """Get sub-agents dictionary."""
        return self._sub_agents
    
    async def run_analysis(self, ctx, customer_id: int, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Run analysis using intelligent orchestration.
        
        Args:
            ctx: ADK invocation context
            customer_id: ID of the customer
            analysis_type: Type of analysis to perform
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            logger.info(f"Starting intelligent analysis for customer {customer_id}, type: {analysis_type}")
            
            # Set context in session state
            ctx.session.state['customer_id'] = customer_id
            ctx.session.state['analysis_type'] = analysis_type
            ctx.session.state['orchestrator_type'] = 'intelligent'
            ctx.session.state['orchestration_start_time'] = datetime.now().isoformat()
            
            # Create analysis prompt based on type
            analysis_prompt = self._create_analysis_prompt(customer_id, analysis_type)
            
            # Execute the intelligent orchestration
            results = []
            async for event in self.agent.run_async(ctx):
                if hasattr(event, 'content') and event.content:
                    results.append({
                        'type': getattr(event, 'event_type', 'content'),
                        'content': str(event.content),
                        'timestamp': datetime.now().isoformat()
                    })
            
            # Get final results from session state
            final_status = ctx.session.state.get('orchestration_status', 'completed')
            
            return {
                'status': 'success',
                'customer_id': customer_id,
                'analysis_type': analysis_type,
                'orchestrator_type': 'intelligent',
                'results': results,
                'final_status': final_status,
                'session_id': str(ctx.session.id) if hasattr(ctx.session, 'id') else 'unknown'
            }
            
        except Exception as e:
            logger.error(f"Error in intelligent analysis: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'customer_id': customer_id,
                'analysis_type': analysis_type
            }
    
    def _create_analysis_prompt(self, customer_id: int, analysis_type: str) -> str:
        """
        Create analysis prompt based on type.
        
        Args:
            customer_id: ID of the customer
            analysis_type: Type of analysis
            
        Returns:
            Analysis prompt string
        """
        base_prompt = f"Please perform {analysis_type} financial analysis for customer {customer_id}."
        
        if analysis_type == "comprehensive":
            return f"""
{base_prompt}

This should include:
1. Spending pattern analysis to understand current financial behavior
2. Goal feasibility assessment based on spending capacity
3. Comprehensive financial advice synthesizing all insights

Use the appropriate agents to gather data and provide recommendations.
"""
        elif analysis_type == "spending":
            return f"""
{base_prompt}

Focus on:
1. Analyzing spending patterns and habits
2. Identifying optimization opportunities
3. Providing specific recommendations for spending improvement

Use the SpendingAnalyzerAgent for detailed analysis.
"""
        elif analysis_type == "goals":
            return f"""
{base_prompt}

Focus on:
1. Evaluating current financial goals
2. Assessing goal feasibility based on spending capacity
3. Creating realistic savings plans
4. Providing goal-specific recommendations

Use both SpendingAnalyzerAgent (for capacity) and GoalPlannerAgent (for planning).
"""
        elif analysis_type == "quick":
            return f"""
{base_prompt}

Provide quick, actionable insights including:
1. Immediate spending optimization opportunities
2. Quick goal adjustments if needed
3. Top 3 priority actions

Use the most appropriate agent(s) for efficient analysis.
"""
        else:
            return f"""
{base_prompt}

Analyze the customer's financial situation and provide appropriate recommendations.
Use the available agents to gather necessary data and insights.
"""
    
    async def run_quick_analysis(self, ctx, customer_id: int, focus_area: Optional[str] = None) -> Dict[str, Any]:
        """
        Run quick analysis using intelligent orchestration.
        
        Args:
            ctx: ADK invocation context
            customer_id: ID of the customer
            focus_area: Optional focus area
            
        Returns:
            Dictionary containing quick analysis results
        """
        analysis_type = f"quick_{focus_area}" if focus_area else "quick"
        return await self.run_analysis(ctx, customer_id, analysis_type)
    
    async def run_goal_analysis(self, ctx, customer_id: int, goal_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Run goal-focused analysis using intelligent orchestration.
        
        Args:
            ctx: ADK invocation context
            customer_id: ID of the customer
            goal_id: Optional specific goal ID
            
        Returns:
            Dictionary containing goal analysis results
        """
        analysis_type = f"goals_{goal_id}" if goal_id else "goals"
        return await self.run_analysis(ctx, customer_id, analysis_type)
    
    def get_agent_selection_reasoning(self, analysis_type: str) -> str:
        """
        Get reasoning for agent selection based on analysis type.
        
        Args:
            analysis_type: Type of analysis
            
        Returns:
            Reasoning string
        """
        reasoning_map = {
            "comprehensive": "Using all agents for complete financial picture: SpendingAnalyzer → GoalPlanner → Advisor",
            "spending": "Using SpendingAnalyzerAgent for detailed spending pattern analysis",
            "goals": "Using SpendingAnalyzerAgent for capacity analysis + GoalPlannerAgent for goal planning",
            "quick": "Using most appropriate agent(s) for efficient quick insights",
            "advice": "Using AdvisorAgent with data from other agents as needed"
        }
        
        return reasoning_map.get(analysis_type, "Using intelligent agent selection based on request analysis")
