"""
SpendingAnalyzerAgent - Analyzes customer spending habits and patterns

This agent uses the MCP database server to analyze customer transactions,
categorize spending patterns, identify trends, and provide insights for
financial decision making.

Part of the Agentic AI Personal Financial Advisor application.
"""

from typing import List, Dict, Any, Optional
import json
from datetime import datetime, timedelta

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

from utils.logging_config import get_logger

logger = get_logger(__name__)

class SpendingAnalyzerAgent:
    """
    Agent specialized in analyzing customer spending patterns and habits.
    
    Key Responsibilities:
    - Analyze transaction data using MCP database tools
    - Categorize spending patterns (fixed vs variable costs)
    - Identify spending trends and anomalies
    - Generate spending behavior insights
    - Provide data for other agents via session state
    """
    
    def __init__(self, mcp_server_path: str):
        """
        Initialize the SpendingAnalyzerAgent.
        
        Args:
            mcp_server_path: Path to the MCP database server script
        """
        self.mcp_server_path = mcp_server_path
        
        # Create the LLM agent with MCP database tools
        self.agent = LlmAgent(
            name="SpendingAnalyzerAgent",
            model="gemini-2.0-flash",  # Cost-effective Gemini model as per ADK insights
            instruction=self._get_agent_instructions(),
            description="Analyzes customer spending habits, categorizes expenses, identifies trends, and provides insights for financial planning",
            tools=[
                MCPToolset(
                    connection_params=StdioServerParameters(
                        command='python3',
                        args=[mcp_server_path]
                    )
                )
            ]
        )
        
        logger.info("SpendingAnalyzerAgent initialized successfully")
    
    def _get_agent_instructions(self) -> str:
        """Get detailed instructions for the agent."""
        return """
You are a SpendingAnalyzerAgent, an expert financial analyst specializing in spending pattern analysis.

Your primary responsibilities:
1. Analyze customer transaction data to understand spending habits
2. Categorize expenses into fixed costs (rent, insurance) vs variable costs (dining, entertainment)
3. Identify spending trends, seasonal patterns, and anomalies
4. Calculate key financial ratios (housing ratio, savings rate, etc.)
5. Provide actionable insights and recommendations for spending optimization
6. Store analysis results in session state for other agents to use

When analyzing spending:
- Use the MCP database tools to retrieve customer transactions and spending summaries
- Focus on the last 6 months of data for trend analysis
- Calculate important ratios like housing costs as % of income
- Identify categories where spending is above or below recommended ranges
- Look for unusual spending patterns that might indicate financial stress or opportunities
- Consider seasonal variations in spending patterns

Always provide:
- Clear, data-driven insights
- Specific recommendations with dollar amounts when possible
- Context about whether spending patterns are healthy or concerning
- Actionable steps the customer can take to improve their financial situation

Store your analysis results in ctx.session.state under the key 'spending_analysis' so other agents can access them.
"""

    async def analyze_customer_spending(self, ctx, customer_id: int, analysis_months: int = 6) -> Dict[str, Any]:
        """
        Perform comprehensive spending analysis for a customer.
        
        Args:
            ctx: ADK invocation context
            customer_id: ID of the customer to analyze
            analysis_months: Number of months to analyze (default 6)
            
        Returns:
            Dictionary containing spending analysis results
        """
        try:
            logger.info(f"Starting spending analysis for customer {customer_id}")
            
            # Store analysis parameters in session state
            ctx.session.state['current_customer_id'] = customer_id
            ctx.session.state['analysis_months'] = analysis_months
            ctx.session.state['analysis_start_time'] = datetime.now().isoformat()
            
            # Run the agent to perform analysis
            analysis_prompt = f"""
Please analyze the spending patterns for customer ID {customer_id} over the last {analysis_months} months.

Steps to follow:
1. First, get the customer profile to understand their background
2. Retrieve their spending summary for the specified period
3. Get detailed transactions to understand spending patterns
4. Calculate key financial ratios and metrics
5. Identify trends, patterns, and anomalies
6. Provide specific recommendations for improvement
7. Store the complete analysis in session state under 'spending_analysis'

Focus on:
- Monthly income vs expenses trends
- Category-wise spending analysis
- Fixed vs variable cost breakdown
- Spending efficiency in each category
- Opportunities for optimization
- Red flags or concerning patterns

Provide a comprehensive analysis with specific insights and actionable recommendations.
"""
            
            # Execute the analysis using the LLM agent
            response = ""
            async for event in self.agent.run_async(ctx):
                if hasattr(event, 'content') and event.content:
                    response += str(event.content)
            
            logger.info(f"Spending analysis completed for customer {customer_id}")
            
            # Return the analysis results from session state
            return ctx.session.state.get('spending_analysis', {
                'status': 'completed',
                'customer_id': customer_id,
                'analysis_months': analysis_months,
                'raw_response': response
            })
            
        except Exception as e:
            logger.error(f"Error in spending analysis: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'customer_id': customer_id
            }
    
    async def get_spending_insights(self, ctx, customer_id: int) -> Dict[str, Any]:
        """
        Get quick spending insights for a customer.
        
        Args:
            ctx: ADK invocation context
            customer_id: ID of the customer
            
        Returns:
            Dictionary containing spending insights
        """
        try:
            logger.info(f"Getting spending insights for customer {customer_id}")
            
            insights_prompt = f"""
Provide quick spending insights for customer ID {customer_id}:

1. Get their recent spending summary (last 3 months)
2. Identify the top 3 spending categories
3. Calculate their monthly savings rate
4. Highlight any immediate concerns or opportunities
5. Give 2-3 quick actionable recommendations

Keep the analysis concise but insightful. Store results in session state under 'spending_insights'.
"""
            
            # Execute the insights analysis
            response = ""
            async for event in self.agent.run_async(ctx):
                if hasattr(event, 'content') and event.content:
                    response += str(event.content)
            
            return ctx.session.state.get('spending_insights', {
                'status': 'completed',
                'customer_id': customer_id,
                'raw_response': response
            })
            
        except Exception as e:
            logger.error(f"Error getting spending insights: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'customer_id': customer_id
            }
    
    async def compare_spending_periods(self, ctx, customer_id: int, period1_months: int = 3, period2_months: int = 3) -> Dict[str, Any]:
        """
        Compare spending between two time periods.
        
        Args:
            ctx: ADK invocation context
            customer_id: ID of the customer
            period1_months: Months for first period (most recent)
            period2_months: Months for second period (older)
            
        Returns:
            Dictionary containing spending comparison
        """
        try:
            logger.info(f"Comparing spending periods for customer {customer_id}")
            
            comparison_prompt = f"""
Compare spending patterns for customer ID {customer_id} between two periods:
- Recent period: Last {period1_months} months
- Previous period: {period1_months + 1} to {period1_months + period2_months} months ago

Analysis steps:
1. Get spending summaries for both periods
2. Compare total spending and income between periods
3. Identify categories with significant changes (>10% difference)
4. Analyze whether changes are positive or concerning
5. Provide insights about spending trends and direction
6. Store comparison results in session state under 'spending_comparison'

Focus on:
- Overall spending trend (increasing/decreasing)
- Category-wise changes
- Impact on savings rate
- Seasonal vs structural changes
"""
            
            # Execute the comparison analysis
            response = ""
            async for event in self.agent.run_async(ctx):
                if hasattr(event, 'content') and event.content:
                    response += str(event.content)
            
            return ctx.session.state.get('spending_comparison', {
                'status': 'completed',
                'customer_id': customer_id,
                'period1_months': period1_months,
                'period2_months': period2_months,
                'raw_response': response
            })
            
        except Exception as e:
            logger.error(f"Error comparing spending periods: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'customer_id': customer_id
            }

def create_spending_analyzer_agent(mcp_server_path: str) -> SpendingAnalyzerAgent:
    """
    Factory function to create a SpendingAnalyzerAgent instance.
    
    Args:
        mcp_server_path: Path to the MCP database server script
        
    Returns:
        Configured SpendingAnalyzerAgent instance
    """
    return SpendingAnalyzerAgent(mcp_server_path)
