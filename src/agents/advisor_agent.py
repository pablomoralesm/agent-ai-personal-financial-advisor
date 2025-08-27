"""AdvisorAgent implementation for the Financial Advisor app.

This agent provides personalized financial advice by integrating insights from
the SpendingAnalyzerAgent and GoalPlannerAgent.
"""

import datetime
from typing import Dict, List, Any, Optional
import logging
import json

from google.adk import Agent, AgentConfig, Tool, ToolConfig, ToolSpec
from google.adk.llm import GeminiLLM
from google.adk.llm.gemini import GeminiConfig
from google.adk.a2a import A2AClient

from src.mcp.mcp_client import FinancialAdvisorMcpClient

class AdvisorAgent(Agent):
    """Agent that provides personalized financial advice."""
    
    def __init__(self, mcp_client: FinancialAdvisorMcpClient, api_key: str,
                spending_analyzer_url: str, goal_planner_url: str):
        """Initialize the AdvisorAgent.
        
        Args:
            mcp_client: MCP client for database access
            api_key: Google API key for Gemini
            spending_analyzer_url: URL for the SpendingAnalyzerAgent A2A endpoint
            goal_planner_url: URL for the GoalPlannerAgent A2A endpoint
        """
        self.mcp_client = mcp_client
        self.spending_analyzer_url = spending_analyzer_url
        self.goal_planner_url = goal_planner_url
        
        # Create A2A clients for other agents
        self.spending_analyzer_client = A2AClient(spending_analyzer_url)
        self.goal_planner_client = A2AClient(goal_planner_url)
        
        # Configure the LLM with higher temperature for more creative advice
        llm_config = GeminiConfig(
            model="gemini-1.5-pro-latest",
            api_key=api_key,
            temperature=0.4,  # Slightly higher for more creative advice
            top_p=0.95,
            top_k=40
        )
        llm = GeminiLLM(llm_config)
        
        # Configure the agent
        agent_config = AgentConfig(
            name="AdvisorAgent",
            description="Provides personalized financial advice",
            llm=llm,
            tools=self._create_tools()
        )
        
        super().__init__(agent_config)
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for the agent.
        
        Returns:
            List[Tool]: List of tools
        """
        tools = []
        
        # Tool to get customer advice history
        tools.append(Tool(
            ToolConfig(
                name="get_customer_advice_history",
                description="Get all advice history for a customer",
                function=self._get_customer_advice_history,
                parameters=[
                    ToolSpec.Parameter(
                        name="customer_id",
                        description="Customer ID",
                        type="integer",
                        required=True
                    )
                ]
            )
        ))
        
        # Tool to add advice
        tools.append(Tool(
            ToolConfig(
                name="add_advice",
                description="Add new advice to the history",
                function=self._add_advice,
                parameters=[
                    ToolSpec.Parameter(
                        name="customer_id",
                        description="Customer ID",
                        type="integer",
                        required=True
                    ),
                    ToolSpec.Parameter(
                        name="advice_text",
                        description="Advice text",
                        type="string",
                        required=True
                    )
                ]
            )
        ))
        
        # Tool to get spending analysis from SpendingAnalyzerAgent
        tools.append(Tool(
            ToolConfig(
                name="get_spending_analysis",
                description="Get spending analysis from SpendingAnalyzerAgent",
                function=self._get_spending_analysis,
                parameters=[
                    ToolSpec.Parameter(
                        name="customer_id",
                        description="Customer ID",
                        type="integer",
                        required=True
                    ),
                    ToolSpec.Parameter(
                        name="months",
                        description="Number of months to analyze",
                        type="integer",
                        required=True
                    )
                ]
            )
        ))
        
        # Tool to get goal planning from GoalPlannerAgent
        tools.append(Tool(
            ToolConfig(
                name="get_goal_planning",
                description="Get goal planning from GoalPlannerAgent",
                function=self._get_goal_planning,
                parameters=[
                    ToolSpec.Parameter(
                        name="customer_id",
                        description="Customer ID",
                        type="integer",
                        required=True
                    ),
                    ToolSpec.Parameter(
                        name="avg_monthly_spending",
                        description="Average monthly spending",
                        type="number",
                        required=True
                    )
                ]
            )
        ))
        
        # Tool to generate personalized advice
        tools.append(Tool(
            ToolConfig(
                name="generate_personalized_advice",
                description="Generate personalized financial advice",
                function=self._generate_personalized_advice,
                parameters=[
                    ToolSpec.Parameter(
                        name="customer_id",
                        description="Customer ID",
                        type="integer",
                        required=True
                    ),
                    ToolSpec.Parameter(
                        name="spending_analysis",
                        description="Spending analysis data",
                        type="object",
                        required=True
                    ),
                    ToolSpec.Parameter(
                        name="goal_planning",
                        description="Goal planning data",
                        type="object",
                        required=True
                    )
                ]
            )
        ))
        
        # Tool to recommend next steps
        tools.append(Tool(
            ToolConfig(
                name="recommend_next_steps",
                description="Recommend next steps for financial improvement",
                function=self._recommend_next_steps,
                parameters=[
                    ToolSpec.Parameter(
                        name="customer_id",
                        description="Customer ID",
                        type="integer",
                        required=True
                    ),
                    ToolSpec.Parameter(
                        name="spending_analysis",
                        description="Spending analysis data",
                        type="object",
                        required=True
                    ),
                    ToolSpec.Parameter(
                        name="goal_planning",
                        description="Goal planning data",
                        type="object",
                        required=True
                    )
                ]
            )
        ))
        
        return tools
    
    # Tool implementations
    
    def _get_customer_advice_history(self, customer_id: int) -> List[Dict[str, Any]]:
        """Get all advice history for a customer."""
        return self.mcp_client.get_customer_advice_history(customer_id)
    
    def _add_advice(self, customer_id: int, advice_text: str) -> Dict[str, Any]:
        """Add new advice to the history."""
        return self.mcp_client.add_advice(
            customer_id=customer_id,
            agent_name="AdvisorAgent",
            advice_text=advice_text
        )
    
    def _get_spending_analysis(self, customer_id: int, months: int) -> Dict[str, Any]:
        """Get spending analysis from SpendingAnalyzerAgent.
        
        Args:
            customer_id: Customer ID
            months: Number of months to analyze
            
        Returns:
            Dict[str, Any]: Spending analysis
        """
        try:
            # Use A2A to call the SpendingAnalyzerAgent
            response = self.spending_analyzer_client.execute(
                "analyze_customer_spending",
                {"customer_id": customer_id, "months": months}
            )
            return response
        except Exception as e:
            logging.error(f"Error getting spending analysis: {e}")
            return {"error": f"Failed to get spending analysis: {str(e)}"}
    
    def _get_goal_planning(self, customer_id: int, avg_monthly_spending: float) -> Dict[str, Any]:
        """Get goal planning from GoalPlannerAgent.
        
        Args:
            customer_id: Customer ID
            avg_monthly_spending: Average monthly spending
            
        Returns:
            Dict[str, Any]: Goal planning
        """
        try:
            # Use A2A to call the GoalPlannerAgent
            response = self.goal_planner_client.execute(
                "plan_customer_goals",
                {"customer_id": customer_id, "avg_monthly_spending": avg_monthly_spending}
            )
            return response
        except Exception as e:
            logging.error(f"Error getting goal planning: {e}")
            return {"error": f"Failed to get goal planning: {str(e)}"}
    
    def _generate_personalized_advice(self, customer_id: int, 
                                     spending_analysis: Dict[str, Any],
                                     goal_planning: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized financial advice.
        
        Args:
            customer_id: Customer ID
            spending_analysis: Spending analysis data
            goal_planning: Goal planning data
            
        Returns:
            Dict[str, Any]: Personalized advice
        """
        # Check for errors in the input data
        if "error" in spending_analysis or "error" in goal_planning:
            error_msg = spending_analysis.get("error", "") or goal_planning.get("error", "")
            return {"error": f"Cannot generate advice: {error_msg}"}
        
        # Extract key information
        customer = spending_analysis.get("customer", {})
        spending_patterns = spending_analysis.get("spending_patterns", {})
        high_spending = spending_analysis.get("high_spending", {})
        spending_trends = spending_analysis.get("trends", {})
        
        has_goals = goal_planning.get("has_goals", False)
        goals = goal_planning.get("goals", [])
        recommendations = goal_planning.get("recommendations", {})
        goal_analysis = goal_planning.get("goal_analysis", [])
        
        # Prepare context for the LLM
        context = {
            "customer_name": customer.get("name", "Customer"),
            "total_spending": spending_patterns.get("total_spending", 0),
            "avg_monthly_spending": spending_patterns.get("avg_monthly_spending", 0),
            "spending_trend": spending_trends.get("trend", "stable"),
            "high_spending_categories": [cat["category"] for cat in high_spending.get("high_spending_categories", [])],
            "has_goals": has_goals,
            "goals": goals,
            "overall_goal_assessment": "realistic" if recommendations.get("overall_realistic", False) else "needs adjustment",
            "total_monthly_contribution": recommendations.get("total_monthly_contribution", 0),
            "estimated_savings_capacity": recommendations.get("estimated_savings_capacity", 0),
        }
        
        # Generate advice using the LLM
        prompt = f"""
        You are a financial advisor providing personalized advice to {context['customer_name']}.
        
        Spending Analysis:
        - Total spending over the past months: ${context['total_spending']:.2f}
        - Average monthly spending: ${context['avg_monthly_spending']:.2f}
        - Spending trend: {context['spending_trend']}
        - High spending categories: {', '.join(context['high_spending_categories']) if context['high_spending_categories'] else 'None identified'}
        
        Goal Assessment:
        - Has financial goals: {'Yes' if context['has_goals'] else 'No'}
        - Overall goal assessment: {context['overall_goal_assessment']}
        - Total monthly contribution needed: ${context['total_monthly_contribution']:.2f}
        - Estimated monthly savings capacity: ${context['estimated_savings_capacity']:.2f}
        
        Based on this information, provide personalized financial advice covering:
        1. Spending habits assessment and recommendations for improvement
        2. Goal feasibility and suggestions for adjustments if needed
        3. Specific actionable steps to improve financial health
        4. Prioritized recommendations (most important first)
        
        Keep your advice concise, practical, and tailored to the customer's specific situation.
        """
        
        try:
            response = self.llm.generate(prompt)
            advice_text = response.text
            
            # Save the advice
            self._add_advice(customer_id, advice_text)
            
            return {
                "customer_id": customer_id,
                "advice_text": advice_text,
                "context": context
            }
        except Exception as e:
            logging.error(f"Error generating advice: {e}")
            return {"error": f"Failed to generate advice: {str(e)}"}
    
    def _recommend_next_steps(self, customer_id: int,
                             spending_analysis: Dict[str, Any],
                             goal_planning: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend next steps for financial improvement.
        
        Args:
            customer_id: Customer ID
            spending_analysis: Spending analysis data
            goal_planning: Goal planning data
            
        Returns:
            Dict[str, Any]: Recommended next steps
        """
        # Check for errors in the input data
        if "error" in spending_analysis or "error" in goal_planning:
            error_msg = spending_analysis.get("error", "") or goal_planning.get("error", "")
            return {"error": f"Cannot recommend next steps: {error_msg}"}
        
        # Extract key information
        high_spending = spending_analysis.get("high_spending", {})
        spending_trends = spending_analysis.get("trends", {})
        
        has_goals = goal_planning.get("has_goals", False)
        recommendations = goal_planning.get("recommendations", {})
        goal_analysis = goal_planning.get("goal_analysis", [])
        
        # Identify next steps based on analysis
        next_steps = []
        
        # Check if spending is increasing
        if spending_trends.get("trend") == "increasing":
            next_steps.append({
                "priority": "high",
                "action": "Review and reduce expenses",
                "description": "Your spending has been increasing. Review your transactions and identify areas to cut back."
            })
        
        # Check high spending categories
        high_spending_categories = high_spending.get("high_spending_categories", [])
        if high_spending_categories:
            next_steps.append({
                "priority": "medium",
                "action": f"Reduce spending in {high_spending_categories[0]['category']}",
                "description": f"This category represents a significant portion of your spending. Look for ways to reduce expenses here."
            })
        
        # Check goal feasibility
        if has_goals and not recommendations.get("overall_realistic", False):
            next_steps.append({
                "priority": "high",
                "action": "Adjust financial goals",
                "description": "Your current goals may not be realistic with your savings capacity. Consider extending timelines or adjusting target amounts."
            })
        
        # Check if savings capacity is low
        estimated_savings = recommendations.get("estimated_savings_capacity", 0)
        if estimated_savings < 200:  # Arbitrary threshold
            next_steps.append({
                "priority": "high",
                "action": "Increase savings capacity",
                "description": "Your current savings capacity is low. Look for ways to increase income or reduce essential expenses."
            })
        
        # If no goals, suggest creating some
        if not has_goals:
            next_steps.append({
                "priority": "medium",
                "action": "Set financial goals",
                "description": "You don't have any financial goals set. Consider setting goals for emergency funds, retirement, or other important life events."
            })
        
        # Always recommend tracking expenses
        next_steps.append({
            "priority": "low",
            "action": "Track expenses regularly",
            "description": "Regularly monitor your spending to stay aware of your financial habits and make adjustments as needed."
        })
        
        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        next_steps.sort(key=lambda x: priority_order.get(x["priority"], 3))
        
        return {
            "customer_id": customer_id,
            "next_steps": next_steps
        }
    
    def provide_financial_advice(self, customer_id: int, months: int = 3) -> Dict[str, Any]:
        """Provide comprehensive financial advice for a customer.
        
        This is the main method to be called by external code.
        
        Args:
            customer_id: Customer ID
            months: Number of months to analyze
            
        Returns:
            Dict[str, Any]: Comprehensive advice and recommendations
        """
        # Get customer info
        try:
            customer = self.mcp_client.get_customer(customer_id)
        except Exception as e:
            logging.error(f"Error getting customer {customer_id}: {e}")
            return {"error": f"Customer with ID {customer_id} not found"}
        
        # Get spending analysis
        spending_analysis = self._get_spending_analysis(customer_id, months)
        if "error" in spending_analysis:
            return spending_analysis
        
        # Get average monthly spending from analysis
        avg_monthly_spending = spending_analysis.get("spending_patterns", {}).get("avg_monthly_spending", 0)
        
        # Get goal planning
        goal_planning = self._get_goal_planning(customer_id, avg_monthly_spending)
        if "error" in goal_planning:
            return goal_planning
        
        # Generate personalized advice
        advice = self._generate_personalized_advice(
            customer_id, 
            spending_analysis,
            goal_planning
        )
        
        # Recommend next steps
        next_steps = self._recommend_next_steps(
            customer_id,
            spending_analysis,
            goal_planning
        )
        
        # Return comprehensive results
        return {
            "customer": customer,
            "spending_analysis": spending_analysis,
            "goal_planning": goal_planning,
            "advice": advice,
            "next_steps": next_steps
        }
