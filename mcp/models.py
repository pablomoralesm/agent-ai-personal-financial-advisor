"""
Database models for the Financial Advisor AI system.

This module defines the SQLAlchemy models for storing customer data,
transactions, goals, and advice history.
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Numeric, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from enum import Enum

# SQLAlchemy Base
Base = declarative_base()


class TransactionCategory(str, Enum):
    """Transaction categories for spending analysis."""
    FOOD_DINING = "food_dining"
    TRANSPORTATION = "transportation"
    SHOPPING = "shopping"
    ENTERTAINMENT = "entertainment"
    BILLS_UTILITIES = "bills_utilities"
    HEALTHCARE = "healthcare"
    TRAVEL = "travel"
    EDUCATION = "education"
    INCOME = "income"
    OTHER = "other"


class GoalType(str, Enum):
    """Types of financial goals."""
    SAVINGS = "savings"
    INVESTMENT = "investment"
    DEBT_PAYOFF = "debt_payoff"
    EMERGENCY_FUND = "emergency_fund"
    RETIREMENT = "retirement"
    OTHER = "other"


class GoalStatus(str, Enum):
    """Status of financial goals."""
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"


# SQLAlchemy Models
class Customer(Base):
    """Customer table for storing user profiles."""
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    age = Column(Integer)
    income = Column(Numeric(15, 2))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="customer", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="customer", cascade="all, delete-orphan")
    advice_history = relationship("Advice", back_populates="customer", cascade="all, delete-orphan")


class Transaction(Base):
    """Transaction table for storing financial transactions."""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text)
    transaction_date = Column(Date, nullable=False)
    is_income = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="transactions")


class Goal(Base):
    """Goal table for storing financial goals."""
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    goal_type = Column(String(50), nullable=False)
    target_amount = Column(Numeric(15, 2), nullable=False)
    current_amount = Column(Numeric(15, 2), default=0)
    target_date = Column(Date)
    status = Column(String(20), default=GoalStatus.ACTIVE.value)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="goals")


class Advice(Base):
    """Advice table for storing AI-generated financial advice."""
    __tablename__ = "advice"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    advice_type = Column(String(50), nullable=False)  # spending, goal_planning, general
    content = Column(Text, nullable=False)
    agent_source = Column(String(50), nullable=False)  # which agent generated this advice
    confidence_score = Column(Numeric(3, 2))  # 0.00 to 1.00
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="advice_history")


# Pydantic Models for API/Agent Communication
class CustomerBase(BaseModel):
    """Base model for customer data."""
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$')
    age: Optional[int] = Field(None, ge=18, le=120)
    income: Optional[Decimal] = Field(None, ge=0)


class CustomerCreate(CustomerBase):
    """Model for creating a new customer."""
    pass


class CustomerResponse(CustomerBase):
    """Model for customer response data."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class TransactionBase(BaseModel):
    """Base model for transaction data."""
    amount: Decimal = Field(..., gt=0)
    category: TransactionCategory
    description: Optional[str] = None
    transaction_date: date
    is_income: bool = False


class TransactionCreate(TransactionBase):
    """Model for creating a new transaction."""
    customer_id: int


class TransactionResponse(TransactionBase):
    """Model for transaction response data."""
    id: int
    customer_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class GoalBase(BaseModel):
    """Base model for goal data."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    goal_type: GoalType
    target_amount: Decimal = Field(..., gt=0)
    current_amount: Decimal = Field(default=Decimal('0'), ge=0)
    target_date: Optional[date] = None
    status: GoalStatus = GoalStatus.ACTIVE


class GoalCreate(GoalBase):
    """Model for creating a new goal."""
    customer_id: int


class GoalResponse(GoalBase):
    """Model for goal response data."""
    id: int
    customer_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class AdviceBase(BaseModel):
    """Base model for advice data."""
    advice_type: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1)
    agent_source: str = Field(..., min_length=1, max_length=50)
    confidence_score: Optional[Decimal] = Field(None, ge=0, le=1)


class AdviceCreate(AdviceBase):
    """Model for creating new advice."""
    customer_id: int


class AdviceResponse(AdviceBase):
    """Model for advice response data."""
    id: int
    customer_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
