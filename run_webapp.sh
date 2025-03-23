#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Check if Ollama server is running
if ! curl -s http://localhost:11434/api/version > /dev/null; then
    echo "Warning: Ollama server does not appear to be running!"
    echo "Please start Ollama server in a separate terminal with: ollama serve"
    echo "Then run this script again."
    exit 1
fi

# Check if deepseek model is available
if ! curl -s http://localhost:11434/api/tags | grep -q "deepseek-r1:7b"; then
    echo "Warning: Deepseek model not found in Ollama."
    echo "Please run: ollama pull deepseek-r1:7b"
    echo "Then run this script again."
    exit 1
fi

# Start Flask app
echo "Starting Stock Analysis AI Web App..."
echo "Open your browser and navigate to: http://127.0.0.1:5000"
python app.py 