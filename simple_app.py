from flask import Flask, render_template, request, jsonify
import subprocess
import json
import os
import markdown
import tempfile
import re
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


# Custom JSON encoder to handle non-serializable objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            # Convert non-serializable objects to strings
            return str(obj)


app = Flask(__name__, static_url_path="/static")
app.json_encoder = CustomJSONEncoder  # Use our custom encoder


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json
        symbol = data.get("symbol", "").strip().upper()
        if not symbol:
            return jsonify(
                {"success": False, "error": "Please provide a valid stock symbol"}
            )

        # Create a temporary file to store the analysis results
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as temp:
            temp_path = temp.name

        # Run the stock_analysis.py script as a subprocess
        process = subprocess.Popen(
            ["python", "stock_analysis.py", "--symbol", symbol, "--output", temp_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            error_msg = stderr.decode("utf-8")
            return jsonify({"success": False, "error": f"Analysis failed: {error_msg}"})

        # Read the results from the temporary file
        try:
            with open(temp_path, "r") as f:
                results = json.load(f)
        except json.JSONDecodeError:
            return jsonify(
                {"success": False, "error": "Failed to parse analysis results"}
            )
        except FileNotFoundError:
            return jsonify(
                {"success": False, "error": "Analysis results file not found"}
            )
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)

        # Fetch historical price data for charting
        price_data, price_error = fetch_price_data(symbol)
        if price_error:
            return jsonify(
                {"success": True, "data": results, "price_error": price_error}
            )

        return jsonify({"success": True, "data": results, "price_data": price_data})
    except Exception as e:
        import traceback

        print(traceback.format_exc())
        return jsonify({"success": False, "error": f"An error occurred: {str(e)}"})


@app.route("/price-data/<symbol>")
def get_price_data(symbol):
    """API endpoint to fetch price data separately"""
    try:
        periods = request.args.get("period", "6mo")
        data, error = fetch_price_data(symbol, periods)

        if error:
            return jsonify({"success": False, "error": error})

        return jsonify({"success": True, "data": data})
    except Exception as e:
        return jsonify({"error": f"Failed to fetch price data: {str(e)}"})


def fetch_price_data(symbol, period="6mo"):
    """Fetch historical price data for the given symbol and time period"""
    try:
        # Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)

        if hist.empty:
            return None, "No price data found for this symbol"

        # Format data for candlestick chart
        chart_data = []
        for index, row in hist.iterrows():
            chart_data.append(
                {
                    "date": index.strftime("%Y-%m-%d"),
                    "open": float(round(row["Open"], 2)),
                    "high": float(round(row["High"], 2)),
                    "low": float(round(row["Low"], 2)),
                    "close": float(round(row["Close"], 2)),
                    "volume": int(row["Volume"]),
                }
            )

        # Get current price and change - using iloc instead of negative indexing
        current_price = float(round(hist["Close"].iloc[-1], 2))
        previous_close = (
            float(round(hist["Close"].iloc[-2], 2)) if len(hist) > 1 else current_price
        )
        change_value = float(round(current_price - previous_close, 2))
        change_percent = float(
            round((change_value / previous_close) * 100, 2) if previous_close > 0 else 0
        )

        price_summary = {
            "current": current_price,
            "change_value": change_value,
            "change_percent": change_percent,
            "is_positive": bool(change_value >= 0),
        }

        return {"chart_data": chart_data, "price_summary": price_summary}, None
    except Exception as e:
        import traceback

        print(traceback.format_exc())
        return None, f"Error fetching price data: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)
