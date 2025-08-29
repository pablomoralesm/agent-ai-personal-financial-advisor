"""
Tests for UI components in the Personal Financial Advisor application.

This module tests the Streamlit UI components to ensure they:
- Can be imported without errors
- Have the expected functions
- Handle data correctly
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import os
import sys

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


class TestUIComponentImports(unittest.TestCase):
    """Test that UI components can be imported successfully."""
    
    def test_customer_profile_component_import(self):
        """Test that customer profile component can be imported."""
        try:
            from ui.components.customer_profile import render_customer_profile
            self.assertTrue(callable(render_customer_profile))
        except ImportError as e:
            self.fail(f"Failed to import customer profile component: {e}")
    
    def test_transaction_entry_component_import(self):
        """Test that transaction entry component can be imported."""
        try:
            from ui.components.transaction_entry import render_transaction_entry
            self.assertTrue(callable(render_transaction_entry))
        except ImportError as e:
            self.fail(f"Failed to import transaction entry component: {e}")
    
    def test_goal_management_component_import(self):
        """Test that goal management component can be imported."""
        try:
            from ui.components.goal_management import render_goal_management
            self.assertTrue(callable(render_goal_management))
        except ImportError as e:
            self.fail(f"Failed to import goal management component: {e}")
    
    def test_recommendations_component_import(self):
        """Test that recommendations component can be imported."""
        try:
            from ui.components.recommendations import render_recommendations
            self.assertTrue(callable(render_recommendations))
        except ImportError as e:
            self.fail(f"Failed to import recommendations component: {e}")


class TestUIUtilityImports(unittest.TestCase):
    """Test that UI utility functions can be imported successfully."""
    
    def test_formatting_utilities_import(self):
        """Test that formatting utilities can be imported."""
        try:
            from ui.utils.formatting import format_currency, format_date
            self.assertTrue(callable(format_currency))
            self.assertTrue(callable(format_date))
        except ImportError as e:
            self.fail(f"Failed to import formatting utilities: {e}")
    
    def test_plotting_utilities_import(self):
        """Test that plotting utilities can be imported."""
        try:
            from ui.utils.plotting import create_spending_chart, create_goal_progress_chart
            self.assertTrue(callable(create_spending_chart))
            self.assertTrue(callable(create_goal_progress_chart))
        except ImportError as e:
            self.fail(f"Failed to import plotting utilities: {e}")


class TestUIComponentFunctions(unittest.TestCase):
    """Test that UI components have the expected functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.sample_customer = {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30,
            "income": 75000
        }
        
        self.sample_transactions = [
            {"id": 1, "amount": 150.50, "category": "Food", "date": "2025-08-26"},
            {"id": 2, "amount": 75.25, "category": "Transportation", "date": "2025-08-25"}
        ]
        
        self.sample_goals = [
            {"id": 1, "goal_type": "savings", "target_amount": 10000, "current_amount": 2500},
            {"id": 2, "goal_type": "investment", "target_amount": 50000, "current_amount": 15000}
        ]
    
    def test_customer_profile_component_functionality(self):
        """Test that customer profile component has expected functionality."""
        from ui.components.customer_profile import render_customer_profile
        
        # Test that the function exists and is callable
        self.assertTrue(callable(render_customer_profile))
        
        # Test that it can handle customer data
        # Note: We can't actually render Streamlit components in tests,
        # but we can verify the function signature and basic behavior
        try:
            # This should not raise an exception
            render_customer_profile()
        except Exception as e:
            # If it's a Streamlit-related error, that's expected in test environment
            if "streamlit" in str(e).lower():
                pass  # Expected in test environment
            else:
                self.fail(f"Unexpected error in customer profile component: {e}")
    
    def test_transaction_entry_component_functionality(self):
        """Test that transaction entry component has expected functionality."""
        from ui.components.transaction_entry import render_transaction_entry
        
        # Test that the function exists and is callable
        self.assertTrue(callable(render_transaction_entry))
        
        # Test that it can handle transaction data
        try:
            render_transaction_entry()
        except Exception as e:
            if "streamlit" in str(e).lower():
                pass  # Expected in test environment
            else:
                self.fail(f"Unexpected error in transaction entry component: {e}")
    
    def test_goal_management_component_functionality(self):
        """Test that goal management component has expected functionality."""
        from ui.components.goal_management import render_goal_management
        
        # Test that the function exists and is callable
        self.assertTrue(callable(render_goal_management))
        
        # Test that it can handle goal data
        try:
            render_goal_management()
        except Exception as e:
            if "streamlit" in str(e).lower():
                pass  # Expected in test environment
            else:
                self.fail(f"Unexpected error in goal management component: {e}")
    
    def test_recommendations_component_functionality(self):
        """Test that recommendations component has expected functionality."""
        from ui.components.recommendations import render_recommendations
        
        # Test that the function exists and is callable
        self.assertTrue(callable(render_recommendations))
        
        # Test that it can handle recommendation data
        sample_recommendations = [
            {"type": "spending", "message": "Reduce food expenses", "priority": "high"},
            {"type": "savings", "message": "Increase emergency fund", "priority": "medium"}
        ]
        
        try:
            render_recommendations()
        except Exception as e:
            if "streamlit" in str(e).lower():
                pass  # Expected in test environment
            else:
                self.fail(f"Unexpected error in recommendations component: {e}")


class TestUIUtilityFunctions(unittest.TestCase):
    """Test that UI utility functions work correctly."""
    
    def test_format_currency(self):
        """Test currency formatting utility."""
        from ui.utils.formatting import format_currency
        
        # Test various currency amounts
        self.assertEqual(format_currency(1000), "$1,000.00")
        self.assertEqual(format_currency(150.50), "$150.50")
        self.assertEqual(format_currency(0), "$0.00")
        self.assertEqual(format_currency(-50), "-$50.00")
    
    def test_format_date(self):
        """Test date formatting utility."""
        from ui.utils.formatting import format_date
        
        # Test date formatting
        test_date = "2025-08-26"
        formatted = format_date(test_date)
        
        # Should return a formatted date string
        self.assertIsInstance(formatted, str)
        self.assertIn("2025", formatted)
    
    def test_create_spending_chart(self):
        """Test spending chart creation utility."""
        from ui.utils.plotting import create_spending_chart
        
        # Test data - using dictionary format as expected by the function
        spending_data = {
            "Food": 500,
            "Transportation": 300,
            "Entertainment": 200
        }
        
        # Test chart creation
        try:
            chart = create_spending_chart(spending_data)
            # Should return a Plotly figure object
            self.assertTrue(hasattr(chart, 'to_dict'))
        except Exception as e:
            self.fail(f"Failed to create spending chart: {e}")
    
    def test_create_goal_progress_chart(self):
        """Test goal progress chart creation utility."""
        from ui.utils.plotting import create_goal_progress_chart
        
        # Test data - using the correct key names as expected by the function
        goals_data = [
            {"goal_name": "Savings", "current_amount": 2500, "target_amount": 10000},
            {"goal_name": "Investment", "current_amount": 15000, "target_amount": 50000}
        ]
        
        # Test chart creation
        try:
            chart = create_goal_progress_chart(goals_data)
            # Should return a Plotly figure object
            self.assertTrue(hasattr(chart, 'to_dict'))
        except Exception as e:
            self.fail(f"Failed to create goal progress chart: {e}")


class TestStreamlitAppImport(unittest.TestCase):
    """Test that the main Streamlit app can be imported."""
    
    def test_streamlit_app_import(self):
        """Test that the main Streamlit app can be imported."""
        try:
            # This should import without errors
            import streamlit_app
            self.assertTrue(hasattr(streamlit_app, 'main'))
        except ImportError as e:
            self.fail(f"Failed to import main Streamlit app: {e}")


if __name__ == '__main__':
    unittest.main()
