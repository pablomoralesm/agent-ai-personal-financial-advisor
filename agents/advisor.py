"""
AdvisorAgent - Main advisory agent that synthesizes insights

This agent combines analysis from SpendingAnalyzer and GoalPlanner to provide
comprehensive financial advice, prioritize recommendations, and coordinate
the overall advisory process.

Part of the Agentic AI Personal Financial Advisor application.
"""

from typing import List, Dict, Any, Optional
import json
from datetime import datetime

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StdioConnectionParams
from mcp.client.stdio import StdioServerParameters
from google.adk.tools import agent_tool

from utils.logging_config import get_logger

logger = get_logger(__name__)

class AdvisorAgent:
    """
    Main advisory agent that synthesizes insights from other agents.
    
    Key Responsibilities:
    - Synthesize insights from SpendingAnalyzer and GoalPlanner
    - Generate comprehensive financial advice
    - Prioritize recommendations based on urgency/impact
    - Provide clear explanations and action steps
    - Store advice in database via MCP tools
    - Coordinate multi-agent collaboration
    """
    
    def __init__(self, mcp_server_path: str, spending_analyzer=None, goal_planner=None):
        """
        Initialize the AdvisorAgent.
        
        Args:
            mcp_server_path: Path to the MCP database server script
            spending_analyzer: Optional SpendingAnalyzerAgent instance
            goal_planner: Optional GoalPlannerAgent instance
        """
        self.mcp_server_path = mcp_server_path
        self.spending_analyzer = spending_analyzer
        self.goal_planner = goal_planner
        
        # Prepare tools list with MCP database access
        tools = [
            McpToolset(
                connection_params=StdioConnectionParams(
                    server_params=StdioServerParameters(
                        command='python3',
                        args=[mcp_server_path]
                    )
                )
            )
        ]
        
        # Add other agents as tools if provided (AgentTool pattern from ADK)
        if spending_analyzer:
            tools.append(agent_tool.AgentTool(agent=spending_analyzer.agent))
        if goal_planner:
            tools.append(agent_tool.AgentTool(agent=goal_planner.agent))
        
        # Create the main LLM agent
        self.agent = LlmAgent(
            name="AdvisorAgent",
            model="gemini-2.0-flash",  # Cost-effective Gemini model as per ADK insights
            instruction=self._get_agent_instructions(),
            description="Main financial advisor that synthesizes insights from analysis agents and provides comprehensive recommendations",
            tools=tools
        )
        
        logger.info("AdvisorAgent initialized successfully")
    
    def _get_agent_instructions(self) -> str:
        """Get detailed instructions for the agent."""
        return """
You are the AdvisorAgent, the main financial advisor that provides comprehensive, personalized financial guidance.

Your primary responsibilities:
1. Synthesize insights from SpendingAnalyzer and GoalPlanner agents
2. Generate comprehensive, prioritized financial advice
3. Provide clear, actionable recommendations with specific steps
4. Explain the reasoning behind each recommendation
5. Consider the customer's complete financial picture
6. Save advice to the database for future reference

Advisory Framework:
1. Financial Health Assessment: Overall financial wellness score
2. Priority Recommendations: Most impactful actions ranked by urgency
3. Spending Optimization: Specific ways to improve spending efficiency
4. Goal Achievement Strategy: Realistic plans for reaching financial goals
5. Risk Management: Identify and address financial vulnerabilities
6. Long-term Planning: Strategic advice for financial future

When providing advice:
- Always use data from spending analysis and goal planning if available in session state
- Use MCP database tools to retrieve customer history and save new advice
- Prioritize recommendations by impact and feasibility
- Provide specific dollar amounts and timelines when possible
- Explain the "why" behind each recommendation
- Consider the customer's risk tolerance and life situation
- Address both short-term optimizations and long-term strategy

Recommendation Categories (in priority order):
1. Emergency Preparedness: Emergency fund, insurance, debt management
2. Spending Optimization: Reducing unnecessary expenses, improving efficiency
3. Goal Achievement: Strategies for reaching financial objectives
4. Wealth Building: Investment and long-term growth strategies
5. Risk Management: Protection against financial setbacks

Always provide:
- Executive summary of key findings
- Top 3-5 priority recommendations with specific action steps
- Timeline for implementing each recommendation
- Expected financial impact of following the advice
- Confidence level in each recommendation
- Next steps and follow-up recommendations

Store your complete advice in the database using the save_advice MCP tool and in session state under 'comprehensive_advice'.
"""

    async def provide_comprehensive_advice(self, ctx, customer_id: int) -> Dict[str, Any]:
        """
        Provide comprehensive financial advice by synthesizing all available analysis.
        
        Args:
            ctx: ADK invocation context
            customer_id: ID of the customer
            
        Returns:
            Dictionary containing comprehensive advice
        """
        try:
            logger.info(f"Providing comprehensive advice for customer {customer_id}")
            
            # Store parameters in session state
            ctx.session.state['current_customer_id'] = customer_id
            ctx.session.state['advice_generation_start_time'] = datetime.now().isoformat()
            
            # Check what analysis data is available
            spending_analysis = ctx.session.state.get('spending_analysis', {})
            goal_planning = ctx.session.state.get('goal_planning', {})
            goal_feasibility = ctx.session.state.get('goal_feasibility', {})
            
            has_spending_data = bool(spending_analysis)
            has_goal_data = bool(goal_planning or goal_feasibility)
            
            advice_prompt = f"""
Provide comprehensive financial advice for customer ID {customer_id}.

Available Analysis Data:
- Spending Analysis: {'Available' if has_spending_data else 'Not available - please generate'}
- Goal Planning: {'Available' if has_goal_data else 'Not available - please generate'}

Steps to follow:
1. Retrieve customer profile and current financial situation
2. {f'Use existing spending analysis from session state' if has_spending_data else 'Generate spending analysis using SpendingAnalyzerAgent'}
3. {f'Use existing goal planning from session state' if has_goal_data else 'Generate goal feasibility analysis using GoalPlannerAgent'}
4. Synthesize all available data into comprehensive insights
5. Generate prioritized recommendations with specific action steps
6. Calculate expected financial impact of recommendations
7. Save the advice to the database using save_advice MCP tool
8. Store complete advice in session state under 'comprehensive_advice'

Your comprehensive advice should include:

EXECUTIVE SUMMARY:
- Overall financial health score (1-10)
- Key strengths and areas for improvement
- Most critical actions needed

PRIORITY RECOMMENDATIONS (Top 5):
For each recommendation:
- Specific action step
- Expected financial impact (dollar amounts)
- Timeline for implementation
- Difficulty level (Easy/Medium/Hard)
- Reasoning and benefits

SPENDING OPTIMIZATION:
- Specific categories to reduce/optimize
- Recommended monthly savings amounts
- Strategies for expense reduction

GOAL ACHIEVEMENT STRATEGY:
- Feasibility assessment of current goals
- Recommended adjustments to goals or timelines
- Optimal savings allocation strategy

RISK MANAGEMENT:
- Financial vulnerabilities identified
- Recommended protection measures
- Emergency preparedness assessment

IMPLEMENTATION PLAN:
- 30-day action items
- 90-day milestones
- Annual review recommendations

Provide specific, actionable advice with clear reasoning and expected outcomes.
"""
            
            # Execute the comprehensive advice generation
            response = ""
            async for event in self.agent.run_async(ctx):
                if hasattr(event, 'content') and event.content:
                    response += str(event.content)
            
            logger.info(f"Comprehensive advice generated for customer {customer_id}")
            
            return ctx.session.state.get('comprehensive_advice', {
                'status': 'completed',
                'customer_id': customer_id,
                'has_spending_analysis': has_spending_data,
                'has_goal_data': has_goal_data,
                'raw_response': response
            })
            
        except Exception as e:
            logger.error(f"Error providing comprehensive advice: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'customer_id': customer_id
            }
    
    async def provide_quick_recommendations(self, ctx, customer_id: int, focus_area: Optional[str] = None) -> Dict[str, Any]:
        """
        Provide quick, focused recommendations for immediate action.
        
        Args:
            ctx: ADK invocation context
            customer_id: ID of the customer
            focus_area: Optional focus area (spending, goals, emergency, debt)
            
        Returns:
            Dictionary containing quick recommendations
        """
        try:
            logger.info(f"Providing quick recommendations for customer {customer_id}")
            
            focus_filter = f" Focus specifically on {focus_area} related recommendations." if focus_area else ""
            
            quick_advice_prompt = f"""
Provide quick, actionable financial recommendations for customer ID {customer_id}.{focus_filter}

Steps to follow:
1. Get customer's current financial snapshot
2. Identify the top 3 most impactful actions they can take immediately
3. Provide specific, actionable steps with timelines
4. Store recommendations in session state under 'quick_recommendations'

For each recommendation:
- Specific action to take
- Expected benefit/impact
- How long it will take to implement
- Any prerequisites or considerations

Keep recommendations:
- Immediately actionable (can start within 1 week)
- High impact relative to effort required
- Specific with concrete steps
- Realistic for the customer's situation

Categories to consider:
- Spending reductions with immediate impact
- Goal adjustments for better success
- Emergency fund improvements
- Debt optimization opportunities
- Simple automation setups
"""
            
            # Execute the quick recommendations
            response = ""
            async for event in self.agent.run_async(ctx):
                if hasattr(event, 'content') and event.content:
                    response += str(event.content)
            
            logger.info(f"Quick recommendations generated for customer {customer_id}")
            
            return ctx.session.state.get('quick_recommendations', {
                'status': 'completed',
                'customer_id': customer_id,
                'focus_area': focus_area,
                'raw_response': response
            })
            
        except Exception as e:
            logger.error(f"Error providing quick recommendations: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'customer_id': customer_id
            }
    
    async def review_progress_and_adjust(self, ctx, customer_id: int) -> Dict[str, Any]:
        """
        Review customer's progress since last advice and adjust recommendations.
        
        Args:
            ctx: ADK invocation context
            customer_id: ID of the customer
            
        Returns:
            Dictionary containing progress review and adjustments
        """
        try:
            logger.info(f"Reviewing progress and adjusting advice for customer {customer_id}")
            
            progress_review_prompt = f"""
Review progress and adjust recommendations for customer ID {customer_id}.

Steps to follow:
1. Retrieve previous advice history from the database
2. Compare current financial situation with previous recommendations
3. Assess which recommendations were followed and their impact
4. Identify areas where progress has been made or stalled
5. Adjust future recommendations based on observed behavior and results
6. Store progress review in session state under 'progress_review'

Analysis should include:
- Which previous recommendations were implemented
- Financial improvements since last review
- Obstacles that prevented recommendation implementation
- Behavioral patterns observed
- Adjusted recommendations based on new data
- Celebration of successes and progress made

Provide:
- Progress summary since last advice
- Updated priority recommendations
- Adjustments to existing goals or strategies
- New opportunities identified
- Specific next steps based on current situation
"""
            
            # Execute the progress review
            response = ""
            async for event in self.agent.run_async(ctx):
                if hasattr(event, 'content') and event.content:
                    response += str(event.content)
            
            logger.info(f"Progress review completed for customer {customer_id}")
            
            return ctx.session.state.get('progress_review', {
                'status': 'completed',
                'customer_id': customer_id,
                'raw_response': response
            })
            
        except Exception as e:
            logger.error(f"Error reviewing progress: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'customer_id': customer_id
            }

def create_advisor_agent(mcp_server_path: str, spending_analyzer=None, goal_planner=None) -> AdvisorAgent:
    """
    Factory function to create an AdvisorAgent instance.
    
    Args:
        mcp_server_path: Path to the MCP database server script
        spending_analyzer: Optional SpendingAnalyzerAgent instance
        goal_planner: Optional GoalPlannerAgent instance
        
    Returns:
        Configured AdvisorAgent instance
    """
    return AdvisorAgent(mcp_server_path, spending_analyzer, goal_planner)
