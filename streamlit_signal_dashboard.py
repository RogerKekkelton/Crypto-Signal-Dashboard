# Streamlit Signal Dashboard (Fixed with Data Check)
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from live_signal_backend import fetch_binance_ohlcv, generate_signal

df = fetch_binance_ohlcv()

if df.empty or len(df) < 60:
    st.error("Unable to fetch sufficient data from Binance. Try reloading.")
    st.stop()

signal = generate_signal(df)

st.set_page_config(page_title="Live Crypto Signal Dashboard", layout="wide")
st.title("Live Crypto Signal Dashboard")

col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Price Chart with Indicators")
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                                 low=df['Low'], close=df['Close'], name='Candles'))
    upper = df['Close'].rolling(20).mean() + 2*df['Close'].rolling(20).std()
    lower = df['Close'].rolling(20).mean() - 2*df['Close'].rolling(20).std()
    fig.add_trace(go.Scatter(x=df.index, y=upper, name='Upper BB'))
    fig.add_trace(go.Scatter(x=df.index, y=lower, name='Lower BB'))
    fig.update_layout(height=600, xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Current Signal")
    st.markdown(f"**Time:** {signal['time']}")
    st.markdown(f"**Price:** ${signal['price']}")
    st.markdown(f"**Signal:** `{signal['signal']}`")
    st.markdown(f"**Confidence:** {signal['confidence']}%")
    st.markdown("**Confluence Logs:**")
    for item in signal['log']:
        st.markdown(f"- {item}")
    st.markdown("---")
    st.markdown(f"**RSI:** {signal['rsi']}")
    st.markdown(f"**OBV Trend:** {signal['obv_trend']}")
    st.markdown(f"**Ichimoku Bullish:** {signal['ichimoku_bullish']}")
    st.markdown(f"**Fibonacci Support Zone:** {signal['fib_support_zone']}")
    st.markdown(f"**Break of Structure:** {signal['bos']}")
    st.markdown(f"**Liquidity Sweep Detected:** {signal['swept_low']}")
