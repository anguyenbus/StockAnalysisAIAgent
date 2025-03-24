"""Flask web application for stock analysis visualization."""

import json
import os
import subprocess
import tempfile
import traceback
from typing import Any, Dict, Optional, Tuple

import yfinance as yf
from flask import Flask, jsonify, render_template, request


# Custom JSON encoder for handling non-serializable objects
class CustomJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for handling non-serializable objects."""

    def default(self, obj: Any) -> Any:
        """Convert non-serializable objects to strings."""
        try:
            return super().default(obj)
        except (ValueError, TypeError, KeyError):
            return str(obj)


app = Flask(__name__, static_url_path="/static")
app.json_encoder = CustomJSONEncoder  # type: ignore


@app.route("/")
def index() -> str:
    """Render the main page."""
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    """Handle stock analysis requests."""
    try:
        data = request.json
        if data is None:  # Handle case when request.json is None
            return jsonify({"success": False, "error": "Invalid JSON data"})

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
            with open(temp_path, "r", encoding="utf-8") as f:
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
    except (ValueError, TypeError, KeyError) as e:
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


def fetch_price_data(
    symbol: str, period: str = "6mo"
) -> Tuple[Optional[Dict], Optional[str]]:
    """Fetch historical price data for the given symbol and time period.

    Args:
        symbol: Stock ticker symbol
        period: Time period for data (default: "6mo")

    Returns:
        Tuple containing price data dictionary and error message (if any)
    """
    try:
        # Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)

        if hist.empty:
            return None, "No price data found for this symbol"

        # Format data for candlestick chart
        chart_data = []
        for idx, row in hist.iterrows():
            chart_data.append(
                {
                    "date": idx.strftime("%Y-%m-%d"),  # type: ignore
                    "open": float(row["Open"]),
                    "high": float(row["High"]),
                    "low": float(row["Low"]),
                    "close": float(row["Close"]),
                    "volume": int(row["Volume"]),
                }
            )

        # Get current price and change
        current_price = float(hist["Close"].iloc[-1])
        previous_close = (
            float(hist["Close"].iloc[-2]) if len(hist) > 1 else current_price
        )
        change_value = round(current_price - previous_close, 2)
        change_percent = (
            round((change_value / previous_close) * 100, 2) if previous_close > 0 else 0
        )

        price_summary = {
            "current": current_price,
            "change_value": change_value,
            "change_percent": change_percent,
            "is_positive": bool(change_value >= 0),
        }

        return {"chart_data": chart_data, "price_summary": price_summary}, None
    except (ValueError, TypeError, KeyError) as e:
        print(traceback.format_exc())
        return None, f"Error fetching price data: {str(e)}"


def run_command(command):
    """Execute a shell command and return the results."""
    try:
        with subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True,
        ) as process:
            _, stderr = process.communicate()
            if process.returncode != 0:
                return False, stderr
            return True, None
    except (subprocess.SubprocessError, OSError) as e:
        return False, str(e)


if __name__ == "__main__":
    app.run(debug=True)
