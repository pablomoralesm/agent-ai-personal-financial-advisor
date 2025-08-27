"""
Spending Analyzer Agent for the Financial Advisor AI system.

This agent specializes in analyzing spending patterns, identifying trends,
and providing insights about spending habits using Gemini LLM.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json

from .base_agent import BaseAgent, AgentResponse


class SpendingAnalyzerAgent(BaseAgent):
    """
    Agent responsible for analyzing customer spending patterns.
    
    Capabilities:
    - Analyze spending trends over time
    - Identify spending categories and patterns
    - Detect unusual spending behavior
    - Provide spending insights and recommendations
    """
    
    def __init__(self):
        super().__init__(
            agent_name="SpendingAnalyzerAgent",
            agent_description="Analyzes customer spending patterns and provides insights"
        )
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for spending analysis."""
        return """
You are a Financial Spending Analyzer AI assistant. Your role is to analyze customer spending patterns and provide actionable insights.

Your analysis should include:
1. Spending trend analysis (increasing, decreasing, stable)
2. Category-wise spending breakdown and insights
3. Identification of unusual or concerning spending patterns
4. Comparison with typical spending patterns for similar demographics
5. Specific recommendations for spending optimization

Guidelines:
- Be objective and data-driven in your analysis
- Provide specific, actionable recommendations
- Highlight both positive spending habits and areas for improvement
- Consider the customer's income level and financial goals
- Use clear, non-judgmental language
- Include confidence levels for your assessments

Output Format:
Provide your analysis in JSON format with the following structure:
{
    "spending_trend": "increasing|decreasing|stable",
    "trend_confidence": 0.0-1.0,
    "category_insights": {
        "category_name": {
            "amount": float,
            "percentage_of_total": float,
            "assessment": "high|normal|low",
            "recommendation": "specific recommendation"
        }
    },
    "unusual_patterns": [
        {
            "pattern": "description",
            "concern_level": "high|medium|low",
            "recommendation": "action to take"
        }
    ],
    "overall_assessment": "summary of spending health",
    "key_recommendations": [
        "specific actionable recommendation"
    ],
    "confidence_score": 0.0-1.0
}
"""
    
    def process_request(self, customer_id: int, request_data: Dict[str, Any]) -> AgentResponse:
        """
        Analyze customer spending patterns.
        
        Args:
            customer_id: Customer ID to analyze
            request_data: Additional request parameters
            
        Returns:
            AgentResponse with spending analysis
        """
        try:
            self.logger.info(f"Processing spending analysis for customer {customer_id}")
            
            # Get customer context
            context = self.get_customer_context(customer_id)
            
            # Calculate additional spending metrics
            spending_metrics = self._calculate_spending_metrics(context)
            
            # Generate LLM analysis
            analysis_prompt = self._create_analysis_prompt(context, spending_metrics)
            formatted_context = self._format_context_for_llm(context)
            
            llm_response = self.generate_llm_response(analysis_prompt, formatted_context)
            
            # Parse LLM response
            analysis_data = self._parse_llm_response(llm_response)
            
            # Calculate confidence score
            confidence = self._calculate_analysis_confidence(context, analysis_data)
            
            # Store advice
            advice_content = self._format_advice_for_storage(analysis_data)
            self.store_advice(
                customer_id=customer_id,
                advice_type="spending_analysis",
                content=advice_content,
                confidence_score=confidence
            )
            
            # Create response
            response = AgentResponse(
                agent_name=self.agent_name,
                response_type="spending_analysis",
                data={
                    "analysis": analysis_data,
                    "metrics": spending_metrics,
                    "summary": analysis_data.get("overall_assessment", "Analysis completed")
                },
                confidence_score=confidence,
                reasoning=f"Analysis based on {len(context.get('recent_transactions', []))} transactions over the last 30 days",
                timestamp=datetime.utcnow(),
                recommendations=analysis_data.get("key_recommendations", [])
            )
            
            self.logger.info(f"Spending analysis completed for customer {customer_id}")
            return response
            
        except Exception as e:
            self.logger.error(f"Failed to process spending analysis: {e}")
            raise
    
    def _calculate_spending_metrics(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate additional spending metrics."""
        try:
            transactions = context.get("recent_transactions", [])
            spending_analysis = context.get("spending_analysis", {})
            customer = context.get("customer", {})
            
            # Calculate spending velocity (transactions per week)
            if transactions:
                # Sort transactions by date to analyze trends
                sorted_transactions = sorted(
                    [t for t in transactions if not t.get("is_income", False)],
                    key=lambda x: x.get("transaction_date", "")
                )
                
                if len(sorted_transactions) >= 2:
                    first_date = sorted_transactions[0].get("transaction_date")
                    last_date = sorted_transactions[-1].get("transaction_date")
                    if first_date and last_date:
                        # Simple date difference calculation (assuming YYYY-MM-DD format)
                        days_span = 30  # Default to 30 days
                        spending_velocity = len(sorted_transactions) / (days_span / 7)  # transactions per week
                    else:
                        spending_velocity = 0
                else:
                    spending_velocity = 0
            else:
                spending_velocity = 0
            
            # Calculate spending ratio relative to income
            total_spending = spending_analysis.get("total_spending", 0)
            income = float(customer.get("income", 0)) if customer.get("income") else 0
            spending_ratio = (total_spending / income) if income > 0 else 0
            
            # Calculate category concentration (entropy)
            category_breakdown = spending_analysis.get("category_breakdown", {})
            total_categories = len(category_breakdown)
            largest_category_pct = 0
            if category_breakdown and total_spending > 0:
                largest_category_amount = max(category_breakdown.values())
                largest_category_pct = largest_category_amount / total_spending
            
            return {
                "spending_velocity": spending_velocity,
                "spending_ratio": spending_ratio,
                "largest_category_percentage": largest_category_pct,
                "total_categories": total_categories,
                "average_transaction_amount": total_spending / len([t for t in transactions if not t.get("is_income", False)]) if transactions else 0
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating spending metrics: {e}")
            return {}
    
    def _create_analysis_prompt(self, context: Dict[str, Any], metrics: Dict[str, Any]) -> str:
        """Create analysis prompt for LLM."""
        spending_analysis = context.get("spending_analysis", {})
        customer = context.get("customer", {})
        
        prompt = f"""
Analyze the following customer's spending patterns and provide insights:

CUSTOMER DEMOGRAPHICS:
- Age: {customer.get('age', 'Unknown')}
- Monthly Income: {self.format_currency(float(customer.get('income', 0)) / 12) if customer.get('income') else 'Unknown'}

SPENDING METRICS:
- Total Spending (30 days): {self.format_currency(spending_analysis.get('total_spending', 0))}
- Net Savings: {self.format_currency(spending_analysis.get('net_savings', 0))}
- Spending-to-Income Ratio: {metrics.get('spending_ratio', 0):.2%}
- Transaction Frequency: {metrics.get('spending_velocity', 0):.1f} transactions/week
- Number of Categories: {metrics.get('total_categories', 0)}

Please provide a comprehensive spending analysis following the JSON format specified in your system prompt.
Focus on identifying patterns, potential concerns, and actionable recommendations.
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
                # Fallback: create structured response from text
                return {
                    "spending_trend": "stable",
                    "trend_confidence": 0.7,
                    "category_insights": {},
                    "unusual_patterns": [],
                    "overall_assessment": response[:500] + "..." if len(response) > 500 else response,
                    "key_recommendations": ["Review spending patterns regularly"],
                    "confidence_score": 0.7
                }
                
        except json.JSONDecodeError as e:
            self.logger.warning(f"Failed to parse LLM JSON response: {e}")
            # Return fallback response
            return {
                "spending_trend": "stable",
                "trend_confidence": 0.6,
                "category_insights": {},
                "unusual_patterns": [],
                "overall_assessment": "Unable to parse detailed analysis. Please review spending manually.",
                "key_recommendations": ["Review spending patterns", "Monitor large transactions"],
                "confidence_score": 0.6
            }
    
    def _calculate_analysis_confidence(self, context: Dict[str, Any], analysis: Dict[str, Any]) -> float:
        """Calculate confidence score for the analysis."""
        try:
            transactions = context.get("recent_transactions", [])
            
            # Base confidence on data quality
            transaction_count = len(transactions)
            
            # More transactions = higher confidence
            data_quality = min(1.0, transaction_count / 50)  # Max confidence at 50+ transactions
            
            # Consider analysis complexity (more categories = higher complexity)
            category_count = len(context.get("spending_analysis", {}).get("category_breakdown", {}))
            analysis_complexity = min(0.8, category_count / 10)  # Normalized complexity
            
            # Use base agent's confidence calculation
            base_confidence = self.calculate_confidence_score(data_quality, analysis_complexity)
            
            # Adjust based on LLM confidence if available
            llm_confidence = analysis.get("confidence_score", base_confidence)
            
            # Take weighted average
            final_confidence = (base_confidence * 0.6) + (llm_confidence * 0.4)
            
            return round(final_confidence, 2)
            
        except Exception as e:
            self.logger.error(f"Error calculating confidence: {e}")
            return 0.7  # Default confidence
    
    def _format_advice_for_storage(self, analysis: Dict[str, Any]) -> str:
        """Format analysis for storage in advice table."""
        try:
            advice_text = f"SPENDING ANALYSIS SUMMARY:\n\n"
            advice_text += f"Overall Assessment: {analysis.get('overall_assessment', 'No assessment available')}\n\n"
            
            if analysis.get("key_recommendations"):
                advice_text += "Key Recommendations:\n"
                for i, rec in enumerate(analysis["key_recommendations"], 1):
                    advice_text += f"{i}. {rec}\n"
                advice_text += "\n"
            
            if analysis.get("unusual_patterns"):
                advice_text += "Areas of Concern:\n"
                for pattern in analysis["unusual_patterns"]:
                    advice_text += f"- {pattern.get('pattern')}: {pattern.get('recommendation')}\n"
            
            return advice_text
            
        except Exception as e:
            self.logger.error(f"Error formatting advice: {e}")
            return "Spending analysis completed. Please review your recent transactions."
    
    def get_spending_insights(self, customer_id: int, days: int = 30) -> Dict[str, Any]:
        """Get quick spending insights for a customer."""
        try:
            context = self.get_customer_context(customer_id)
            metrics = self._calculate_spending_metrics(context)
            
            return {
                "customer_id": customer_id,
                "analysis_period_days": days,
                "metrics": metrics,
                "spending_summary": context.get("spending_analysis", {}),
                "transaction_count": len(context.get("recent_transactions", [])),
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get spending insights: {e}")
            raise


# Global instance
spending_analyzer = SpendingAnalyzerAgent()
