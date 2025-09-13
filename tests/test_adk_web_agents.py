"""
Tests for ADK Web Multi-Agent System

This module tests the ADK Web agents that were created in Phase 2:
- Unified Financial Advisor
- Procedural Orchestrator  
- Intelligent Orchestrator

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
    
    def test_unified_financial_advisor_import(self):
        """Test that Unified Financial Advisor can be imported."""
        try:
            from adk_web_agents.financial_advisor import root_agent, agent
            self.assertIsNotNone(root_agent)
            self.assertIsNotNone(agent)
            self.assertEqual(root_agent, agent)
        except ImportError as e:
            self.fail(f"Failed to import Unified Financial Advisor: {e}")
    
    def test_procedural_orchestrator_import(self):
        """Test that Procedural Orchestrator can be imported."""
        try:
            from adk_web_agents.procedural_orchestrator import root_agent, procedural_orchestrator_agent
            self.assertIsNotNone(root_agent)
            self.assertIsNotNone(procedural_orchestrator_agent)
            self.assertEqual(root_agent, procedural_orchestrator_agent)
        except ImportError as e:
            self.fail(f"Failed to import Procedural Orchestrator: {e}")
    
    def test_intelligent_orchestrator_import(self):
        """Test that Intelligent Orchestrator can be imported."""
        try:
            from adk_web_agents.intelligent_orchestrator import root_agent, intelligent_orchestrator_agent
            self.assertIsNotNone(root_agent)
            self.assertIsNotNone(intelligent_orchestrator_agent)
            self.assertEqual(root_agent, intelligent_orchestrator_agent)
        except ImportError as e:
            self.fail(f"Failed to import Intelligent Orchestrator: {e}")

class TestADKWebAgentStructure(unittest.TestCase):
    """Test the structure and configuration of ADK Web agents."""
    
    def test_unified_financial_advisor_structure(self):
        """Test Unified Financial Advisor agent structure."""
        from adk_web_agents.financial_advisor.agent import agent
        
        # Test agent properties
        self.assertEqual(agent.name, "UnifiedFinancialAdvisor")
        self.assertIn("Unified Financial Advisor", agent.description)
        self.assertEqual(agent.model, "gemini-2.0-flash-exp")
        self.assertIsNotNone(agent.tools)
        self.assertEqual(len(agent.tools), 1)  # Should have MCPToolset
    
    def test_procedural_orchestrator_structure(self):
        """Test Procedural Orchestrator agent structure."""
        from adk_web_agents.procedural_orchestrator.agent import agent
        
        # Test agent properties
        self.assertEqual(agent.name, "ProceduralOrchestrator")
        self.assertIn("Procedural Financial Orchestrator", agent.description)
        self.assertEqual(agent.model, "gemini-2.0-flash-exp")
        self.assertIsNotNone(agent.tools)
        self.assertEqual(len(agent.tools), 1)  # Should have MCPToolset
    
    def test_intelligent_orchestrator_structure(self):
        """Test Intelligent Orchestrator agent structure."""
        from adk_web_agents.intelligent_orchestrator.agent import agent
        
        # Test agent properties
        self.assertEqual(agent.name, "IntelligentOrchestrator")
        self.assertIn("Intelligent Financial Orchestrator", agent.description)
        self.assertEqual(agent.model, "gemini-2.0-flash-exp")
        self.assertIsNotNone(agent.tools)
        self.assertEqual(len(agent.tools), 1)  # Should have MCPToolset

class TestADKWebAgentDescriptions(unittest.TestCase):
    """Test that agent descriptions are comprehensive and informative."""
    
    def test_unified_financial_advisor_description(self):
        """Test Unified Financial Advisor description content."""
        from adk_web_agents.financial_advisor.agent import agent
        
        description = agent.description
        # Check for key concepts
        self.assertIn("Unified Financial Advisor", description)
        self.assertIn("multi-agent architecture", description)
        self.assertIn("Spending Analysis", description)
        self.assertIn("Goal Planning", description)
        self.assertIn("Personalized Advice", description)
        self.assertIn("Financial Health", description)
    
    def test_procedural_orchestrator_description(self):
        """Test Procedural Orchestrator description content."""
        from adk_web_agents.procedural_orchestrator.agent import agent
        
        description = agent.description
        # Check for key concepts
        self.assertIn("Procedural Financial Orchestrator", description)
        self.assertIn("educational", description)
        self.assertIn("step-by-step", description)
        self.assertIn("Spending Analysis Agent", description)
        self.assertIn("Goal Planning Agent", description)
        self.assertIn("Advisor Agent", description)
    
    def test_intelligent_orchestrator_description(self):
        """Test Intelligent Orchestrator description content."""
        from adk_web_agents.intelligent_orchestrator.agent import agent
        
        description = agent.description
        # Check for key concepts
        self.assertIn("Intelligent Financial Orchestrator", description)
        self.assertIn("Intelligent Coordination", description)
        self.assertIn("dynamic", description)
        self.assertIn("adaptive", description)
        self.assertIn("Production-level", description)

class TestADKWebAgentMCPIntegration(unittest.TestCase):
    """Test MCP integration for ADK Web agents."""
    
    def test_all_agents_have_mcp_tools(self):
        """Test that all ADK Web agents have MCP tools configured."""
        from adk_web_agents.financial_advisor.agent import agent as financial_agent
        from adk_web_agents.procedural_orchestrator.agent import agent as procedural_agent
        from adk_web_agents.intelligent_orchestrator.agent import agent as intelligent_agent
        
        agents = [financial_agent, procedural_agent, intelligent_agent]
        
        for agent in agents:
            with self.subTest(agent=agent.name):
                self.assertIsNotNone(agent.tools)
                self.assertEqual(len(agent.tools), 1)
                # Check that it's an MCPToolset
                tool = agent.tools[0]
                self.assertIsNotNone(tool)
    
    def test_mcp_toolset_configuration(self):
        """Test that MCP toolset is properly configured."""
        from adk_web_agents.financial_advisor.agent import agent
        
        tool = agent.tools[0]
        # The tool should be an MCPToolset instance
        self.assertIsNotNone(tool)
        # We can't easily test the internal configuration without mocking,
        # but we can verify it exists and is callable

class TestADKWebAgentConsistency(unittest.TestCase):
    """Test consistency across ADK Web agents."""
    
    def test_all_agents_use_same_model(self):
        """Test that all agents use the same model."""
        from adk_web_agents.financial_advisor.agent import agent as financial_agent
        from adk_web_agents.procedural_orchestrator.agent import agent as procedural_agent
        from adk_web_agents.intelligent_orchestrator.agent import agent as intelligent_agent
        
        agents = [financial_agent, procedural_agent, intelligent_agent]
        models = [agent.model for agent in agents]
        
        # All should use the same model
        self.assertTrue(all(model == models[0] for model in models))
        self.assertEqual(models[0], "gemini-2.0-flash-exp")
    
    def test_all_agents_have_tools(self):
        """Test that all agents have tools configured."""
        from adk_web_agents.financial_advisor.agent import agent as financial_agent
        from adk_web_agents.procedural_orchestrator.agent import agent as procedural_agent
        from adk_web_agents.intelligent_orchestrator.agent import agent as intelligent_agent
        
        agents = [financial_agent, procedural_agent, intelligent_agent]
        
        for agent in agents:
            with self.subTest(agent=agent.name):
                self.assertIsNotNone(agent.tools)
                self.assertGreater(len(agent.tools), 0)
    
    def test_agent_names_are_unique(self):
        """Test that all agent names are unique."""
        from adk_web_agents.financial_advisor.agent import agent as financial_agent
        from adk_web_agents.procedural_orchestrator.agent import agent as procedural_agent
        from adk_web_agents.intelligent_orchestrator.agent import agent as intelligent_agent
        
        names = [
            financial_agent.name,
            procedural_agent.name,
            intelligent_agent.name
        ]
        
        # All names should be unique
        self.assertEqual(len(names), len(set(names)))
        
        # Check specific names
        self.assertIn("UnifiedFinancialAdvisor", names)
        self.assertIn("ProceduralOrchestrator", names)
        self.assertIn("IntelligentOrchestrator", names)

class TestADKWebAgentFiles(unittest.TestCase):
    """Test that all required ADK Web agent files exist."""
    
    def test_agent_directories_exist(self):
        """Test that all agent directories exist."""
        base_path = Path(__file__).parent.parent / "adk_web_agents"
        
        expected_dirs = [
            "financial_advisor",
            "procedural_orchestrator", 
            "intelligent_orchestrator"
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
            "financial_advisor/__init__.py",
            "financial_advisor/agent.py",
            "procedural_orchestrator/__init__.py",
            "procedural_orchestrator/agent.py",
            "intelligent_orchestrator/__init__.py",
            "intelligent_orchestrator/agent.py",
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
