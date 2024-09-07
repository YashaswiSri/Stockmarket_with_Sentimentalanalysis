import streamlit as st,pandas as pd,numpy as np,yfinance as yf 
import plotly.express as px
    
st.title('Stock Dashboard')
ticker=st.sidebar.text_input('Ticker')
start_date=st.sidebar.date_input('Start Date')
end_date=st.sidebar.date_input('End Date')

data=yf.download(ticker,start=start_date,end=end_date)
fig=px.line(data,x=data.index,y=data['Adj Close'],title=ticker)
st.plotly_chart(fig)


from stocknews import StockNews     
st.header(f'News of {ticker}')
sn=StockNews(ticker,save_news=False)
df_news=sn.read_rss()
for i in range(10):
    st.subheader(f'News {i+1}')
    st.write(df_news['published'][i])
    st.write(df_news['title'][i])
    st.write(df_news['summary'][i])
    title_sentiment=df_news['sentiment_title'][i]
    st.write(f'Title Sentiment {title_sentiment}')
    news_sentiment=df_news['sentiment_summary'][i]
    st.write(f'News Sentiment {news_sentiment}')