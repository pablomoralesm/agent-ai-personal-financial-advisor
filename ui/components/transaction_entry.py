"""
Transaction Entry component for the Streamlit UI.

Allows users to add new transactions and view transaction history.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

def render_transaction_entry():
    """Render the transaction entry and management interface."""
    if not st.session_state.get('customer_id'):
        st.warning("No customer selected")
        return
    
    # Create two columns: form and history
    col1, col2 = st.columns([1, 2])
    
    with col1:
        render_transaction_form()
    
    with col2:
        render_transaction_history()

def render_transaction_form():
    """Render the transaction entry form."""
    st.markdown("#### ➕ Add New Transaction")
    
    with st.form("transaction_form", clear_on_submit=True):
        # Transaction type
        transaction_type = st.selectbox(
            "Transaction Type *",
            options=["expense", "income"],
            format_func=lambda x: "💰 Income" if x == "income" else "💸 Expense",
            help="Select whether this is income or an expense"
        )
        
        # Amount
        amount = st.number_input(
            "Amount ($) *",
            min_value=0.01,
            max_value=100000.00,
            value=0.01,
            step=0.01,
            format="%.2f",
            help="Enter the transaction amount"
        )
        
        # Category
        categories = get_categories_for_type(transaction_type)
        category = st.selectbox(
            "Category *",
            options=categories,
            help="Select the appropriate category for this transaction"
        )
        
        # Subcategory (optional)
        subcategories = get_subcategories_for_category(category)
        subcategory = st.selectbox(
            "Subcategory",
            options=[""] + subcategories,
            help="Optional: Select a more specific subcategory"
        ) if subcategories else None
        
        # Description
        description = st.text_input(
            "Description",
            placeholder="Brief description of the transaction",
            help="Optional: Add a description to help remember this transaction"
        )
        
        # Date
        transaction_date = st.date_input(
            "Date *",
            value=date.today(),
            max_value=date.today(),
            help="Date when the transaction occurred"
        )
        
        # Payment method
        payment_methods = [
            "Cash", "Debit Card", "Credit Card", "Bank Transfer", 
            "Check", "Digital Wallet", "Direct Deposit", "Other"
        ]
        payment_method = st.selectbox(
            "Payment Method",
            options=[""] + payment_methods,
            help="Optional: How was this transaction paid?"
        )
        
        # Submit button
        submitted = st.form_submit_button(
            "💾 Add Transaction",
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            if amount > 0 and category:
                success = add_transaction(
                    customer_id=st.session_state.customer_id,
                    amount=amount,
                    category=category,
                    subcategory=subcategory if subcategory else None,
                    description=description if description else None,
                    transaction_date=transaction_date,
                    transaction_type=transaction_type,
                    payment_method=payment_method if payment_method else None
                )
                
                if success:
                    st.success("✅ Transaction added successfully!")
                    st.rerun()  # Refresh to show new transaction
                else:
                    st.error("❌ Failed to add transaction. Please try again.")
            else:
                st.error("❌ Please fill in all required fields (marked with *)")

def get_categories_for_type(transaction_type: str) -> List[str]:
    """Get categories based on transaction type."""
    if transaction_type == "income":
        return [
            "Salary",
            "Freelance", 
            "Investment Income",
            "Business Income",
            "Rental Income",
            "Other Income"
        ]
    else:  # expense
        return [
            "Housing",
            "Transportation", 
            "Food & Dining",
            "Healthcare",
            "Entertainment",
            "Shopping",
            "Education",
            "Savings & Investment",
            "Debt Payments",
            "Insurance",
            "Taxes",
            "Utilities",
            "Other Expenses"
        ]

def get_subcategories_for_category(category: str) -> List[str]:
    """Get subcategories for a given category."""
    subcategories_map = {
        # Income subcategories
        "Salary": ["Base Salary", "Overtime", "Bonus", "Commission"],
        "Freelance": ["Consulting", "Design Work", "Writing", "Programming"],
        "Investment Income": ["Dividends", "Interest", "Capital Gains", "Rental"],
        
        # Expense subcategories
        "Housing": ["Rent", "Mortgage", "Property Tax", "HOA Fees", "Maintenance", "Utilities"],
        "Transportation": ["Car Payment", "Gas", "Insurance", "Maintenance", "Public Transport", "Parking"],
        "Food & Dining": ["Groceries", "Restaurants", "Takeout", "Coffee", "Alcohol"],
        "Healthcare": ["Doctor Visits", "Dental", "Prescription", "Insurance", "Mental Health"],
        "Entertainment": ["Movies", "Streaming", "Games", "Sports", "Hobbies", "Travel"],
        "Shopping": ["Clothing", "Electronics", "Home Goods", "Personal Care", "Gifts"],
        "Education": ["Tuition", "Books", "Courses", "Training", "Supplies"],
        "Savings & Investment": ["Emergency Fund", "Retirement", "Stocks", "Bonds", "Real Estate"],
        "Debt Payments": ["Credit Cards", "Student Loans", "Personal Loans", "Mortgage"],
        "Insurance": ["Health", "Auto", "Home", "Life", "Disability"],
        "Utilities": ["Electric", "Gas", "Water", "Internet", "Phone", "Cable"]
    }
    
    return subcategories_map.get(category, [])

def add_transaction(
    customer_id: int,
    amount: float,
    category: str,
    transaction_date: date,
    transaction_type: str,
    subcategory: Optional[str] = None,
    description: Optional[str] = None,
    payment_method: Optional[str] = None
) -> bool:
    """Add a new transaction via database client."""
    try:
        # Import the database client functions
        from utils.database_client import add_transaction as db_add_transaction
        
        # Save transaction to database
        success = db_add_transaction(
            customer_id=customer_id,
            amount=amount,
            category=category,
            transaction_date=transaction_date.strftime('%Y-%m-%d'),
            transaction_type=transaction_type,
            subcategory=subcategory,
            description=description,
            payment_method=payment_method
        )
        
        if success:
            logger.info(f"Transaction saved successfully for customer {customer_id}")
            return True
        else:
            logger.error("Failed to save transaction to database")
            return False
            
    except Exception as e:
        logger.error(f"Error saving transaction: {e}")
        st.error(f"Failed to save transaction: {e}")
        return False

def render_transaction_history():
    """Render the transaction history table."""
    st.markdown("#### 📋 Recent Transactions")
    
    # Get transactions (mock data + any added via form)
    transactions = get_customer_transactions(st.session_state.customer_id)
    
    if not transactions:
        st.info("No transactions found. Add your first transaction using the form on the left!")
        return
    
    # Filter controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Date range filter
        date_range = st.selectbox(
            "📅 Time Period",
            options=["Last 30 days", "Last 3 months", "Last 6 months", "All time"],
            key="transaction_date_filter"
        )
    
    with col2:
        # Category filter
        all_categories = list(set(t['category'] for t in transactions))
        selected_categories = st.multiselect(
            "🏷️ Categories",
            options=all_categories,
            default=all_categories,
            key="transaction_category_filter"
        )
    
    with col3:
        # Transaction type filter
        transaction_types = st.multiselect(
            "💱 Type",
            options=["income", "expense"],
            default=["income", "expense"],
            format_func=lambda x: "💰 Income" if x == "income" else "💸 Expense",
            key="transaction_type_filter"
        )
    
    # Apply filters
    filtered_transactions = filter_transactions(
        transactions, date_range, selected_categories, transaction_types
    )
    
    if not filtered_transactions:
        st.warning("No transactions match the selected filters.")
        return
    
    # Display summary stats
    render_transaction_summary(filtered_transactions)
    
    # Convert to DataFrame for display
    df = pd.DataFrame(filtered_transactions)
    
    # Format the DataFrame
    if not df.empty:
        # Format date column
        df['transaction_date'] = pd.to_datetime(df['transaction_date']).dt.strftime('%Y-%m-%d')
        
        # Format amount with currency and color coding
        df['amount_display'] = df.apply(
            lambda row: f"${row['amount']:,.2f}" if row['transaction_type'] == 'expense' 
            else f"+${row['amount']:,.2f}", axis=1
        )
        
        # Select and reorder columns for display
        display_columns = ['transaction_date', 'category', 'subcategory', 'description', 'amount_display', 'payment_method']
        available_columns = [col for col in display_columns if col in df.columns]
        df_display = df[available_columns].copy()
        
        # Rename columns for better display
        column_names = {
            'transaction_date': 'Date',
            'category': 'Category', 
            'subcategory': 'Subcategory',
            'description': 'Description',
            'amount_display': 'Amount',
            'payment_method': 'Payment Method'
        }
        df_display = df_display.rename(columns=column_names)
        
        # Display the table
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Amount": st.column_config.TextColumn(
                    "Amount",
                    help="Transaction amount (+ for income, - for expenses)"
                ),
                "Date": st.column_config.DateColumn(
                    "Date",
                    help="Transaction date"
                )
            }
        )
        
        # Export option
        if st.button("📥 Export to CSV"):
            csv = df_display.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"transactions_customer_{st.session_state.customer_id}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

def get_customer_transactions(customer_id: int) -> List[Dict[str, Any]]:
    """Get transactions for a customer from database via database client."""
    try:
        # Import the database client functions
        from utils.database_client import get_transactions_by_customer
        
        # Get transactions from database
        transactions = get_transactions_by_customer(customer_id)
        
        logger.info(f"Retrieved {len(transactions)} transactions for customer {customer_id}")
        return transactions
            
    except Exception as e:
        logger.error(f"Error getting transactions: {e}")
        st.error(f"Failed to load transactions: {e}")
        return []

def filter_transactions(
    transactions: List[Dict[str, Any]], 
    date_range: str, 
    categories: List[str], 
    transaction_types: List[str]
) -> List[Dict[str, Any]]:
    """Filter transactions based on criteria."""
    filtered = transactions.copy()
    
    # Filter by date range
    if date_range != "All time":
        days_map = {
            "Last 30 days": 30,
            "Last 3 months": 90,
            "Last 6 months": 180
        }
        days = days_map.get(date_range, 30)
        cutoff_date = datetime.now() - timedelta(days=days)
        
        filtered = [
            t for t in filtered 
            if t.get('transaction_date') and (
                # Handle both string and date objects
                (isinstance(t['transaction_date'], str) and 
                 datetime.strptime(t['transaction_date'], '%Y-%m-%d').date() >= cutoff_date.date()) or
                (isinstance(t['transaction_date'], date) and 
                 t['transaction_date'] >= cutoff_date.date()) or
                (hasattr(t['transaction_date'], 'date') and 
                 t['transaction_date'].date() >= cutoff_date.date())
            )
        ]
    
    # Filter by categories
    if categories:
        filtered = [t for t in filtered if t.get('category') in categories]
    
    # Filter by transaction types
    if transaction_types:
        filtered = [t for t in filtered if t.get('transaction_type') in transaction_types]
    
    # Sort by date (newest first)
    def get_transaction_date(t):
        date_val = t.get('transaction_date')
        if isinstance(date_val, str):
            return datetime.strptime(date_val, '%Y-%m-%d').date()
        elif isinstance(date_val, date):
            return date_val
        elif hasattr(date_val, 'date'):
            return date_val.date()
        else:
            return date.min  # Default to earliest date if parsing fails
    
    filtered.sort(key=get_transaction_date, reverse=True)
    
    return filtered

def render_transaction_summary(transactions: List[Dict[str, Any]]):
    """Render summary statistics for filtered transactions."""
    if not transactions:
        return
    
    # Calculate summaries
    total_income = sum(t['amount'] for t in transactions if t['transaction_type'] == 'income')
    total_expenses = sum(t['amount'] for t in transactions if t['transaction_type'] == 'expense')
    net_amount = total_income - total_expenses
    transaction_count = len(transactions)
    
    # Display in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Total Income",
            value=f"${total_income:,.2f}",
            help="Total income in selected period"
        )
    
    with col2:
        st.metric(
            label="💸 Total Expenses", 
            value=f"${total_expenses:,.2f}",
            help="Total expenses in selected period"
        )
    
    with col3:
        st.metric(
            label="📊 Net Amount",
            value=f"${net_amount:,.2f}",
            delta="Positive" if net_amount >= 0 else "Negative",
            delta_color="normal" if net_amount >= 0 else "inverse",
            help="Income minus expenses"
        )
    
    with col4:
        st.metric(
            label="📝 Transactions",
            value=transaction_count,
            help="Total number of transactions"
        )
