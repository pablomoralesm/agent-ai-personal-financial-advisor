"""GoalPlannerAgent implementation for the Financial Advisor app.

This agent helps customers set and track financial goals.
"""

import datetime
from typing import Dict, List, Any, Optional
import logging

from google.adk import Agent, AgentConfig, Tool, ToolConfig, ToolSpec
from google.adk.llm import GeminiLLM
from google.adk.llm.gemini import GeminiConfig

from src.mcp.mcp_client import FinancialAdvisorMcpClient

class GoalPlannerAgent(Agent):
    """Agent that helps customers set and track financial goals."""
    
    def __init__(self, mcp_client: FinancialAdvisorMcpClient, api_key: str):
        """Initialize the GoalPlannerAgent.
        
        Args:
            mcp_client: MCP client for database access
            api_key: Google API key for Gemini
        """
        self.mcp_client = mcp_client
        
        # Configure the LLM
        llm_config = GeminiConfig(
            model="gemini-1.5-pro-latest",
            api_key=api_key,
            temperature=0.2,
            top_p=0.95,
            top_k=40
        )
        llm = GeminiLLM(llm_config)
        
        # Configure the agent
        agent_config = AgentConfig(
            name="GoalPlannerAgent",
            description="Helps customers set and track financial goals",
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
        
        # Tool to get customer goals
        tools.append(Tool(
            ToolConfig(
                name="get_customer_goals",
                description="Get all goals for a customer",
                function=self._get_customer_goals,
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
        
        # Tool to get a specific goal
        tools.append(Tool(
            ToolConfig(
                name="get_goal",
                description="Get a specific goal by ID",
                function=self._get_goal,
                parameters=[
                    ToolSpec.Parameter(
                        name="goal_id",
                        description="Goal ID",
                        type="integer",
                        required=True
                    )
                ]
            )
        ))
        
        # Tool to create a goal
        tools.append(Tool(
            ToolConfig(
                name="create_goal",
                description="Create a new goal for a customer",
                function=self._create_goal,
                parameters=[
                    ToolSpec.Parameter(
                        name="customer_id",
                        description="Customer ID",
                        type="integer",
                        required=True
                    ),
                    ToolSpec.Parameter(
                        name="goal_type",
                        description="Goal type",
                        type="string",
                        required=True
                    ),
                    ToolSpec.Parameter(
                        name="target_amount",
                        description="Target amount",
                        type="number",
                        required=True
                    ),
                    ToolSpec.Parameter(
                        name="current_amount",
                        description="Current amount",
                        type="number",
                        required=True
                    ),
                    ToolSpec.Parameter(
                        name="target_date",
                        description="Target date (YYYY-MM-DD)",
                        type="string",
                        required=True
                    ),
                    ToolSpec.Parameter(
                        name="description",
                        description="Goal description",
                        type="string",
                        required=True
                    )
                ]
            )
        ))
        
        # Tool to update goal progress
        tools.append(Tool(
            ToolConfig(
                name="update_goal_progress",
                description="Update the current amount for a goal",
                function=self._update_goal_progress,
                parameters=[
                    ToolSpec.Parameter(
                        name="goal_id",
                        description="Goal ID",
                        type="integer",
                        required=True
                    ),
                    ToolSpec.Parameter(
                        name="current_amount",
                        description="Current amount",
                        type="number",
                        required=True
                    )
                ]
            )
        ))
        
        # Tool to calculate goal progress
        tools.append(Tool(
            ToolConfig(
                name="calculate_goal_progress",
                description="Calculate progress for a goal",
                function=self._calculate_goal_progress,
                parameters=[
                    ToolSpec.Parameter(
                        name="goal_id",
                        description="Goal ID",
                        type="integer",
                        required=True
                    )
                ]
            )
        ))
        
        # Tool to calculate monthly contribution
        tools.append(Tool(
            ToolConfig(
                name="calculate_monthly_contribution",
                description="Calculate required monthly contribution to reach a goal",
                function=self._calculate_monthly_contribution,
                parameters=[
                    ToolSpec.Parameter(
                        name="goal_id",
                        description="Goal ID",
                        type="integer",
                        required=True
                    )
                ]
            )
        ))
        
        # Tool to recommend goal adjustments
        tools.append(Tool(
            ToolConfig(
                name="recommend_goal_adjustments",
                description="Recommend adjustments to goals based on spending analysis",
                function=self._recommend_goal_adjustments,
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
        
        # Tool to evaluate goal feasibility
        tools.append(Tool(
            ToolConfig(
                name="evaluate_goal_feasibility",
                description="Evaluate the feasibility of a goal",
                function=self._evaluate_goal_feasibility,
                parameters=[
                    ToolSpec.Parameter(
                        name="goal_id",
                        description="Goal ID",
                        type="integer",
                        required=True
                    ),
                    ToolSpec.Parameter(
                        name="monthly_savings_capacity",
                        description="Monthly savings capacity",
                        type="number",
                        required=True
                    )
                ]
            )
        ))
        
        return tools
    
    # Tool implementations
    
    def _get_customer_goals(self, customer_id: int) -> List[Dict[str, Any]]:
        """Get all goals for a customer."""
        return self.mcp_client.get_customer_goals(customer_id)
    
    def _get_goal(self, goal_id: int) -> Dict[str, Any]:
        """Get a specific goal by ID."""
        return self.mcp_client.get_goal(goal_id)
    
    def _create_goal(self, customer_id: int, goal_type: str, target_amount: float,
                   current_amount: float, target_date: str, description: str) -> Dict[str, Any]:
        """Create a new goal for a customer."""
        return self.mcp_client.create_goal(
            customer_id, goal_type, target_amount, current_amount, target_date, description
        )
    
    def _update_goal_progress(self, goal_id: int, current_amount: float) -> Dict[str, Any]:
        """Update the current amount for a goal."""
        return self.mcp_client.update_goal_progress(goal_id, current_amount)
    
    def _calculate_goal_progress(self, goal_id: int) -> Dict[str, Any]:
        """Calculate progress for a goal.
        
        Args:
            goal_id: Goal ID
            
        Returns:
            Dict[str, Any]: Goal progress details
        """
        goal = self.mcp_client.get_goal(goal_id)
        
        # Calculate percentage complete
        progress_percentage = (goal["current_amount"] / goal["target_amount"]) * 100 if goal["target_amount"] > 0 else 0
        
        # Calculate remaining amount
        remaining_amount = goal["target_amount"] - goal["current_amount"]
        
        # Calculate days until target date
        target_date = datetime.datetime.strptime(goal["target_date"], "%Y-%m-%d").date()
        days_remaining = (target_date - datetime.date.today()).days
        
        # Calculate months remaining
        months_remaining = days_remaining / 30.0
        
        return {
            "goal": goal,
            "progress_percentage": progress_percentage,
            "remaining_amount": remaining_amount,
            "days_remaining": days_remaining,
            "months_remaining": months_remaining
        }
    
    def _calculate_monthly_contribution(self, goal_id: int) -> Dict[str, Any]:
        """Calculate required monthly contribution to reach a goal.
        
        Args:
            goal_id: Goal ID
            
        Returns:
            Dict[str, Any]: Monthly contribution details
        """
        # Get goal progress
        progress = self._calculate_goal_progress(goal_id)
        
        # Calculate required monthly contribution
        monthly_contribution = 0
        if progress["months_remaining"] > 0:
            monthly_contribution = progress["remaining_amount"] / progress["months_remaining"]
        
        return {
            "goal": progress["goal"],
            "monthly_contribution": monthly_contribution,
            "months_remaining": progress["months_remaining"],
            "progress_percentage": progress["progress_percentage"]
        }
    
    def _recommend_goal_adjustments(self, customer_id: int, avg_monthly_spending: float) -> Dict[str, Any]:
        """Recommend adjustments to goals based on spending analysis.
        
        Args:
            customer_id: Customer ID
            avg_monthly_spending: Average monthly spending
            
        Returns:
            Dict[str, Any]: Goal adjustment recommendations
        """
        # Get customer goals
        goals = self.mcp_client.get_customer_goals(customer_id)
        
        # Assume savings capacity is 20% of average monthly spending
        estimated_savings_capacity = avg_monthly_spending * 0.2
        
        # Analyze each goal
        goal_recommendations = []
        total_monthly_contribution = 0
        
        for goal in goals:
            # Calculate required monthly contribution
            progress = self._calculate_goal_progress(goal["id"])
            monthly_contribution = 0
            if progress["months_remaining"] > 0:
                monthly_contribution = progress["remaining_amount"] / progress["months_remaining"]
            
            total_monthly_contribution += monthly_contribution
            
            # Evaluate if the goal is realistic
            is_realistic = monthly_contribution <= estimated_savings_capacity
            
            # Add recommendation
            goal_recommendations.append({
                "goal": goal,
                "monthly_contribution": monthly_contribution,
                "is_realistic": is_realistic,
                "progress_percentage": progress["progress_percentage"],
                "months_remaining": progress["months_remaining"]
            })
        
        # Overall assessment
        overall_realistic = total_monthly_contribution <= estimated_savings_capacity
        
        return {
            "goal_recommendations": goal_recommendations,
            "total_monthly_contribution": total_monthly_contribution,
            "estimated_savings_capacity": estimated_savings_capacity,
            "overall_realistic": overall_realistic
        }
    
    def _evaluate_goal_feasibility(self, goal_id: int, monthly_savings_capacity: float) -> Dict[str, Any]:
        """Evaluate the feasibility of a goal.
        
        Args:
            goal_id: Goal ID
            monthly_savings_capacity: Monthly savings capacity
            
        Returns:
            Dict[str, Any]: Goal feasibility assessment
        """
        # Calculate required monthly contribution
        contribution_info = self._calculate_monthly_contribution(goal_id)
        
        # Determine if the goal is feasible
        is_feasible = contribution_info["monthly_contribution"] <= monthly_savings_capacity
        
        # Calculate feasibility percentage
        feasibility_percentage = (monthly_savings_capacity / contribution_info["monthly_contribution"]) * 100 if contribution_info["monthly_contribution"] > 0 else 100
        
        # Suggest adjusted target date if not feasible
        adjusted_target_date = None
        if not is_feasible and contribution_info["monthly_contribution"] > 0:
            # Calculate how many months it would take with current savings capacity
            months_needed = contribution_info["goal"]["remaining_amount"] / monthly_savings_capacity
            adjusted_target_date = (datetime.date.today() + datetime.timedelta(days=int(months_needed * 30))).isoformat()
        
        return {
            "goal": contribution_info["goal"],
            "monthly_contribution": contribution_info["monthly_contribution"],
            "monthly_savings_capacity": monthly_savings_capacity,
            "is_feasible": is_feasible,
            "feasibility_percentage": min(feasibility_percentage, 100),
            "adjusted_target_date": adjusted_target_date
        }
    
    def plan_customer_goals(self, customer_id: int, avg_monthly_spending: float) -> Dict[str, Any]:
        """Plan and evaluate customer goals.
        
        This is the main method to be called by external code.
        
        Args:
            customer_id: Customer ID
            avg_monthly_spending: Average monthly spending
            
        Returns:
            Dict[str, Any]: Goal planning results
        """
        # Get customer info
        try:
            customer = self.mcp_client.get_customer(customer_id)
        except Exception as e:
            logging.error(f"Error getting customer {customer_id}: {e}")
            return {"error": f"Customer with ID {customer_id} not found"}
        
        # Get customer goals
        goals = self.mcp_client.get_customer_goals(customer_id)
        
        # If no goals, return empty analysis
        if not goals:
            return {
                "customer": customer,
                "goals": [],
                "has_goals": False,
                "message": "No financial goals found for this customer."
            }
        
        # Recommend goal adjustments
        recommendations = self._recommend_goal_adjustments(customer_id, avg_monthly_spending)
        
        # Create detailed goal analysis
        goal_analysis = []
        for goal_rec in recommendations["goal_recommendations"]:
            goal = goal_rec["goal"]
            
            # Evaluate feasibility
            feasibility = self._evaluate_goal_feasibility(goal["id"], recommendations["estimated_savings_capacity"])
            
            goal_analysis.append({
                "goal": goal,
                "progress": goal_rec["progress_percentage"],
                "monthly_contribution": goal_rec["monthly_contribution"],
                "is_realistic": goal_rec["is_realistic"],
                "months_remaining": goal_rec["months_remaining"],
                "feasibility": feasibility
            })
        
        # Save analysis as advice
        analysis_summary = (
            f"Goal Planning Analysis:\n"
            f"- Total monthly contribution needed: ${recommendations['total_monthly_contribution']:.2f}\n"
            f"- Estimated monthly savings capacity: ${recommendations['estimated_savings_capacity']:.2f}\n"
            f"- Overall assessment: {'Realistic' if recommendations['overall_realistic'] else 'Needs adjustment'}\n\n"
            f"Goal-specific recommendations:\n"
        )
        
        for goal_rec in recommendations["goal_recommendations"]:
            analysis_summary += (
                f"- {goal_rec['goal']['goal_type']} (${goal_rec['goal']['target_amount']:.2f}):\n"
                f"  * Progress: {goal_rec['progress_percentage']:.1f}%\n"
                f"  * Monthly contribution needed: ${goal_rec['monthly_contribution']:.2f}\n"
                f"  * Assessment: {'Realistic' if goal_rec['is_realistic'] else 'Needs adjustment'}\n"
            )
        
        try:
            self.mcp_client.add_advice(
                customer_id=customer_id,
                agent_name="GoalPlannerAgent",
                advice_text=analysis_summary
            )
        except Exception as e:
            logging.error(f"Error saving goal planning analysis: {e}")
        
        # Return comprehensive analysis
        return {
            "customer": customer,
            "goals": goals,
            "has_goals": True,
            "recommendations": recommendations,
            "goal_analysis": goal_analysis,
            "analysis_summary": analysis_summary
        }
