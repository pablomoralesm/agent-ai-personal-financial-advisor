"""
Advisor Agent for the Financial Advisor AI system.

This agent synthesizes inputs from other agents and provides final
comprehensive financial recommendations and action plans.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from .base_agent import BaseAgent, AgentResponse, AgentMessage


class AdvisorAgent(BaseAgent):
    """
    Agent responsible for providing comprehensive financial advice.
    
    Capabilities:
    - Synthesize inputs from SpendingAnalyzerAgent and GoalPlannerAgent
    - Provide prioritized financial recommendations
    - Create comprehensive action plans
    - Offer personalized financial guidance
    """
    
    def __init__(self):
        super().__init__(
            agent_name="AdvisorAgent",
            agent_description="Provides comprehensive financial advice by synthesizing analysis from other agents"
        )
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for financial advising."""
        return """
You are a Comprehensive Financial Advisor AI assistant. Your role is to synthesize spending analysis and goal planning data to provide holistic financial advice.

Your advice should include:
1. Overall financial health assessment
2. Prioritized action plan with specific steps
3. Short-term and long-term recommendations
4. Risk assessment and mitigation strategies
5. Behavioral insights and motivation strategies
6. Follow-up schedule and monitoring plan

Guidelines:
- Provide actionable, specific advice
- Consider the customer's complete financial picture
- Prioritize recommendations by impact and feasibility
- Be encouraging while being realistic
- Address both immediate concerns and long-term planning
- Include specific timeframes and measurable goals
- Consider behavioral psychology in recommendations

Output Format:
Provide your advice in JSON format with the following structure:
{
    "financial_health_score": 0-100,
    "health_assessment": "poor|fair|good|excellent",
    "priority_actions": [
        {
            "action": "specific action to take",
            "priority": "high|medium|low",
            "timeframe": "immediate|1-month|3-months|6-months",
            "expected_impact": "description of impact",
            "difficulty": "easy|moderate|challenging"
        }
    ],
    "spending_recommendations": [
        {
            "category": "spending category",
            "recommendation": "specific recommendation",
            "potential_savings": float,
            "implementation_tips": ["tip1", "tip2"]
        }
    ],
    "goal_recommendations": [
        {
            "goal_type": "goal type",
            "recommendation": "specific recommendation",
            "rationale": "why this is important",
            "next_steps": ["step1", "step2"]
        }
    ],
    "risk_factors": [
        {
            "risk": "description of risk",
            "severity": "high|medium|low",
            "mitigation": "how to address this risk"
        }
    ],
    "motivational_insights": [
        "insight or encouragement"
    ],
    "follow_up_plan": {
        "check_in_frequency": "weekly|monthly|quarterly",
        "key_metrics_to_track": ["metric1", "metric2"],
        "milestone_dates": ["date1", "date2"]
    },
    "overall_summary": "comprehensive summary of advice",
    "confidence_score": 0.0-1.0
}
"""
    
    def process_request(self, customer_id: int, request_data: Dict[str, Any]) -> AgentResponse:
        """
        Process comprehensive financial advisory request.
        
        Args:
            customer_id: Customer ID
            request_data: Request data, may include analysis from other agents
            
        Returns:
            AgentResponse with comprehensive financial advice
        """
        try:
            self.logger.info(f"Processing comprehensive advice for customer {customer_id}")
            
            # Get customer context
            context = self.get_customer_context(customer_id)
            
            # Get analysis from other agents if available
            spending_analysis = request_data.get("spending_analysis")
            goal_planning = request_data.get("goal_planning")
            
            # If no agent analysis provided, get recent advice from database
            if not spending_analysis or not goal_planning:
                recent_advice = self.mcp.get_advice_history(customer_id)
                
                if not spending_analysis:
                    spending_advice = [a for a in recent_advice if a.advice_type == "spending_analysis"]
                    spending_analysis = spending_advice[0].model_dump() if spending_advice else None
                
                if not goal_planning:
                    goal_advice = [a for a in recent_advice if a.advice_type == "goal_planning"]
                    goal_planning = goal_advice[0].model_dump() if goal_advice else None
            
            # Calculate financial health metrics
            health_metrics = self._calculate_financial_health(context)
            
            # Generate comprehensive advice
            advice_prompt = self._create_advice_prompt(context, spending_analysis, goal_planning, health_metrics)
            formatted_context = self._format_context_for_llm(context)
            
            llm_response = self.generate_llm_response(advice_prompt, formatted_context)
            
            # Parse LLM response
            advice_data = self._parse_llm_response(llm_response)
            
            # Calculate confidence score
            confidence = self._calculate_advice_confidence(context, advice_data)
            
            # Store advice
            advice_content = self._format_advice_for_storage(advice_data)
            self.store_advice(
                customer_id=customer_id,
                advice_type="comprehensive_advice",
                content=advice_content,
                confidence_score=confidence
            )
            
            # Create response
            response = AgentResponse(
                agent_name=self.agent_name,
                response_type="comprehensive_advice",
                data={
                    "advice": advice_data,
                    "health_metrics": health_metrics,
                    "summary": advice_data.get("overall_summary", "Comprehensive financial advice provided"),
                    "health_score": advice_data.get("financial_health_score", 70)
                },
                confidence_score=confidence,
                reasoning="Analysis based on spending patterns, goal feasibility, and overall financial health",
                timestamp=datetime.utcnow(),
                recommendations=self._extract_key_recommendations(advice_data)
            )
            
            self.logger.info(f"Comprehensive advice completed for customer {customer_id}")
            return response
            
        except Exception as e:
            self.logger.error(f"Failed to process comprehensive advice: {e}")
            raise
    
    def _calculate_financial_health(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall financial health metrics."""
        try:
            spending_analysis = context.get("spending_analysis", {})
            customer = context.get("customer", {})
            goals = context.get("active_goals", [])
            
            # Income and spending metrics
            monthly_income = float(customer.get("income", 0)) / 12 if customer.get("income") else 0
            monthly_spending = spending_analysis.get("total_spending", 0)
            monthly_savings = spending_analysis.get("net_savings", 0)
            
            # Calculate key ratios
            savings_rate = (monthly_savings / monthly_income) if monthly_income > 0 else 0
            spending_ratio = (monthly_spending / monthly_income) if monthly_income > 0 else 1
            
            # Emergency fund assessment (assume 3-6 months expenses needed)
            emergency_fund_needed = monthly_spending * 4
            emergency_fund_ratio = 0.5  # Assume 50% coverage for demo
            
            # Goal progress assessment
            goal_progress_scores = []
            for goal in goals:
                current = float(goal.get("current_amount", 0))
                target = float(goal.get("target_amount", 1))
                progress = current / target
                goal_progress_scores.append(progress)
            
            avg_goal_progress = sum(goal_progress_scores) / len(goal_progress_scores) if goal_progress_scores else 0
            
            # Calculate overall health score (0-100)
            health_score = 0
            
            # Savings rate component (30 points max)
            if savings_rate >= 0.2:  # 20% or more
                health_score += 30
            elif savings_rate >= 0.1:  # 10-20%
                health_score += 20
            elif savings_rate >= 0.05:  # 5-10%
                health_score += 10
            
            # Spending control component (25 points max)
            if spending_ratio <= 0.7:  # Spending 70% or less of income
                health_score += 25
            elif spending_ratio <= 0.85:  # 70-85%
                health_score += 15
            elif spending_ratio <= 1.0:  # 85-100%
                health_score += 5
            
            # Emergency fund component (25 points max)
            health_score += min(25, emergency_fund_ratio * 25)
            
            # Goal progress component (20 points max)
            health_score += min(20, avg_goal_progress * 20)
            
            # Determine health assessment
            if health_score >= 80:
                health_assessment = "excellent"
            elif health_score >= 65:
                health_assessment = "good"
            elif health_score >= 45:
                health_assessment = "fair"
            else:
                health_assessment = "poor"
            
            return {
                "health_score": round(health_score),
                "health_assessment": health_assessment,
                "savings_rate": round(savings_rate, 3),
                "spending_ratio": round(spending_ratio, 3),
                "emergency_fund_ratio": round(emergency_fund_ratio, 3),
                "avg_goal_progress": round(avg_goal_progress, 3),
                "monthly_income": monthly_income,
                "monthly_spending": monthly_spending,
                "monthly_savings": monthly_savings
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating financial health: {e}")
            return {"health_score": 50, "health_assessment": "fair"}
    
    def _create_advice_prompt(self, context: Dict[str, Any], spending_analysis: Optional[Dict[str, Any]], 
                            goal_planning: Optional[Dict[str, Any]], health_metrics: Dict[str, Any]) -> str:
        """Create comprehensive advice prompt for LLM."""
        prompt = f"""
Provide comprehensive financial advice for a customer based on the following information:

FINANCIAL HEALTH METRICS:
- Overall Health Score: {health_metrics.get('health_score', 50)}/100
- Health Assessment: {health_metrics.get('health_assessment', 'Unknown')}
- Savings Rate: {health_metrics.get('savings_rate', 0):.1%}
- Spending Ratio: {health_metrics.get('spending_ratio', 0):.1%}
- Monthly Income: {self.format_currency(health_metrics.get('monthly_income', 0))}
- Monthly Spending: {self.format_currency(health_metrics.get('monthly_spending', 0))}
- Monthly Savings: {self.format_currency(health_metrics.get('monthly_savings', 0))}

SPENDING ANALYSIS SUMMARY:
"""
        
        if spending_analysis:
            if isinstance(spending_analysis, dict) and "content" in spending_analysis:
                # This is advice from database
                prompt += f"{spending_analysis.get('content', 'No spending analysis available')}\n"
            else:
                # This is direct analysis data
                prompt += f"Analysis available with recommendations\n"
        else:
            prompt += "No recent spending analysis available\n"
        
        prompt += "\nGOAL PLANNING SUMMARY:\n"
        if goal_planning:
            if isinstance(goal_planning, dict) and "content" in goal_planning:
                # This is advice from database
                prompt += f"{goal_planning.get('content', 'No goal planning available')}\n"
            else:
                # This is direct planning data
                prompt += f"Goal planning available with timeline recommendations\n"
        else:
            prompt += "No recent goal planning available\n"
        
        prompt += f"""
Please provide comprehensive financial advice following the JSON format specified in your system prompt.
Focus on creating an actionable plan that addresses the customer's current financial situation.
Consider both immediate needs and long-term financial goals.
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
                    "financial_health_score": 70,
                    "health_assessment": "fair",
                    "priority_actions": [
                        {
                            "action": "Review and optimize monthly spending",
                            "priority": "high",
                            "timeframe": "1-month",
                            "expected_impact": "Improved savings rate",
                            "difficulty": "moderate"
                        }
                    ],
                    "spending_recommendations": [],
                    "goal_recommendations": [],
                    "risk_factors": [],
                    "motivational_insights": ["Small consistent changes lead to significant improvements"],
                    "follow_up_plan": {
                        "check_in_frequency": "monthly",
                        "key_metrics_to_track": ["spending", "savings"],
                        "milestone_dates": []
                    },
                    "overall_summary": "Continue working on improving your financial habits through consistent spending tracking and goal setting.",
                    "confidence_score": 0.7
                }
                
        except json.JSONDecodeError as e:
            self.logger.warning(f"Failed to parse LLM JSON response: {e}")
            return {
                "financial_health_score": 65,
                "health_assessment": "fair",
                "priority_actions": [],
                "spending_recommendations": [],
                "goal_recommendations": [],
                "risk_factors": [],
                "motivational_insights": [],
                "follow_up_plan": {"check_in_frequency": "monthly", "key_metrics_to_track": [], "milestone_dates": []},
                "overall_summary": "Please review your financial situation and consider consulting with a financial advisor.",
                "confidence_score": 0.6
            }
    
    def _calculate_advice_confidence(self, context: Dict[str, Any], advice_data: Dict[str, Any]) -> float:
        """Calculate confidence score for the advice."""
        try:
            # Base confidence on data completeness
            transactions = context.get("recent_transactions", [])
            goals = context.get("active_goals", [])
            
            data_quality = 0.0
            
            # Transaction data quality
            if len(transactions) >= 20:
                data_quality += 0.4
            elif len(transactions) >= 10:
                data_quality += 0.3
            elif len(transactions) >= 5:
                data_quality += 0.2
            
            # Goal data quality
            if len(goals) >= 2:
                data_quality += 0.3
            elif len(goals) >= 1:
                data_quality += 0.2
            
            # Customer profile completeness
            customer = context.get("customer", {})
            if customer.get("income"):
                data_quality += 0.2
            if customer.get("age"):
                data_quality += 0.1
            
            # LLM confidence
            llm_confidence = advice_data.get("confidence_score", 0.7)
            
            # Final confidence is weighted average
            final_confidence = (data_quality * 0.6) + (llm_confidence * 0.4)
            
            return round(final_confidence, 2)
            
        except Exception as e:
            self.logger.error(f"Error calculating advice confidence: {e}")
            return 0.7
    
    def _format_advice_for_storage(self, advice_data: Dict[str, Any]) -> str:
        """Format advice for storage in advice table."""
        try:
            advice_text = f"COMPREHENSIVE FINANCIAL ADVICE:\n\n"
            
            # Health assessment
            health_score = advice_data.get("financial_health_score", 0)
            health_assessment = advice_data.get("health_assessment", "Unknown")
            advice_text += f"Financial Health: {health_score}/100 ({health_assessment.title()})\n\n"
            
            # Priority actions
            priority_actions = advice_data.get("priority_actions", [])
            if priority_actions:
                advice_text += "PRIORITY ACTIONS:\n"
                for i, action in enumerate(priority_actions[:5], 1):  # Top 5 actions
                    advice_text += f"{i}. {action.get('action')} (Priority: {action.get('priority')}, Timeframe: {action.get('timeframe')})\n"
                advice_text += "\n"
            
            # Spending recommendations
            spending_recs = advice_data.get("spending_recommendations", [])
            if spending_recs:
                advice_text += "SPENDING RECOMMENDATIONS:\n"
                for rec in spending_recs[:3]:  # Top 3 recommendations
                    advice_text += f"- {rec.get('category')}: {rec.get('recommendation')}\n"
                advice_text += "\n"
            
            # Goal recommendations
            goal_recs = advice_data.get("goal_recommendations", [])
            if goal_recs:
                advice_text += "GOAL RECOMMENDATIONS:\n"
                for rec in goal_recs[:3]:  # Top 3 recommendations
                    advice_text += f"- {rec.get('goal_type')}: {rec.get('recommendation')}\n"
                advice_text += "\n"
            
            # Overall summary
            summary = advice_data.get("overall_summary", "")
            if summary:
                advice_text += f"SUMMARY:\n{summary}\n"
            
            return advice_text
            
        except Exception as e:
            self.logger.error(f"Error formatting advice: {e}")
            return "Comprehensive financial advice completed. Please review your financial plan regularly."
    
    def _extract_key_recommendations(self, advice_data: Dict[str, Any]) -> List[str]:
        """Extract key recommendations for the response."""
        try:
            recommendations = []
            
            # Add priority actions
            priority_actions = advice_data.get("priority_actions", [])
            for action in priority_actions[:3]:  # Top 3 priority actions
                recommendations.append(action.get("action", ""))
            
            # Add motivational insights
            insights = advice_data.get("motivational_insights", [])
            recommendations.extend(insights[:2])  # Top 2 insights
            
            return [rec for rec in recommendations if rec]  # Filter out empty strings
            
        except Exception as e:
            self.logger.error(f"Error extracting recommendations: {e}")
            return ["Review your financial plan regularly"]
    
    def handle_agent_message(self, message: AgentMessage) -> Optional[AgentResponse]:
        """Handle messages from other agents for A2A collaboration."""
        try:
            self.logger.info(f"Received A2A message from {message.sender}: {message.message_type}")
            
            if message.message_type == "analysis_complete":
                # Another agent completed analysis - we can use this for comprehensive advice
                customer_id = message.content.get("customer_id")
                if customer_id:
                    # Prepare request data with the other agent's analysis
                    request_data = {
                        f"{message.sender.lower()}_analysis": message.content.get("analysis_data")
                    }
                    return self.process_request(customer_id, request_data)
            
            elif message.message_type == "request_synthesis":
                # Explicit request for synthesis
                customer_id = message.content.get("customer_id")
                spending_analysis = message.content.get("spending_analysis")
                goal_planning = message.content.get("goal_planning")
                
                if customer_id:
                    request_data = {
                        "spending_analysis": spending_analysis,
                        "goal_planning": goal_planning
                    }
                    return self.process_request(customer_id, request_data)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error handling agent message: {e}")
            return None


# Global instance
advisor_agent = AdvisorAgent()
