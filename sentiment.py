import streamlit as st
import json
from datetime import datetime, timedelta
from faker import Faker
from faker.providers import date_time
from faker.providers import internet
import random

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import pytz
from dotenv import load_dotenv
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from plotly.utils import PlotlyJSONEncoder

fake = Faker()
Faker.seed(20)

date_format = "%b-%d-%y %H:%M %S"
EST = pytz.timezone('US/Eastern')


def get_price_history(ticker):

    data_dict = []

    date = datetime.now() - timedelta(days=20)

    for i in range(20):

        date_time_num = date + timedelta(days=i)
        price = random.randrange(100)
        data_dict.append([date_time_num.strftime(date_format), price])

    # Set column names
    columns = ['Date Time', 'Price']
    df = pd.DataFrame(data_dict, columns=columns)
    df['Date Time'] = pd.to_datetime(df['Date Time'], format=date_format)
    df.sort_values(by='Date Time', ascending=True)
    df.reset_index(inplace=True)
    df.drop('index', axis=1, inplace=True)

    return df


def get_news(ticker) -> pd.DataFrame:

    date = datetime.now() - timedelta(days=3)

    data_dict = []
    for i in range(20):

        date_time_i_str = (
            date - timedelta(days=random.randrange(3))).strftime(date_format)
        title_i = fake.paragraph(nb_sentences=1)
        description_i = fake.paragraph(nb_sentences=3)
        link_i = fake.uri()
        data_dict.append(
            [date_time_i_str, title_i, description_i, f'<a href="{link_i}">{title_i}</a>'])

    # Set column names
    columns = ['Date Time', 'Headline', 'Description', 'Headline + Link']
    df = pd.DataFrame(data_dict, columns=columns)
    df['Date Time'] = pd.to_datetime(
        df['Date Time'], format=date_format, utc=False)

    df.sort_values(by='Date Time', ascending=False)
    df.reset_index(inplace=True)
    df.drop('index', axis=1, inplace=True)

    return df


def score_news(news_df) -> pd.DataFrame:
    vader = SentimentIntensityAnalyzer()
    scores = news_df['Headline'].apply(vader.polarity_scores).tolist()
    scores_df = pd.DataFrame(scores)

    # Join the DataFrames of the news and the list of dicts
    scored_news_df = news_df.join(scores_df, rsuffix='_right')
    scored_news_df = scored_news_df.set_index('Date Time')
    scored_news_df = scored_news_df.rename(
        columns={"compound": "Sentiment Score"})

    return scored_news_df


def plot_sentiment(df, ticker) -> go.Figure:

    # Group by date and ticker columns from scored_news and calculate the max
    max_scores = df.resample('h').max(numeric_only=True)

    # Plot a bar chart with plotly
    fig = px.bar(data_frame=max_scores, x=max_scores.index, y='Sentiment Score',
                 title=f"{ticker} Hourly Sentiment Scores")
    return fig


def plot_hourly_price(df, ticker) -> go.Figure:

    fig = px.line(data_frame=df, x=df['Date Time'],
                  y="Price", title=f"{ticker} Price")
    return fig


def convert_headline_to_link(df: pd.DataFrame) -> pd.DataFrame:

    df['Headline'] = df['Headline + Link']
    df.drop('Headline + Link', inplace=True, axis=1)

    return df


def style_negative(v, props=''):
    return props if float(v) < 0.5000 else None


def style_positive(v, props=''):
    return props if float(v) > 0.5000 else None


def main():

    st.title('Stock Analysis App')

    ticker = st.text_input('Enter Stock Ticker').strip().upper()

    if st.button('Analyze'):

        news_df = get_news(ticker)
        scored_news_df = score_news(news_df)
        fig_bar_sentiment = plot_sentiment(scored_news_df, ticker)
        fig_line_price_history = plot_hourly_price(
            get_price_history(ticker), ticker)
        scored_news_df = convert_headline_to_link(scored_news_df)

        st.plotly_chart(fig_bar_sentiment)
        st.plotly_chart(fig_line_price_history)
        #st.write(scored_news_df.to_html(classes='mystyle',
                                        # render_links=True, escape=False))


if __name__ == '__main__':
    main()





'''pricing_data,fundamental_data,news=st.tabs(["Pricing Data","Fundamental Data","Top 10 News"])



with pricing_data:
    st.header('Price Movements')
    data2=data
    data2['%Change']=data['Adj Close']/data['Adj Close'].shift(1)-1
    data2.dropna(inplace=True)
    st.write(data2)
    annual_return=data2['%Change'].mean()*252*100
    st.write('Annual Return is ',annual_return,'%')
    stdev=np.std(data2['%Change'])*np.sqrt(252)
    st.write('Standard Deviation is ',stdev*100,'%')
    st.write('Risk Adj. Return is ',annual_return/(stdev*100))
    
    
from alpha_vantage.fundamentaldata import FundamentalData
with fundamental_data:
    key='7BL7X8AB5I263X5N'
    fd=FundamentalData(key,output_format='pandas')
    st.subheader('Balance sheet')
    balance_sheet=fd.get_balance_sheet_annual(ticker)[0]
    bs=balance_sheet.T[2:]
    bs.columns=list(balance_sheet.T.iloc[0])
    st.write(bs)
    st.subheader('Income Statement')
    income_statement=fd.get_income_statement_annual(ticker)[0]
    is1=income_statement.T[2:]
    is1.columns=list(income_statement.T.iloc[0])
    st.write(is1)
    st.subheader('Cash Flow Statement')
    cash_flow=fd.get_cash_flow_annual(ticker)[0]
    cf=cash_flow.T[2:]
    cf.columns=list(cash_flow.T.iloc[0])
    st.write(cf)
   
    
from stocknews import StockNews
with news:
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
        st.write(f'News Sentiment {news_sentiment}')'''
        
        