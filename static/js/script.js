document.addEventListener('DOMContentLoaded', function () {
    const analysisForm = document.getElementById('analysisForm');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const errorMessage = document.getElementById('errorMessage');
    const analysisResults = document.getElementById('analysisResults');
    const stockTitle = document.getElementById('stockTitle');

    // Price and chart elements
    const currentPrice = document.getElementById('currentPrice');
    const priceChange = document.getElementById('priceChange');
    const miniChart = document.getElementById('miniChart');
    const candlestickChart = document.getElementById('candlestickChart');
    const periodButtons = document.querySelectorAll('.period-btn');

    // Content containers
    const recommendationContent = document.getElementById('recommendationContent');
    const technicalContent = document.getElementById('technicalContent');
    const marketContent = document.getElementById('marketContent');
    const newsContent = document.getElementById('newsContent');

    // Current state
    let currentSymbol = '';

    analysisForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const stockSymbol = document.getElementById('stockSymbol').value.trim().toUpperCase();

        if (!stockSymbol) {
            showError('Please enter a valid stock symbol');
            return;
        }

        // Reset UI state
        resetUI();

        // Show loading indicator
        loadingIndicator.classList.remove('d-none');

        // Submit form data via AJAX
        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symbol: stockSymbol })
        })
            .then(response => response.json())
            .then(data => {
                // Hide loading indicator
                loadingIndicator.classList.add('d-none');

                if (!data.success) {
                    showError(data.error || 'Failed to analyze the stock.');
                    return;
                }

                // Save current symbol for later use (with period buttons)
                currentSymbol = stockSymbol;

                // Display results
                displayResults(data.data, data.price_data);
            })
            .catch(error => {
                console.error('Error:', error);
                loadingIndicator.classList.add('d-none');
                showError('An error occurred while analyzing the stock. Please try again later.');
            });
    });

    // Add event listeners to period buttons
    periodButtons.forEach(button => {
        button.addEventListener('click', function () {
            // Only proceed if we have a current symbol
            if (!currentSymbol) return;

            // Update active button
            periodButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            // Get selected period
            const period = this.getAttribute('data-period');

            // Fetch and update chart
            fetchPriceData(currentSymbol, period);
        });
    });

    function resetUI() {
        // Hide error message and results
        errorMessage.classList.add('d-none');
        errorMessage.textContent = '';
        analysisResults.classList.add('d-none');

        // Clear previous content
        recommendationContent.innerHTML = '';
        technicalContent.innerHTML = '';
        marketContent.innerHTML = '';
        newsContent.innerHTML = '';

        // Reset charts
        currentPrice.textContent = '$0.00';
        priceChange.innerHTML = '';
        priceChange.className = 'badge';

        if (miniChart._context) Plotly.purge(miniChart);
        if (candlestickChart._context) Plotly.purge(candlestickChart);

        // Reset current symbol
        currentSymbol = '';
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.remove('d-none');
        console.error('Error:', message);
    }

    function displayResults(analysisData, priceData) {
        // Check if we have valid data
        if (!analysisData) {
            showError('Invalid analysis data received.');
            return;
        }

        try {
            // Populate content
            recommendationContent.innerHTML = analysisData.recommendation || '';
            technicalContent.innerHTML = analysisData.technical_analysis || '';
            marketContent.innerHTML = analysisData.market_analysis || '';
            newsContent.innerHTML = analysisData.news_analysis || '';

            // Display price data and charts if available
            if (priceData) {
                updatePriceSummary(priceData.price_summary);
                renderCandlestickChart(priceData.chart_data);
                renderMiniChart(priceData.chart_data);
            }

            // Show results container
            analysisResults.classList.remove('d-none');
        } catch (error) {
            console.error('Error displaying results:', error);
            showError('Error displaying analysis results. Please try again.');
        }
    }

    function updatePriceSummary(summary) {
        try {
            if (!summary) return;

            currentPrice.textContent = `$${summary.current}`;

            const changeText = `${summary.is_positive ? '+' : ''}${summary.change_value} (${summary.is_positive ? '+' : ''}${summary.change_percent}%)`;
            priceChange.textContent = changeText;

            // Set the appropriate class based on price change
            priceChange.className = 'badge';
            if (summary.is_positive) {
                priceChange.classList.add('bg-success');
            } else {
                priceChange.classList.add('bg-danger');
            }
        } catch (error) {
            console.error('Error updating price summary:', error);
        }
    }

    function renderCandlestickChart(chartData) {
        try {
            if (!chartData || chartData.length === 0) return;

            const dates = chartData.map(d => d.date);
            const opens = chartData.map(d => d.open);
            const highs = chartData.map(d => d.high);
            const lows = chartData.map(d => d.low);
            const closes = chartData.map(d => d.close);
            const volumes = chartData.map(d => d.volume);

            // Create candlestick trace
            const candlestick = {
                x: dates,
                open: opens,
                high: highs,
                low: lows,
                close: closes,
                increasing: { line: { color: '#26a69a' } },
                decreasing: { line: { color: '#ef5350' } },
                type: 'candlestick',
                name: 'Price'
            };

            // Create volume trace as a bar chart at the bottom
            const volume = {
                x: dates,
                y: volumes,
                type: 'bar',
                name: 'Volume',
                marker: {
                    color: 'rgba(100, 100, 100, 0.3)'
                },
                yaxis: 'y2'
            };

            const data = [candlestick, volume];

            const layout = {
                dragmode: 'zoom',
                margin: {
                    r: 10,
                    t: 25,
                    b: 40,
                    l: 60
                },
                showlegend: false,
                xaxis: {
                    autorange: true,
                    rangeslider: {
                        visible: false
                    },
                    type: 'date'
                },
                yaxis: {
                    autorange: true,
                    title: 'Price',
                    domain: [0.3, 1]
                },
                yaxis2: {
                    autorange: true,
                    domain: [0, 0.2],
                    showticklabels: false
                },
                plot_bgcolor: '#f8f9fa',
                paper_bgcolor: '#ffffff'
            };

            const config = {
                responsive: true,
                displayModeBar: false
            };

            Plotly.newPlot(candlestickChart, data, layout, config);
        } catch (error) {
            console.error('Error rendering candlestick chart:', error);
            candlestickChart.innerHTML = '<div class="alert alert-danger">Failed to render chart</div>';
        }
    }

    function renderMiniChart(chartData) {
        try {
            if (!chartData || chartData.length === 0) return;

            const dates = chartData.map(d => d.date);
            const closes = chartData.map(d => d.close);

            // Determine line color based on trend
            const color = closes[closes.length - 1] >= closes[0] ? '#26a69a' : '#ef5350';

            const trace = {
                x: dates,
                y: closes,
                type: 'scatter',
                mode: 'lines',
                line: {
                    color: color,
                    width: 1.5
                },
                hoverinfo: 'none'
            };

            const layout = {
                height: 100,
                margin: {
                    l: 0, r: 0, b: 0, t: 0, pad: 0
                },
                xaxis: {
                    showticklabels: false,
                    showgrid: false,
                    zeroline: false
                },
                yaxis: {
                    showticklabels: false,
                    showgrid: false,
                    zeroline: false
                },
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)'
            };

            const config = {
                displayModeBar: false
            };

            Plotly.newPlot(miniChart, [trace], layout, config);
        } catch (error) {
            console.error('Error rendering mini chart:', error);
        }
    }

    function fetchPriceData(symbol, period) {
        fetch(`/price-data/${symbol}?period=${period}`)
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    console.error('Error fetching price data:', data.error);
                    return;
                }

                try {
                    // Update the charts with the new data
                    renderCandlestickChart(data.data.chart_data);
                    renderMiniChart(data.data.chart_data);

                    // Update price summary
                    updatePriceSummary(data.data.price_summary);
                } catch (error) {
                    console.error('Error processing price data:', error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    // Helper function to format recommendations (preserved from original)
    function formatRecommendation(html) {
        if (!html) return '';

        // Create a temporary div to parse the HTML
        const temp = document.createElement('div');
        temp.innerHTML = html;

        // Find the recommendation
        const recommendation = findRecommendation(temp);

        if (recommendation) {
            const recommendationClass = getRecommendationClass(recommendation);
            // Create a styled recommendation highlight
            const highlight = `<div class="recommendation-highlight ${recommendationClass}">${recommendation}</div>`;
            temp.innerHTML = highlight + temp.innerHTML;
        }

        return temp.innerHTML;
    }

    function findRecommendation(element) {
        // Common recommendation phrases
        const recommendationPatterns = [
            /\b(Strong Buy|Buy|Hold|Sell|Strong Sell)\b/i,
            /\brecommendation\s*:\s*(Strong Buy|Buy|Hold|Sell|Strong Sell)\b/i,
            /\brecommend\s*(Strong Buy|Buy|Hold|Sell|Strong Sell)\b/i
        ];

        const text = element.textContent;

        for (const pattern of recommendationPatterns) {
            const match = text.match(pattern);
            if (match && match[1]) {
                return match[1];
            }
        }

        return null;
    }

    function getRecommendationClass(recommendation) {
        const normalized = recommendation.toLowerCase().trim();

        if (normalized.includes('strong buy')) return 'strong-buy';
        if (normalized.includes('buy')) return 'buy';
        if (normalized.includes('hold')) return 'hold';
        if (normalized.includes('sell') && normalized.includes('strong')) return 'strong-sell';
        if (normalized.includes('sell')) return 'sell';

        return '';
    }
}); 