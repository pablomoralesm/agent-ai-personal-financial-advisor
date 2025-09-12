#!/usr/bin/env python3
"""
MCP Database Server for Financial Advisor Application (STDIO Version)

This version is designed to work with ADK's StdioServerParameters,
running as a subprocess that communicates via stdin/stdout.

Part of the Agentic AI Personal Financial Advisor application.
"""

import sys
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, date
from decimal import Decimal

# Import shared components
try:
    # Try relative import first (when used as module)
    from .shared import (
        DatabaseManager, 
        get_database_config,
        setup_logging,
        get_customer_profile,
        create_customer,
        add_transaction,
        get_transactions_by_customer,
        get_spending_summary,
        create_financial_goal,
        get_financial_goals,
        update_goal_progress,
        save_advice,
        get_advice_history,
        log_agent_interaction,
        get_spending_categories
    )
except ImportError:
    # Fall back to absolute import (when run directly)
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from mcp_server.shared import (
        DatabaseManager, 
        get_database_config,
        setup_logging,
        get_customer_profile,
        create_customer,
        add_transaction,
        get_transactions_by_customer,
        get_spending_summary,
        create_financial_goal,
        get_financial_goals,
        update_goal_progress,
        save_advice,
        get_advice_history,
        log_agent_interaction,
        get_spending_categories
    )

# Configure logging
logger = setup_logging()

# Get database configuration and initialize database manager
db_config = get_database_config()
db_manager = DatabaseManager(db_config)

# ============================================================================
# WRAPPER FUNCTIONS FOR STDIO COMPATIBILITY
# ============================================================================

def get_customer_profile_wrapper(customer_id: int) -> Dict[str, Any]:
    """Get customer profile information."""
    result = get_customer_profile(customer_id, db_manager)
    if "error" in result:
        return {"success": False, "error": result["error"]}
    return {"success": True, "customer": result}

def get_transactions_by_customer_wrapper(customer_id: int, months: int = 6) -> Dict[str, Any]:
    """Get customer transactions for analysis."""
    return get_transactions_by_customer(customer_id, months=months, db_manager=db_manager)

def get_spending_summary_wrapper(customer_id: int, months: int = 6) -> Dict[str, Any]:
    """Get spending summary for customer."""
    return get_spending_summary(customer_id, months, db_manager)

def get_financial_goals_wrapper(customer_id: int) -> Dict[str, Any]:
    """Get customer financial goals."""
    return get_financial_goals(customer_id, db_manager=db_manager)

def save_advice_wrapper(customer_id: int, agent_name: str, advice_type: str, advice_content: str, 
                       confidence_score: float = None, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    """Save financial advice from agents."""
    result = save_advice(customer_id, agent_name, advice_type, advice_content, 
                        confidence_score, metadata, db_manager)
    if "error" in result:
        return {"success": False, "error": result["error"]}
    return {"success": True, "message": "Advice saved successfully"}

def get_advice_history_wrapper(customer_id: int, limit: int = 10) -> Dict[str, Any]:
    """Get customer advice history."""
    return get_advice_history(customer_id, limit=limit, db_manager=db_manager)

def log_agent_interaction_wrapper(session_id: str, from_agent: str, interaction_type: str, 
                                 message_content: str, customer_id: int = None, 
                                 to_agent: str = None, context_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Log an interaction between agents or agent activities."""
    result = log_agent_interaction(session_id, from_agent, interaction_type, message_content,
                                  customer_id, to_agent, context_data, db_manager)
    if "error" in result:
        return {"success": False, "error": result["error"]}
    return {"success": True, "message": "Agent interaction logged successfully"}

def get_spending_categories_wrapper() -> Dict[str, Any]:
    """Get all available spending categories."""
    return get_spending_categories(db_manager)

class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle Decimal types."""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)

def main():
    """Main function for STDIO MCP server."""
    try:
        # Test database connection
        db_manager.get_connection().close()
        logger.info("Database connection successful")
        
        # Simple STDIO protocol for ADK
        logger.info("Starting STDIO MCP server for ADK...")
        
        # Read input from stdin
        for line in sys.stdin:
            try:
                # Skip empty lines
                if not line.strip():
                    continue
                    
                # Parse JSON-RPC 2.0 input
                data = json.loads(line.strip())
                
                # Handle MCP protocol messages
                if data.get('method') == 'initialize':
                    # Respond to MCP initialization
                    response = {
                        "jsonrpc": "2.0",
                        "id": data.get('id'),
                        "result": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {
                                "tools": {}
                            },
                            "serverInfo": {
                                "name": "financial-advisor-database-server",
                                "version": "1.0.0"
                            }
                        }
                    }
                    print(json.dumps(response))
                    sys.stdout.flush()
                    continue
                elif data.get('method') == 'tools/list':
                    # List available tools
                    response = {
                        "jsonrpc": "2.0",
                        "id": data.get('id'),
                        "result": {
                            "tools": [
                                {
                                    "name": "get_customer_profile",
                                    "description": "Get customer profile information",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {
                                            "customer_id": {"type": "integer", "description": "Customer ID"}
                                        },
                                        "required": ["customer_id"]
                                    }
                                },
                                {
                                    "name": "get_transactions_by_customer",
                                    "description": "Get customer transactions",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {
                                            "customer_id": {"type": "integer", "description": "Customer ID"},
                                            "months": {"type": "integer", "description": "Number of months", "default": 6}
                                        },
                                        "required": ["customer_id"]
                                    }
                                },
                                {
                                    "name": "get_spending_summary",
                                    "description": "Get customer spending summary",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {
                                            "customer_id": {"type": "integer", "description": "Customer ID"},
                                            "months": {"type": "integer", "description": "Number of months", "default": 6}
                                        },
                                        "required": ["customer_id"]
                                    }
                                },
                                {
                                    "name": "get_financial_goals",
                                    "description": "Get customer financial goals",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {
                                            "customer_id": {"type": "integer", "description": "Customer ID"}
                                        },
                                        "required": ["customer_id"]
                                    }
                                },
                                {
                                    "name": "save_advice",
                                    "description": "Save financial advice",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {
                                            "customer_id": {"type": "integer", "description": "Customer ID"},
                                            "agent_name": {"type": "string", "description": "Agent name"},
                                            "advice_type": {"type": "string", "description": "Type of advice"},
                                            "advice_content": {"type": "string", "description": "Advice content"},
                                            "confidence_score": {"type": "number", "description": "Confidence score"},
                                            "metadata": {"type": "object", "description": "Additional metadata"}
                                        },
                                        "required": ["customer_id", "agent_name", "advice_type", "advice_content"]
                                    }
                                },
                                {
                                    "name": "get_advice_history",
                                    "description": "Get customer advice history",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {
                                            "customer_id": {"type": "integer", "description": "Customer ID"},
                                            "limit": {"type": "integer", "description": "Number of records to return", "default": 10}
                                        },
                                        "required": ["customer_id"]
                                    }
                                },
                                {
                                    "name": "log_agent_interaction",
                                    "description": "Log agent interaction",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {
                                            "session_id": {"type": "string", "description": "Session ID"},
                                            "from_agent": {"type": "string", "description": "Source agent"},
                                            "interaction_type": {"type": "string", "description": "Type of interaction"},
                                            "message_content": {"type": "string", "description": "Message content"},
                                            "customer_id": {"type": "integer", "description": "Customer ID"},
                                            "to_agent": {"type": "string", "description": "Target agent"},
                                            "context_data": {"type": "object", "description": "Context data"}
                                        },
                                        "required": ["session_id", "from_agent", "interaction_type", "message_content"]
                                    }
                                },
                                {
                                    "name": "get_spending_categories",
                                    "description": "Get spending categories",
                                    "inputSchema": {
                                        "type": "object",
                                        "properties": {}
                                    }
                                }
                            ]
                        }
                    }
                    print(json.dumps(response))
                    sys.stdout.flush()
                    continue
                elif data.get('method') == 'tools/call':
                    # Execute tool call
                    tool_name = data.get('params', {}).get('name')
                    tool_params = data.get('params', {}).get('arguments', {})
                    
                    # Execute function based on tool name
                    if tool_name == 'get_customer_profile':
                        result = get_customer_profile_wrapper(tool_params.get('customer_id'))
                    elif tool_name == 'get_transactions_by_customer':
                        result = get_transactions_by_customer_wrapper(tool_params.get('customer_id'), tool_params.get('months', 6))
                    elif tool_name == 'get_spending_summary':
                        result = get_spending_summary_wrapper(tool_params.get('customer_id'), tool_params.get('months', 6))
                    elif tool_name == 'get_financial_goals':
                        result = get_financial_goals_wrapper(tool_params.get('customer_id'))
                    elif tool_name == 'save_advice':
                        result = save_advice_wrapper(
                            tool_params.get('customer_id'),
                            tool_params.get('agent_name'),
                            tool_params.get('advice_type'),
                            tool_params.get('advice_content'),
                            tool_params.get('confidence_score'),
                            tool_params.get('metadata')
                        )
                    elif tool_name == 'get_advice_history':
                        result = get_advice_history_wrapper(tool_params.get('customer_id'), tool_params.get('limit', 10))
                    elif tool_name == 'log_agent_interaction':
                        result = log_agent_interaction_wrapper(
                            tool_params.get('session_id'),
                            tool_params.get('from_agent'),
                            tool_params.get('interaction_type'),
                            tool_params.get('message_content'),
                            tool_params.get('customer_id'),
                            tool_params.get('to_agent'),
                            tool_params.get('context_data')
                        )
                    elif tool_name == 'get_spending_categories':
                        result = get_spending_categories_wrapper()
                    else:
                        result = {"success": False, "error": f"Unknown tool: {tool_name}"}
                    
                    # Send JSON-RPC response
                    response = {
                        "jsonrpc": "2.0",
                        "id": data.get('id'),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(result)
                                }
                            ]
                        }
                    }
                    print(json.dumps(response))
                    sys.stdout.flush()
                    continue
                else:
                    # Unknown method
                    response = {
                        "jsonrpc": "2.0",
                        "id": data.get('id'),
                        "error": {
                            "code": -32601,
                            "message": f"Method not found: {data.get('method')}"
                        }
                    }
                    print(json.dumps(response))
                    sys.stdout.flush()
                    continue
                
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
                error_result = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": f"Parse error: {e}"
                    }
                }
                print(json.dumps(error_result))
                sys.stdout.flush()
            except Exception as e:
                logger.error(f"Function execution error: {e}")
                error_result = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {e}"
                    }
                }
                print(json.dumps(error_result))
                sys.stdout.flush()
                
    except Exception as e:
        logger.error(f"Failed to start STDIO MCP server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
