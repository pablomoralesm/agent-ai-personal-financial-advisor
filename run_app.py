#!/usr/bin/env python3
"""
Startup script for the AI Personal Financial Advisor Streamlit application.

This script ensures proper Python path configuration and launches the Streamlit app.
"""

import os
import sys
import subprocess

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Set PYTHONPATH environment variable
os.environ['PYTHONPATH'] = f"{project_root}:{os.environ.get('PYTHONPATH', '')}"

# Test imports before starting Streamlit
try:
    from utils.logging_config import get_logger
    from agents.orchestrator import create_financial_advisor_orchestrator
    print("✅ All imports successful - starting Streamlit app...")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all dependencies are installed and the virtual environment is activated.")
    sys.exit(1)

# Launch Streamlit
if __name__ == "__main__":
    streamlit_cmd = [
        sys.executable, "-m", "streamlit", "run", 
        os.path.join(project_root, "streamlit_app.py")
    ]
    
    # Add any command line arguments passed to this script
    streamlit_cmd.extend(sys.argv[1:])
    
    try:
        subprocess.run(streamlit_cmd)
    except KeyboardInterrupt:
        print("\n👋 Streamlit app stopped by user")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")
        sys.exit(1)
