# Stock Analysis AI Agent

This tool uses Ollama with the deepseek-r1:7b model to analyze stocks and provide investment recommendations.

## Features

- Technical analysis: Evaluates price movements, trends, and technical indicators
- Market analysis: Analyzes sector performance, market cap, and other market factors
- News analysis: Examines recent news related to the stock
- Final recommendation: Combines all analyses to provide an investment recommendation

## Installation

### For Mac Users

1. Make sure you have Python 3.8+ installed:
   ```bash
   python3 --version
   ```

2. Run the installation script (creates a virtual environment automatically):
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

   This script will:
   - Create a Python virtual environment named `venv`
   - Activate the virtual environment
   - Install Ollama
   - Install all required Python packages

3. Start Ollama server in a separate terminal window:
   ```bash
   # In a separate terminal or tab:
   ollama serve
   ```

4. In another terminal window, pull the deepseek model:
   ```bash
   # In another terminal or tab:
   ollama pull deepseek-r1:7b
   ```

5. For future sessions, activate the virtual environment before running:
   ```bash
   source venv/bin/activate
   ```

## Usage

1. Make sure your virtual environment is activated:
   ```bash
   source venv/bin/activate
   ```

2. Ensure the Ollama server is running in a separate terminal:
   ```bash
   # In a separate terminal window
   ollama serve
   ```

3. Run the analysis:
   ```bash
   python stock_analysis.py <STOCK_SYMBOL>
   ```

For example:

```bash
python stock_analysis.py AAPL    # Analyze Apple Inc.
python stock_analysis.py MSFT    # Analyze Microsoft
python stock_analysis.py GOOG    # Analyze Google/Alphabet
```

You can use country-specific suffixes for non-US stocks:

```bash
python stock_analysis.py INFY.NS  # Analyze Infosys (India)
python stock_analysis.py 9984.T   # Analyze SoftBank (Japan)
```

## How It Works

The tool uses a workflow graph with the following nodes:

1. Technical Analysis: Calculates indicators like SMA, RSI, and volume trends
2. Market Analysis: Gathers information about sector, market cap, and PE ratio
3. News Analysis: Processes recent news about the stock
4. Recommendation: Combines all analyses to generate a final recommendation

The LLM (deepseek-r1:7b) processes each step and provides detailed analysis.

## Requirements

- Python 3.8 or higher
- Ollama installed (https://ollama.com)
- Required Python packages:
  - langchain
  - langchain-core
  - langgraph
  - yfinance
  - langchain-openai
- An internet connection to fetch stock data

## Troubleshooting for Mac

- If you get permission errors when running Ollama, you might need to run:
  ```bash
  sudo chmod +x /usr/local/bin/ollama
  ```

- If Ollama server exits with an error (Exit 1), try running it in a dedicated terminal window without the background process:
  ```bash
  # In a terminal dedicated to this purpose:
  ollama serve
  ```

- If you have issues with the virtual environment, you can create it manually:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install langchain langchain-core langgraph yfinance langchain-openai
  ```

## Example Output

The output provides a comprehensive analysis of the stock, including:

- Technical analysis with trend analysis and key signals
- Market analysis with sector performance and risk assessment
- News analysis with sentiment and potential impact
- Final recommendation with confidence score and target price range
