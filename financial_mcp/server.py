"""
MCP (Model Context Protocol) Server for the Financial Advisor AI system.

This module provides the MCPServer class that acts as an interface between
the AI agents and the database, handling all data persistence operations.
"""

from typing import List, Optional, Dict, Any, Union
from datetime import datetime, date
import logging
from decimal import Decimal

from .database import db_manager
from .models import (
    Customer, Transaction, Goal, Advice,
    CustomerCreate, TransactionCreate, GoalCreate, AdviceCreate,
    CustomerResponse, TransactionResponse, GoalResponse, AdviceResponse,
    TransactionCategory, GoalType, GoalStatus
)

logger = logging.getLogger(__name__)


class MCPServer:
    """
    MCP Server for handling all data persistence operations.
    
    This server provides a high-level interface for agents to interact
    with the database without needing to know SQLAlchemy details.
    """
    
    def __init__(self, database_manager=None):
        """Initialize MCP server with database manager."""
        self.db = database_manager or db_manager
        # Only ensure tables exist if we can connect to the database
        try:
            self._ensure_tables_exist()
        except Exception as e:
            logger.warning(f"Could not ensure tables exist: {e}")
    
    def _ensure_tables_exist(self):
        """Ensure database tables exist."""
        try:
            self.db.create_tables()
            logger.info("MCP Server initialized with database tables")
        except Exception as e:
            logger.error(f"Failed to initialize MCP server: {e}")
            raise
    
    def health_check(self) -> Dict[str, Any]:
        """Check server health and database connectivity."""
        try:
            db_connected = self.db.test_connection()
            return {
                "status": "healthy" if db_connected else "unhealthy",
                "database_connected": db_connected,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "error",
                "database_connected": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
    
    # Customer operations
    def create_customer_profile(self, name: str, email: str, age: Optional[int] = None, 
                              income: Optional[Union[float, Decimal]] = None) -> CustomerResponse:
        """Create a new customer profile."""
        try:
            customer_data = CustomerCreate(
                name=name,
                email=email,
                age=age,
                income=Decimal(str(income)) if income is not None else None
            )
            customer = self.db.create_customer(customer_data)
            logger.info(f"Created customer profile for {email}")
            
            # Convert to dict first to avoid session issues
            customer_dict = {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "age": customer.age,
                "income": customer.income,
                "created_at": customer.created_at,
                "updated_at": customer.updated_at
            }
            return CustomerResponse(**customer_dict)
        except Exception as e:
            logger.error(f"Failed to create customer profile: {e}")
            raise
    
    def get_customer_profile(self, customer_id: Optional[int] = None, 
                           email: Optional[str] = None) -> Optional[CustomerResponse]:
        """Get customer profile by ID or email."""
        try:
            if customer_id:
                customer = self.db.get_customer(customer_id)
            elif email:
                customer = self.db.get_customer_by_email(email)
            else:
                raise ValueError("Either customer_id or email must be provided")
            
            if customer:
                customer_dict = {
                    "id": customer.id,
                    "name": customer.name,
                    "email": customer.email,
                    "age": customer.age,
                    "income": customer.income,
                    "created_at": customer.created_at,
                    "updated_at": customer.updated_at
                }
                return CustomerResponse(**customer_dict)
            return None
        except Exception as e:
            logger.error(f"Failed to get customer profile: {e}")
            raise
    
    def update_customer_profile(self, customer_id: int, update_data: Dict[str, Any]) -> Optional[CustomerResponse]:
        """Update customer profile."""
        try:
            customer = self.db.update_customer(customer_id, update_data)
            logger.info(f"Updated customer profile {customer_id}")
            if customer:
                customer_dict = {
                    "id": customer.id,
                    "name": customer.name,
                    "email": customer.email,
                    "age": customer.age,
                    "income": customer.income,
                    "created_at": customer.created_at,
                    "updated_at": customer.updated_at
                }
                return CustomerResponse(**customer_dict)
            return None
        except Exception as e:
            logger.error(f"Failed to update customer profile: {e}")
            raise
    
    # Transaction operations
    def add_transaction(self, customer_id: int, amount: Union[float, Decimal], 
                       category: Union[str, TransactionCategory], description: Optional[str] = None,
                       transaction_date: Optional[date] = None, is_income: bool = False) -> TransactionResponse:
        """Add a new transaction."""
        try:
            if isinstance(category, str):
                # Validate category string
                category_value = category
            else:
                category_value = category.value
            
            transaction_data = TransactionCreate(
                customer_id=customer_id,
                amount=Decimal(str(amount)),
                category=category_value,
                description=description,
                transaction_date=transaction_date or date.today(),
                is_income=is_income
            )
            transaction = self.db.create_transaction(transaction_data)
            logger.info(f"Added transaction for customer {customer_id}: {amount}")
            return TransactionResponse.from_orm(transaction)
        except Exception as e:
            logger.error(f"Failed to add transaction: {e}")
            raise
    
    def get_customer_transactions(self, customer_id: int, limit: Optional[int] = None) -> List[TransactionResponse]:
        """Get transactions for a customer."""
        try:
            transactions = self.db.get_customer_transactions(customer_id, limit)
            return [TransactionResponse.from_orm(t) for t in transactions]
        except Exception as e:
            logger.error(f"Failed to get customer transactions: {e}")
            raise
    
    def get_spending_analysis(self, customer_id: int, days: int = 30) -> Dict[str, Any]:
        """Get detailed spending analysis for a customer."""
        try:
            return self.db.get_spending_summary(customer_id, days)
        except Exception as e:
            logger.error(f"Failed to get spending analysis: {e}")
            raise
    
    # Goal operations
    def create_financial_goal(self, customer_id: int, title: str, goal_type: Union[str, GoalType],
                            target_amount: Union[float, Decimal], description: Optional[str] = None,
                            target_date: Optional[date] = None) -> GoalResponse:
        """Create a new financial goal."""
        try:
            if isinstance(goal_type, str):
                goal_type_value = goal_type
            else:
                goal_type_value = goal_type.value
            
            goal_data = GoalCreate(
                customer_id=customer_id,
                title=title,
                description=description,
                goal_type=goal_type_value,
                target_amount=Decimal(str(target_amount)),
                target_date=target_date
            )
            goal = self.db.create_goal(goal_data)
            logger.info(f"Created financial goal for customer {customer_id}: {title}")
            return GoalResponse.from_orm(goal)
        except Exception as e:
            logger.error(f"Failed to create financial goal: {e}")
            raise
    
    def get_customer_goals(self, customer_id: int, active_only: bool = False) -> List[GoalResponse]:
        """Get financial goals for a customer."""
        try:
            goals = self.db.get_customer_goals(customer_id, active_only)
            return [GoalResponse.from_orm(g) for g in goals]
        except Exception as e:
            logger.error(f"Failed to get customer goals: {e}")
            raise
    
    def update_goal_progress(self, goal_id: int, current_amount: Union[float, Decimal],
                           status: Optional[Union[str, GoalStatus]] = None) -> Optional[GoalResponse]:
        """Update goal progress."""
        try:
            update_data = {"current_amount": Decimal(str(current_amount))}
            if status:
                update_data["status"] = status.value if isinstance(status, GoalStatus) else status
            
            goal = self.db.update_goal(goal_id, update_data)
            if goal:
                logger.info(f"Updated goal progress {goal_id} to {current_amount}")
                # Convert to dict first to avoid session issues
                goal_dict = {
                    "id": goal.id,
                    "customer_id": goal.customer_id,
                    "title": goal.title,
                    "description": goal.description,
                    "goal_type": goal.goal_type,
                    "target_amount": goal.target_amount,
                    "current_amount": goal.current_amount,
                    "target_date": goal.target_date,
                    "status": goal.status,
                    "created_at": goal.created_at,
                    "updated_at": goal.updated_at
                }
                return GoalResponse(**goal_dict)
            return None
        except Exception as e:
            logger.error(f"Failed to update goal progress: {e}")
            raise
    
    # Advice operations
    def store_advice(self, customer_id: int, advice_type: str, content: str, 
                    agent_source: str, confidence_score: Optional[float] = None) -> AdviceResponse:
        """Store AI-generated advice."""
        try:
            advice_data = AdviceCreate(
                customer_id=customer_id,
                advice_type=advice_type,
                content=content,
                agent_source=agent_source,
                confidence_score=Decimal(str(confidence_score)) if confidence_score is not None else None
            )
            advice = self.db.create_advice(advice_data)
            logger.info(f"Stored advice for customer {customer_id} from {agent_source}")
            return AdviceResponse.from_orm(advice)
        except Exception as e:
            logger.error(f"Failed to store advice: {e}")
            raise
    
    def get_advice_history(self, customer_id: int, advice_type: Optional[str] = None) -> List[AdviceResponse]:
        """Get advice history for a customer."""
        try:
            advice_list = self.db.get_customer_advice(customer_id, advice_type)
            return [AdviceResponse.from_orm(a) for a in advice_list]
        except Exception as e:
            logger.error(f"Failed to get advice history: {e}")
            raise
    
    # Utility methods for agents
    def get_customer_context(self, customer_id: int) -> Dict[str, Any]:
        """Get comprehensive customer context for agents."""
        try:
            customer = self.get_customer_profile(customer_id=customer_id)
            if not customer:
                raise ValueError(f"Customer {customer_id} not found")
            
            transactions = self.get_customer_transactions(customer_id, limit=100)
            goals = self.get_customer_goals(customer_id, active_only=True)
            spending_analysis = self.get_spending_analysis(customer_id)
            recent_advice = self.get_advice_history(customer_id)[:10]  # Last 10 advice entries
            
            return {
                "customer": customer.model_dump(),
                "recent_transactions": [t.model_dump() for t in transactions],
                "active_goals": [g.model_dump() for g in goals],
                "spending_analysis": spending_analysis,
                "recent_advice": [a.model_dump() for a in recent_advice]
            }
        except Exception as e:
            logger.error(f"Failed to get customer context: {e}")
            raise


# Global MCP server instance
mcp_server = MCPServer()
