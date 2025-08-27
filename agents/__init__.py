"""
Agents module for the Financial Advisor AI system.

This module contains specialized AI agents that work together to provide
comprehensive financial advice:
- SpendingAnalyzerAgent: Analyzes spending patterns
- GoalPlannerAgent: Plans financial goals
- AdvisorAgent: Provides final recommendations
"""

from .base_agent import BaseAgent
from .spending_analyzer import SpendingAnalyzerAgent
from .goal_planner import GoalPlannerAgent
from .advisor import AdvisorAgent

__all__ = [
    "BaseAgent",
    "SpendingAnalyzerAgent", 
    "GoalPlannerAgent",
    "AdvisorAgent"
]
