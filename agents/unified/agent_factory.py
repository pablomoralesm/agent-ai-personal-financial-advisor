"""
Agent Factory for Unified Multi-Agent System

This module provides factory functions for creating agents and orchestrators
for different deployment contexts (Streamlit and ADK Web).

Part of the Agentic AI Personal Financial Advisor application.
"""

from typing import Dict, Any, Optional, List
from pathlib import Path

from .base_agent import UnifiedAgent, UnifiedOrchestratorBase
from .procedural_orchestrator import ProceduralOrchestrator
from .intelligent_orchestrator import IntelligentOrchestrator
from .deployment_configs import DeploymentConfig, DeploymentContext, OrchestratorType
from utils.logging_config import get_logger

logger = get_logger(__name__)

class AgentFactory:
    """
    Factory for creating unified agents and orchestrators.
    
    Provides context-aware creation of agents and orchestrators for
    different deployment contexts with appropriate configurations.
    """
    
    @staticmethod
    def create_spending_analyzer(mcp_server_path: str, deployment_context: str = "streamlit") -> UnifiedAgent:
        """
        Create a spending analyzer agent.
        
        Args:
            mcp_server_path: Path to the MCP database server script
            deployment_context: Context (streamlit, adk_web)
            
        Returns:
            Configured SpendingAnalyzer agent
        """
        return UnifiedAgent(
            name="SpendingAnalyzerAgent",
            mcp_server_path=mcp_server_path,
            deployment_context=deployment_context,
            model="gemini-2.0-flash",
            instruction="""
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
""",
            description="Analyzes customer spending habits, categorizes expenses, identifies trends, and provides insights for financial planning"
        )
    
    @staticmethod
    def create_goal_planner(mcp_server_path: str, deployment_context: str = "streamlit") -> UnifiedAgent:
        """
        Create a goal planner agent.
        
        Args:
            mcp_server_path: Path to the MCP database server script
            deployment_context: Context (streamlit, adk_web)
            
        Returns:
            Configured GoalPlanner agent
        """
        return UnifiedAgent(
            name="GoalPlannerAgent",
            mcp_server_path=mcp_server_path,
            deployment_context=deployment_context,
            model="gemini-2.0-flash",
            instruction="""
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
""",
            description="Evaluates financial goal feasibility, creates savings plans, tracks progress, and provides goal planning recommendations"
        )
    
    @staticmethod
    def create_advisor(mcp_server_path: str, deployment_context: str = "streamlit") -> UnifiedAgent:
        """
        Create an advisor agent.
        
        Args:
            mcp_server_path: Path to the MCP database server script
            deployment_context: Context (streamlit, adk_web)
            
        Returns:
            Configured Advisor agent
        """
        return UnifiedAgent(
            name="AdvisorAgent",
            mcp_server_path=mcp_server_path,
            deployment_context=deployment_context,
            model="gemini-2.0-flash",
            instruction="""
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
""",
            description="Main financial advisor that synthesizes insights from analysis agents and provides comprehensive recommendations"
        )
    
    @staticmethod
    def create_individual_agents(mcp_server_path: str, deployment_context: str = "streamlit") -> Dict[str, UnifiedAgent]:
        """
        Create all individual agents.
        
        Args:
            mcp_server_path: Path to the MCP database server script
            deployment_context: Context (streamlit, adk_web)
            
        Returns:
            Dictionary containing all agents
        """
        agents = {
            'spending_analyzer': AgentFactory.create_spending_analyzer(mcp_server_path, deployment_context),
            'goal_planner': AgentFactory.create_goal_planner(mcp_server_path, deployment_context),
            'advisor': AgentFactory.create_advisor(mcp_server_path, deployment_context)
        }
        
        logger.info(f"Created {len(agents)} individual agents for {deployment_context}")
        return agents

class OrchestratorFactory:
    """
    Factory for creating orchestrators based on context and type.
    """
    
    @staticmethod
    def create_orchestrator(orchestrator_type: str, mcp_server_path: str, 
                          deployment_context: str = "streamlit") -> UnifiedOrchestratorBase:
        """
        Create an orchestrator based on type and context.
        
        Args:
            orchestrator_type: Type of orchestrator (procedural, intelligent)
            mcp_server_path: Path to the MCP database server script
            deployment_context: Context (streamlit, adk_web)
            
        Returns:
            Configured orchestrator instance
            
        Raises:
            ValueError: If orchestrator type is not supported for the context
        """
        # Check if the context supports the orchestrator type
        if not DeploymentConfig.supports_orchestrator_type(deployment_context, orchestrator_type):
            supported_types = DeploymentConfig.get_supported_orchestrator_types(deployment_context)
            raise ValueError(
                f"Orchestrator type '{orchestrator_type}' not supported for context '{deployment_context}'. "
                f"Supported types: {supported_types}"
            )
        
        # Create individual agents
        agents = AgentFactory.create_individual_agents(mcp_server_path, deployment_context)
        
        if orchestrator_type == OrchestratorType.PROCEDURAL.value:
            orchestrator = ProceduralOrchestrator(mcp_server_path, deployment_context)
            orchestrator.set_sub_agents(
                agents['spending_analyzer'],
                agents['goal_planner'],
                agents['advisor']
            )
            return orchestrator
            
        elif orchestrator_type == OrchestratorType.INTELLIGENT.value:
            orchestrator = IntelligentOrchestrator(mcp_server_path, deployment_context)
            orchestrator.set_sub_agents(
                agents['spending_analyzer'],
                agents['goal_planner'],
                agents['advisor']
            )
            return orchestrator
            
        else:
            raise ValueError(f"Unknown orchestrator type: {orchestrator_type}")
    
    @staticmethod
    def create_for_streamlit(mcp_server_path: str) -> ProceduralOrchestrator:
        """
        Create orchestrator for Streamlit context (procedural only).
        
        Args:
            mcp_server_path: Path to the MCP database server script
            
        Returns:
            Procedural orchestrator for educational use
        """
        return OrchestratorFactory.create_orchestrator(
            OrchestratorType.PROCEDURAL.value,
            mcp_server_path,
            DeploymentContext.STREAMLIT.value
        )
    
    @staticmethod
    def create_for_adk_web(mcp_server_path: str, orchestrator_type: str = "procedural") -> UnifiedOrchestratorBase:
        """
        Create orchestrator for ADK Web context (both types available).
        
        Args:
            mcp_server_path: Path to the MCP database server script
            orchestrator_type: Type of orchestrator (procedural, intelligent)
            
        Returns:
            Configured orchestrator for development use
        """
        return OrchestratorFactory.create_orchestrator(
            orchestrator_type,
            mcp_server_path,
            DeploymentContext.ADK_WEB.value
        )
    
    @staticmethod
    def create_hybrid_system(mcp_server_path: str) -> Dict[str, UnifiedOrchestratorBase]:
        """
        Create both orchestrators for ADK Web hybrid system.
        
        Args:
            mcp_server_path: Path to the MCP database server script
            
        Returns:
            Dictionary containing both orchestrators
        """
        return {
            'procedural': OrchestratorFactory.create_for_adk_web(mcp_server_path, 'procedural'),
            'intelligent': OrchestratorFactory.create_for_adk_web(mcp_server_path, 'intelligent')
        }
