"""SpendingAnalyzerAgent implementation for the Financial Advisor app.

This agent analyzes customer spending patterns and identifies trends.
"""

import datetime
from typing import Dict, List, Any, Optional
import logging

from google.adk import Agent, AgentConfig, Tool, ToolConfig, ToolSpec
from google.adk.llm import GeminiLLM
from google.adk.llm.gemini import GeminiConfig

from src.mcp.mcp_client import FinancialAdvisorMcpClient

class SpendingAnalyzerAgent(Agent):
    """Agent that analyzes customer spending patterns."""
    
    def __init__(self, mcp_client: FinancialAdvisorMcpClient, api_key: str):
        """Initialize the SpendingAnalyzerAgent.
        
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
            name="SpendingAnalyzerAgent",
            description="Analyzes customer spending patterns and identifies trends",
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
        
        # Tool to get customer transactions
        tools.append(Tool(
            ToolConfig(
                name="get_customer_transactions",
                description="Get all transactions for a customer",
                function=self._get_customer_transactions,
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
        
        # Tool to get transactions by category
        tools.append(Tool(
            ToolConfig(
                name="get_transactions_by_category",
                description="Get transactions by category for a customer",
                function=self._get_transactions_by_category,
                parameters=[
                    ToolSpec.Parameter(
                        name="customer_id",
                        description="Customer ID",
                        type="integer",
                        required=True
                    ),
                    ToolSpec.Parameter(
                        name="category",
                        description="Transaction category",
                        type="string",
                        required=True
                    )
                ]
            )
        ))
        
        # Tool to get transactions by date range
        tools.append(Tool(
            ToolConfig(
                name="get_transactions_by_date_range",
                description="Get transactions within a date range for a customer",
                function=self._get_transactions_by_date_range,
                parameters=[
                    ToolSpec.Parameter(
                        name="customer_id",
                        description="Customer ID",
                        type="integer",
                        required=True
                    ),
                    ToolSpec.Parameter(
                        name="start_date",
                        description="Start date (YYYY-MM-DD)",
                        type="string",
                        required=True
                    ),
                    ToolSpec.Parameter(
                        name="end_date",
                        description="End date (YYYY-MM-DD)",
                        type="string",
                        required=True
                    )
                ]
            )
        ))
        
        # Tool to get spending by category
        tools.append(Tool(
            ToolConfig(
                name="get_spending_by_category",
                description="Get total spending by category for a customer",
                function=self._get_spending_by_category,
                parameters=[
                    ToolSpec.Parameter(
                        name="customer_id",
                        description="Customer ID",
                        type="integer",
                        required=True
                    ),
                    ToolSpec.Parameter(
                        name="start_date",
                        description="Start date (YYYY-MM-DD)",
                        type="string",
                        required=True
                    ),
                    ToolSpec.Parameter(
                        name="end_date",
                        description="End date (YYYY-MM-DD)",
                        type="string",
                        required=True
                    )
                ]
            )
        ))
        
        # Tool to get monthly spending
        tools.append(Tool(
            ToolConfig(
                name="get_monthly_spending",
                description="Get monthly spending totals for a customer",
                function=self._get_monthly_spending,
                parameters=[
                    ToolSpec.Parameter(
                        name="customer_id",
                        description="Customer ID",
                        type="integer",
                        required=True
                    ),
                    ToolSpec.Parameter(
                        name="year",
                        description="Year",
                        type="integer",
                        required=True
                    )
                ]
            )
        ))
        
        # Tool to analyze spending patterns
        tools.append(Tool(
            ToolConfig(
                name="analyze_spending_patterns",
                description="Analyze spending patterns for a customer",
                function=self._analyze_spending_patterns,
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
        
        # Tool to identify high spending categories
        tools.append(Tool(
            ToolConfig(
                name="identify_high_spending_categories",
                description="Identify categories with high spending",
                function=self._identify_high_spending_categories,
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
                    ),
                    ToolSpec.Parameter(
                        name="threshold_percentage",
                        description="Threshold percentage for high spending",
                        type="number",
                        required=True
                    )
                ]
            )
        ))
        
        # Tool to calculate spending trends
        tools.append(Tool(
            ToolConfig(
                name="calculate_spending_trends",
                description="Calculate spending trends over time",
                function=self._calculate_spending_trends,
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
        
        return tools
    
    # Tool implementations
    
    def _get_customer_transactions(self, customer_id: int) -> List[Dict[str, Any]]:
        """Get all transactions for a customer."""
        return self.mcp_client.get_customer_transactions(customer_id)
    
    def _get_transactions_by_category(self, customer_id: int, category: str) -> List[Dict[str, Any]]:
        """Get transactions by category for a customer."""
        return self.mcp_client.get_transactions_by_category(customer_id, category)
    
    def _get_transactions_by_date_range(self, customer_id: int, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get transactions within a date range for a customer."""
        return self.mcp_client.get_transactions_by_date_range(customer_id, start_date, end_date)
    
    def _get_spending_by_category(self, customer_id: int, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get total spending by category for a customer."""
        return self.mcp_client.get_spending_by_category(customer_id, start_date, end_date)
    
    def _get_monthly_spending(self, customer_id: int, year: int) -> List[Dict[str, Any]]:
        """Get monthly spending totals for a customer."""
        return self.mcp_client.get_monthly_spending(customer_id, year)
    
    def _analyze_spending_patterns(self, customer_id: int, months: int) -> Dict[str, Any]:
        """Analyze spending patterns for a customer.
        
        Args:
            customer_id: Customer ID
            months: Number of months to analyze
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        # Calculate date range
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=30 * months)
        
        # Get spending by category
        spending_by_category = self.mcp_client.get_spending_by_category(
            customer_id, 
            start_date.isoformat(),
            end_date.isoformat()
        )
        
        # Get monthly spending
        current_year = end_date.year
        monthly_spending = []
        
        # Get data for current year and previous year if needed
        monthly_spending.extend(self.mcp_client.get_monthly_spending(customer_id, current_year))
        if start_date.year < current_year:
            monthly_spending.extend(self.mcp_client.get_monthly_spending(customer_id, start_date.year))
        
        # Calculate total spending
        total_spending = sum(category["total_amount"] for category in spending_by_category)
        
        # Calculate percentage for each category
        for category in spending_by_category:
            category["percentage"] = (category["total_amount"] / total_spending) * 100 if total_spending > 0 else 0
        
        # Calculate average monthly spending
        avg_monthly_spending = total_spending / months if months > 0 else 0
        
        return {
            "spending_by_category": spending_by_category,
            "monthly_spending": monthly_spending,
            "total_spending": total_spending,
            "avg_monthly_spending": avg_monthly_spending,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
    
    def _identify_high_spending_categories(self, customer_id: int, months: int, threshold_percentage: float) -> List[Dict[str, Any]]:
        """Identify categories with high spending.
        
        Args:
            customer_id: Customer ID
            months: Number of months to analyze
            threshold_percentage: Threshold percentage for high spending
            
        Returns:
            List[Dict[str, Any]]: High spending categories
        """
        # Get spending analysis
        analysis = self._analyze_spending_patterns(customer_id, months)
        
        # Filter categories above threshold
        high_spending = [
            category for category in analysis["spending_by_category"]
            if category["percentage"] >= threshold_percentage
        ]
        
        return {
            "high_spending_categories": high_spending,
            "threshold_percentage": threshold_percentage,
            "total_spending": analysis["total_spending"]
        }
    
    def _calculate_spending_trends(self, customer_id: int, months: int) -> Dict[str, Any]:
        """Calculate spending trends over time.
        
        Args:
            customer_id: Customer ID
            months: Number of months to analyze
            
        Returns:
            Dict[str, Any]: Spending trends
        """
        # Calculate date range
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=30 * months)
        
        # Get monthly spending for the period
        current_year = end_date.year
        monthly_data = []
        
        # Get data for current year and previous year if needed
        monthly_data.extend(self.mcp_client.get_monthly_spending(customer_id, current_year))
        if start_date.year < current_year:
            monthly_data.extend(self.mcp_client.get_monthly_spending(customer_id, start_date.year))
        
        # Sort by month/year
        monthly_data.sort(key=lambda x: (x["year"] if "year" in x else current_year, x["month"]))
        
        # Calculate trend (increasing, decreasing, stable)
        trend = "stable"
        if len(monthly_data) >= 2:
            first_half = monthly_data[:len(monthly_data)//2]
            second_half = monthly_data[len(monthly_data)//2:]
            
            first_half_avg = sum(month["total_amount"] for month in first_half) / len(first_half)
            second_half_avg = sum(month["total_amount"] for month in second_half) / len(second_half)
            
            # Calculate percentage change
            percent_change = ((second_half_avg - first_half_avg) / first_half_avg) * 100 if first_half_avg > 0 else 0
            
            if percent_change > 5:
                trend = "increasing"
            elif percent_change < -5:
                trend = "decreasing"
        
        return {
            "monthly_data": monthly_data,
            "trend": trend,
            "months_analyzed": months,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
    
    def analyze_customer_spending(self, customer_id: int, months: int = 3) -> Dict[str, Any]:
        """Analyze customer spending and provide insights.
        
        This is the main method to be called by external code.
        
        Args:
            customer_id: Customer ID
            months: Number of months to analyze
            
        Returns:
            Dict[str, Any]: Comprehensive analysis results
        """
        # Get customer info
        try:
            customer = self.mcp_client.get_customer(customer_id)
        except Exception as e:
            logging.error(f"Error getting customer {customer_id}: {e}")
            return {"error": f"Customer with ID {customer_id} not found"}
        
        # Perform spending analysis
        spending_patterns = self._analyze_spending_patterns(customer_id, months)
        
        # Identify high spending categories (>= 15% of total)
        high_spending = self._identify_high_spending_categories(customer_id, months, 15.0)
        
        # Calculate spending trends
        trends = self._calculate_spending_trends(customer_id, months)
        
        # Save analysis as advice
        analysis_summary = (
            f"Spending Analysis for the past {months} months:\n"
            f"- Total spending: ${spending_patterns['total_spending']:.2f}\n"
            f"- Average monthly spending: ${spending_patterns['avg_monthly_spending']:.2f}\n"
            f"- Spending trend: {trends['trend']}\n"
            f"- High spending categories: {', '.join(cat['category'] for cat in high_spending['high_spending_categories'])}\n"
        )
        
        try:
            self.mcp_client.add_advice(
                customer_id=customer_id,
                agent_name="SpendingAnalyzerAgent",
                advice_text=analysis_summary
            )
        except Exception as e:
            logging.error(f"Error saving spending analysis: {e}")
        
        # Return comprehensive analysis
        return {
            "customer": customer,
            "spending_patterns": spending_patterns,
            "high_spending": high_spending,
            "trends": trends,
            "analysis_summary": analysis_summary
        }
