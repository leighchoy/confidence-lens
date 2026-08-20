# confidence-lens
A quantitative ML and RAG oriented model using historical price data, sentiment analysis and economic context to provide confidence trade signals

1. Tech Stack and environment
Python, use of Alpha Vantage apis for fundamentals data and news and sentiment data. Use of yfinance for stock price data. Use of ta library in Python for technical analysis metrics. Use of Groq api for language model. Use of Logistic Regression, XGBoost classifier and Random Forest classifier for predictive signal model. Use of Streamlit for app.

2. Structure and Technical choices
i. Initially was using Finnhub for the news data and Finbert for making sentiment, discovered small limit to range of news dates so switched to Alpha Vantage which had sentiment built into the api and larger date range.
ii. Used ta library as opposed to manually creating technical analysis metrics due to ease and everything I needed was in the library
iii. Tried to use Claude and Gemini as language models but there was no free tier for Claude and Gemini was simply not working for me
iv. Used Logistic Regression as a baseline for my other 2 models. Use Random Forest and XGBoost classifiers as I wanted the model to produce a ‘Buy’ or ‘Don’t Buy/Hold’ signal. Initially tested on 350 rows of data and a forecast of 10 days. XGBoost proved to be the best overall performing model. Random Forest would likely need more rows of data.
v. Chose to use Streamlit to keep everything within Python as opposed to something like node.js for a symbiotically and simpler structure/project.
vi. No functions are defined in main.py.
3. Future Improvements
i. Can add versatility by adding real-time market data using Alpaca WebSocket stream
ii. Macroeconomic indicators such as interest rates for market wide context
iii. Comparable company analysis for sector wide analysis and context
iv. Instead of just giving signal on direction, could use regression models to predict range of price change
v. Proper backtesting or adding algorithmic trading options
vi. Paper trading for trading practice or testing of trading algorithms

mode = st.radio("Signal Mode",
                        ["High Precision (fewer, more accurate signals)",
                         "High Recall (more signals, lower accuracy)"])


    with col3:
        forecast = st.selectbox("Prediction Forecast",
                                 ["10 Days", "20 days", "1 month", "3 months"])

