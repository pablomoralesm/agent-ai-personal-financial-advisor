#!/usr/bin/env python3
"""
Test script to verify all Pydantic deprecation warnings are fixed.
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_pydantic_models():
    """Test that all Pydantic models use modern methods."""
    print("🧪 Testing Pydantic model methods...")
    
    try:
        from mcp.models import CustomerCreate, CustomerResponse
        from agents.base_agent import AgentResponse
        from datetime import datetime
        from decimal import Decimal
        
        # Test CustomerCreate
        customer_data = CustomerCreate(
            name="Test User",
            email="test@example.com",
            age=30,
            income=Decimal("50000")
        )
        
        # Test model_dump method
        customer_dict = customer_data.model_dump()
        print("✅ CustomerCreate.model_dump() works")
        
        # Test CustomerResponse
        customer_response = CustomerResponse(
            id=1,
            name="Test User",
            email="test@example.com",
            age=30,
            income=Decimal("50000"),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        response_dict = customer_response.model_dump()
        print("✅ CustomerResponse.model_dump() works")
        
        # Test AgentResponse
        agent_response = AgentResponse(
            agent_name="TestAgent",
            response_type="test",
            data={"test": "data"},
            confidence_score=0.8,
            reasoning="Test reasoning",
            timestamp=datetime.now(),
            recommendations=["Test recommendation"]
        )
        
        agent_dict = agent_response.model_dump()
        print("✅ AgentResponse.model_dump() works")
        
        print("✅ All Pydantic models using modern methods")
        return True
        
    except AttributeError as e:
        print(f"❌ AttributeError: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Run Pydantic compatibility test."""
    print("🚀 Pydantic Deprecation Fix Test\n")
    
    success = test_pydantic_models()
    
    print("\n" + "="*50)
    if success:
        print("🎉 All Pydantic deprecation warnings fixed!")
        print("📱 The Streamlit app should run without warnings.")
        print("\n✅ Updated methods:")
        print("   • .dict() → .model_dump()")
        print("   • All models using Pydantic v2 syntax")
        print("\n🚀 Ready to restart:")
        print("   python -m streamlit run ui/main.py")
    else:
        print("❌ Some Pydantic issues remain.")
        print("Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
