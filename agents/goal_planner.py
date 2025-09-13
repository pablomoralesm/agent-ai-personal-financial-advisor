"""
GoalPlannerAgent - Helps customers set and plan financial goals

This agent uses spending analysis data and MCP database tools to evaluate
goal feasibility, create realistic savings plans, and track progress toward
financial objectives.

Part of the Agentic AI Personal Financial Advisor application.
"""

from typing import List, Dict, Any, Optional
import json
from datetime import datetime, timedelta, date

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StdioConnectionParams
from mcp.client.stdio import StdioServerParameters

from utils.logging_config import get_logger

logger = get_logger(__name__)

class GoalPlannerAgent:
    """
    Agent specialized in financial goal planning and feasibility analysis.
    
    Key Responsibilities:
    - Assess financial goal feasibility based on spending analysis
    - Create realistic savings/investment plans
    - Track progress toward goals
    - Suggest goal prioritization and adjustments
    - Coordinate with SpendingAnalyzer for realistic planning
    """
    
    def __init__(self, mcp_server_path: str):
        """
        Initialize the GoalPlannerAgent.
        
        Args:
            mcp_server_path: Path to the MCP database server script
        """
        self.mcp_server_path = mcp_server_path
        
        # Create the LLM agent with MCP database tools
        self.agent = LlmAgent(
            name="GoalPlannerAgent",
            model="gemini-2.0-flash",  # Cost-effective Gemini model as per ADK insights
            instruction=self._get_agent_instructions(),
            description="Evaluates financial goal feasibility, creates savings plans, tracks progress, and provides goal planning recommendations",
            tools=[
                McpToolset(
                    connection_params=StdioConnectionParams(
                        server_params=StdioServerParameters(
                            command='python3',
                            args=[mcp_server_path]
                        )
                    )
                )
            ]
        )
        
        logger.info("GoalPlannerAgent initialized successfully")
    
    def _get_agent_instructions(self) -> str:
        """Get detailed instructions for the agent."""
        return """
You are a GoalPlannerAgent, an expert financial planner specializing in goal setting and achievement planning.

Your primary responsibilities:
1. Evaluate the feasibility of customer financial goals based on their spending patterns
2. Create realistic, time-bound savings and investment plans
3. Prioritize multiple goals based on urgency, importance, and feasibility
4. Track progress toward existing goals and suggest adjustments
5. Recommend optimal savings strategies and timelines
6. Store goal planning results in session state for other agents to use

When planning goals:
- Always use spending analysis data from session state if available
- Use MCP database tools to retrieve existing goals and customer financial data
- Consider the customer's available savings capacity after essential expenses
- Factor in goal priority levels (emergency fund first, then other goals)
- Provide realistic timelines based on actual saving capacity
- Consider different savings strategies (fixed amount vs percentage-based)
- Account for potential income changes or life events

Goal Planning Framework:
1. Emergency Fund: 3-6 months of expenses (highest priority)
2. High-Interest Debt Payoff: Credit cards, personal loans (high priority)
3. Short-term Goals: Vacation, purchases (1-2 years)
4. Medium-term Goals: Home down payment, car (2-5 years)
5. Long-term Goals: Retirement, children's education (5+ years)

Always provide:
- Realistic monthly savings amounts needed for each goal
- Adjusted timelines if original targets are unrealistic
- Priority ranking with clear reasoning
- Specific action steps and milestones
- Alternative strategies if goals seem unachievable

Store your analysis results in ctx.session.state under the key 'goal_planning' so other agents can access them.
"""

    async def evaluate_goal_feasibility(self, ctx, customer_id: int, goal_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Evaluate the feasibility of customer's financial goals.
        
        Args:
            ctx: ADK invocation context
            customer_id: ID of the customer
            goal_id: Optional specific goal ID to evaluate (if None, evaluates all goals)
            
        Returns:
            Dictionary containing goal feasibility analysis
        """
        try:
            logger.info(f"Evaluating goal feasibility for customer {customer_id}")
            
            # Store parameters in session state
            ctx.session.state['current_customer_id'] = customer_id
            ctx.session.state['goal_evaluation_start_time'] = datetime.now().isoformat()
            
            # Check if spending analysis is available in session state
            spending_analysis = ctx.session.state.get('spending_analysis', {})
            has_spending_data = bool(spending_analysis)
            
            if goal_id:
                feasibility_prompt = f"""
Evaluate the feasibility of goal ID {goal_id} for customer ID {customer_id}.

Steps to follow:
1. Retrieve the specific goal details from the database
2. Get the customer's financial profile and current spending patterns
3. {'Use the existing spending analysis data from session state' if has_spending_data else 'Analyze their spending to determine available savings capacity'}
4. Calculate realistic timeline and monthly savings needed
5. Assess feasibility based on their financial capacity
6. Provide specific recommendations for achieving this goal
7. Store the evaluation in session state under 'goal_feasibility'

Analysis should include:
- Current progress toward the goal
- Monthly savings needed to meet target date
- Feasibility rating (High/Medium/Low/Unrealistic)
- Recommended adjustments if needed
- Impact on other financial goals
"""
            else:
                feasibility_prompt = f"""
Evaluate the feasibility of ALL financial goals for customer ID {customer_id}.

Steps to follow:
1. Retrieve all active goals for the customer
2. Get their complete financial profile and spending patterns
3. {'Use the existing spending analysis data from session state' if has_spending_data else 'Analyze their spending to determine total available savings capacity'}
4. Evaluate each goal individually for feasibility
5. Prioritize goals based on importance and achievability
6. Calculate optimal savings allocation across all goals
7. Store the complete evaluation in session state under 'goal_feasibility'

For each goal, provide:
- Feasibility assessment (High/Medium/Low/Unrealistic)
- Recommended monthly savings amount
- Adjusted timeline if original is unrealistic
- Priority ranking with reasoning
- Potential conflicts with other goals

Overall recommendations:
- Total monthly savings needed across all goals
- Suggested priority order for goal achievement
- Strategies for maximizing goal achievement success
"""
            
            # Execute the feasibility analysis
            response = ""
            async for event in self.agent.run_async(ctx):
                if hasattr(event, 'content') and event.content:
                    response += str(event.content)
            
            logger.info(f"Goal feasibility evaluation completed for customer {customer_id}")
            
            return ctx.session.state.get('goal_feasibility', {
                'status': 'completed',
                'customer_id': customer_id,
                'goal_id': goal_id,
                'has_spending_analysis': has_spending_data,
                'raw_response': response
            })
            
        except Exception as e:
            logger.error(f"Error in goal feasibility evaluation: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'customer_id': customer_id,
                'goal_id': goal_id
            }
    
    async def create_savings_plan(self, ctx, customer_id: int, goal_id: int, target_monthly_amount: Optional[float] = None) -> Dict[str, Any]:
        """
        Create a detailed savings plan for a specific goal.
        
        Args:
            ctx: ADK invocation context
            customer_id: ID of the customer
            goal_id: ID of the goal to create a plan for
            target_monthly_amount: Optional target monthly savings amount
            
        Returns:
            Dictionary containing savings plan details
        """
        try:
            logger.info(f"Creating savings plan for goal {goal_id}, customer {customer_id}")
            
            savings_plan_prompt = f"""
Create a detailed savings plan for goal ID {goal_id} for customer ID {customer_id}.

Steps to follow:
1. Retrieve the specific goal details (target amount, current amount, target date)
2. Get customer's financial capacity from spending analysis or database
3. Calculate the monthly savings needed to reach the goal by target date
4. {f'Consider the suggested target monthly amount of ${target_monthly_amount}' if target_monthly_amount else 'Determine optimal monthly savings amount based on their capacity'}
5. Create a month-by-month savings plan with milestones
6. Suggest specific savings strategies and account types
7. Store the complete plan in session state under 'savings_plan'

The savings plan should include:
- Monthly savings amount recommendation
- Timeline with quarterly milestones
- Specific savings strategies (automatic transfers, separate accounts, etc.)
- Contingency planning for missed months
- Integration with other financial goals
- Recommended account types (high-yield savings, CDs, etc.)
- Progress tracking methods

Also consider:
- Seasonal variations in income/expenses
- Potential for increased savings over time (raises, bonuses)
- Emergency fund requirements
- Tax implications if applicable
"""
            
            # Execute the savings plan creation
            response = ""
            async for event in self.agent.run_async(ctx):
                if hasattr(event, 'content') and event.content:
                    response += str(event.content)
            
            logger.info(f"Savings plan created for goal {goal_id}")
            
            return ctx.session.state.get('savings_plan', {
                'status': 'completed',
                'customer_id': customer_id,
                'goal_id': goal_id,
                'target_monthly_amount': target_monthly_amount,
                'raw_response': response
            })
            
        except Exception as e:
            logger.error(f"Error creating savings plan: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'customer_id': customer_id,
                'goal_id': goal_id
            }
    
    async def track_goal_progress(self, ctx, customer_id: int) -> Dict[str, Any]:
        """
        Track progress toward all customer goals and provide updates.
        
        Args:
            ctx: ADK invocation context
            customer_id: ID of the customer
            
        Returns:
            Dictionary containing goal progress tracking
        """
        try:
            logger.info(f"Tracking goal progress for customer {customer_id}")
            
            progress_prompt = f"""
Track and analyze goal progress for customer ID {customer_id}.

Steps to follow:
1. Retrieve all financial goals for the customer
2. Analyze current progress vs target for each goal
3. Calculate progress rate and projected completion dates
4. Identify goals that are on track, ahead, or behind schedule
5. Analyze recent savings patterns to assess consistency
6. Provide specific recommendations for goals that are behind
7. Store progress analysis in session state under 'goal_progress'

For each goal, analyze:
- Current amount vs target amount (percentage complete)
- Time remaining vs savings needed (on track analysis)
- Recent contribution patterns (consistent vs sporadic)
- Projected completion date based on current rate
- Recommendations for improvement if behind schedule

Overall assessment:
- Which goals are performing well
- Which goals need attention or strategy changes
- Overall savings discipline and consistency
- Suggestions for improving goal achievement rates
"""
            
            # Execute the progress tracking
            response = ""
            async for event in self.agent.run_async(ctx):
                if hasattr(event, 'content') and event.content:
                    response += str(event.content)
            
            logger.info(f"Goal progress tracking completed for customer {customer_id}")
            
            return ctx.session.state.get('goal_progress', {
                'status': 'completed',
                'customer_id': customer_id,
                'raw_response': response
            })
            
        except Exception as e:
            logger.error(f"Error tracking goal progress: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'customer_id': customer_id
            }
    
    async def recommend_goal_adjustments(self, ctx, customer_id: int) -> Dict[str, Any]:
        """
        Recommend adjustments to goals based on current financial situation.
        
        Args:
            ctx: ADK invocation context
            customer_id: ID of the customer
            
        Returns:
            Dictionary containing goal adjustment recommendations
        """
        try:
            logger.info(f"Recommending goal adjustments for customer {customer_id}")
            
            adjustment_prompt = f"""
Analyze customer ID {customer_id}'s financial goals and recommend adjustments.

Steps to follow:
1. Review all current goals and their feasibility
2. Assess recent changes in income/spending patterns
3. Identify goals that may need timeline or amount adjustments
4. Consider life changes that might affect goal priorities
5. Recommend specific adjustments (amounts, dates, priorities)
6. Suggest new goals if appropriate
7. Store recommendations in session state under 'goal_adjustments'

Types of adjustments to consider:
- Extending or shortening target dates
- Adjusting target amounts (up or down)
- Changing priority levels
- Splitting large goals into smaller milestones
- Pausing goals temporarily if needed
- Adding new goals based on improved financial capacity

For each recommended adjustment:
- Clear reasoning for why the change is needed
- Specific new targets or timelines
- Impact on other goals
- Steps to implement the adjustment
- Expected benefits of the change
"""
            
            # Execute the adjustment recommendations
            response = ""
            async for event in self.agent.run_async(ctx):
                if hasattr(event, 'content') and event.content:
                    response += str(event.content)
            
            logger.info(f"Goal adjustment recommendations completed for customer {customer_id}")
            
            return ctx.session.state.get('goal_adjustments', {
                'status': 'completed',
                'customer_id': customer_id,
                'raw_response': response
            })
            
        except Exception as e:
            logger.error(f"Error recommending goal adjustments: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'customer_id': customer_id
            }

def create_goal_planner_agent(mcp_server_path: str) -> GoalPlannerAgent:
    """
    Factory function to create a GoalPlannerAgent instance.
    
    Args:
        mcp_server_path: Path to the MCP database server script
        
    Returns:
        Configured GoalPlannerAgent instance
    """
    return GoalPlannerAgent(mcp_server_path)
