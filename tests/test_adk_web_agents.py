"""
Tests for ADK Web Multi-Agent System

This module tests the current ADK Web agents:
- Standalone Financial Advisor
- Sequencer Agent (Sequential Orchestrator)
- Orchestrator Agent (Intelligent Orchestrator)
- Spending Analyzer Agent
- Goal Planner Agent
- Advisor Agent

Part of the Agentic AI Personal Financial Advisor application.
"""

import unittest
import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class TestADKWebAgentDiscovery(unittest.TestCase):
    """Test that ADK Web agents can be discovered and imported."""
    
    def test_standalone_agent_import(self):
        """Test that Standalone Agent can be imported."""
        try:
            from adk_web_agents.standalone.agent import agent
            self.assertIsNotNone(agent)
            self.assertEqual(agent.name, "StandaloneFinancialAdvisor")
        except ImportError as e:
            self.fail(f"Failed to import Standalone Agent: {e}")
    
    def test_sequencer_agent_import(self):
        """Test that Sequencer Agent can be imported."""
        try:
            from adk_web_agents.sequencer.agent import agent
            self.assertIsNotNone(agent)
            self.assertEqual(agent.name, "SequencerAgent")
        except ImportError as e:
            self.fail(f"Failed to import Sequencer Agent: {e}")
    
    def test_orchestrator_agent_import(self):
        """Test that Orchestrator Agent can be imported."""
        try:
            from adk_web_agents.orchestrator.agent import agent
            self.assertIsNotNone(agent)
            self.assertEqual(agent.name, "OrchestratorAgent")
        except ImportError as e:
            self.fail(f"Failed to import Orchestrator Agent: {e}")
    
    def test_spending_analyzer_agent_import(self):
        """Test that Spending Analyzer Agent can be imported."""
        try:
            from adk_web_agents.spending_analyzer.agent import agent
            self.assertIsNotNone(agent)
            self.assertEqual(agent.name, "SpendingAnalyzerAgent")
        except ImportError as e:
            self.fail(f"Failed to import Spending Analyzer Agent: {e}")
    
    def test_goal_planner_agent_import(self):
        """Test that Goal Planner Agent can be imported."""
        try:
            from adk_web_agents.goal_planner.agent import agent
            self.assertIsNotNone(agent)
            self.assertEqual(agent.name, "GoalPlannerAgent")
        except ImportError as e:
            self.fail(f"Failed to import Goal Planner Agent: {e}")
    
    def test_advisor_agent_import(self):
        """Test that Advisor Agent can be imported."""
        try:
            from adk_web_agents.advisor.agent import agent
            self.assertIsNotNone(agent)
            self.assertEqual(agent.name, "AdvisorAgent")
        except ImportError as e:
            self.fail(f"Failed to import Advisor Agent: {e}")

class TestADKWebAgentStructure(unittest.TestCase):
    """Test the structure and configuration of ADK Web agents."""
    
    def test_standalone_agent_structure(self):
        """Test Standalone Agent structure."""
        from adk_web_agents.standalone.agent import agent
        
        # Test agent properties
        self.assertEqual(agent.name, "StandaloneFinancialAdvisor")
        self.assertIn("Pure MCP-only financial advisor", agent.description)
        self.assertEqual(agent.model, "gemini-2.0-flash-exp")
        self.assertIsNotNone(agent.tools)
        self.assertEqual(len(agent.tools), 1)  # Should have MCPToolset
    
    def test_sequencer_agent_structure(self):
        """Test Sequencer Agent structure."""
        from adk_web_agents.sequencer.agent import agent
        
        # Test agent properties
        self.assertEqual(agent.name, "SequencerAgent")
        self.assertIn("Sequential Financial Analysis Orchestrator", agent.description)
        self.assertIsNotNone(agent.sub_agents)
        self.assertEqual(len(agent.sub_agents), 3)  # Should have 3 sub-agents
    
    def test_orchestrator_agent_structure(self):
        """Test Orchestrator Agent structure."""
        from adk_web_agents.orchestrator.agent import agent
        
        # Test agent properties
        self.assertEqual(agent.name, "OrchestratorAgent")
        self.assertIn("Intelligent Financial Orchestrator", agent.description)
        self.assertEqual(agent.model, "gemini-2.0-flash-exp")
        self.assertIsNotNone(agent.tools)
        self.assertGreater(len(agent.tools), 1)  # Has MCPToolset + agent tools
    
    def test_spending_analyzer_agent_structure(self):
        """Test Spending Analyzer Agent structure."""
        from adk_web_agents.spending_analyzer.agent import agent
        
        # Test agent properties
        self.assertEqual(agent.name, "SpendingAnalyzerAgent")
        self.assertIn("Analyzes customer spending habits", agent.description)
        self.assertEqual(agent.model, "gemini-2.0-flash-exp")
        self.assertIsNotNone(agent.tools)
        self.assertEqual(len(agent.tools), 1)  # Should have MCPToolset
    
    def test_goal_planner_agent_structure(self):
        """Test Goal Planner Agent structure."""
        from adk_web_agents.goal_planner.agent import agent
        
        # Test agent properties
        self.assertEqual(agent.name, "GoalPlannerAgent")
        self.assertIn("Evaluates financial goal feasibility", agent.description)
        self.assertEqual(agent.model, "gemini-2.0-flash-exp")
        self.assertIsNotNone(agent.tools)
        self.assertEqual(len(agent.tools), 1)  # Should have MCPToolset
    
    def test_advisor_agent_structure(self):
        """Test Advisor Agent structure."""
        from adk_web_agents.advisor.agent import agent
        
        # Test agent properties
        self.assertEqual(agent.name, "AdvisorAgent")
        self.assertIn("Main financial advisor", agent.description)
        self.assertEqual(agent.model, "gemini-2.0-flash-exp")
        self.assertIsNotNone(agent.tools)
        self.assertEqual(len(agent.tools), 1)  # Should have MCPToolset

class TestADKWebAgentDescriptions(unittest.TestCase):
    """Test that agent descriptions are comprehensive and informative."""
    
    def test_standalone_agent_description(self):
        """Test Standalone Agent description content."""
        from adk_web_agents.standalone.agent import agent
        
        description = agent.description
        # Check for key concepts
        self.assertIn("Pure MCP-only financial advisor", description)
        self.assertIn("comprehensive analysis", description)
        self.assertIn("direct database tool access", description)
    
    def test_sequencer_agent_description(self):
        """Test Sequencer Agent description content."""
        from adk_web_agents.sequencer.agent import agent
        
        description = agent.description
        # Check for key concepts
        self.assertIn("Sequential Financial Analysis Orchestrator", description)
        self.assertIn("step-by-step", description)
        self.assertIn("Spending Analysis", description)
        self.assertIn("Goal Planning", description)
        self.assertIn("Advisory Services", description)
    
    def test_orchestrator_agent_description(self):
        """Test Orchestrator Agent description content."""
        from adk_web_agents.orchestrator.agent import agent
        
        description = agent.description
        # Check for key concepts
        self.assertIn("Intelligent Financial Orchestrator", description)
        self.assertIn("Intelligent Coordination", description)
        self.assertIn("dynamic", description)
        self.assertIn("Adaptive Approach", description)

class TestADKWebAgentMCPIntegration(unittest.TestCase):
    """Test MCP integration for ADK Web agents."""
    
    def test_standalone_agent_has_mcp_tools(self):
        """Test that Standalone Agent has MCP tools configured."""
        from adk_web_agents.standalone.agent import agent
        
        self.assertIsNotNone(agent.tools)
        self.assertEqual(len(agent.tools), 1)
        # Check that it's an MCPToolset
        tool = agent.tools[0]
        self.assertIsNotNone(tool)
    
    def test_sequencer_agent_has_sub_agents(self):
        """Test that Sequencer Agent has sub-agents configured."""
        from adk_web_agents.sequencer.agent import agent
        
        self.assertIsNotNone(agent.sub_agents)
        self.assertEqual(len(agent.sub_agents), 3)
        
        # Check sub-agent names
        sub_agent_names = [sub_agent.name for sub_agent in agent.sub_agents]
        self.assertIn("SpendingAnalyzerAgent", sub_agent_names)
        self.assertIn("GoalPlannerAgent", sub_agent_names)
        self.assertIn("AdvisorAgent", sub_agent_names)
    
    def test_orchestrator_agent_has_mcp_tools(self):
        """Test that Orchestrator Agent has MCP tools configured."""
        from adk_web_agents.orchestrator.agent import agent
        
        self.assertIsNotNone(agent.tools)
        self.assertGreater(len(agent.tools), 1)  # Has MCPToolset + agent tools
        # Check that it has tools
        for tool in agent.tools:
            self.assertIsNotNone(tool)

class TestADKWebAgentConsistency(unittest.TestCase):
    """Test consistency across ADK Web agents."""
    
    def test_all_agents_use_same_model(self):
        """Test that all agents use the same model."""
        from adk_web_agents.standalone.agent import agent as standalone_agent
        from adk_web_agents.orchestrator.agent import agent as orchestrator_agent
        from adk_web_agents.spending_analyzer.agent import agent as spending_agent
        from adk_web_agents.goal_planner.agent import agent as goal_agent
        from adk_web_agents.advisor.agent import agent as advisor_agent
        
        agents = [standalone_agent, orchestrator_agent, spending_agent, goal_agent, advisor_agent]
        models = [agent.model for agent in agents]
        
        # All should use the same model
        self.assertTrue(all(model == models[0] for model in models))
        self.assertEqual(models[0], "gemini-2.0-flash-exp")
    
    def test_all_agents_have_tools(self):
        """Test that all agents have tools configured."""
        from adk_web_agents.standalone.agent import agent as standalone_agent
        from adk_web_agents.orchestrator.agent import agent as orchestrator_agent
        from adk_web_agents.spending_analyzer.agent import agent as spending_agent
        from adk_web_agents.goal_planner.agent import agent as goal_agent
        from adk_web_agents.advisor.agent import agent as advisor_agent
        
        agents = [standalone_agent, orchestrator_agent, spending_agent, goal_agent, advisor_agent]
        
        for agent in agents:
            with self.subTest(agent=agent.name):
                self.assertIsNotNone(agent.tools)
                self.assertGreater(len(agent.tools), 0)
    
    def test_agent_names_are_unique(self):
        """Test that all agent names are unique."""
        from adk_web_agents.standalone.agent import agent as standalone_agent
        from adk_web_agents.sequencer.agent import agent as sequencer_agent
        from adk_web_agents.orchestrator.agent import agent as orchestrator_agent
        from adk_web_agents.spending_analyzer.agent import agent as spending_agent
        from adk_web_agents.goal_planner.agent import agent as goal_agent
        from adk_web_agents.advisor.agent import agent as advisor_agent
        
        names = [
            standalone_agent.name,
            sequencer_agent.name,
            orchestrator_agent.name,
            spending_agent.name,
            goal_agent.name,
            advisor_agent.name
        ]
        
        # All names should be unique
        self.assertEqual(len(names), len(set(names)))
        
        # Check specific names
        self.assertIn("StandaloneFinancialAdvisor", names)
        self.assertIn("SequencerAgent", names)
        self.assertIn("OrchestratorAgent", names)
        self.assertIn("SpendingAnalyzerAgent", names)
        self.assertIn("GoalPlannerAgent", names)
        self.assertIn("AdvisorAgent", names)

class TestADKWebAgentFiles(unittest.TestCase):
    """Test that all required ADK Web agent files exist."""
    
    def test_agent_directories_exist(self):
        """Test that all agent directories exist."""
        base_path = Path(__file__).parent.parent / "adk_web_agents"
        
        expected_dirs = [
            "standalone",
            "sequencer",
            "orchestrator",
            "spending_analyzer",
            "goal_planner",
            "advisor"
        ]
        
        for dir_name in expected_dirs:
            with self.subTest(directory=dir_name):
                dir_path = base_path / dir_name
                self.assertTrue(dir_path.exists(), f"Directory {dir_name} does not exist")
                self.assertTrue(dir_path.is_dir(), f"{dir_name} is not a directory")
    
    def test_agent_files_exist(self):
        """Test that all required agent files exist."""
        base_path = Path(__file__).parent.parent / "adk_web_agents"
        
        expected_files = [
            "standalone/__init__.py",
            "standalone/agent.py",
            "sequencer/__init__.py",
            "sequencer/agent.py",
            "orchestrator/__init__.py",
            "orchestrator/agent.py",
            "spending_analyzer/__init__.py",
            "spending_analyzer/agent.py",
            "goal_planner/__init__.py",
            "goal_planner/agent.py",
            "advisor/__init__.py",
            "advisor/agent.py",
            "README.md"
        ]
        
        for file_path in expected_files:
            with self.subTest(file=file_path):
                full_path = base_path / file_path
                self.assertTrue(full_path.exists(), f"File {file_path} does not exist")
                self.assertTrue(full_path.is_file(), f"{file_path} is not a file")
    
    def test_readme_exists_and_has_content(self):
        """Test that README exists and has meaningful content."""
        readme_path = Path(__file__).parent.parent / "adk_web_agents" / "README.md"
        
        self.assertTrue(readme_path.exists(), "README.md does not exist")
        
        with open(readme_path, 'r') as f:
            content = f.read()
        
        # Check for key sections
        self.assertIn("# ADK Web Multi-Agent System", content)
        self.assertIn("Architecture Overview", content)
        self.assertIn("Getting Started", content)
        self.assertIn("Agent Capabilities", content)

if __name__ == '__main__':
    unittest.main()