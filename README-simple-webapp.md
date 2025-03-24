# Stock Analysis AI Web Application (Simplified)

This is a simplified web interface for the Stock Analysis AI tool that uses Ollama with the deepseek-r1:7b model to analyze stocks and provide investment recommendations.

## Features

- User-friendly interface for entering stock symbols
- **Interactive stock charts** with candlestick patterns and price history
- **Time period selection** for different chart ranges (1M, 6M, 1Y, 5Y)
- Beautifully formatted analysis results with tabs for different sections
- Responsive design that works on desktop and mobile devices
- Color-coded recommendations for easy interpretation

## Simple Installation

1. Make sure you have installed the main Stock Analysis AI tool first by running `./install.sh`

2. Install the web application dependencies:
   ```bash
   chmod +x install_webapp.sh
   ./install_webapp.sh
   ```

## Running the Web Application

1. Make sure Ollama server is running in a separate terminal:
   ```bash
   # In terminal window #1
   ollama serve
   ```

2. Pull the deepseek model if you haven't already:
   ```bash
   # In terminal window #2
   ollama pull deepseek-r1:7b
   ```

3. Start the web application:
   ```bash
   # In terminal window #2
   source venv/bin/activate
   python simple_app.py
   ```

4. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Usage

1. Enter a stock symbol in the search box (e.g., AAPL, MSFT, GOOG)
2. Click "Analyze" or press Enter
3. The analysis will run (this may take a minute or two)
4. Results will be displayed with:
   - **Interactive stock charts** showing price history in candlestick format
   - Price summary with current price and change indicators
   - Adjustable time periods (1M, 6M, 1Y, 5Y) for different chart views
   - Tabs for different analysis sections:
     - Recommendation: The final investment recommendation
     - Technical Analysis: Analysis of price movements and technical indicators
     - Market Analysis: Sector performance and market context
     - News Analysis: Recent news sentiment and impact

## Tips

- For non-US stocks, include the appropriate exchange suffix:
  - Indian stocks: Add .NS (e.g., INFY.NS)
  - Japanese stocks: Add .T (e.g., 9984.T)
- Use the period buttons to see different timeframes of stock performance
- Hover over the candlestick chart to see detailed price information for specific dates

## Troubleshooting

- If you see an error about Ollama not being available, make sure the Ollama server is running
- If the analysis takes too long, check your internet connection and Ollama server status
- If the web interface doesn't load, ensure Flask is installed properly
- If charts don't load, verify you have yfinance and pandas installed correctly
