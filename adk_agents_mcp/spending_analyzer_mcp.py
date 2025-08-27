"""
MCP-Enhanced Spending Analyzer Agent for the Financial Advisor AI system.

This agent demonstrates the use of Google's Model Context Protocol (MCP) toolset
within the ADK framework for database connectivity and financial analysis.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json

from google.adk import Agent
from google.adk.tools import MCPToolset
from google.adk.tools.mcp_tool.mcp_toolset import StdioConnectionParams, SseConnectionParams

from .mcp_database_config import mcp_setup, mcp_config
from financial_mcp.server import mcp_server  # Fallback for simulation


class MCPDatabaseTools:
    """
    Simulated MCP database tools for financial analysis.
    
    In a production environment, these would be provided by a proper MCP server.
    This class simulates the MCP tools approach for educational purposes.
    """
    
    @staticmethod
    def get_customer_financial_profile(customer_id: int, days_back: int = 90) -> Dict[str, Any]:
        """Simulate MCP tool for getting customer financial profile."""
        try:
            # This simulates what an MCP server would do
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days_back)
            
            # Get data using our existing database (simulating MCP server access)
            from financial_mcp.database import db_manager
            customer = db_manager.get_customer(customer_id)
            
            # Get transactions from MCP server
            transactions = mcp_server.get_customer_transactions(customer_id)
            
            # Filter transactions by date range
            filtered_transactions = [
                t for t in transactions 
                if hasattr(t, 'date') and start_date <= t.date <= end_date
            ]
            
            # Calculate metrics
            total_income = sum(t.amount for t in filtered_transactions if t.amount > 0)
            total_expenses = abs(sum(t.amount for t in filtered_transactions if t.amount < 0))
            
            # Category breakdown
            category_breakdown = {}
            for t in filtered_transactions:
                if t.amount < 0:  # Only expenses
                    category = t.category.value if hasattr(t.category, 'value') else str(t.category)
                    category_breakdown[category] = category_breakdown.get(category, 0) + abs(t.amount)
            
            return {
                "tool_name": "get_customer_financial_profile",
                "mcp_source": True,
                "customer": {
                    "id": customer.id,
                    "name": customer.name,
                    "age": customer.age,
                    "income": float(customer.income)
                },
                "analysis_period": {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "days": days_back
                },
                "financial_summary": {
                    "total_income": float(total_income),
                    "total_expenses": float(total_expenses),
                    "net_cash_flow": float(total_income - total_expenses),
                    "transaction_count": len(filtered_transactions),
                    "expense_categories": {k: float(v) for k, v in category_breakdown.items()}
                },
                "transactions": [
                    {
                        "id": t.id,
                        "amount": float(t.amount),
                        "category": t.category.value if hasattr(t.category, 'value') else str(t.category),
                        "description": t.description,
                        "date": t.date.isoformat() if hasattr(t, 'date') else str(t.created_at.date())
                    } for t in filtered_transactions
                ]
            }
        except Exception as e:
            return {
                "tool_name": "get_customer_financial_profile",
                "error": f"MCP tool failed: {str(e)}",
                "mcp_source": True
            }
    
    @staticmethod 
    def get_spending_analysis_data(customer_id: int, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """Simulate MCP tool for spending analysis."""
        try:
            # This would be provided by the MCP server in a real implementation
            profile_data = MCPDatabaseTools.get_customer_financial_profile(customer_id, 90)
            
            if 'error' in profile_data:
                return profile_data
            
            # Enhanced analysis for spending patterns
            transactions = profile_data['transactions']
            categories = profile_data['financial_summary']['expense_categories']
            
            # Calculate spending trends
            monthly_spending = {}
            for transaction in transactions:
                if float(transaction['amount']) < 0:  # Expenses only
                    month_key = transaction['date'][:7]  # YYYY-MM
                    monthly_spending[month_key] = monthly_spending.get(month_key, 0) + abs(float(transaction['amount']))
            
            # Identify top spending categories
            sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
            
            return {
                "tool_name": "get_spending_analysis_data",
                "mcp_source": True,
                "customer_id": customer_id,
                "spending_trends": {
                    "monthly_breakdown": monthly_spending,
                    "top_categories": sorted_categories[:5],
                    "total_expenses": profile_data['financial_summary']['total_expenses'],
                    "average_transaction": profile_data['financial_summary']['total_expenses'] / max(1, len([t for t in transactions if float(t['amount']) < 0]))
                },
                "insights": {
                    "highest_spending_category": sorted_categories[0][0] if sorted_categories else "none",
                    "transaction_frequency": len(transactions) / 90 * 30,  # Per month estimate
                    "expense_ratio": profile_data['financial_summary']['total_expenses'] / max(1, profile_data['financial_summary']['total_income'])
                }
            }
        except Exception as e:
            return {
                "tool_name": "get_spending_analysis_data", 
                "error": f"MCP tool failed: {str(e)}",
                "mcp_source": True
            }


class SpendingAnalyzerMCP:
    """
    MCP-Enhanced ADK agent for analyzing customer spending patterns.
    
    This implementation demonstrates how to use Google's MCP toolset within
    the ADK framework for database connectivity and analysis.
    """
    
    def __init__(self):
        """Initialize the MCP-enhanced spending analyzer agent."""
        
        # Define the system prompt for spending analysis
        self.system_prompt = """
You are a Financial Spending Analyzer AI assistant powered by Model Context Protocol (MCP) tools. Your role is to analyze customer spending patterns using structured database tools and provide actionable insights.

You have access to MCP database tools that provide:
- Customer financial profiles with transaction history
- Spending analysis data with trends and categories
- Real-time database queries for specific insights

Your analysis should include:
1. Spending trend analysis (increasing, decreasing, stable)
2. Category-wise spending breakdown and insights
3. Identification of unusual or concerning spending patterns
4. Comparison with healthy spending patterns
5. Specific recommendations for spending optimization

Guidelines:
- Leverage the MCP tools to get accurate, real-time data
- Be objective and data-driven in your analysis
- Provide specific, actionable recommendations
- Highlight both positive spending habits and areas for improvement
- Consider the customer's income level and financial capacity
- Use clear, non-judgmental language
- Include confidence levels for your assessments
- Reference the MCP data sources in your analysis

Output Format:
Provide your analysis as a JSON object with the following structure:
{
    "analysis": {
        "data_source": "MCP Tools",
        "overall_assessment": "string",
        "spending_trends": {
            "trend": "increasing|decreasing|stable",
            "confidence": "high|medium|low",
            "details": "string",
            "mcp_data_used": ["tool_name1", "tool_name2"]
        },
        "category_insights": [
            {
                "category": "string",
                "amount": number,
                "percentage": number,
                "insight": "string",
                "recommendation": "string"
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
            "timeline": "string",
            "based_on_mcp_data": "string"
        }
    ],
    "mcp_tools_used": ["tool_name1", "tool_name2"],
    "confidence_score": number,
    "next_review_date": "ISO date string"
}
"""
        
        # For now, we'll simulate MCP tools since setting up a full MCP server
        # is complex. In production, this would connect to a real MCP server.
        self.mcp_tools = MCPDatabaseTools()
        
        # Create the ADK agent (without MCP toolset for now, we'll simulate)
        self.agent = Agent(
            name="spending_analyzer_mcp",
            model="gemini-1.5-flash",
            description="Analyzes customer spending patterns using MCP database tools",
            instruction=self.system_prompt,
            tools=[]  # We'll simulate MCP tools instead of using real ones for now
        )
    
    def analyze_spending_with_mcp(self, customer_id: int, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze spending patterns using MCP tools for database access.
        
        Args:
            customer_id: ID of the customer to analyze
            context: Optional additional context for the analysis
            
        Returns:
            Dictionary containing MCP-enhanced analysis results
        """
        try:
            # Step 1: Use MCP tools to get financial data
            financial_profile = self.mcp_tools.get_customer_financial_profile(customer_id, 90)
            
            if 'error' in financial_profile:
                return {
                    'success': False,
                    'error': financial_profile['error'],
                    'agent_name': 'SpendingAnalyzerMCP',
                    'mcp_enabled': True,
                    'timestamp': datetime.now().isoformat()
                }
            
            # Step 2: Get detailed spending analysis data
            spending_data = self.mcp_tools.get_spending_analysis_data(customer_id)
            
            if 'error' in spending_data:
                return {
                    'success': False,
                    'error': spending_data['error'],
                    'agent_name': 'SpendingAnalyzerMCP',
                    'mcp_enabled': True,
                    'timestamp': datetime.now().isoformat()
                }
            
            # Step 3: Prepare comprehensive prompt with MCP data
            analysis_prompt = f"""
Please analyze the following MCP-sourced financial data for customer ID {customer_id}:

MCP Tool: Customer Financial Profile
{json.dumps(financial_profile, indent=2)}

MCP Tool: Spending Analysis Data  
{json.dumps(spending_data, indent=2)}

Additional Context:
{json.dumps(context or {}, indent=2)}

Please provide a comprehensive spending analysis following the specified JSON format. 
Note that this data comes from MCP database tools and should be referenced in your analysis.
Focus on actionable insights based on the structured MCP data provided.
"""
            
            # Step 4: Use ADK agent to generate analysis
            response = self.agent.run(analysis_prompt)
            
            # Step 5: Parse and enhance the response
            try:
                response_text = str(response)
                if '{' in response_text and '}' in response_text:
                    json_start = response_text.find('{')
                    json_end = response_text.rfind('}') + 1
                    json_str = response_text[json_start:json_end]
                    analysis_result = json.loads(json_str)
                else:
                    analysis_result = {
                        'analysis': {
                            'data_source': 'MCP Tools',
                            'overall_assessment': response_text
                        },
                        'recommendations': [],
                        'mcp_tools_used': ['get_customer_financial_profile', 'get_spending_analysis_data'],
                        'confidence_score': 0.7
                    }
            except json.JSONDecodeError:
                analysis_result = {
                    'analysis': {
                        'data_source': 'MCP Tools',
                        'overall_assessment': str(response)
                    },
                    'recommendations': [],
                    'mcp_tools_used': ['get_customer_financial_profile', 'get_spending_analysis_data'], 
                    'confidence_score': 0.5
                }
            
            # Step 6: Add MCP metadata
            analysis_result.update({
                'success': True,
                'agent_name': 'SpendingAnalyzerMCP',
                'framework': 'Google ADK + MCP',
                'mcp_enabled': True,
                'customer_id': customer_id,
                'analysis_date': datetime.now().isoformat(),
                'data_sources': {
                    'mcp_tools_used': ['get_customer_financial_profile', 'get_spending_analysis_data'],
                    'mcp_server_simulation': True,
                    'database_access_method': 'MCP Tools'
                },
                'raw_mcp_data': {
                    'financial_profile': financial_profile,
                    'spending_data': spending_data
                }
            })
            
            return analysis_result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"MCP-enhanced analysis failed: {str(e)}",
                'agent_name': 'SpendingAnalyzerMCP',
                'framework': 'Google ADK + MCP',
                'mcp_enabled': True,
                'customer_id': customer_id,
                'timestamp': datetime.now().isoformat()
            }
    
    def get_mcp_tools_info(self) -> Dict[str, Any]:
        """Get information about available MCP tools."""
        return {
            'available_tools': [
                'get_customer_financial_profile',
                'get_spending_analysis_data'
            ],
            'mcp_server_config': mcp_setup.get_mcp_connection_params(),
            'simulation_mode': True,
            'note': 'This implementation simulates MCP tools for educational purposes'
        }
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about this MCP-enhanced agent."""
        return {
            'name': 'SpendingAnalyzerMCP',
            'description': 'MCP-enhanced ADK agent for analyzing customer spending patterns',
            'version': '1.0.0',
            'capabilities': [
                'MCP database tool integration',
                'Real-time financial data access',
                'Spending trend analysis',
                'Category-wise spending breakdown',
                'Pattern identification',
                'MCP-based recommendations'
            ],
            'model': 'gemini-1.5-flash',
            'framework': 'Google ADK + MCP',
            'mcp_tools': self.get_mcp_tools_info()
        }


# Create a global instance for easy access
spending_analyzer_mcp = SpendingAnalyzerMCP()
