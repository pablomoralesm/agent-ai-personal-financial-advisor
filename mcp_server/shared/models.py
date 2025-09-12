"""
Shared Pydantic models for MCP Database Servers.

This module contains Pydantic models for data validation and serialization
used by both server implementations.
"""

from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field


class Customer(BaseModel):
    """Customer model for validation and serialization."""
    id: Optional[int] = None
    name: str
    email: str
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None


class Transaction(BaseModel):
    """Transaction model for validation and serialization."""
    id: Optional[int] = None
    customer_id: int
    amount: Decimal
    category: str
    subcategory: Optional[str] = None
    description: Optional[str] = None
    transaction_date: date
    transaction_type: str  # 'income' or 'expense'
    payment_method: Optional[str] = None


class FinancialGoal(BaseModel):
    """Financial goal model for validation and serialization."""
    id: Optional[int] = None
    customer_id: int
    goal_name: str
    goal_type: str
    target_amount: Decimal
    current_amount: Decimal = Decimal('0.00')
    target_date: Optional[date] = None
    priority: str = 'medium'  # 'low', 'medium', 'high'
    status: str = 'active'  # 'active', 'completed', 'paused', 'cancelled'
    description: Optional[str] = None


class AdviceHistory(BaseModel):
    """Advice history model for validation and serialization."""
    id: Optional[int] = None
    customer_id: int
    agent_name: str
    advice_type: str
    advice_content: str
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    metadata: Optional[dict] = None


class AgentInteraction(BaseModel):
    """Agent interaction model for validation and serialization."""
    id: Optional[int] = None
    session_id: str
    customer_id: Optional[int] = None
    from_agent: str
    to_agent: Optional[str] = None
    interaction_type: str
    message_content: str
    context_data: Optional[dict] = None


class SpendingCategory(BaseModel):
    """Spending category model for validation and serialization."""
    category_name: str
    parent_category: Optional[str] = None
    description: Optional[str] = None
    is_income: bool = False
    is_active: bool = True
