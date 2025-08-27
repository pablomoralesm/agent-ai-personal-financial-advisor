"""
Database manager for MySQL operations using SQLAlchemy.

This module provides the DatabaseManager class for handling all database
operations including connection management, table creation, and CRUD operations.
"""

from typing import List, Optional, Dict, Any
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from config.database import db_config
from .models import Base, Customer, Transaction, Goal, Advice
from .models import CustomerCreate, TransactionCreate, GoalCreate, AdviceCreate

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self, config=None):
        """Initialize database manager with configuration."""
        self.config = config or db_config
        self.engine = None
        self.SessionLocal = None
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize SQLAlchemy engine and session factory."""
        try:
            connection_string = self.config.get_connection_string()
            self.engine = create_engine(
                connection_string,
                echo=False,  # Set to True for SQL debugging
                pool_pre_ping=True,  # Verify connections before use
                pool_recycle=3600,   # Recycle connections after 1 hour
            )
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            logger.info("Database engine initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize database engine: {e}")
            # Set to None so we can handle gracefully
            self.engine = None
            self.SessionLocal = None
    
    @contextmanager
    def get_session(self):
        """Context manager for database sessions."""
        if not self.SessionLocal:
            raise RuntimeError("Database not initialized. Please check your database configuration.")
        
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    def create_tables(self):
        """Create all database tables."""
        if not self.engine:
            raise RuntimeError("Database engine not initialized")
        
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            raise
    
    def drop_tables(self):
        """Drop all database tables (use with caution!)."""
        try:
            Base.metadata.drop_all(bind=self.engine)
            logger.info("Database tables dropped successfully")
        except Exception as e:
            logger.error(f"Failed to drop tables: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Test database connection."""
        if not self.SessionLocal:
            logger.error("Database not initialized")
            return False
        
        try:
            with self.get_session() as session:
                session.execute(text("SELECT 1"))
                logger.info("Database connection test successful")
                return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    # Customer CRUD operations
    def create_customer(self, customer_data: CustomerCreate) -> Customer:
        """Create a new customer."""
        with self.get_session() as session:
            customer = Customer(**customer_data.model_dump())
            session.add(customer)
            session.flush()
            session.refresh(customer)
            # Expunge to avoid DetachedInstanceError
            session.expunge(customer)
            return customer
    
    def get_customer(self, customer_id: int) -> Optional[Customer]:
        """Get customer by ID."""
        with self.get_session() as session:
            customer = session.query(Customer).filter(Customer.id == customer_id).first()
            if customer:
                session.expunge(customer)
            return customer
    
    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """Get customer by email."""
        with self.get_session() as session:
            customer = session.query(Customer).filter(Customer.email == email).first()
            if customer:
                session.expunge(customer)
            return customer
    
    def get_all_customers(self) -> List[Customer]:
        """Get all customers."""
        with self.get_session() as session:
            customers = session.query(Customer).all()
            # Expunge all customers to avoid session issues
            for customer in customers:
                session.expunge(customer)
            return customers
    
    def update_customer(self, customer_id: int, update_data: Dict[str, Any]) -> Optional[Customer]:
        """Update customer information."""
        with self.get_session() as session:
            customer = session.query(Customer).filter(Customer.id == customer_id).first()
            if customer:
                for key, value in update_data.items():
                    if hasattr(customer, key):
                        setattr(customer, key, value)
                session.flush()
                session.refresh(customer)
                session.expunge(customer)
            return customer
    
    # Transaction CRUD operations
    def create_transaction(self, transaction_data: TransactionCreate) -> Transaction:
        """Create a new transaction."""
        with self.get_session() as session:
            transaction = Transaction(**transaction_data.model_dump())
            session.add(transaction)
            session.flush()
            session.refresh(transaction)
            session.expunge(transaction)
            return transaction
    
    def get_customer_transactions(self, customer_id: int, limit: Optional[int] = None) -> List[Transaction]:
        """Get transactions for a customer."""
        with self.get_session() as session:
            query = session.query(Transaction).filter(Transaction.customer_id == customer_id)
            query = query.order_by(Transaction.transaction_date.desc())
            if limit:
                query = query.limit(limit)
            transactions = query.all()
            # Expunge all transactions to avoid session issues
            for transaction in transactions:
                session.expunge(transaction)
            return transactions
    
    def get_transactions_by_category(self, customer_id: int, category: str) -> List[Transaction]:
        """Get transactions by category for a customer."""
        with self.get_session() as session:
            return session.query(Transaction).filter(
                Transaction.customer_id == customer_id,
                Transaction.category == category
            ).all()
    
    # Goal CRUD operations
    def create_goal(self, goal_data: GoalCreate) -> Goal:
        """Create a new goal."""
        with self.get_session() as session:
            goal = Goal(**goal_data.model_dump())
            session.add(goal)
            session.flush()
            session.refresh(goal)
            session.expunge(goal)
            return goal
    
    def get_customer_goals(self, customer_id: int, active_only: bool = False) -> List[Goal]:
        """Get goals for a customer."""
        with self.get_session() as session:
            query = session.query(Goal).filter(Goal.customer_id == customer_id)
            if active_only:
                query = query.filter(Goal.status == "active")
            goals = query.order_by(Goal.created_at.desc()).all()
            # Expunge all goals to avoid session issues
            for goal in goals:
                session.expunge(goal)
            return goals
    
    def update_goal(self, goal_id: int, update_data: Dict[str, Any]) -> Optional[Goal]:
        """Update goal information."""
        with self.get_session() as session:
            goal = session.query(Goal).filter(Goal.id == goal_id).first()
            if goal:
                for key, value in update_data.items():
                    if hasattr(goal, key):
                        setattr(goal, key, value)
                session.flush()
                session.refresh(goal)
                session.expunge(goal)
            return goal
    
    # Advice CRUD operations
    def create_advice(self, advice_data: AdviceCreate) -> Advice:
        """Create new advice entry."""
        with self.get_session() as session:
            advice = Advice(**advice_data.model_dump())
            session.add(advice)
            session.flush()
            session.refresh(advice)
            session.expunge(advice)
            return advice
    
    def get_customer_advice(self, customer_id: int, advice_type: Optional[str] = None) -> List[Advice]:
        """Get advice history for a customer."""
        with self.get_session() as session:
            query = session.query(Advice).filter(Advice.customer_id == customer_id)
            if advice_type:
                query = query.filter(Advice.advice_type == advice_type)
            advice_list = query.order_by(Advice.created_at.desc()).all()
            # Expunge all advice entries to avoid session issues
            for advice in advice_list:
                session.expunge(advice)
            return advice_list
    
    # Analytics and reporting methods
    def get_spending_summary(self, customer_id: int, days: int = 30) -> Dict[str, Any]:
        """Get spending summary for the last N days."""
        with self.get_session() as session:
            from sqlalchemy import func
            from datetime import datetime, timedelta
            
            start_date = datetime.now().date() - timedelta(days=days)
            
            # Total spending
            total_spending = session.query(func.sum(Transaction.amount)).filter(
                Transaction.customer_id == customer_id,
                Transaction.is_income == False,
                Transaction.transaction_date >= start_date
            ).scalar() or 0
            
            # Total income
            total_income = session.query(func.sum(Transaction.amount)).filter(
                Transaction.customer_id == customer_id,
                Transaction.is_income == True,
                Transaction.transaction_date >= start_date
            ).scalar() or 0
            
            # Spending by category
            category_spending = session.query(
                Transaction.category,
                func.sum(Transaction.amount).label('total')
            ).filter(
                Transaction.customer_id == customer_id,
                Transaction.is_income == False,
                Transaction.transaction_date >= start_date
            ).group_by(Transaction.category).all()
            
            return {
                "total_spending": float(total_spending),
                "total_income": float(total_income),
                "net_savings": float(total_income - total_spending),
                "category_breakdown": {cat: float(total) for cat, total in category_spending},
                "period_days": days
            }


# Global database manager instance
db_manager = DatabaseManager()
