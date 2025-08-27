"""
ADK-based Advisor Agent for the Financial Advisor AI system.

This agent uses Google's Agent Development Kit (ADK) to synthesize inputs 
from other agents and provide comprehensive financial recommendations.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from google.adk import Agent
from financial_mcp.server import mcp_server
from .spending_analyzer_adk import spending_analyzer_adk
from .goal_planner_adk import goal_planner_adk


class AdvisorADK:
    """
    ADK-based agent for providing comprehensive financial advice.
    
    This implementation uses Google's Agent Development Kit to synthesize
    analysis from other ADK agents and provide holistic financial guidance.
    """
    
    def __init__(self):
        """Initialize the ADK-based advisor agent."""
        
        # Define the system prompt for comprehensive financial advising
        self.system_prompt = """
You are a Comprehensive Financial Advisor AI assistant. Your role is to synthesize spending analysis and goal planning data to provide holistic financial advice.

Your advice should include:
1. Overall financial health assessment
2. Prioritized action plan with specific steps
3. Short-term and long-term recommendations
4. Risk assessment and mitigation strategies
5. Behavioral insights and motivation strategies
6. Follow-up schedule and monitoring plan

Guidelines:
- Provide actionable, specific advice
- Consider the customer's complete financial picture
- Prioritize recommendations by impact and feasibility
- Be encouraging while being realistic
- Address both immediate concerns and long-term planning
- Use motivational language that empowers the customer
- Consider psychological aspects of financial behavior
- Balance conservative advice with growth opportunities

Output Format:
Provide your comprehensive advice as a JSON object with the following structure:
{
    "overall_assessment": {
        "financial_health_score": number,
        "key_strengths": ["string"],
        "primary_concerns": ["string"],
        "summary": "string"
    },
    "prioritized_action_plan": [
        {
            "priority": number,
            "action": "string",
            "category": "spending|saving|investment|goal",
            "timeline": "immediate|short_term|long_term",
            "expected_impact": "string",
            "difficulty": "easy|moderate|challenging"
        }
    ],
    "recommendations": {
        "immediate_actions": ["string"],
        "short_term_goals": ["string"],
        "long_term_strategy": ["string"],
        "risk_mitigation": ["string"]
    },
    "behavioral_insights": {
        "spending_patterns": "string",
        "goal_setting_approach": "string",
        "suggested_improvements": ["string"]
    },
    "monitoring_plan": {
        "review_frequency": "string",
        "key_metrics_to_track": ["string"],
        "warning_signs": ["string"],
        "success_milestones": ["string"]
    },
    "motivation_strategy": {
        "key_motivators": ["string"],
        "potential_obstacles": ["string"],
        "success_reinforcement": ["string"]
    },
    "confidence_score": number,
    "next_review_date": "ISO date string"
}
"""
        
        # Create the ADK agent
        self.agent = Agent(
            name="financial_advisor",
            model="gemini-1.5-flash",
            description="Provides comprehensive financial advice by synthesizing analysis from other agents",
            instruction=self.system_prompt,
            tools=[]  # We'll handle coordination with other agents separately
        )
    
    def provide_comprehensive_advice(self, customer_id: int, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Provide comprehensive financial advice by coordinating with other ADK agents.
        
        Args:
            customer_id: ID of the customer
            context: Optional additional context for the advice
            
        Returns:
            Dictionary containing comprehensive financial advice
        """
        try:
            # Get basic customer information
            try:
                customer = mcp_server.get_customer_by_id(customer_id)
                customer_info = {
                    'id': customer.id,
                    'name': customer.name,
                    'age': customer.age,
                    'income': float(customer.income)
                }
            except Exception:
                customer_info = {'id': customer_id, 'note': 'Customer details not available'}
            
            # Get spending analysis from SpendingAnalyzerADK
            spending_analysis = spending_analyzer_adk.analyze_spending(customer_id, context)
            
            # Get goal analysis from GoalPlannerADK (for existing goals)
            goals_analysis = []
            try:
                goals = mcp_server.get_goals_by_customer(customer_id)
                for goal in goals[:3]:  # Analyze top 3 goals to avoid overwhelming the prompt
                    goal_data = {
                        'title': goal.title,
                        'target_amount': float(goal.target_amount),
                        'current_amount': float(goal.current_amount or 0),
                        'target_date': goal.target_date.isoformat() if goal.target_date else None,
                        'goal_type': goal.goal_type.value
                    }
                    goal_analysis = goal_planner_adk.analyze_goal(customer_id, goal_data, context)
                    goals_analysis.append(goal_analysis)
            except Exception as e:
                goals_analysis = [{'error': f'Could not analyze goals: {str(e)}'}]
            
            # Prepare comprehensive analysis prompt
            advice_prompt = f"""
Please provide comprehensive financial advice for customer ID {customer_id} based on the following analysis:

Customer Information:
{json.dumps(customer_info, indent=2)}

Spending Analysis Results:
{json.dumps(spending_analysis, indent=2)}

Goal Planning Analysis Results:
{json.dumps(goals_analysis, indent=2)}

Additional Context:
{json.dumps(context or {}, indent=2)}

Please synthesize all this information to provide holistic financial advice that addresses the customer's complete financial picture. Consider both the spending patterns and goal planning results to create a comprehensive action plan.

Follow the specified JSON format for your response.
"""
            
            # Use ADK agent to generate comprehensive advice
            response = self.agent.run(advice_prompt)
            
            # Parse the response
            try:
                # Extract JSON from response if it's wrapped in text
                response_text = str(response)
                if '{' in response_text and '}' in response_text:
                    json_start = response_text.find('{')
                    json_end = response_text.rfind('}') + 1
                    json_str = response_text[json_start:json_end]
                    advice_result = json.loads(json_str)
                else:
                    # If no JSON found, wrap the response
                    advice_result = {
                        'overall_assessment': {'summary': response_text},
                        'prioritized_action_plan': [],
                        'recommendations': {},
                        'confidence_score': 0.5
                    }
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                advice_result = {
                    'overall_assessment': {'summary': str(response)},
                    'prioritized_action_plan': [],
                    'recommendations': {},
                    'confidence_score': 0.5
                }
            
            # Add metadata and source data
            advice_result.update({
                'success': True,
                'agent_name': 'AdvisorADK',
                'customer_id': customer_id,
                'advice_date': datetime.now().isoformat(),
                'source_analyses': {
                    'spending_analysis_success': spending_analysis.get('success', False),
                    'goals_analyzed': len(goals_analysis),
                    'framework': 'Google ADK'
                }
            })
            
            return advice_result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Comprehensive advice generation failed: {str(e)}",
                'agent_name': 'AdvisorADK',
                'customer_id': customer_id,
                'timestamp': datetime.now().isoformat()
            }
    
    def synthesize_agent_outputs(self, spending_analysis: Dict[str, Any], goal_analysis: Dict[str, Any], 
                                customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesize outputs from different agents into coherent advice.
        
        Args:
            spending_analysis: Results from spending analyzer
            goal_analysis: Results from goal planner
            customer_data: Customer information
            
        Returns:
            Dictionary containing synthesized advice
        """
        try:
            synthesis_prompt = f"""
Synthesize the following agent analyses into coherent, comprehensive financial advice:

Customer Data:
{json.dumps(customer_data, indent=2)}

Spending Analysis:
{json.dumps(spending_analysis, indent=2)}

Goal Analysis:
{json.dumps(goal_analysis, indent=2)}

Focus on:
1. Identifying connections between spending patterns and goal achievement
2. Resolving any conflicts between recommendations
3. Creating a unified action plan
4. Prioritizing recommendations based on impact and feasibility

Provide your synthesis following the specified JSON format.
"""
            
            response = self.agent.run(synthesis_prompt)
            
            # Parse the response (similar to other methods)
            try:
                response_text = str(response)
                if '{' in response_text and '}' in response_text:
                    json_start = response_text.find('{')
                    json_end = response_text.rfind('}') + 1
                    json_str = response_text[json_start:json_end]
                    synthesis_result = json.loads(json_str)
                else:
                    synthesis_result = {
                        'overall_assessment': {'summary': response_text},
                        'prioritized_action_plan': [],
                        'recommendations': {},
                        'confidence_score': 0.5
                    }
            except json.JSONDecodeError:
                synthesis_result = {
                    'overall_assessment': {'summary': str(response)},
                    'prioritized_action_plan': [],
                    'recommendations': {},
                    'confidence_score': 0.5
                }
            
            synthesis_result.update({
                'success': True,
                'agent_name': 'AdvisorADK',
                'synthesis_date': datetime.now().isoformat(),
                'method': 'agent_output_synthesis'
            })
            
            return synthesis_result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Synthesis failed: {str(e)}",
                'agent_name': 'AdvisorADK',
                'timestamp': datetime.now().isoformat()
            }
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about this ADK agent."""
        return {
            'name': 'AdvisorADK',
            'description': 'ADK-based agent for comprehensive financial advice synthesis',
            'version': '1.0.0',
            'capabilities': [
                'Multi-agent coordination',
                'Comprehensive advice synthesis',
                'Prioritized action planning',
                'Behavioral insights',
                'Risk assessment',
                'Monitoring strategy development'
            ],
            'model': 'gemini-1.5-flash',
            'framework': 'Google ADK',
            'coordinates_with': ['SpendingAnalyzerADK', 'GoalPlannerADK']
        }


# Create a global instance for easy access
advisor_adk = AdvisorADK()
