"""
Input helper functions for better number input handling in Streamlit.
"""

import streamlit as st
from typing import Optional, Union


def number_input_text(label: str, value: float = 0.0, min_value: Optional[float] = None, 
                     max_value: Optional[float] = None, step: float = 1.0, 
                     format_str: str = "%.2f", key: Optional[str] = None) -> float:
    """
    Alternative number input using text input with validation.
    
    This sometimes works better than st.number_input when there are issues
    with typing in the number fields.
    """
    
    # Format the default value
    default_str = format_str % value
    
    # Create text input
    input_str = st.text_input(
        label, 
        value=default_str, 
        key=key,
        help=f"Enter a number. Min: {min_value if min_value is not None else 'None'}, Max: {max_value if max_value is not None else 'None'}"
    )
    
    try:
        # Try to convert to float
        number_value = float(input_str.replace('$', '').replace(',', '').strip())
        
        # Validate range
        if min_value is not None and number_value < min_value:
            st.error(f"Value must be at least {min_value}")
            return value
            
        if max_value is not None and number_value > max_value:
            st.error(f"Value must be at most {max_value}")
            return value
            
        return number_value
        
    except ValueError:
        st.error(f"Please enter a valid number")
        return value


def currency_input(label: str, value: float = 0.0, min_value: float = 0.0, 
                  key: Optional[str] = None) -> float:
    """Specialized currency input field."""
    return number_input_text(
        label=label,
        value=value,
        min_value=min_value,
        step=0.01,
        format_str="%.2f",
        key=key
    )


def integer_input(label: str, value: int = 0, min_value: Optional[int] = None,
                 max_value: Optional[int] = None, key: Optional[str] = None) -> int:
    """Specialized integer input field."""
    result = number_input_text(
        label=label,
        value=float(value),
        min_value=float(min_value) if min_value is not None else None,
        max_value=float(max_value) if max_value is not None else None,
        step=1.0,
        format_str="%.0f",
        key=key
    )
    return int(result)


def working_number_input(label: str, value: float = 0.0, min_value: Optional[float] = None,
                        max_value: Optional[float] = None, step: float = 1.0,
                        format_str: str = "%.2f", key: Optional[str] = None,
                        use_text_fallback: bool = False) -> float:
    """
    Number input with fallback to text input if there are issues.
    
    Args:
        use_text_fallback: If True, uses text input instead of number input
    """
    
    if use_text_fallback:
        return number_input_text(label, value, min_value, max_value, step, format_str, key)
    else:
        try:
            return st.number_input(
                label=label,
                min_value=min_value,
                max_value=max_value,
                value=value,
                step=step,
                format=format_str,
                key=key
            )
        except Exception as e:
            st.warning(f"Number input issue, using text input instead: {e}")
            return number_input_text(label, value, min_value, max_value, step, format_str, key)
