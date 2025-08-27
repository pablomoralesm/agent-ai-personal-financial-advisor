#!/usr/bin/env python3
"""
Simple import test for the Financial Advisor AI system.

This script tests that all modules can be imported correctly
without requiring database connections or API keys.
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all module imports."""
    print("🧪 Testing imports...")
    
    successes = []
    failures = []
    
    # Test basic imports
    tests = [
        ("Config modules", ["config.database", "config.gemini"]),
        ("MCP models", ["mcp.models"]),
        ("Agent base", ["agents.base_agent"]),
        ("Spending analyzer", ["agents.spending_analyzer"]),
        ("Goal planner", ["agents.goal_planner"]),
        ("Advisor agent", ["agents.advisor"]),
        ("UI utilities", ["ui.utils"]),
        ("Core libraries", ["streamlit", "pandas", "plotly", "sqlalchemy", "pydantic"])
    ]
    
    for test_name, modules in tests:
        try:
            for module in modules:
                __import__(module)
            print(f"✅ {test_name}: All imports successful")
            successes.append(test_name)
        except Exception as e:
            print(f"❌ {test_name}: {e}")
            failures.append((test_name, str(e)))
    
    # Test agent instantiation (without database)
    try:
        from agents.base_agent import AgentResponse
        from agents.spending_analyzer import SpendingAnalyzerAgent
        from agents.goal_planner import GoalPlannerAgent
        from agents.advisor import AdvisorAgent
        
        # Test that classes can be imported
        print("✅ Agent classes: Import successful")
        successes.append("Agent classes")
        
        # Test basic class instantiation
        print("ℹ️  Note: Agent initialization requires API keys")
        
    except Exception as e:
        print(f"❌ Agent classes: {e}")
        failures.append(("Agent classes", str(e)))
    
    # Test UI components
    try:
        from ui.utils import format_currency, get_transaction_categories
        
        # Test utility functions
        assert format_currency(1234.56) == "$1,234.56"
        categories = get_transaction_categories()
        assert len(categories) > 0
        
        print("✅ UI utilities: Functions working correctly")
        successes.append("UI utilities")
        
    except Exception as e:
        print(f"❌ UI utilities: {e}")
        failures.append(("UI utilities", str(e)))
    
    # Test model validation
    try:
        from financial_mcp.models import TransactionCategory, GoalType, CustomerCreate
        from decimal import Decimal
        
        # Test enum access
        categories = list(TransactionCategory)
        goal_types = list(GoalType)
        
        # Test model creation (without database)
        customer_data = {
            "name": "Test User",
            "email": "test@example.com",
            "age": 30,
            "income": Decimal("50000")
        }
        customer = CustomerCreate(**customer_data)
        
        print("✅ Data models: Validation working correctly")
        successes.append("Data models")
        
    except Exception as e:
        print(f"❌ Data models: {e}")
        failures.append(("Data models", str(e)))
    
    return successes, failures

def main():
    """Run import tests."""
    print("🚀 Financial Advisor AI - Import Test\n")
    
    successes, failures = test_imports()
    
    print("\n" + "="*50)
    print("📊 IMPORT TEST SUMMARY")
    print("="*50)
    
    print(f"\n✅ SUCCESSFUL ({len(successes)}):")
    for success in successes:
        print(f"   • {success}")
    
    if failures:
        print(f"\n❌ FAILED ({len(failures)}):")
        for name, error in failures:
            print(f"   • {name}: {error}")
    
    success_rate = len(successes) / (len(successes) + len(failures)) * 100
    print(f"\n📈 Success Rate: {success_rate:.1f}%")
    
    if len(failures) == 0:
        print("\n🎉 All imports successful! The application structure is ready.")
        print("\n📝 Next steps:")
        print("   1. Set up MySQL database")
        print("   2. Configure Google API key in .env file")
        print("   3. Run: streamlit run ui/main.py")
    else:
        print("\n⚠️  Some imports failed. Please check dependencies.")
    
    return len(failures) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
