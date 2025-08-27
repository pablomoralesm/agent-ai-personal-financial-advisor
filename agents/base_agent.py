"""
Base Agent class for the Financial Advisor AI system.

This module provides the abstract base class that all specialized agents
inherit from, defining the common interface and shared functionality.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass
import logging
import google.generativeai as genai
from pydantic import BaseModel

from config.gemini import gemini_config
from mcp.server import mcp_server

logger = logging.getLogger(__name__)


@dataclass
class AgentMessage:
    """Standard message format for agent communication."""
    sender: str
    recipient: str
    message_type: str
    content: Dict[str, Any]
    timestamp: datetime
    correlation_id: Optional[str] = None


class AgentResponse(BaseModel):
    """Standard response format from agents."""
    agent_name: str
    response_type: str
    data: Dict[str, Any]
    confidence_score: float
    reasoning: str
    timestamp: datetime
    recommendations: Optional[List[str]] = None


class BaseAgent(ABC):
    """
    Abstract base class for all financial advisor agents.
    
    This class provides common functionality including:
    - Gemini LLM integration
    - MCP server communication
    - Message handling
    - Logging and error handling
    """
    
    def __init__(self, agent_name: str, agent_description: str):
        """Initialize base agent."""
        self.agent_name = agent_name
        self.agent_description = agent_description
        self.mcp = mcp_server
        self.logger = logging.getLogger(f"agents.{agent_name.lower()}")
        
        # Initialize Gemini model
        if gemini_config:
            try:
                self.model = genai.GenerativeModel(
                    model_name=gemini_config.model_name,
                    generation_config=gemini_config.get_generation_config()
                )
                self.logger.info(f"{self.agent_name} initialized with Gemini model")
            except Exception as e:
                self.logger.error(f"Failed to initialize Gemini model: {e}")
                self.model = None
        else:
            self.logger.warning("Gemini configuration not available")
            self.model = None
    
    @abstractmethod
    def process_request(self, customer_id: int, request_data: Dict[str, Any]) -> AgentResponse:
        """
        Process a request and return a response.
        
        Args:
            customer_id: ID of the customer
            request_data: Request-specific data
            
        Returns:
            AgentResponse with the agent's analysis and recommendations
        """
        pass
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent's LLM interactions."""
        pass
    
    def generate_llm_response(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Generate response using Gemini LLM.
        
        Args:
            prompt: The prompt to send to the LLM
            context: Optional context information
            
        Returns:
            Generated response text
        """
        if not self.model:
            raise RuntimeError("Gemini model not available")
        
        try:
            # Combine system prompt, context, and user prompt
            full_prompt = self.get_system_prompt()
            
            if context:
                full_prompt += f"\n\nCONTEXT:\n{context}"
            
            full_prompt += f"\n\nUSER REQUEST:\n{prompt}"
            
            response = self.model.generate_content(full_prompt)
            
            if response.text:
                self.logger.debug(f"LLM response generated successfully")
                return response.text
            else:
                raise RuntimeError("Empty response from LLM")
                
        except Exception as e:
            self.logger.error(f"LLM generation failed: {e}")
            raise
    
    def get_customer_context(self, customer_id: int) -> Dict[str, Any]:
        """Get customer context from MCP server."""
        try:
            return self.mcp.get_customer_context(customer_id)
        except Exception as e:
            self.logger.error(f"Failed to get customer context: {e}")
            raise
    
    def store_advice(self, customer_id: int, advice_type: str, content: str, 
                    confidence_score: Optional[float] = None):
        """Store advice in the database via MCP server."""
        try:
            self.mcp.store_advice(
                customer_id=customer_id,
                advice_type=advice_type,
                content=content,
                agent_source=self.agent_name,
                confidence_score=confidence_score
            )
            self.logger.info(f"Stored advice for customer {customer_id}")
        except Exception as e:
            self.logger.error(f"Failed to store advice: {e}")
            raise
    
    def handle_agent_message(self, message: AgentMessage) -> Optional[AgentResponse]:
        """
        Handle incoming message from another agent.
        
        Args:
            message: Message from another agent
            
        Returns:
            Optional response to the sender
        """
        self.logger.info(f"Received message from {message.sender}: {message.message_type}")
        
        # Default implementation - subclasses can override for specific behavior
        if message.message_type == "request_analysis":
            customer_id = message.content.get("customer_id")
            if customer_id:
                return self.process_request(customer_id, message.content)
        
        return None
    
    def format_currency(self, amount: float) -> str:
        """Format currency amount for display."""
        return f"${amount:,.2f}"
    
    def calculate_confidence_score(self, data_quality: float, analysis_complexity: float) -> float:
        """
        Calculate confidence score based on data quality and analysis complexity.
        
        Args:
            data_quality: Quality of input data (0.0 to 1.0)
            analysis_complexity: Complexity of the analysis (0.0 to 1.0, higher = more complex)
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        # Simple confidence calculation - can be enhanced
        base_confidence = data_quality * 0.7 + (1.0 - analysis_complexity) * 0.3
        return max(0.0, min(1.0, base_confidence))
    
    def _format_context_for_llm(self, context: Dict[str, Any]) -> str:
        """Format customer context for LLM consumption."""
        try:
            customer = context.get("customer", {})
            spending_analysis = context.get("spending_analysis", {})
            recent_transactions = context.get("recent_transactions", [])
            active_goals = context.get("active_goals", [])
            
            formatted_context = f"""
CUSTOMER PROFILE:
- Name: {customer.get('name', 'Unknown')}
- Age: {customer.get('age', 'Unknown')}
- Income: {self.format_currency(float(customer.get('income', 0))) if customer.get('income') else 'Unknown'}

SPENDING SUMMARY (Last 30 days):
- Total Spending: {self.format_currency(spending_analysis.get('total_spending', 0))}
- Total Income: {self.format_currency(spending_analysis.get('total_income', 0))}
- Net Savings: {self.format_currency(spending_analysis.get('net_savings', 0))}

CATEGORY BREAKDOWN:
"""
            
            for category, amount in spending_analysis.get('category_breakdown', {}).items():
                formatted_context += f"- {category.replace('_', ' ').title()}: {self.format_currency(amount)}\n"
            
            if active_goals:
                formatted_context += "\nACTIVE FINANCIAL GOALS:\n"
                for goal in active_goals:
                    progress = (float(goal.get('current_amount', 0)) / float(goal.get('target_amount', 1))) * 100
                    formatted_context += f"- {goal.get('title')}: {progress:.1f}% complete ({self.format_currency(float(goal.get('current_amount', 0)))} / {self.format_currency(float(goal.get('target_amount', 0)))})\n"
            
            if recent_transactions:
                formatted_context += f"\nRECENT TRANSACTIONS (Last {min(len(recent_transactions), 10)}):\n"
                for transaction in recent_transactions[:10]:
                    formatted_context += f"- {transaction.get('transaction_date')}: {self.format_currency(float(transaction.get('amount', 0)))} - {transaction.get('category', 'Unknown')} - {transaction.get('description', 'No description')}\n"
            
            return formatted_context
            
        except Exception as e:
            self.logger.error(f"Error formatting context: {e}")
            return "Error processing customer context"
    
    def __str__(self) -> str:
        """String representation of the agent."""
        return f"{self.agent_name}: {self.agent_description}"
