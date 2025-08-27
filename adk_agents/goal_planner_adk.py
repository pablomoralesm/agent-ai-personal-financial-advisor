"""
ADK-based Goal Planner Agent for the Financial Advisor AI system.

This agent uses Google's Agent Development Kit (ADK) to help customers set 
realistic financial goals, create actionable plans, and track progress.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal
import json

from google.adk import Agent
from financial_mcp.server import mcp_server
from financial_mcp.models import GoalType


class GoalPlanningToolset:
    """Custom toolset for goal planning data retrieval and analysis."""
    
    @staticmethod
    def get_customer_financial_profile(customer_id: int) -> Dict[str, Any]:
        """
        Get comprehensive financial profile for goal planning.
        
        Args:
            customer_id: ID of the customer
            
        Returns:
            Dictionary containing financial profile data
        """
        try:
            # Get customer basic info
            customer = mcp_server.get_customer_by_id(customer_id)
            
            # Get recent transactions (last 90 days) for spending analysis
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=90)
            
            transactions = mcp_server.get_customer_transactions(customer_id)
            
            # Calculate financial metrics
            total_income = sum(t.amount for t in transactions if t.amount > 0)
            total_expenses = abs(sum(t.amount for t in transactions if t.amount < 0))
            monthly_income = total_income / 3  # 90 days = ~3 months
            monthly_expenses = total_expenses / 3
            
            # Get existing goals
            goals = mcp_server.get_goals_by_customer(customer_id)
            
            # Convert goals to serializable format
            goals_data = []
            for goal in goals:
                goals_data.append({
                    'id': goal.id,
                    'title': goal.title,
                    'description': goal.description,
                    'goal_type': goal.goal_type.value,
                    'target_amount': float(goal.target_amount),
                    'current_amount': float(goal.current_amount or 0),
                    'target_date': goal.target_date.isoformat() if goal.target_date else None,
                    'is_achieved': goal.is_achieved,
                    'created_at': goal.created_at.isoformat()
                })
            
            return {
                'customer': {
                    'id': customer.id,
                    'name': customer.name,
                    'age': customer.age,
                    'income': float(customer.income)
                },
                'financial_metrics': {
                    'monthly_income': float(monthly_income),
                    'monthly_expenses': float(monthly_expenses),
                    'disposable_income': float(monthly_income - monthly_expenses),
                    'savings_rate': float((monthly_income - monthly_expenses) / monthly_income * 100) if monthly_income > 0 else 0
                },
                'existing_goals': goals_data,
                'analysis_period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'days': 90
                }
            }
        except Exception as e:
            return {'error': f"Failed to retrieve financial profile: {str(e)}"}


class GoalPlannerADK:
    """
    ADK-based agent for financial goal planning and tracking.
    
    This implementation uses Google's Agent Development Kit to provide
    the same functionality as the custom GoalPlannerAgent.
    """
    
    def __init__(self):
        """Initialize the ADK-based goal planner agent."""
        
        # Define the system prompt for goal planning
        self.system_prompt = """
You are a Financial Goal Planning AI assistant. Your role is to help customers set realistic financial goals and create actionable plans to achieve them.

Your analysis should include:
1. Goal feasibility assessment based on current financial situation
2. Realistic timeline and savings plan
3. Monthly/weekly savings targets
4. Potential obstacles and mitigation strategies
5. Alternative goal scenarios (stretch, moderate, conservative)
6. Progress tracking recommendations

Guidelines:
- Be realistic but encouraging in your assessments
- Consider the customer's income, spending patterns, and existing financial commitments
- Provide specific, actionable steps
- Include fallback plans for different scenarios
- Use motivational language while being honest about challenges
- Consider the customer's age and time horizon
- Factor in inflation and potential income changes

Output Format:
Provide your analysis as a JSON object with the following structure:
{
    "goal_analysis": {
        "feasibility_score": number,
        "feasibility_assessment": "string",
        "recommended_timeline": "string",
        "required_monthly_savings": number,
        "challenges": ["string"],
        "success_factors": ["string"]
    },
    "savings_plan": {
        "conservative_scenario": {
            "monthly_amount": number,
            "timeline_months": number,
            "success_probability": number
        },
        "moderate_scenario": {
            "monthly_amount": number,
            "timeline_months": number,
            "success_probability": number
        },
        "stretch_scenario": {
            "monthly_amount": number,
            "timeline_months": number,
            "success_probability": number
        }
    },
    "action_plan": [
        {
            "step": number,
            "action": "string",
            "timeline": "string",
            "priority": "high|medium|low"
        }
    ],
    "recommendations": [
        {
            "category": "string",
            "recommendation": "string",
            "impact": "string"
        }
    ],
    "progress_tracking": {
        "review_frequency": "string",
        "key_metrics": ["string"],
        "milestone_schedule": ["string"]
    },
    "confidence_score": number
}
"""
        
        # Create the ADK agent
        self.agent = Agent(
            name="goal_planner",
            model="gemini-1.5-flash",
            description="Plans and tracks financial goals based on spending patterns and income",
            instruction=self.system_prompt,
            tools=[]  # We'll handle data retrieval separately
        )
    
    def analyze_goal(self, customer_id: int, goal_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze a financial goal for feasibility and create an action plan.
        
        Args:
            customer_id: ID of the customer
            goal_data: Dictionary containing goal information (title, target_amount, target_date, etc.)
            context: Optional additional context for the analysis
            
        Returns:
            Dictionary containing goal analysis and recommendations
        """
        try:
            # Get customer financial profile
            financial_profile = GoalPlanningToolset.get_customer_financial_profile(customer_id)
            
            if 'error' in financial_profile:
                return {
                    'success': False,
                    'error': financial_profile['error'],
                    'agent_name': 'GoalPlannerADK',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Prepare the analysis prompt
            analysis_prompt = f"""
Please analyze the following financial goal for customer ID {customer_id}:

Customer Financial Profile:
{json.dumps(financial_profile, indent=2)}

Goal to Analyze:
{json.dumps(goal_data, indent=2)}

Additional Context:
{json.dumps(context or {}, indent=2)}

Please provide a comprehensive goal analysis and planning recommendation following the specified JSON format.
Consider the customer's current financial situation, existing goals, and the feasibility of achieving this new goal.
"""
            
            # Use ADK agent to generate analysis
            response = self.agent.run(analysis_prompt)
            
            # Parse the response
            try:
                # Extract JSON from response if it's wrapped in text
                response_text = str(response)
                if '{' in response_text and '}' in response_text:
                    json_start = response_text.find('{')
                    json_end = response_text.rfind('}') + 1
                    json_str = response_text[json_start:json_end]
                    analysis_result = json.loads(json_str)
                else:
                    # If no JSON found, wrap the response
                    analysis_result = {
                        'goal_analysis': {'feasibility_assessment': response_text},
                        'savings_plan': {},
                        'action_plan': [],
                        'recommendations': [],
                        'confidence_score': 0.5
                    }
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                analysis_result = {
                    'goal_analysis': {'feasibility_assessment': str(response)},
                    'savings_plan': {},
                    'action_plan': [],
                    'recommendations': [],
                    'confidence_score': 0.5
                }
            
            # Add metadata
            analysis_result.update({
                'success': True,
                'agent_name': 'GoalPlannerADK',
                'customer_id': customer_id,
                'analysis_date': datetime.now().isoformat(),
                'goal_data': goal_data
            })
            
            return analysis_result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Goal analysis failed: {str(e)}",
                'agent_name': 'GoalPlannerADK',
                'customer_id': customer_id,
                'timestamp': datetime.now().isoformat()
            }
    
    def track_goal_progress(self, customer_id: int, goal_id: int) -> Dict[str, Any]:
        """
        Track progress on an existing goal and provide recommendations.
        
        Args:
            customer_id: ID of the customer
            goal_id: ID of the goal to track
            
        Returns:
            Dictionary containing progress analysis and recommendations
        """
        try:
            # Get the specific goal
            goal = mcp_server.get_goal_by_id(goal_id)
            if not goal or goal.customer_id != customer_id:
                return {
                    'success': False,
                    'error': 'Goal not found or access denied',
                    'agent_name': 'GoalPlannerADK',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Get financial profile for updated context
            financial_profile = GoalPlanningToolset.get_customer_financial_profile(customer_id)
            
            if 'error' in financial_profile:
                return {
                    'success': False,
                    'error': financial_profile['error'],
                    'agent_name': 'GoalPlannerADK',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Calculate progress metrics
            progress_percentage = (float(goal.current_amount or 0) / float(goal.target_amount)) * 100
            remaining_amount = float(goal.target_amount) - float(goal.current_amount or 0)
            
            # Calculate time metrics
            if goal.target_date:
                days_remaining = (goal.target_date - date.today()).days
                months_remaining = max(1, days_remaining / 30.44)  # Average days per month
            else:
                days_remaining = None
                months_remaining = None
            
            progress_data = {
                'goal': {
                    'id': goal.id,
                    'title': goal.title,
                    'target_amount': float(goal.target_amount),
                    'current_amount': float(goal.current_amount or 0),
                    'progress_percentage': progress_percentage,
                    'remaining_amount': remaining_amount,
                    'target_date': goal.target_date.isoformat() if goal.target_date else None,
                    'days_remaining': days_remaining,
                    'months_remaining': months_remaining
                }
            }
            
            # Prepare progress tracking prompt
            tracking_prompt = f"""
Please analyze the progress on the following financial goal:

Goal Progress Data:
{json.dumps(progress_data, indent=2)}

Current Financial Profile:
{json.dumps(financial_profile, indent=2)}

Please provide recommendations for staying on track or adjusting the goal plan.
Focus on actionable advice based on current progress and financial situation.

Provide response in this JSON format:
{{
    "progress_assessment": {{
        "status": "on_track|behind|ahead",
        "assessment": "string",
        "key_insights": ["string"]
    }},
    "recommendations": [
        {{
            "type": "adjustment|motivation|strategy",
            "recommendation": "string",
            "rationale": "string"
        }}
    ],
    "next_steps": ["string"],
    "confidence_score": number
}}
"""
            
            # Use ADK agent to generate progress analysis
            response = self.agent.run(tracking_prompt)
            
            # Parse the response
            try:
                response_text = str(response)
                if '{' in response_text and '}' in response_text:
                    json_start = response_text.find('{')
                    json_end = response_text.rfind('}') + 1
                    json_str = response_text[json_start:json_end]
                    tracking_result = json.loads(json_str)
                else:
                    tracking_result = {
                        'progress_assessment': {'assessment': response_text},
                        'recommendations': [],
                        'next_steps': [],
                        'confidence_score': 0.5
                    }
            except json.JSONDecodeError:
                tracking_result = {
                    'progress_assessment': {'assessment': str(response)},
                    'recommendations': [],
                    'next_steps': [],
                    'confidence_score': 0.5
                }
            
            # Add metadata and progress data
            tracking_result.update({
                'success': True,
                'agent_name': 'GoalPlannerADK',
                'customer_id': customer_id,
                'goal_id': goal_id,
                'tracking_date': datetime.now().isoformat(),
                'progress_data': progress_data
            })
            
            return tracking_result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Progress tracking failed: {str(e)}",
                'agent_name': 'GoalPlannerADK',
                'customer_id': customer_id,
                'goal_id': goal_id,
                'timestamp': datetime.now().isoformat()
            }
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about this ADK agent."""
        return {
            'name': 'GoalPlannerADK',
            'description': 'ADK-based agent for financial goal planning and tracking',
            'version': '1.0.0',
            'capabilities': [
                'Goal feasibility assessment',
                'Savings plan creation',
                'Timeline recommendations',
                'Progress tracking',
                'Goal optimization suggestions'
            ],
            'model': 'gemini-1.5-flash',
            'framework': 'Google ADK'
        }


# Create a global instance for easy access
goal_planner_adk = GoalPlannerADK()
