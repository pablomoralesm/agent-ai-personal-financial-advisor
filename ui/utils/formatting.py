"""
Formatting utilities for the Streamlit UI.

Provides common formatting functions for financial data display.
"""

from typing import Union, Optional
from datetime import datetime, date
import locale

def format_currency(
    amount: Union[float, int], 
    currency_symbol: str = "$",
    include_cents: bool = True,
    negative_in_parentheses: bool = False
) -> str:
    """
    Format a number as currency.
    
    Args:
        amount: The amount to format
        currency_symbol: Currency symbol to use
        include_cents: Whether to include cents in the formatting
        negative_in_parentheses: Whether to show negative amounts in parentheses
        
    Returns:
        Formatted currency string
    """
    if amount is None:
        return "N/A"
    
    # Handle negative amounts
    is_negative = amount < 0
    abs_amount = abs(amount)
    
    # Format the number
    if include_cents:
        formatted = f"{abs_amount:,.2f}"
    else:
        formatted = f"{abs_amount:,.0f}"
    
    # Add currency symbol
    currency_str = f"{currency_symbol}{formatted}"
    
    # Handle negative formatting
    if is_negative:
        if negative_in_parentheses:
            currency_str = f"({currency_str})"
        else:
            currency_str = f"-{currency_str}"
    
    return currency_str

def format_percentage(
    value: Union[float, int],
    decimal_places: int = 1,
    include_sign: bool = False
) -> str:
    """
    Format a number as a percentage.
    
    Args:
        value: The value to format (as decimal, e.g., 0.15 for 15%)
        decimal_places: Number of decimal places to show
        include_sign: Whether to include + sign for positive values
        
    Returns:
        Formatted percentage string
    """
    if value is None:
        return "N/A"
    
    percentage = value * 100
    formatted = f"{percentage:.{decimal_places}f}%"
    
    if include_sign and value > 0:
        formatted = f"+{formatted}"
    
    return formatted

def format_large_number(
    number: Union[float, int],
    precision: int = 1
) -> str:
    """
    Format large numbers with K, M, B suffixes.
    
    Args:
        number: The number to format
        precision: Number of decimal places for abbreviated numbers
        
    Returns:
        Formatted number string
    """
    if number is None:
        return "N/A"
    
    abs_number = abs(number)
    sign = "-" if number < 0 else ""
    
    if abs_number >= 1_000_000_000:
        formatted = f"{sign}{abs_number / 1_000_000_000:.{precision}f}B"
    elif abs_number >= 1_000_000:
        formatted = f"{sign}{abs_number / 1_000_000:.{precision}f}M"
    elif abs_number >= 1_000:
        formatted = f"{sign}{abs_number / 1_000:.{precision}f}K"
    else:
        formatted = f"{sign}{abs_number:.0f}"
    
    return formatted

def format_date(
    date_value: Union[datetime, date, str],
    format_string: str = "%Y-%m-%d"
) -> str:
    """
    Format a date value.
    
    Args:
        date_value: Date to format
        format_string: Format string for the date
        
    Returns:
        Formatted date string
    """
    if date_value is None:
        return "N/A"
    
    if isinstance(date_value, str):
        try:
            date_value = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
        except ValueError:
            return date_value  # Return as-is if parsing fails
    
    if isinstance(date_value, datetime):
        return date_value.strftime(format_string)
    elif isinstance(date_value, date):
        return date_value.strftime(format_string)
    
    return str(date_value)

def format_time_period(days: int) -> str:
    """
    Format a number of days into a human-readable time period.
    
    Args:
        days: Number of days
        
    Returns:
        Formatted time period string
    """
    if days is None or days < 0:
        return "N/A"
    
    if days == 0:
        return "Today"
    elif days == 1:
        return "1 day"
    elif days < 7:
        return f"{days} days"
    elif days < 30:
        weeks = days // 7
        remaining_days = days % 7
        if weeks == 1:
            week_str = "1 week"
        else:
            week_str = f"{weeks} weeks"
        
        if remaining_days == 0:
            return week_str
        elif remaining_days == 1:
            return f"{week_str}, 1 day"
        else:
            return f"{week_str}, {remaining_days} days"
    elif days < 365:
        months = days // 30
        remaining_days = days % 30
        if months == 1:
            month_str = "1 month"
        else:
            month_str = f"{months} months"
        
        if remaining_days < 7:
            return month_str
        else:
            weeks = remaining_days // 7
            if weeks == 1:
                return f"{month_str}, 1 week"
            else:
                return f"{month_str}, {weeks} weeks"
    else:
        years = days // 365
        remaining_days = days % 365
        if years == 1:
            year_str = "1 year"
        else:
            year_str = f"{years} years"
        
        if remaining_days < 30:
            return year_str
        else:
            months = remaining_days // 30
            if months == 1:
                return f"{year_str}, 1 month"
            else:
                return f"{year_str}, {months} months"

def format_financial_ratio(
    numerator: Union[float, int],
    denominator: Union[float, int],
    as_percentage: bool = True,
    decimal_places: int = 1
) -> str:
    """
    Format a financial ratio.
    
    Args:
        numerator: Numerator of the ratio
        denominator: Denominator of the ratio
        as_percentage: Whether to format as percentage
        decimal_places: Number of decimal places
        
    Returns:
        Formatted ratio string
    """
    if denominator is None or denominator == 0:
        return "N/A"
    
    if numerator is None:
        return "N/A"
    
    ratio = numerator / denominator
    
    if as_percentage:
        return format_percentage(ratio, decimal_places)
    else:
        return f"{ratio:.{decimal_places}f}"

def format_goal_status(
    current_amount: Union[float, int],
    target_amount: Union[float, int],
    target_date: Optional[Union[datetime, date, str]] = None
) -> dict:
    """
    Format goal status information.
    
    Args:
        current_amount: Current amount saved
        target_amount: Target amount for the goal
        target_date: Target date for the goal
        
    Returns:
        Dictionary with formatted goal status information
    """
    if target_amount is None or target_amount <= 0:
        return {
            'progress_percentage': "N/A",
            'remaining_amount': "N/A",
            'status': "Invalid target"
        }
    
    current = current_amount or 0
    progress = (current / target_amount) * 100
    remaining = target_amount - current
    
    # Determine status
    if progress >= 100:
        status = "Completed ✅"
    elif progress >= 75:
        status = "On Track 🟢"
    elif progress >= 50:
        status = "Making Progress 🟡"
    elif progress >= 25:
        status = "Behind Schedule 🟠"
    else:
        status = "Needs Attention 🔴"
    
    # Calculate time-based status if target date provided
    time_status = ""
    if target_date:
        if isinstance(target_date, str):
            try:
                target_date = datetime.fromisoformat(target_date.replace('Z', '+00:00')).date()
            except ValueError:
                target_date = None
        
        if target_date:
            days_remaining = (target_date - date.today()).days
            if days_remaining < 0:
                time_status = " (Overdue)"
            elif days_remaining == 0:
                time_status = " (Due Today)"
            else:
                time_status = f" ({format_time_period(days_remaining)} remaining)"
    
    return {
        'progress_percentage': f"{progress:.1f}%",
        'remaining_amount': format_currency(remaining),
        'status': status + time_status,
        'progress_decimal': progress / 100
    }

def format_savings_rate_assessment(savings_rate: float) -> dict:
    """
    Format savings rate with assessment.
    
    Args:
        savings_rate: Savings rate as percentage (e.g., 15.5 for 15.5%)
        
    Returns:
        Dictionary with formatted savings rate and assessment
    """
    if savings_rate is None:
        return {
            'formatted_rate': "N/A",
            'assessment': "Unknown",
            'color': "gray"
        }
    
    formatted_rate = f"{savings_rate:.1f}%"
    
    if savings_rate >= 20:
        assessment = "Excellent"
        color = "green"
    elif savings_rate >= 15:
        assessment = "Good"
        color = "lightgreen"
    elif savings_rate >= 10:
        assessment = "Fair"
        color = "orange"
    elif savings_rate >= 5:
        assessment = "Below Target"
        color = "red"
    else:
        assessment = "Critical"
        color = "darkred"
    
    return {
        'formatted_rate': formatted_rate,
        'assessment': assessment,
        'color': color
    }

def format_spending_category_analysis(
    amount: Union[float, int],
    total_spending: Union[float, int],
    recommended_percentage: Optional[float] = None
) -> dict:
    """
    Format spending category analysis.
    
    Args:
        amount: Amount spent in category
        total_spending: Total spending amount
        recommended_percentage: Recommended percentage for this category
        
    Returns:
        Dictionary with formatted analysis
    """
    if total_spending is None or total_spending <= 0:
        return {
            'amount': format_currency(amount or 0),
            'percentage': "N/A",
            'status': "Unknown"
        }
    
    current_amount = amount or 0
    percentage = (current_amount / total_spending) * 100
    
    status = "Normal"
    color = "green"
    
    if recommended_percentage:
        if percentage > recommended_percentage * 1.2:  # 20% over recommended
            status = "High"
            color = "red"
        elif percentage > recommended_percentage * 1.1:  # 10% over recommended
            status = "Above Average"
            color = "orange"
        elif percentage < recommended_percentage * 0.8:  # 20% below recommended
            status = "Low"
            color = "blue"
    
    return {
        'amount': format_currency(current_amount),
        'percentage': f"{percentage:.1f}%",
        'status': status,
        'color': color,
        'recommended': f"{recommended_percentage:.1f}%" if recommended_percentage else None
    }

def format_emergency_fund_assessment(
    emergency_fund: Union[float, int],
    monthly_expenses: Union[float, int]
) -> dict:
    """
    Format emergency fund assessment.
    
    Args:
        emergency_fund: Current emergency fund amount
        monthly_expenses: Monthly expenses amount
        
    Returns:
        Dictionary with formatted assessment
    """
    if monthly_expenses is None or monthly_expenses <= 0:
        return {
            'amount': format_currency(emergency_fund or 0),
            'months_covered': "N/A",
            'status': "Unknown"
        }
    
    fund_amount = emergency_fund or 0
    months_covered = fund_amount / monthly_expenses
    
    if months_covered >= 6:
        status = "Excellent"
        color = "green"
    elif months_covered >= 3:
        status = "Good"
        color = "lightgreen"
    elif months_covered >= 1:
        status = "Minimal"
        color = "orange"
    else:
        status = "Critical"
        color = "red"
    
    return {
        'amount': format_currency(fund_amount),
        'months_covered': f"{months_covered:.1f} months",
        'status': status,
        'color': color
    }
