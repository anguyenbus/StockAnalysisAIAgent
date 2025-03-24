#!/usr/bin/env python3

# Add docstring at the module level
"""Stock analysis module using LangChain and Ollama for AI-powered market insights."""

import argparse
import json
from datetime import datetime
from typing import Annotated, Any, Dict

import pandas as pd
import yfinance as yf
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, Graph, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


# Define the State class to track our analysis state
class State(TypedDict):
    """State class to track analysis state and results."""

    messages: Annotated[list, add_messages]
    symbol: str
    llm: ChatOpenAI
    results: Dict[str, Any]


# Initialize the ollama endpoint
def setup_llm() -> ChatOpenAI:
    """Initialize and configure the Ollama LLM endpoint.

    Returns:
        ChatOpenAI: Configured LLM instance
    """
    return ChatOpenAI(
        model="deepseek-r1:7b",
        api_key="ollama",
        base_url="http://127.0.0.1:11434/v1",
        temperature=0,
        top_p=0.7,
    )


# Technical Analysis Node
def technical_analysis(state: State) -> State:
    """Perform technical analysis on the stock.

    Args:
        state: Current analysis state

    Returns:
        State: Updated state with technical analysis results
    """
    symbol = state["symbol"]
    llm = state["llm"]

    # Fetch technical data
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1y")

    # Calculate indicators
    sma_20 = hist["Close"].rolling(window=20).mean()
    sma_50 = hist["Close"].rolling(window=50).mean()
    rsi = calculate_rsi(hist["Close"])

    data = {
        "current_price": hist["Close"].iloc[-1],
        "sma_20": sma_20.iloc[-1],
        "sma_50": sma_50.iloc[-1],
        "rsi": rsi.iloc[-1],
        "volume_trend": hist["Volume"].iloc[-5:].mean()
        / hist["Volume"].iloc[-20:].mean(),
    }

    # Use the new RunnableSequence approach with pipe syntax
    prompt = PromptTemplate.from_template(
        """Analyze these technical indicators for {symbol}:
        {data}

        Provide:
        1. Trend analysis
        2. Support/Resistance levels
        3. Technical rating (Bullish/Neutral/Bearish)
        4. Key signals
        """
    )

    # Use the new invoke method instead of run
    chain = prompt | llm
    analysis = chain.invoke({"symbol": symbol, "data": json.dumps(data, indent=2)})

    # Extract the content from AIMessage if needed
    analysis_text = analysis.content if hasattr(analysis, "content") else str(analysis)

    state["results"]["technical"] = {"data": data, "analysis": analysis_text}
    return state


# Market Analysis Node
def market_analysis(state: State) -> State:
    """Perform market analysis on the stock.

    Args:
        state: Current analysis state

    Returns:
        State: Updated state with market analysis results
    """
    symbol = state["symbol"]
    llm = state["llm"]

    # Fetch market data
    stock = yf.Ticker(symbol)
    info = stock.info

    data = {
        "sector": info.get("sector", "Unknown"),
        "industry": info.get("industry", "Unknown"),
        "market_cap": info.get("marketCap", 0),
        "beta": info.get("beta", 1.0),
        "pe_ratio": info.get("trailingPE", 0),
    }

    # Use the new RunnableSequence approach with pipe syntax
    prompt = PromptTemplate.from_template(
        """Analyze the market context for {symbol}:
        {data}

        Provide:
        1. Market sentiment
        2. Sector analysis
        3. Risk assessment
        4. Market outlook
        """
    )

    # Use the new invoke method instead of run
    chain = prompt | llm
    analysis = chain.invoke({"symbol": symbol, "data": json.dumps(data, indent=2)})

    # Extract the content from AIMessage if needed
    analysis_text = analysis.content if hasattr(analysis, "content") else str(analysis)

    state["results"]["market"] = {"data": data, "analysis": analysis_text}
    return state


# News Analysis Node
def news_analysis(state: State) -> State:
    """Perform news analysis on the stock.

    Args:
        state: Current analysis state

    Returns:
        State: Updated state with news analysis results
    """
    symbol = state["symbol"]
    llm = state["llm"]

    # Fetch news
    stock = yf.Ticker(symbol)
    news = stock.news[:5]  # Last 5 news items

    news_data = [
        {
            "title": item.get("title", ""),
            "publisher": item.get("publisher", ""),
            "timestamp": datetime.fromtimestamp(
                item.get("providerPublishTime", 0)
            ).strftime("%Y-%m-%d"),
        }
        for item in news
    ]

    # Use the new RunnableSequence approach with pipe syntax
    prompt = PromptTemplate.from_template(
        """Analyze these recent news items for {symbol}:
        {news}

        Provide:
        1. Overall sentiment
        2. Key developments
        3. Potential impact
        4. Risk factors
        """
    )

    # Use the new invoke method instead of run
    chain = prompt | llm
    analysis = chain.invoke({"symbol": symbol, "news": json.dumps(news_data, indent=2)})

    # Extract the content from AIMessage if needed
    analysis_text = analysis.content if hasattr(analysis, "content") else str(analysis)

    state["results"]["news"] = {"data": news_data, "analysis": analysis_text}
    return state


# Final Recommendation Node
def generate_recommendation(state: State) -> State:
    """Generate final investment recommendation.

    Args:
        state: Current analysis state

    Returns:
        State: Updated state with final recommendation
    """
    symbol = state["symbol"]
    llm = state["llm"]
    results = state["results"]

    # Use the new RunnableSequence approach with pipe syntax
    prompt = PromptTemplate.from_template(
        """Based on the following analyses for {symbol}, provide a final recommendation:

        Technical Analysis:
        {technical}

        Market Analysis:
        {market}

        News Analysis:
        {news}

        Provide:
        1. Final recommendation (Strong Buy/Buy/Hold/Sell/Strong Sell)
        2. Confidence score (1-10)
        3. Key reasons
        4. Risk factors
        5. Target price range
        """
    )

    # Use the new invoke method instead of run
    chain = prompt | llm
    recommendation = chain.invoke(
        {
            "symbol": symbol,
            "technical": results["technical"]["analysis"],
            "market": results["market"]["analysis"],
            "news": results["news"]["analysis"],
        }
    )

    # Extract the content from AIMessage if needed
    recommendation_text = (
        recommendation.content
        if hasattr(recommendation, "content")
        else str(recommendation)
    )

    state["results"]["recommendation"] = recommendation_text
    return state


def calculate_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """Calculate the Relative Strength Index (RSI) indicator.

    Args:
        prices: Series of price data
        period: RSI calculation period (default: 14)

    Returns:
        pd.Series: Calculated RSI values
    """
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs_value = gain / loss
    return 100 - (100 / (1 + rs_value))


def create_analysis_graph() -> Graph:
    """Create the analysis workflow graph.

    Returns:
        Graph: Compiled workflow graph
    """
    # Create workflow graph
    workflow = StateGraph(State)

    # Add nodes
    workflow.add_node("technical", technical_analysis)
    workflow.add_node("market", market_analysis)
    workflow.add_node("news", news_analysis)
    workflow.add_node("recommendation", generate_recommendation)

    # Define edges
    workflow.add_edge("technical", "market")
    workflow.add_edge("market", "news")
    workflow.add_edge("news", "recommendation")
    workflow.add_edge(START, "technical")

    # Set end node
    workflow.add_edge("recommendation", END)

    return workflow.compile()


class StockAdvisor:
    """Main class for performing stock analysis."""

    def __init__(self):
        """Initialize StockAdvisor with LLM and analysis graph."""
        self.llm = setup_llm()
        self.graph = create_analysis_graph()

    def analyze_stock(self, symbol: str) -> Dict[str, Any]:
        """Run complete stock analysis for given symbol.

        Args:
            symbol: Stock ticker symbol

        Returns:
            Dict[str, Any]: Analysis results
        """
        print(f"\nAnalyzing {symbol}...")

        # Initialize state
        init_state: State = {"symbol": symbol, "llm": self.llm, "results": {}}

        # Run analysis
        final_state = self.graph.invoke(init_state)
        return final_state["results"]


# Helper function to run analysis
def run_analysis(symbol: str) -> Dict[str, Any]:
    """Run stock analysis and format results.

    Args:
        symbol: Stock ticker symbol

    Returns:
        Dict[str, Any]: Formatted analysis results
    """
    advisor = StockAdvisor()
    results = advisor.analyze_stock(symbol)

    print(f"\n=== Stock Analysis Report for {symbol} ===")

    print("\n=== Technical Analysis ===")
    print(results["technical"]["analysis"])

    print("\n=== Market Analysis ===")
    print(results["market"]["analysis"])

    print("\n=== News Analysis ===")
    print(results["news"]["analysis"])

    print("\n=== Final Recommendation ===")
    print(results["recommendation"])

    # Format results for web display (in markdown)
    formatted_results = {
        "symbol": symbol,
        "recommendation": str(results["recommendation"]),
        "technical_analysis": str(results["technical"]["analysis"]),
        "market_analysis": str(results["market"]["analysis"]),
        "news_analysis": str(results["news"]["analysis"]),
    }

    return formatted_results


def main() -> None:
    """Main function to run the stock analysis tool."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Stock Analysis Tool")
    parser.add_argument(
        "--symbol", required=True, help="Stock symbol to analyze (e.g., AAPL)"
    )
    parser.add_argument("--output", help="Path to save results as JSON")
    args = parser.parse_args()

    # Run analysis
    results = run_analysis(args.symbol)

    # Save results to JSON file if output path is provided
    if args.output:
        with open(args.output, "w", encoding="utf-8") as file:
            # Use a custom encoder to ensure all objects are serializable
            class CustomEncoder(json.JSONEncoder):
                """Custom JSON encoder for handling non-serializable objects."""

                def default(self, o):
                    """Convert non-serializable objects to strings."""
                    try:
                        return super().default(o)
                    except TypeError:
                        return str(o)

            json.dump(results, file, cls=CustomEncoder)
        print(f"\nResults saved to {args.output}")
    else:
        # Print results to stdout as JSON
        print(json.dumps(results, default=str))

    return results


if __name__ == "__main__":
    main()
