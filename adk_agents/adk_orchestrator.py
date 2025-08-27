"""
ADK-based Agent Orchestrator for the Financial Advisor AI system.

This orchestrator coordinates multiple ADK agents to provide comprehensive
financial analysis and advice through agent-to-agent collaboration.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

from google.adk import Agent
from financial_mcp.server import mcp_server
from financial_mcp.models import Advice, AdviceCreate
from .spending_analyzer_adk import spending_analyzer_adk
from .goal_planner_adk import goal_planner_adk
from .advisor_adk import advisor_adk


class ADKOrchestrator:
    """
    Orchestrator for coordinating ADK-based financial advisor agents.
    
    This class manages the workflow of multiple ADK agents working together
    to provide comprehensive financial advice through A2A (Agent-to-Agent) collaboration.
    """
    
    def __init__(self):
        """Initialize the ADK orchestrator."""
        self.spending_analyzer = spending_analyzer_adk
        self.goal_planner = goal_planner_adk
        self.advisor = advisor_adk
        
        # Workflow configuration
        self.workflow_config = {
            'parallel_execution': True,
            'timeout_seconds': 120,
            'retry_attempts': 2,
            'error_handling': 'graceful'
        }
    
    async def run_comprehensive_analysis(self, customer_id: int, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run comprehensive financial analysis using all ADK agents.
        
        Args:
            customer_id: ID of the customer to analyze
            context: Optional context for the analysis
            
        Returns:
            Dictionary containing comprehensive analysis results
        """
        workflow_start = datetime.now()
        
        try:
            # Validate customer exists
            try:
                customer = mcp_server.get_customer_by_id(customer_id)
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Customer not found: {str(e)}',
                    'workflow_id': f'adk_analysis_{customer_id}_{int(workflow_start.timestamp())}',
                    'timestamp': workflow_start.isoformat()
                }
            
            # Prepare workflow context
            workflow_context = {
                'customer_id': customer_id,
                'workflow_start': workflow_start.isoformat(),
                'orchestrator': 'ADKOrchestrator',
                'user_context': context or {}
            }
            
            # Step 1: Run spending analysis and goal analysis in parallel
            if self.workflow_config['parallel_execution']:
                spending_task = self._run_with_timeout(
                    self.spending_analyzer.analyze_spending,
                    customer_id, workflow_context
                )
                
                # Get goals for analysis
                goals_task = self._run_with_timeout(
                    self._analyze_customer_goals,
                    customer_id, workflow_context
                )
                
                # Execute in parallel
                spending_analysis, goals_analysis = await asyncio.gather(
                    spending_task, goals_task, return_exceptions=True
                )
                
                # Handle exceptions
                if isinstance(spending_analysis, Exception):
                    spending_analysis = {
                        'success': False,
                        'error': f'Spending analysis failed: {str(spending_analysis)}',
                        'agent_name': 'SpendingAnalyzerADK'
                    }
                
                if isinstance(goals_analysis, Exception):
                    goals_analysis = {
                        'success': False,
                        'error': f'Goals analysis failed: {str(goals_analysis)}',
                        'agent_name': 'GoalPlannerADK'
                    }
            else:
                # Sequential execution
                spending_analysis = await self._run_with_timeout(
                    self.spending_analyzer.analyze_spending,
                    customer_id, workflow_context
                )
                
                goals_analysis = await self._run_with_timeout(
                    self._analyze_customer_goals,
                    customer_id, workflow_context
                )
            
            # Step 2: Synthesize results using the advisor agent
            advisor_analysis = await self._run_with_timeout(
                self.advisor.provide_comprehensive_advice,
                customer_id, workflow_context
            )
            
            # Step 3: Create comprehensive results
            workflow_end = datetime.now()
            execution_time = (workflow_end - workflow_start).total_seconds()
            
            comprehensive_results = {
                'success': True,
                'workflow_id': f'adk_analysis_{customer_id}_{int(workflow_start.timestamp())}',
                'customer_id': customer_id,
                'execution_time_seconds': execution_time,
                'workflow_start': workflow_start.isoformat(),
                'workflow_end': workflow_end.isoformat(),
                'orchestrator': 'ADKOrchestrator',
                'framework': 'Google ADK',
                
                # Agent results
                'spending_analysis': spending_analysis,
                'goals_analysis': goals_analysis,
                'comprehensive_advice': advisor_analysis,
                
                # Workflow metadata
                'agents_executed': [
                    self.spending_analyzer.get_agent_info(),
                    self.goal_planner.get_agent_info(),
                    self.advisor.get_agent_info()
                ],
                'workflow_config': self.workflow_config
            }
            
            # Step 4: Store advice in database
            await self._store_advice_results(customer_id, comprehensive_results)
            
            return comprehensive_results
            
        except Exception as e:
            workflow_end = datetime.now()
            return {
                'success': False,
                'error': f'Workflow execution failed: {str(e)}',
                'workflow_id': f'adk_analysis_{customer_id}_{int(workflow_start.timestamp())}',
                'customer_id': customer_id,
                'workflow_start': workflow_start.isoformat(),
                'workflow_end': workflow_end.isoformat(),
                'execution_time_seconds': (workflow_end - workflow_start).total_seconds(),
                'orchestrator': 'ADKOrchestrator'
            }
    
    async def _analyze_customer_goals(self, customer_id: int, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze all customer goals using the goal planner agent.
        
        Args:
            customer_id: ID of the customer
            context: Workflow context
            
        Returns:
            Dictionary containing goals analysis results
        """
        try:
            goals = mcp_server.get_goals_by_customer(customer_id)
            
            if not goals:
                return {
                    'success': True,
                    'message': 'No goals found for analysis',
                    'goals_count': 0,
                    'agent_name': 'GoalPlannerADK'
                }
            
            goals_analysis = []
            
            # Analyze each goal
            for goal in goals:
                goal_data = {
                    'id': goal.id,
                    'title': goal.title,
                    'description': goal.description,
                    'target_amount': float(goal.target_amount),
                    'current_amount': float(goal.current_amount or 0),
                    'target_date': goal.target_date.isoformat() if goal.target_date else None,
                    'goal_type': goal.goal_type.value
                }
                
                analysis = self.goal_planner.analyze_goal(customer_id, goal_data, context)
                goals_analysis.append(analysis)
            
            return {
                'success': True,
                'goals_count': len(goals),
                'individual_analyses': goals_analysis,
                'agent_name': 'GoalPlannerADK'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Goals analysis failed: {str(e)}',
                'agent_name': 'GoalPlannerADK'
            }
    
    async def _run_with_timeout(self, func, *args) -> Any:
        """
        Run a function with timeout protection.
        
        Args:
            func: Function to execute
            *args: Arguments for the function
            
        Returns:
            Function result or raises TimeoutError
        """
        try:
            with ThreadPoolExecutor() as executor:
                future = executor.submit(func, *args)
                return await asyncio.wait_for(
                    asyncio.wrap_future(future),
                    timeout=self.workflow_config['timeout_seconds']
                )
        except asyncio.TimeoutError:
            raise TimeoutError(f"Function {func.__name__} timed out after {self.workflow_config['timeout_seconds']} seconds")
    
    async def _store_advice_results(self, customer_id: int, results: Dict[str, Any]) -> None:
        """
        Store advice results in the database.
        
        Args:
            customer_id: ID of the customer
            results: Comprehensive analysis results
        """
        try:
            # Extract key recommendations for storage
            recommendations = []
            
            # Add spending recommendations
            if results['spending_analysis'].get('success') and 'recommendations' in results['spending_analysis']:
                spending_recs = results['spending_analysis']['recommendations']
                if isinstance(spending_recs, list):
                    for rec in spending_recs[:3]:  # Top 3 recommendations
                        if isinstance(rec, dict) and 'action' in rec:
                            recommendations.append(f"Spending: {rec['action']}")
                        else:
                            recommendations.append(f"Spending: {str(rec)}")
            
            # Add advisor recommendations
            if results['comprehensive_advice'].get('success'):
                advice = results['comprehensive_advice']
                if 'prioritized_action_plan' in advice and isinstance(advice['prioritized_action_plan'], list):
                    for action in advice['prioritized_action_plan'][:3]:  # Top 3 actions
                        if isinstance(action, dict) and 'action' in action:
                            recommendations.append(f"Action: {action['action']}")
            
            # Create advice record
            advice_data = AdviceCreate(
                customer_id=customer_id,
                advice_text=json.dumps({
                    'summary': 'Comprehensive ADK-based financial analysis',
                    'recommendations': recommendations,
                    'workflow_id': results['workflow_id'],
                    'execution_time': results['execution_time_seconds'],
                    'framework': 'Google ADK'
                }),
                confidence_score=results['comprehensive_advice'].get('confidence_score', 0.7),
                recommendations=recommendations[:5]  # Store top 5 recommendations
            )
            
            # Store in database
            mcp_server.create_advice(advice_data)
            
        except Exception as e:
            # Log error but don't fail the entire workflow
            print(f"Warning: Failed to store advice results: {str(e)}")
    
    def run_analysis_sync(self, customer_id: int, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Synchronous wrapper for running comprehensive analysis.
        
        Args:
            customer_id: ID of the customer to analyze
            context: Optional context for the analysis
            
        Returns:
            Dictionary containing comprehensive analysis results
        """
        try:
            # Create new event loop if none exists
            try:
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    raise RuntimeError("Event loop is closed")
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Run the async analysis
            return loop.run_until_complete(
                self.run_comprehensive_analysis(customer_id, context)
            )
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Synchronous analysis execution failed: {str(e)}',
                'customer_id': customer_id,
                'timestamp': datetime.now().isoformat(),
                'orchestrator': 'ADKOrchestrator'
            }
    
    def get_orchestrator_info(self) -> Dict[str, Any]:
        """Get information about this ADK orchestrator."""
        return {
            'name': 'ADKOrchestrator',
            'description': 'Coordinates multiple ADK agents for comprehensive financial analysis',
            'version': '1.0.0',
            'framework': 'Google ADK',
            'managed_agents': [
                'SpendingAnalyzerADK',
                'GoalPlannerADK', 
                'AdvisorADK'
            ],
            'capabilities': [
                'Parallel agent execution',
                'Workflow orchestration',
                'A2A (Agent-to-Agent) coordination',
                'Error handling and recovery',
                'Result synthesis and storage'
            ],
            'workflow_config': self.workflow_config
        }


# Create a global instance for easy access
adk_orchestrator = ADKOrchestrator()
