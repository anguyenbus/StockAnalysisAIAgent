#!/bin/bash

# Ensure we're in a Python virtualenv
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Please activate your Python virtual environment first."
    echo "Example: source venv/bin/activate"
    exit 1
fi

# Install the required packages for the web application
pip install flask markdown yfinance pandas

echo "Web application dependencies installed successfully."
echo "To run the web application:"
echo "1. Make sure Ollama server is running in a separate terminal with 'ollama serve'"
echo "2. Run the web application with 'python simple_app.py'"
echo "3. Open http://127.0.0.1:5000 in your browser" 