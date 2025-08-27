"""
Plotting utilities for the Streamlit UI.

Provides common chart and visualization functions using Plotly.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, Any, List, Optional
import numpy as np

def create_spending_chart(spending_data: Dict[str, float], chart_type: str = 'pie') -> go.Figure:
    """
    Create a spending breakdown chart.
    
    Args:
        spending_data: Dictionary of category -> amount
        chart_type: Type of chart ('pie', 'bar', 'donut')
        
    Returns:
        Plotly figure object
    """
    if not spending_data:
        return go.Figure()
    
    categories = list(spending_data.keys())
    amounts = list(spending_data.values())
    
    if chart_type == 'pie':
        fig = px.pie(
            values=amounts,
            names=categories,
            title="Spending Breakdown by Category"
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Amount: $%{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
        )
        
    elif chart_type == 'donut':
        fig = go.Figure(data=[go.Pie(
            labels=categories,
            values=amounts,
            hole=0.4
        )])
        
        fig.update_layout(title_text="Spending Breakdown by Category")
        
    elif chart_type == 'bar':
        fig = px.bar(
            x=categories,
            y=amounts,
            title="Spending by Category",
            labels={'x': 'Category', 'y': 'Amount ($)'}
        )
        
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>Amount: $%{y:,.0f}<extra></extra>'
        )
    
    fig.update_layout(
        showlegend=True,
        height=400,
        font_size=12
    )
    
    return fig

def create_goal_progress_chart(goals: List[Dict[str, Any]]) -> go.Figure:
    """
    Create a goal progress chart.
    
    Args:
        goals: List of goal dictionaries
        
    Returns:
        Plotly figure object
    """
    if not goals:
        return go.Figure()
    
    goal_names = [g['goal_name'] for g in goals]
    progress_percentages = [
        (g['current_amount'] / g['target_amount'] * 100) if g['target_amount'] > 0 else 0 
        for g in goals
    ]
    target_amounts = [g['target_amount'] for g in goals]
    current_amounts = [g['current_amount'] for g in goals]
    
    # Create horizontal bar chart
    fig = go.Figure()
    
    # Add progress bars
    fig.add_trace(go.Bar(
        y=goal_names,
        x=progress_percentages,
        orientation='h',
        name='Progress %',
        text=[f"{p:.1f}%" for p in progress_percentages],
        textposition='inside',
        marker=dict(
            color=progress_percentages,
            colorscale='RdYlGn',
            cmin=0,
            cmax=100
        ),
        hovertemplate='<b>%{y}</b><br>Progress: %{x:.1f}%<br>Current: $%{customdata[0]:,.0f}<br>Target: $%{customdata[1]:,.0f}<extra></extra>',
        customdata=list(zip(current_amounts, target_amounts))
    ))
    
    fig.update_layout(
        title="Goal Progress Overview",
        xaxis_title="Progress (%)",
        yaxis_title="Goals",
        height=max(300, len(goals) * 60),
        showlegend=False,
        xaxis=dict(range=[0, 100])
    )
    
    return fig

def create_income_expense_trend(monthly_data: List[Dict[str, Any]]) -> go.Figure:
    """
    Create income vs expense trend chart.
    
    Args:
        monthly_data: List of monthly data dictionaries
        
    Returns:
        Plotly figure object
    """
    if not monthly_data:
        return go.Figure()
    
    df = pd.DataFrame(monthly_data)
    
    fig = go.Figure()
    
    # Add income line
    fig.add_trace(go.Scatter(
        x=df['month'],
        y=df['income'],
        mode='lines+markers',
        name='Income',
        line=dict(color='green', width=3),
        marker=dict(size=8),
        hovertemplate='<b>Income</b><br>Month: %{x}<br>Amount: $%{y:,.0f}<extra></extra>'
    ))
    
    # Add expenses line
    fig.add_trace(go.Scatter(
        x=df['month'],
        y=df['expenses'],
        mode='lines+markers',
        name='Expenses',
        line=dict(color='red', width=3),
        marker=dict(size=8),
        hovertemplate='<b>Expenses</b><br>Month: %{x}<br>Amount: $%{y:,.0f}<extra></extra>'
    ))
    
    # Add savings area
    fig.add_trace(go.Scatter(
        x=df['month'],
        y=df['savings'],
        mode='lines+markers',
        name='Savings',
        line=dict(color='blue', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(0, 100, 255, 0.2)',
        hovertemplate='<b>Savings</b><br>Month: %{x}<br>Amount: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Monthly Income, Expenses & Savings Trend",
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        hovermode='x unified',
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_savings_rate_gauge(savings_rate: float, target_rate: float = 20.0) -> go.Figure:
    """
    Create a gauge chart for savings rate.
    
    Args:
        savings_rate: Current savings rate percentage
        target_rate: Target savings rate percentage
        
    Returns:
        Plotly figure object
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=savings_rate,
        delta={'reference': target_rate, 'suffix': '%'},
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Savings Rate"},
        gauge={
            'axis': {'range': [None, 50]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 10], 'color': "lightgray"},
                {'range': [10, 20], 'color': "gray"},
                {'range': [20, 30], 'color': "lightgreen"},
                {'range': [30, 50], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': target_rate
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        font={'color': "darkblue", 'family': "Arial"}
    )
    
    return fig

def create_category_comparison_chart(
    current_spending: Dict[str, float],
    recommended_spending: Dict[str, float]
) -> go.Figure:
    """
    Create a comparison chart of current vs recommended spending.
    
    Args:
        current_spending: Current spending by category
        recommended_spending: Recommended spending by category
        
    Returns:
        Plotly figure object
    """
    categories = list(current_spending.keys())
    current_amounts = [current_spending.get(cat, 0) for cat in categories]
    recommended_amounts = [recommended_spending.get(cat, 0) for cat in categories]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Current Spending',
        x=categories,
        y=current_amounts,
        marker_color='lightcoral',
        hovertemplate='<b>Current</b><br>%{x}: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='Recommended Spending',
        x=categories,
        y=recommended_amounts,
        marker_color='lightblue',
        hovertemplate='<b>Recommended</b><br>%{x}: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Current vs Recommended Spending by Category',
        xaxis_title='Category',
        yaxis_title='Amount ($)',
        barmode='group',
        height=400,
        hovermode='x unified'
    )
    
    return fig

def create_financial_health_radar(metrics: Dict[str, float]) -> go.Figure:
    """
    Create a radar chart for financial health metrics.
    
    Args:
        metrics: Dictionary of metric name -> score (0-100)
        
    Returns:
        Plotly figure object
    """
    categories = list(metrics.keys())
    values = list(metrics.values())
    
    # Close the radar chart
    categories += [categories[0]]
    values += [values[0]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Financial Health Score',
        marker_color='blue',
        hovertemplate='<b>%{theta}</b><br>Score: %{r:.0f}/100<extra></extra>'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        title="Financial Health Overview",
        height=400
    )
    
    return fig

def create_goal_timeline_chart(goals: List[Dict[str, Any]]) -> go.Figure:
    """
    Create a timeline chart showing goal target dates.
    
    Args:
        goals: List of goal dictionaries with target dates
        
    Returns:
        Plotly figure object
    """
    if not goals:
        return go.Figure()
    
    # Filter goals with target dates
    goals_with_dates = [g for g in goals if g.get('target_date')]
    
    if not goals_with_dates:
        return go.Figure()
    
    goal_names = [g['goal_name'] for g in goals_with_dates]
    target_dates = [pd.to_datetime(g['target_date']) for g in goals_with_dates]
    progress = [(g['current_amount'] / g['target_amount'] * 100) if g['target_amount'] > 0 else 0 for g in goals_with_dates]
    
    fig = go.Figure()
    
    # Add scatter plot for goals
    fig.add_trace(go.Scatter(
        x=target_dates,
        y=goal_names,
        mode='markers',
        marker=dict(
            size=[max(10, p/5) for p in progress],  # Size based on progress
            color=progress,
            colorscale='RdYlGn',
            cmin=0,
            cmax=100,
            showscale=True,
            colorbar=dict(title="Progress %")
        ),
        text=[f"{p:.1f}%" for p in progress],
        textposition="middle right",
        hovertemplate='<b>%{y}</b><br>Target Date: %{x}<br>Progress: %{text}<extra></extra>'
    ))
    
    # Add vertical line for today
    fig.add_vline(
        x=pd.Timestamp.now(),
        line_dash="dash",
        line_color="red",
        annotation_text="Today"
    )
    
    fig.update_layout(
        title="Goal Timeline and Progress",
        xaxis_title="Target Date",
        yaxis_title="Goals",
        height=max(300, len(goals_with_dates) * 50),
        showlegend=False
    )
    
    return fig

def create_net_worth_projection(
    current_assets: float,
    current_liabilities: float,
    monthly_savings: float,
    months: int = 60
) -> go.Figure:
    """
    Create a net worth projection chart.
    
    Args:
        current_assets: Current total assets
        current_liabilities: Current total liabilities
        monthly_savings: Monthly savings amount
        months: Number of months to project
        
    Returns:
        Plotly figure object
    """
    months_range = list(range(months + 1))
    assets_projection = [current_assets + (month * monthly_savings) for month in months_range]
    liabilities_projection = [current_liabilities for _ in months_range]  # Assuming static for simplicity
    net_worth_projection = [assets - liabilities for assets, liabilities in zip(assets_projection, liabilities_projection)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months_range,
        y=assets_projection,
        mode='lines',
        name='Assets',
        line=dict(color='green', width=2),
        hovertemplate='<b>Assets</b><br>Month: %{x}<br>Amount: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=months_range,
        y=liabilities_projection,
        mode='lines',
        name='Liabilities',
        line=dict(color='red', width=2),
        hovertemplate='<b>Liabilities</b><br>Month: %{x}<br>Amount: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=months_range,
        y=net_worth_projection,
        mode='lines',
        name='Net Worth',
        line=dict(color='blue', width=3),
        fill='tonexty',
        fillcolor='rgba(0, 100, 255, 0.1)',
        hovertemplate='<b>Net Worth</b><br>Month: %{x}<br>Amount: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"Net Worth Projection ({months} months)",
        xaxis_title="Months from Now",
        yaxis_title="Amount ($)",
        height=400,
        hovermode='x unified'
    )
    
    return fig
