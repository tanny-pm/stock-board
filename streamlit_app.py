from datetime import date, datetime

import pandas as pd
import pandas_datareader.stooq as stooq
import plotly.graph_objects as go
import streamlit as st


@st.cache
def download_stock_price(ticker: str, start: date, end: date):
    df_stock = stooq.StooqDailyReader(ticker, start, end).read()
    if len(df_stock) == 0:
        raise ValueError("No data found")
    return df_stock


df_stock = pd.DataFrame()

st.title("Stock Price Dashboard")

# Input form
with st.sidebar.form("input_ticker"):
    ticker = st.text_input("Ticker", "AAPL")
    submitted = st.form_submit_button("Submit")
    if submitted:
        end = datetime.now().date()
        start = datetime(end.year - 1, end.month, end.day).date()
        try:
            df_stock = download_stock_price(ticker, start, end)
        except ValueError as e:
            st.error(e, icon="🚨")

# Output
tab1, tab2 = st.tabs(["📈 Chart", "🗒️ Table"])

with tab1:
    st.header("Candlestick chart")
    if df_stock.empty:
        st.info("No data. Submit the ticker.", icon="ℹ️")
    else:
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
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Dataframe")
    if df_stock.empty:
        st.info("No data. Submit the ticker.", icon="ℹ️")
    else:
        st.dataframe(df_stock.style.highlight_max(axis=0), use_container_width=True)
