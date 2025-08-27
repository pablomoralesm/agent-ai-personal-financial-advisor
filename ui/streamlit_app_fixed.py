"""
Simple test version of the Streamlit app to debug import issues.
"""

import streamlit as st
import os
import sys

# Add the project root to Python path for imports
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

st.title("🏦 AI Personal Financial Advisor - Test")

st.write("**System Information:**")
st.write(f"Current working directory: `{os.getcwd()}`")
st.write(f"Project root: `{project_root}`")
st.write(f"Python executable: `{sys.executable}`")

st.write("**Python Path:**")
for i, path in enumerate(sys.path):
    st.write(f"{i+1}. `{path}`")

st.write("**Testing Imports:**")

try:
    from utils.logging_config import get_logger
    st.success("✅ utils.logging_config import successful")
    
    logger = get_logger("test")
    st.success("✅ Logger creation successful")
    
except Exception as e:
    st.error(f"❌ Import error: {e}")
    st.write("**Full traceback:**")
    import traceback
    st.code(traceback.format_exc())

try:
    from agents.orchestrator import create_financial_advisor_orchestrator
    st.success("✅ Orchestrator import successful")
    
except Exception as e:
    st.error(f"❌ Orchestrator import error: {e}")
    st.write("**Full traceback:**")
    import traceback
    st.code(traceback.format_exc())

st.write("---")
st.write("If all imports are successful, the main app should work!")

if st.button("🚀 Launch Main App"):
    st.info("Main app launch would be triggered here")
