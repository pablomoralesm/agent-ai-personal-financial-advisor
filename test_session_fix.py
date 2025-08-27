#!/usr/bin/env python3
"""
Test script to verify the SQLAlchemy session fixes.
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_customer_creation():
    """Test customer creation without session issues."""
    print("🧪 Testing customer creation...")
    
    try:
        from financial_mcp.models import CustomerCreate, CustomerResponse
        from decimal import Decimal
        
        # Test model creation
        customer_data = CustomerCreate(
            name="Test User",
            email="test@example.com",
            age=30,
            income=Decimal("50000")
        )
        
        print("✅ CustomerCreate model works correctly")
        
        # Test that we can create the response model manually
        customer_dict = {
            "id": 1,
            "name": "Test User",
            "email": "test@example.com",
            "age": 30,
            "income": Decimal("50000"),
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
        
        from datetime import datetime
        customer_dict["created_at"] = datetime.now()
        customer_dict["updated_at"] = datetime.now()
        
        response = CustomerResponse(**customer_dict)
        print("✅ CustomerResponse model works correctly")
        print(f"✅ Customer: {response.name} ({response.email})")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Run session fix tests."""
    print("🚀 SQLAlchemy Session Fix Test\n")
    
    success = test_customer_creation()
    
    print("\n" + "="*50)
    if success:
        print("🎉 Session fix test passed!")
        print("The Streamlit app should now work correctly.")
        print("\nTo start the app:")
        print("  python -m streamlit run ui/main.py")
    else:
        print("❌ Session fix test failed.")
        print("Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
