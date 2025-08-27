#!/bin/bash

echo "🔧 Fixing installation warnings..."

# 1. Update pip to latest version
echo "📦 Updating pip..."
python3 -m pip install --upgrade pip

# 2. Add Python bin to PATH if not already there
PYTHON_BIN_PATH="$HOME/Library/Python/3.9/bin"
if [[ ":$PATH:" != *":$PYTHON_BIN_PATH:"* ]]; then
    echo "🛤️  Adding Python bin directory to PATH..."
    echo 'export PATH="$HOME/Library/Python/3.9/bin:$PATH"' >> ~/.zshrc
    echo "✅ PATH updated. Please run 'source ~/.zshrc' or restart your terminal."
else
    echo "✅ Python bin directory already in PATH"
fi

# 3. Verify streamlit installation
echo "🧪 Testing Streamlit installation..."
if python3 -c "import streamlit; print('✅ Streamlit imported successfully')" 2>/dev/null; then
    echo "✅ Streamlit is working correctly"
else
    echo "❌ Streamlit import failed"
fi

# 4. Check if streamlit command is accessible
if command -v streamlit &> /dev/null; then
    echo "✅ Streamlit command is accessible"
    streamlit --version
else
    echo "⚠️  Streamlit command not found in PATH"
    echo "You can still run it with: python3 -m streamlit run ui/main.py"
fi

echo "🎉 Warning fixes completed!"
echo ""
echo "📋 Summary:"
echo "- Pip updated to latest version"
echo "- Python bin directory added to PATH"
echo "- Streamlit installation verified"
echo ""
echo "🚀 To start the application:"
echo "   source ~/.zshrc  # (if PATH was updated)"
echo "   streamlit run ui/main.py"
echo "   # OR"
echo "   python3 -m streamlit run ui/main.py"
