import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf 
import plotly.express as px
from stocknews import StockNews     

st.title('Stock Dashboard')
ticker = st.sidebar.text_input('Ticker')
start_date = st.sidebar.date_input('Start Date')
end_date = st.sidebar.date_input('End Date')

data = yf.download(ticker, start=start_date, end=end_date)
fig = px.line(data, x=data.index, y=data['Adj Close'], title=ticker)
st.plotly_chart(fig)

st.header(f'News of {ticker}')
sn = StockNews(ticker, save_news=False)
df_news = sn.read_rss()

# List to store polarities of news summaries
summary_polarities = []

for i in range(10):
    st.subheader(f'News {i+1}')
    st.write(df_news['published'][i])
    st.write(df_news['title'][i])
    st.write(df_news['summary'][i])
    title_sentiment = df_news['sentiment_title'][i]
    st.write(f'Title Sentiment: {title_sentiment}')
    news_sentiment = df_news['sentiment_summary'][i]
    st.write(f'News Sentiment: {news_sentiment}')
    
    # Append polarity of news summary to the list
    summary_polarities.append(news_sentiment)

# Calculate average polarity
average_polarity = np.mean(summary_polarities)

st.subheader('FINAL DECISION :')
# Determine sentiment based on average polarity
sentiment_message = ""
if average_polarity > 0.5:
    sentiment_message = ("Based on the sentiment analysis of recent news articles, "
                         "it appears that the market sentiment towards this stock is overwhelmingly positive. "
                         "The news summaries exhibit a strong bullish tone, suggesting increasing confidence "
                         "and potential for upward movement in the stock price. Investors may find these sentiments "
                         "reassuring, indicating favorable conditions and potential opportunities for investment. "
                         "However, it's essential to conduct thorough research and consider various factors before "
                         "making any investment decisions.")
elif average_polarity < -0.5:
    sentiment_message = ("Analysis of recent news articles reveals a prevailing sentiment leaning towards caution or "
                         "pessimism regarding this stock. The summaries reflect concerns or negative outlooks that "
                         "could impact investor confidence and potentially lead to downward pressure on the stock price. "
                         "Investors may interpret these sentiments as warning signs or indications of potential risks "
                         "associated with holding or acquiring the stock. It's advisable for investors to exercise "
                         "caution and evaluate their investment strategies in light of this sentiment analysis.")
elif -0.1 <= average_polarity <= 0.1:
    sentiment_message = ("The sentiment analysis of recent news articles suggests a mixed or slightly negative outlook "
                         "for this stock. While not overwhelmingly bearish, the summaries indicate some reservations or "
                         "uncertainties that may give investors pause before considering significant investments. Factors "
                         "such as market conditions, industry trends, or company-specific developments may contribute to "
                         "this cautious sentiment. Investors may opt for a more conservative approach, awaiting further "
                         "clarity or positive signals before making substantial buying decisions.")
elif average_polarity > 0.1:
    sentiment_message = ("Based on the sentiment analysis of recent news articles, "
                         "it appears that the market sentiment towards this stock is positive. "
                         "The news summaries exhibit a strong bullish tone, suggesting increasing confidence "
                         "and potential for upward movement in the stock price. Investors may find these sentiments "
                         "reassuring, indicating favorable conditions and potential opportunities for investment. "
                         "However, it's essential to conduct thorough research and consider various factors before "
                         "making any investment decisions.")
elif average_polarity < -0.1:
    sentiment_message = ("Analysis of recent news articles reveals a prevailing sentiment leaning towards caution or "
                         "pessimism regarding this stock. The summaries reflect concerns or negative outlooks that "
                         "could impact investor confidence and potentially lead to downward pressure on the stock price. "
                         "Investors may interpret these sentiments as warning signs or indications of potential risks "
                         "associated with holding or acquiring the stock. It's advisable for investors to exercise "
                         "caution and evaluate their investment strategies in light of this sentiment analysis.")

# Display sentiment message
if sentiment_message:
    st.write(sentiment_message)
