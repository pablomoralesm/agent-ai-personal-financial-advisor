"""
ADK-based Spending Analyzer Agent for the Financial Advisor AI system.

This agent uses Google's Agent Development Kit (ADK) to analyze spending patterns,
identify trends, and provide insights about spending habits using Gemini LLM.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json

from google.adk import Agent
from financial_mcp.server import mcp_server
from financial_mcp.models import TransactionCategory


class SpendingAnalysisToolset:
    """Custom tool for spending analysis data retrieval."""
    
    @staticmethod
    def get_customer_transactions(customer_id: int, days: int = 90) -> Dict[str, Any]:
        """
        Retrieve customer transactions for analysis.
        
        Args:
            customer_id: ID of the customer
            days: Number of days to look back (default: 90)
            
        Returns:
            Dictionary containing transaction data and summary statistics
        """
        try:
            # Calculate date range
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)
            
            # Get transactions from database
            transactions = mcp_server.get_customer_transactions(customer_id)
            
            # Calculate summary statistics
            total_income = sum(t.amount for t in transactions if t.amount > 0)
            total_expenses = abs(sum(t.amount for t in transactions if t.amount < 0))
            
            # Category breakdown
            category_breakdown = {}
            for t in transactions:
                if t.amount < 0:  # Only expenses
                    category = t.category.value
                    category_breakdown[category] = category_breakdown.get(category, 0) + abs(t.amount)
            
            # Convert transactions to serializable format
            transaction_data = []
            for t in transactions:
                transaction_data.append({
                    'id': t.id,
                    'amount': float(t.amount),
                    'category': t.category.value,
                    'description': t.description,
                    'date': t.date.isoformat(),
                    'created_at': t.created_at.isoformat()
                })
            
            return {
                'transactions': transaction_data,
                'summary': {
                    'total_income': float(total_income),
                    'total_expenses': float(total_expenses),
                    'net_cash_flow': float(total_income - total_expenses),
                    'transaction_count': len(transactions),
                    'date_range': {
                        'start': start_date.isoformat(),
                        'end': end_date.isoformat(),
                        'days': days
                    },
                    'category_breakdown': {k: float(v) for k, v in category_breakdown.items()}
                }
            }
        except Exception as e:
            return {'error': f"Failed to retrieve transaction data: {str(e)}"}


class SpendingAnalyzerADK:
    """
    ADK-based agent for analyzing customer spending patterns.
    
    This implementation uses Google's Agent Development Kit to provide
    the same functionality as the custom SpendingAnalyzerAgent.
    """
    
    def __init__(self):
        """Initialize the ADK-based spending analyzer agent."""
        
        # Define the system prompt for spending analysis
        self.system_prompt = """
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
- Focus on actionable insights rather than just data reporting

Output Format:
Provide your analysis as a JSON object with the following structure:
{
    "analysis": {
        "overall_assessment": "string",
        "spending_trends": {
            "trend": "increasing|decreasing|stable",
            "confidence": "high|medium|low",
            "details": "string"
        },
        "category_insights": [
            {
                "category": "string",
                "amount": number,
                "percentage": number,
                "insight": "string"
            }
        ],
        "concerning_patterns": ["string"],
        "positive_patterns": ["string"]
    },
    "recommendations": [
        {
            "priority": "high|medium|low",
            "category": "string",
            "action": "string",
            "expected_impact": "string",
            "timeline": "string"
        }
    ],
    "confidence_score": number,
    "next_review_date": "ISO date string"
}
"""
        
        # Create the ADK agent
        self.agent = Agent(
            name="spending_analyzer",
            model="gemini-1.5-flash",
            description="Analyzes customer spending patterns and provides insights",
            instruction=self.system_prompt,
            tools=[]  # We'll handle data retrieval separately
        )
    
    def analyze_spending(self, customer_id: int, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze spending patterns for a customer using ADK.
        
        Args:
            customer_id: ID of the customer to analyze
            context: Optional additional context for the analysis
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Get transaction data using our custom toolset
            transaction_data = SpendingAnalysisToolset.get_customer_transactions(
                customer_id=customer_id,
                days=90
            )
            
            if 'error' in transaction_data:
                return {
                    'success': False,
                    'error': transaction_data['error'],
                    'agent_name': 'SpendingAnalyzerADK',
                    'timestamp': datetime.now().isoformat()
                }
            
            # Get customer info for context
            try:
                customer = mcp_server.get_customer_by_id(customer_id)
                customer_context = {
                    'name': customer.name,
                    'age': customer.age,
                    'income': float(customer.income)
                }
            except Exception:
                customer_context = {'note': 'Customer details not available'}
            
            # Prepare the analysis prompt
            analysis_prompt = f"""
Please analyze the following spending data for customer ID {customer_id}:

Customer Context:
{json.dumps(customer_context, indent=2)}

Transaction Data (Last 90 days):
{json.dumps(transaction_data, indent=2)}

Additional Context:
{json.dumps(context or {}, indent=2)}

Please provide a comprehensive spending analysis following the specified JSON format.
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
                        'analysis': {'overall_assessment': response_text},
                        'recommendations': [],
                        'confidence_score': 0.5
                    }
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                analysis_result = {
                    'analysis': {'overall_assessment': str(response)},
                    'recommendations': [],
                    'confidence_score': 0.5
                }
            
            # Add metadata
            analysis_result.update({
                'success': True,
                'agent_name': 'SpendingAnalyzerADK',
                'customer_id': customer_id,
                'analysis_date': datetime.now().isoformat(),
                'data_period_days': 90,
                'transaction_count': transaction_data['summary']['transaction_count']
            })
            
            return analysis_result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Analysis failed: {str(e)}",
                'agent_name': 'SpendingAnalyzerADK',
                'customer_id': customer_id,
                'timestamp': datetime.now().isoformat()
            }
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about this ADK agent."""
        return {
            'name': 'SpendingAnalyzerADK',
            'description': 'ADK-based agent for analyzing customer spending patterns',
            'version': '1.0.0',
            'capabilities': [
                'Spending trend analysis',
                'Category-wise spending breakdown',
                'Pattern identification',
                'Spending recommendations',
                'Financial insights generation'
            ],
            'model': 'gemini-1.5-flash',
            'framework': 'Google ADK'
        }


# Create a global instance for easy access
spending_analyzer_adk = SpendingAnalyzerADK()
