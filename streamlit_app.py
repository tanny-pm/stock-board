from datetime import date, datetime

import numpy as np
import pandas as pd
import pandas_datareader.stooq as stooq
import plotly.graph_objects as go
import streamlit as st


@st.cache
def download_stock_price(ticker: str, start: date, end: date):
    return stooq.StooqDailyReader(ticker, start, end).read()


st.title("Stock Price Dashboard")

with st.form("input_ticker"):
    ticker = st.text_input("Ticker", "AAPL")
    submitted = st.form_submit_button("Submit")
    if submitted:
        end = datetime.now().date()
        start = datetime(end.year - 1, end.month, end.day).date()
        df_stock = download_stock_price(ticker, start, end)

st.header("Dataframe")
st.dataframe(df_stock.style.highlight_max(axis=0), use_container_width=True)


# https://myfrankblog.com/stock_price_chart_with_python_plotly/

st.header("Candlestick chart")
fig = go.Figure(
    data=[
        go.Candlestick(
            x=df_stock.index,
            open=df_stock["Open"],
            high=df_stock["High"],
            low=df_stock["Low"],
            close=df_stock["Close"],
            showlegend=False,
        )
    ]
)
fig.update_layout(
    title_text=f"CandlestickChart of {ticker}",
    yaxis_title="Price",
    xaxis_title="Date",
)
fig.update_xaxes(tickformat="%Y/%m/%d")
fig.update_yaxes(separatethousands=True)
st.plotly_chart(fig)
