from datetime import date, datetime

import numpy as np
import pandas as pd
import pandas_datareader.stooq as stooq
import streamlit as st


@st.cache
def download_stock_price(ticker: str, start: date, end: date):
    return stooq.StooqDailyReader(ticker, start, end).read()


st.title("Stock Price Dashboard")


ticker = "AAPL"
end = datetime.now().date()
start = datetime(end.year - 1, end.month, end.day).date()
df_stock = download_stock_price(ticker, start, end)

df_stock
