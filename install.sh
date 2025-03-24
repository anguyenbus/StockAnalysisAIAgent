#!/bin/bash

# Create a Python virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Error: Virtual environment activation failed."
    exit 1
else
    echo "Virtual environment activated successfully."
fi

# Install Ollama
echo "Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

# Install required Python packages
echo "Installing required Python packages..."
pip install langchain langchain-core langgraph yfinance langchain-openai

echo "====================================================================="
echo "Installation complete!"
echo "To use the stock analysis tool:"
echo ""
echo "1. Activate the virtual environment (if not already activated):"
echo "   source venv/bin/activate"
echo ""
echo "2. Start Ollama server in a separate terminal window:"
echo "   # In a separate terminal or tab:"
echo "   ollama serve"
echo ""
echo "3. In another terminal, pull the deepseek model:"
echo "   ollama pull deepseek-r1:7b"
echo ""
echo "4. Run the analysis with:"
echo "   python stock_analysis.py <STOCK_SYMBOL>"
echo ""
echo "NOTE: Make sure Ollama server is running before running the analysis script."
echo "====================================================================="
