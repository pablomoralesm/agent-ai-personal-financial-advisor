"""
Agent Coordinator for the Financial Advisor AI system.

This module orchestrates Agent-to-Agent (A2A) communication and coordinates
the execution of multiple agents to provide comprehensive financial advice.
"""

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
import uuid

from agents.base_agent import BaseAgent, AgentMessage, AgentResponse
from agents.spending_analyzer import spending_analyzer
from agents.goal_planner import goal_planner
from agents.advisor import advisor_agent

logger = logging.getLogger(__name__)


class WorkflowStatus(Enum):
    """Status of workflow execution."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class WorkflowStep:
    """Represents a step in an agent workflow."""
    step_id: str
    agent: BaseAgent
    depends_on: List[str]  # List of step IDs this step depends on
    request_data: Dict[str, Any]
    status: WorkflowStatus = WorkflowStatus.PENDING
    result: Optional[AgentResponse] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


@dataclass
class Workflow:
    """Represents a complete agent workflow."""
    workflow_id: str
    customer_id: int
    steps: List[WorkflowStep]
    status: WorkflowStatus = WorkflowStatus.PENDING
    created_at: datetime = None
    completed_at: Optional[datetime] = None
    results: Dict[str, AgentResponse] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.results is None:
            self.results = {}


class AgentCoordinator:
    """
    Coordinates the execution of multiple agents for comprehensive financial advice.
    
    Features:
    - Orchestrates agent execution workflows
    - Manages A2A communication
    - Handles dependencies between agents
    - Provides workflow status tracking
    - Supports both sequential and parallel execution
    """
    
    def __init__(self):
        """Initialize the agent coordinator."""
        self.agents = {
            "spending_analyzer": spending_analyzer,
            "goal_planner": goal_planner,
            "advisor": advisor_agent
        }
        self.active_workflows: Dict[str, Workflow] = {}
        self.logger = logging.getLogger("orchestrator.coordinator")
    
    def create_comprehensive_analysis_workflow(self, customer_id: int, 
                                             goal_info: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a workflow for comprehensive financial analysis.
        
        Args:
            customer_id: Customer ID to analyze
            goal_info: Optional goal information for planning
            
        Returns:
            Workflow ID for tracking
        """
        workflow_id = str(uuid.uuid4())
        
        # Define workflow steps
        steps = [
            WorkflowStep(
                step_id="spending_analysis",
                agent=self.agents["spending_analyzer"],
                depends_on=[],  # No dependencies
                request_data={"customer_id": customer_id}
            ),
            WorkflowStep(
                step_id="goal_planning",
                agent=self.agents["goal_planner"],
                depends_on=[],  # Can run in parallel with spending analysis
                request_data={
                    "customer_id": customer_id,
                    **(goal_info or {})
                }
            ),
            WorkflowStep(
                step_id="comprehensive_advice",
                agent=self.agents["advisor"],
                depends_on=["spending_analysis", "goal_planning"],  # Depends on both analyses
                request_data={"customer_id": customer_id}
            )
        ]
        
        workflow = Workflow(
            workflow_id=workflow_id,
            customer_id=customer_id,
            steps=steps
        )
        
        self.active_workflows[workflow_id] = workflow
        self.logger.info(f"Created comprehensive analysis workflow {workflow_id} for customer {customer_id}")
        
        return workflow_id
    
    def create_spending_analysis_workflow(self, customer_id: int) -> str:
        """Create a workflow for spending analysis only."""
        workflow_id = str(uuid.uuid4())
        
        steps = [
            WorkflowStep(
                step_id="spending_analysis",
                agent=self.agents["spending_analyzer"],
                depends_on=[],
                request_data={"customer_id": customer_id}
            )
        ]
        
        workflow = Workflow(
            workflow_id=workflow_id,
            customer_id=customer_id,
            steps=steps
        )
        
        self.active_workflows[workflow_id] = workflow
        self.logger.info(f"Created spending analysis workflow {workflow_id} for customer {customer_id}")
        
        return workflow_id
    
    def create_goal_planning_workflow(self, customer_id: int, goal_info: Dict[str, Any]) -> str:
        """Create a workflow for goal planning only."""
        workflow_id = str(uuid.uuid4())
        
        steps = [
            WorkflowStep(
                step_id="goal_planning",
                agent=self.agents["goal_planner"],
                depends_on=[],
                request_data={
                    "customer_id": customer_id,
                    **goal_info
                }
            )
        ]
        
        workflow = Workflow(
            workflow_id=workflow_id,
            customer_id=customer_id,
            steps=steps
        )
        
        self.active_workflows[workflow_id] = workflow
        self.logger.info(f"Created goal planning workflow {workflow_id} for customer {customer_id}")
        
        return workflow_id
    
    async def execute_workflow(self, workflow_id: str, 
                              progress_callback: Optional[Callable[[str, str, str], None]] = None) -> Dict[str, AgentResponse]:
        """
        Execute a workflow asynchronously.
        
        Args:
            workflow_id: ID of the workflow to execute
            progress_callback: Optional callback for progress updates (workflow_id, step_id, status)
            
        Returns:
            Dictionary of step results
        """
        if workflow_id not in self.active_workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.active_workflows[workflow_id]
        workflow.status = WorkflowStatus.RUNNING
        
        try:
            self.logger.info(f"Starting execution of workflow {workflow_id}")
            
            # Execute steps based on dependencies
            completed_steps = set()
            
            while len(completed_steps) < len(workflow.steps):
                # Find steps that can be executed (dependencies satisfied)
                ready_steps = []
                for step in workflow.steps:
                    if (step.status == WorkflowStatus.PENDING and 
                        all(dep in completed_steps for dep in step.depends_on)):
                        ready_steps.append(step)
                
                if not ready_steps:
                    # Check if we have failed steps blocking progress
                    failed_steps = [s for s in workflow.steps if s.status == WorkflowStatus.FAILED]
                    if failed_steps:
                        raise RuntimeError(f"Workflow blocked by failed steps: {[s.step_id for s in failed_steps]}")
                    else:
                        raise RuntimeError("Workflow deadlock: no ready steps but not all completed")
                
                # Execute ready steps (can be parallel)
                tasks = []
                for step in ready_steps:
                    task = self._execute_step(step, workflow, progress_callback)
                    tasks.append(task)
                
                # Wait for all ready steps to complete
                step_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Process results
                for i, result in enumerate(step_results):
                    step = ready_steps[i]
                    if isinstance(result, Exception):
                        step.status = WorkflowStatus.FAILED
                        step.error = str(result)
                        self.logger.error(f"Step {step.step_id} failed: {result}")
                    else:
                        step.status = WorkflowStatus.COMPLETED
                        step.result = result
                        workflow.results[step.step_id] = result
                        completed_steps.add(step.step_id)
                        self.logger.info(f"Step {step.step_id} completed successfully")
            
            workflow.status = WorkflowStatus.COMPLETED
            workflow.completed_at = datetime.utcnow()
            self.logger.info(f"Workflow {workflow_id} completed successfully")
            
            return workflow.results
            
        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            self.logger.error(f"Workflow {workflow_id} failed: {e}")
            raise
    
    async def _execute_step(self, step: WorkflowStep, workflow: Workflow, 
                          progress_callback: Optional[Callable[[str, str, str], None]]) -> AgentResponse:
        """Execute a single workflow step."""
        step.status = WorkflowStatus.RUNNING
        step.started_at = datetime.utcnow()
        
        if progress_callback:
            progress_callback(workflow.workflow_id, step.step_id, "running")
        
        try:
            # Prepare request data with dependencies' results
            request_data = step.request_data.copy()
            
            # Add results from dependency steps
            for dep_step_id in step.depends_on:
                if dep_step_id in workflow.results:
                    request_data[f"{dep_step_id}_result"] = workflow.results[dep_step_id]
                    # Also add the analysis data directly for easier access
                    if dep_step_id == "spending_analysis":
                        request_data["spending_analysis"] = workflow.results[dep_step_id].data
                    elif dep_step_id == "goal_planning":
                        request_data["goal_planning"] = workflow.results[dep_step_id].data
            
            # Execute the agent
            result = step.agent.process_request(workflow.customer_id, request_data)
            
            step.completed_at = datetime.utcnow()
            
            if progress_callback:
                progress_callback(workflow.workflow_id, step.step_id, "completed")
            
            # Send A2A message to dependent agents if needed
            await self._send_a2a_notifications(step, result, workflow)
            
            return result
            
        except Exception as e:
            step.error = str(e)
            if progress_callback:
                progress_callback(workflow.workflow_id, step.step_id, "failed")
            raise
    
    async def _send_a2a_notifications(self, completed_step: WorkflowStep, result: AgentResponse, 
                                    workflow: Workflow):
        """Send A2A notifications to other agents about completed analysis."""
        try:
            # Create message about completed analysis
            message = AgentMessage(
                sender=completed_step.agent.agent_name,
                recipient="all",  # Broadcast to all interested agents
                message_type="analysis_complete",
                content={
                    "customer_id": workflow.customer_id,
                    "step_id": completed_step.step_id,
                    "analysis_data": result.data,
                    "confidence_score": result.confidence_score
                },
                timestamp=datetime.utcnow(),
                correlation_id=workflow.workflow_id
            )
            
            # Send to relevant agents (in a real system, this might use a message queue)
            for agent_name, agent in self.agents.items():
                if agent != completed_step.agent:
                    try:
                        response = agent.handle_agent_message(message)
                        if response:
                            self.logger.info(f"Agent {agent_name} responded to A2A message from {completed_step.agent.agent_name}")
                    except Exception as e:
                        self.logger.warning(f"Agent {agent_name} failed to handle A2A message: {e}")
            
        except Exception as e:
            self.logger.error(f"Failed to send A2A notifications: {e}")
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get the current status of a workflow."""
        if workflow_id not in self.active_workflows:
            return {"error": f"Workflow {workflow_id} not found"}
        
        workflow = self.active_workflows[workflow_id]
        
        step_statuses = []
        for step in workflow.steps:
            step_status = {
                "step_id": step.step_id,
                "agent": step.agent.agent_name,
                "status": step.status.value,
                "depends_on": step.depends_on,
                "started_at": step.started_at.isoformat() if step.started_at else None,
                "completed_at": step.completed_at.isoformat() if step.completed_at else None,
                "error": step.error
            }
            step_statuses.append(step_status)
        
        return {
            "workflow_id": workflow_id,
            "customer_id": workflow.customer_id,
            "status": workflow.status.value,
            "created_at": workflow.created_at.isoformat(),
            "completed_at": workflow.completed_at.isoformat() if workflow.completed_at else None,
            "steps": step_statuses,
            "results_available": list(workflow.results.keys())
        }
    
    def get_workflow_results(self, workflow_id: str) -> Optional[Dict[str, AgentResponse]]:
        """Get the results of a completed workflow."""
        if workflow_id not in self.active_workflows:
            return None
        
        workflow = self.active_workflows[workflow_id]
        return workflow.results if workflow.status == WorkflowStatus.COMPLETED else None
    
    def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel a running workflow."""
        if workflow_id not in self.active_workflows:
            return False
        
        workflow = self.active_workflows[workflow_id]
        if workflow.status == WorkflowStatus.RUNNING:
            workflow.status = WorkflowStatus.CANCELLED
            self.logger.info(f"Workflow {workflow_id} cancelled")
            return True
        
        return False
    
    def cleanup_completed_workflows(self, max_age_hours: int = 24):
        """Clean up completed workflows older than specified hours."""
        cutoff_time = datetime.utcnow() - timedelta(hours=max_age_hours)
        
        to_remove = []
        for workflow_id, workflow in self.active_workflows.items():
            if (workflow.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED, WorkflowStatus.CANCELLED] and
                workflow.completed_at and workflow.completed_at < cutoff_time):
                to_remove.append(workflow_id)
        
        for workflow_id in to_remove:
            del self.active_workflows[workflow_id]
        
        if to_remove:
            self.logger.info(f"Cleaned up {len(to_remove)} old workflows")
    
    def get_agent_info(self) -> Dict[str, Dict[str, str]]:
        """Get information about available agents."""
        return {
            agent_name: {
                "name": agent.agent_name,
                "description": agent.agent_description,
                "available": True
            }
            for agent_name, agent in self.agents.items()
        }


# Global coordinator instance
agent_coordinator = AgentCoordinator()
