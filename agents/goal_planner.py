"""
Goal Planner Agent for the Financial Advisor AI system.

This agent specializes in helping customers set realistic financial goals,
creating actionable plans, and tracking progress towards goal achievement.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal
import json

from .base_agent import BaseAgent, AgentResponse


class GoalPlannerAgent(BaseAgent):
    """
    Agent responsible for financial goal planning and tracking.
    
    Capabilities:
    - Analyze goal feasibility based on current financial situation
    - Create realistic timeline and savings plans
    - Suggest goal modifications for better achievability
    - Track progress and provide milestone recommendations
    """
    
    def __init__(self):
        super().__init__(
            agent_name="GoalPlannerAgent",
            agent_description="Plans and tracks financial goals based on spending patterns and income"
        )
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for goal planning."""
        return """
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
- Suggest goal modifications if original goal is unrealistic
- Use clear, motivational language

Output Format:
Provide your analysis in JSON format with the following structure:
{
    "goal_feasibility": "highly_feasible|feasible|challenging|unrealistic",
    "feasibility_confidence": 0.0-1.0,
    "recommended_timeline_months": integer,
    "monthly_savings_target": float,
    "weekly_savings_target": float,
    "goal_scenarios": {
        "conservative": {
            "timeline_months": integer,
            "monthly_target": float,
            "success_probability": 0.0-1.0
        },
        "moderate": {
            "timeline_months": integer,
            "monthly_target": float,
            "success_probability": 0.0-1.0
        },
        "stretch": {
            "timeline_months": integer,
            "monthly_target": float,
            "success_probability": 0.0-1.0
        }
    },
    "potential_obstacles": [
        {
            "obstacle": "description",
            "impact": "high|medium|low",
            "mitigation": "strategy to overcome"
        }
    ],
    "actionable_steps": [
        "specific step to take"
    ],
    "progress_milestones": [
        {
            "milestone": "description",
            "target_amount": float,
            "target_date": "YYYY-MM-DD"
        }
    ],
    "recommendations": [
        "specific recommendation"
    ],
    "confidence_score": 0.0-1.0
}
"""
    
    def process_request(self, customer_id: int, request_data: Dict[str, Any]) -> AgentResponse:
        """
        Process goal planning request.
        
        Args:
            customer_id: Customer ID
            request_data: Request data containing goal information
            
        Returns:
            AgentResponse with goal planning analysis
        """
        try:
            self.logger.info(f"Processing goal planning for customer {customer_id}")
            
            # Get customer context
            context = self.get_customer_context(customer_id)
            
            # Extract goal information from request
            goal_info = self._extract_goal_info(request_data)
            
            # Calculate financial capacity
            financial_capacity = self._calculate_financial_capacity(context)
            
            # Generate LLM analysis
            planning_prompt = self._create_planning_prompt(context, goal_info, financial_capacity)
            formatted_context = self._format_context_for_llm(context)
            
            llm_response = self.generate_llm_response(planning_prompt, formatted_context)
            
            # Parse LLM response
            planning_data = self._parse_llm_response(llm_response)
            
            # Calculate confidence score
            confidence = self._calculate_planning_confidence(context, goal_info, planning_data)
            
            # Store advice
            advice_content = self._format_advice_for_storage(planning_data, goal_info)
            self.store_advice(
                customer_id=customer_id,
                advice_type="goal_planning",
                content=advice_content,
                confidence_score=confidence
            )
            
            # Create response
            response = AgentResponse(
                agent_name=self.agent_name,
                response_type="goal_planning",
                data={
                    "goal_plan": planning_data,
                    "goal_info": goal_info,
                    "financial_capacity": financial_capacity,
                    "summary": f"Goal planning completed for {goal_info.get('title', 'financial goal')}"
                },
                confidence_score=confidence,
                reasoning=f"Analysis based on current savings capacity and {len(context.get('recent_transactions', []))} recent transactions",
                timestamp=datetime.utcnow(),
                recommendations=planning_data.get("recommendations", [])
            )
            
            self.logger.info(f"Goal planning completed for customer {customer_id}")
            return response
            
        except Exception as e:
            self.logger.error(f"Failed to process goal planning: {e}")
            raise
    
    def _extract_goal_info(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract goal information from request data."""
        # Check if we have existing goals from comprehensive analysis
        existing_goals = request_data.get("existing_goals", [])
        
        if existing_goals:
            # Use the first active goal, or create a summary if multiple goals
            if len(existing_goals) == 1:
                goal = existing_goals[0]
                return {
                    "title": goal.get("title", "Financial Goal"),
                    "target_amount": float(goal.get("target_amount", 0)),
                    "goal_type": goal.get("goal_type", "savings"),
                    "target_date": goal.get("target_date"),
                    "description": goal.get("description", ""),
                    "priority": "high",  # Existing goals are high priority
                    "current_amount": float(goal.get("current_amount", 0)),
                    "is_existing": True,
                    "existing_goals": existing_goals  # Include all for context
                }
            else:
                # Multiple goals - create a summary
                total_target = sum(float(g.get("target_amount", 0)) for g in existing_goals)
                total_current = sum(float(g.get("current_amount", 0)) for g in existing_goals)
                goal_types = list(set(g.get("goal_type", "savings") for g in existing_goals))
                
                return {
                    "title": f"Multiple Financial Goals ({len(existing_goals)} goals)",
                    "target_amount": total_target,
                    "goal_type": goal_types[0] if goal_types else "savings",
                    "target_date": None,  # Multiple dates, so no single target
                    "description": f"Analysis of {len(existing_goals)} active financial goals",
                    "priority": "high",
                    "current_amount": total_current,
                    "is_existing": True,
                    "existing_goals": existing_goals  # Include all for context
                }
        else:
            # New goal being planned
            return {
                "title": request_data.get("goal_title", "Financial Goal"),
                "target_amount": float(request_data.get("target_amount", 0)),
                "goal_type": request_data.get("goal_type", "savings"),
                "target_date": request_data.get("target_date"),
                "description": request_data.get("description", ""),
                "priority": request_data.get("priority", "medium"),
                "current_amount": 0.0,
                "is_existing": False,
                "existing_goals": []
            }
    
    def _calculate_financial_capacity(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate customer's financial capacity for goal achievement."""
        try:
            spending_analysis = context.get("spending_analysis", {})
            customer = context.get("customer", {})
            
            monthly_income = float(customer.get("income", 0)) / 12 if customer.get("income") else 0
            monthly_spending = spending_analysis.get("total_spending", 0)
            monthly_savings = spending_analysis.get("net_savings", 0)
            
            # Calculate savings rate
            savings_rate = (monthly_savings / monthly_income) if monthly_income > 0 else 0
            
            # Calculate available capacity (conservative estimate)
            # Assume customer can realistically save 10-20% more by optimizing spending
            potential_additional_savings = monthly_spending * 0.15  # 15% spending optimization
            total_savings_capacity = monthly_savings + potential_additional_savings
            
            # Calculate emergency fund requirement (3-6 months of expenses)
            emergency_fund_target = monthly_spending * 4
            existing_savings = 0  # Would need to be tracked separately
            
            return {
                "monthly_income": monthly_income,
                "monthly_spending": monthly_spending,
                "current_monthly_savings": monthly_savings,
                "savings_rate": savings_rate,
                "total_savings_capacity": total_savings_capacity,
                "emergency_fund_target": emergency_fund_target,
                "available_for_goals": max(0, total_savings_capacity - (emergency_fund_target * 0.1))  # Reserve 10% for emergency fund building
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating financial capacity: {e}")
            return {}
    
    def _create_planning_prompt(self, context: Dict[str, Any], goal_info: Dict[str, Any], 
                              financial_capacity: Dict[str, Any]) -> str:
        """Create planning prompt for LLM."""
        is_existing = goal_info.get('is_existing', False)
        existing_goals = goal_info.get('existing_goals', [])
        
        if is_existing and existing_goals:
            # Format existing goals information
            goals_details = ""
            for i, goal in enumerate(existing_goals, 1):
                current = float(goal.get('current_amount', 0))
                target = float(goal.get('target_amount', 0))
                progress = (current / target * 100) if target > 0 else 0
                goals_details += f"""
Goal {i}: {goal.get('title', 'Unnamed Goal')}
- Type: {goal.get('goal_type', 'Unknown')}
- Target: {self.format_currency(target)}
- Current: {self.format_currency(current)} ({progress:.1f}% complete)
- Target Date: {goal.get('target_date', 'Not specified')}
- Description: {goal.get('description', 'No description')}"""
            
            prompt = f"""
Analyze the existing financial goals for this customer and provide optimization recommendations:

EXISTING GOALS:{goals_details}

CURRENT FINANCIAL CAPACITY:
- Monthly Income: {self.format_currency(financial_capacity.get('monthly_income', 0))}
- Monthly Spending: {self.format_currency(financial_capacity.get('monthly_spending', 0))}
- Current Monthly Savings: {self.format_currency(financial_capacity.get('current_monthly_savings', 0))}
- Savings Rate: {financial_capacity.get('savings_rate', 0):.1%}
- Total Savings Capacity: {self.format_currency(financial_capacity.get('total_savings_capacity', 0))}
- Available for Goals: {self.format_currency(financial_capacity.get('available_for_goals', 0))}

Please analyze the feasibility of achieving these existing goals and provide recommendations for:
1. Optimizing progress toward current goals
2. Adjusting timelines if needed
3. Prioritizing goals if resources are limited
4. Identifying opportunities to accelerate progress

Focus on practical strategies to improve the customer's progress toward their existing financial goals.
Follow the JSON format specified in your system prompt.
"""
        else:
            # New goal planning
            prompt = f"""
Create a comprehensive financial goal plan for the following customer:

GOAL DETAILS:
- Goal: {goal_info.get('title', 'Unknown')}
- Target Amount: {self.format_currency(goal_info.get('target_amount', 0))}
- Goal Type: {goal_info.get('goal_type', 'Unknown')}
- Target Date: {goal_info.get('target_date', 'Not specified')}
- Priority: {goal_info.get('priority', 'Medium')}

FINANCIAL CAPACITY:
- Monthly Income: {self.format_currency(financial_capacity.get('monthly_income', 0))}
- Monthly Spending: {self.format_currency(financial_capacity.get('monthly_spending', 0))}
- Current Monthly Savings: {self.format_currency(financial_capacity.get('current_monthly_savings', 0))}
- Savings Rate: {financial_capacity.get('savings_rate', 0):.1%}
- Total Savings Capacity: {self.format_currency(financial_capacity.get('total_savings_capacity', 0))}
- Available for Goals: {self.format_currency(financial_capacity.get('available_for_goals', 0))}

Please analyze the goal feasibility and create a detailed plan following the JSON format specified in your system prompt.
Consider the customer's current financial situation and provide realistic timelines and strategies.
"""
        
        return prompt
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured data."""
        try:
            # Try to extract JSON from response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # Fallback: create basic structured response
                return {
                    "goal_feasibility": "feasible",
                    "feasibility_confidence": 0.7,
                    "recommended_timeline_months": 24,
                    "monthly_savings_target": 0,
                    "weekly_savings_target": 0,
                    "goal_scenarios": {
                        "conservative": {"timeline_months": 36, "monthly_target": 0, "success_probability": 0.8},
                        "moderate": {"timeline_months": 24, "monthly_target": 0, "success_probability": 0.6},
                        "stretch": {"timeline_months": 12, "monthly_target": 0, "success_probability": 0.3}
                    },
                    "potential_obstacles": [],
                    "actionable_steps": ["Create a monthly savings plan", "Track progress regularly"],
                    "progress_milestones": [],
                    "recommendations": ["Start saving immediately", "Review and adjust plan quarterly"],
                    "confidence_score": 0.7
                }
                
        except json.JSONDecodeError as e:
            self.logger.warning(f"Failed to parse LLM JSON response: {e}")
            return {
                "goal_feasibility": "feasible",
                "feasibility_confidence": 0.6,
                "recommended_timeline_months": 24,
                "monthly_savings_target": 0,
                "weekly_savings_target": 0,
                "goal_scenarios": {},
                "potential_obstacles": [],
                "actionable_steps": ["Review goal planning"],
                "progress_milestones": [],
                "recommendations": ["Consult with a financial advisor"],
                "confidence_score": 0.6
            }
    
    def _calculate_planning_confidence(self, context: Dict[str, Any], goal_info: Dict[str, Any], 
                                     planning_data: Dict[str, Any]) -> float:
        """Calculate confidence score for the goal plan."""
        try:
            # Base confidence on data quality
            transactions = context.get("recent_transactions", [])
            data_quality = min(1.0, len(transactions) / 30)  # More transactions = better data
            
            # Consider goal specificity
            goal_specificity = 0.5
            if goal_info.get("target_amount", 0) > 0:
                goal_specificity += 0.2
            if goal_info.get("target_date"):
                goal_specificity += 0.2
            if goal_info.get("goal_type") != "unknown":
                goal_specificity += 0.1
            
            # Use base agent's confidence calculation
            analysis_complexity = 0.6  # Goal planning is moderately complex
            base_confidence = self.calculate_confidence_score(data_quality, analysis_complexity)
            
            # Adjust based on LLM confidence and goal specificity
            llm_confidence = planning_data.get("confidence_score", base_confidence)
            
            # Weighted average
            final_confidence = (base_confidence * 0.4) + (llm_confidence * 0.4) + (goal_specificity * 0.2)
            
            return round(final_confidence, 2)
            
        except Exception as e:
            self.logger.error(f"Error calculating planning confidence: {e}")
            return 0.7
    
    def _format_advice_for_storage(self, planning_data: Dict[str, Any], goal_info: Dict[str, Any]) -> str:
        """Format goal plan for storage in advice table."""
        try:
            advice_text = f"GOAL PLANNING SUMMARY:\n\n"
            advice_text += f"Goal: {goal_info.get('title', 'Financial Goal')}\n"
            advice_text += f"Target Amount: {self.format_currency(goal_info.get('target_amount', 0))}\n"
            advice_text += f"Feasibility: {planning_data.get('goal_feasibility', 'Unknown').replace('_', ' ').title()}\n\n"
            
            timeline = planning_data.get('recommended_timeline_months', 0)
            if timeline > 0:
                advice_text += f"Recommended Timeline: {timeline} months\n"
                
            monthly_target = planning_data.get('monthly_savings_target', 0)
            if monthly_target > 0:
                advice_text += f"Monthly Savings Target: {self.format_currency(monthly_target)}\n\n"
            
            if planning_data.get("actionable_steps"):
                advice_text += "Action Steps:\n"
                for i, step in enumerate(planning_data["actionable_steps"], 1):
                    advice_text += f"{i}. {step}\n"
                advice_text += "\n"
            
            if planning_data.get("recommendations"):
                advice_text += "Recommendations:\n"
                for i, rec in enumerate(planning_data["recommendations"], 1):
                    advice_text += f"{i}. {rec}\n"
            
            return advice_text
            
        except Exception as e:
            self.logger.error(f"Error formatting advice: {e}")
            return "Goal planning completed. Please review your financial plan."
    
    def create_goal_from_plan(self, customer_id: int, planning_data: Dict[str, Any], 
                            goal_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a goal in the database based on the planning analysis."""
        try:
            # Calculate target date if not provided
            target_date = goal_info.get("target_date")
            if not target_date and planning_data.get("recommended_timeline_months"):
                months = planning_data["recommended_timeline_months"]
                target_date = (datetime.now() + timedelta(days=months * 30)).date()
            
            # Create goal via MCP server
            goal_response = self.mcp.create_financial_goal(
                customer_id=customer_id,
                title=goal_info.get("title", "Financial Goal"),
                goal_type=goal_info.get("goal_type", "savings"),
                target_amount=Decimal(str(goal_info.get("target_amount", 0))),
                description=goal_info.get("description"),
                target_date=target_date
            )
            
            self.logger.info(f"Created goal {goal_response.id} for customer {customer_id}")
            return goal_response.model_dump()
            
        except Exception as e:
            self.logger.error(f"Failed to create goal: {e}")
            return None
    
    def track_goal_progress(self, customer_id: int, goal_id: int) -> Dict[str, Any]:
        """Track progress towards a specific goal."""
        try:
            # Get current customer context
            context = self.get_customer_context(customer_id)
            goals = context.get("active_goals", [])
            
            # Find the specific goal
            target_goal = None
            for goal in goals:
                if goal.get("id") == goal_id:
                    target_goal = goal
                    break
            
            if not target_goal:
                raise ValueError(f"Goal {goal_id} not found for customer {customer_id}")
            
            # Calculate progress metrics
            current_amount = float(target_goal.get("current_amount", 0))
            target_amount = float(target_goal.get("target_amount", 1))
            progress_percentage = (current_amount / target_amount) * 100
            
            remaining_amount = target_amount - current_amount
            
            # Calculate time-based progress
            target_date = target_goal.get("target_date")
            if target_date:
                # Simple date calculation
                today = datetime.now().date()
                # Assuming target_date is a string in YYYY-MM-DD format
                target_dt = datetime.strptime(target_date, "%Y-%m-%d").date() if isinstance(target_date, str) else target_date
                days_remaining = (target_dt - today).days
                months_remaining = max(1, days_remaining / 30)
                
                required_monthly_savings = remaining_amount / months_remaining
            else:
                days_remaining = None
                months_remaining = None
                required_monthly_savings = 0
            
            # Get current savings rate
            financial_capacity = self._calculate_financial_capacity(context)
            current_monthly_savings = financial_capacity.get("current_monthly_savings", 0)
            
            return {
                "goal_id": goal_id,
                "goal_title": target_goal.get("title"),
                "current_amount": current_amount,
                "target_amount": target_amount,
                "progress_percentage": round(progress_percentage, 1),
                "remaining_amount": remaining_amount,
                "days_remaining": days_remaining,
                "months_remaining": round(months_remaining, 1) if months_remaining else None,
                "required_monthly_savings": round(required_monthly_savings, 2),
                "current_monthly_savings": current_monthly_savings,
                "is_on_track": current_monthly_savings >= required_monthly_savings if required_monthly_savings > 0 else True,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to track goal progress: {e}")
            raise


# Global instance
goal_planner = GoalPlannerAgent()
