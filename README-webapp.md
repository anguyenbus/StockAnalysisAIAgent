# Stock Analysis AI Web Application

This is a web interface for the Stock Analysis AI tool that uses Ollama with the deepseek-r1:7b model to analyze stocks and provide investment recommendations.

## Features

- User-friendly interface for entering stock symbols
- Beautifully formatted analysis results with tabs for different sections
- Responsive design that works on desktop and mobile devices
- Color-coded recommendations for easy interpretation

## Installation

1. Make sure you have installed the main Stock Analysis AI tool first, following the instructions in the main README.md file.

2. Install the additional web application dependencies:
   ```bash
   source venv/bin/activate  # Activate your virtual environment
   pip install -r requirements-webapp.txt
   ```

## Running the Web Application

1. Make sure Ollama server is running in a separate terminal:
   ```bash
   # In a separate terminal
   ollama serve
   ```

2. Start the Flask web server:
   ```bash
   source venv/bin/activate  # Activate your virtual environment
   python app.py
   ```

3. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## Usage

1. Enter a stock symbol in the search box (e.g., AAPL, MSFT, GOOG)
2. Click "Analyze" or press Enter
3. The analysis will run (this may take a minute or two)
4. Results will be displayed with tabs for:
   - Recommendation: The final investment recommendation
   - Technical Analysis: Analysis of price movements and technical indicators
   - Market Analysis: Sector performance and market context
   - News Analysis: Recent news sentiment and impact

## Tips

- For non-US stocks, include the appropriate exchange suffix:
  - Indian stocks: Add .NS (e.g., INFY.NS)
  - Japanese stocks: Add .T (e.g., 9984.T)
  - Other countries will have their own suffix formats

## Requirements

- All requirements from the main Stock Analysis AI tool
- Flask: Web framework
- Markdown: For formatting analysis output

## Troubleshooting

- If you see an error about Ollama not being available, make sure the Ollama server is running in a separate terminal
- If the analysis takes too long, check your internet connection and Ollama server status
- If the web interface doesn't load, ensure Flask is installed and the server is running 