from flask import Flask, render_template, request, jsonify
import stock_analysis
import traceback
import markdown

app = Flask(__name__, static_url_path="/static")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
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
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": f"An error occurred: {str(e)}"})


if __name__ == "__main__":
    app.run(debug=True)
