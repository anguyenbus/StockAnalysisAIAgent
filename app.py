"""Simple Flask web application for stock analysis."""

import traceback
from typing import Any, Dict

import markdown
from flask import Flask, jsonify, render_template, request

import stock_analysis

app = Flask(__name__, static_url_path="/static")


@app.route("/")
def index() -> str:
    """Render the main page."""
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze() -> Dict[str, Any]:
    """Handle stock analysis requests."""
    try:
        symbol = request.form.get("symbol", "").strip().upper()
        if not symbol:
            return jsonify({"error": "Please provide a valid stock symbol"})

        # Run the analysis
        results = stock_analysis.run_analysis(symbol)

        # Format results with markdown
        formatted_results = {
            "symbol": symbol,
            "technical": markdown.markdown(results["technical"]["analysis"]),
            "market": markdown.markdown(results["market"]["analysis"]),
            "news": markdown.markdown(results["news"]["analysis"]),
            "recommendation": markdown.markdown(results["recommendation"]),
        }

        return jsonify({"success": True, "results": formatted_results})
    except Exception as exc:
        print(traceback.format_exc())
        return jsonify({"error": f"An error occurred: {str(exc)}"})


if __name__ == "__main__":
    app.run(debug=True)
