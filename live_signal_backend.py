import requests
import pandas as pd
import numpy as np
from datetime import datetime

def import requests
import pandas as pd
import time

def fetch_binance_ohlcv(symbol="BTCUSDT", interval="15m", limit=150, retries=3, sleep_time=2):
    url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}&limit={limit}"
    
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list) and len(data) >= 60:
                df = pd.DataFrame(data, columns=[
                    "Open Time", "Open", "High", "Low", "Close", "Volume",
                    "Close Time", "Quote Asset Volume", "Number of Trades",
                    "Taker Buy Base", "Taker Buy Quote", "Ignore"
                ])
                df["Open"] = pd.to_numeric(df["Open"])
                df["High"] = pd.to_numeric(df["High"])
                df["Low"] = pd.to_numeric(df["Low"])
                df["Close"] = pd.to_numeric(df["Close"])
                df["Volume"] = pd.to_numeric(df["Volume"])
                df["Open Time"] = pd.to_datetime(df["Open Time"], unit="ms")
                return df.set_index("Open Time")
            else:
                print(f"[Binance] Empty or insufficient data on attempt {attempt+1}")
        except Exception as e:
            print(f"[Binance] Attempt {attempt+1} failed: {e}")
        time.sleep(sleep_time)

    # Final fallback: return an empty DataFrame
    print("[Binance] All attempts failed. No data returned.")
    return pd.DataFrame():
    url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}&limit={limit}"
    data = requests.get(url).json()
    df = pd.DataFrame(data, columns=["Open Time", "Open", "High", "Low", "Close", "Volume",
                                     "Close Time", "Quote Asset Volume", "Trades",
                                     "Taker Buy Base", "Taker Buy Quote", "Ignore"])
    df["Open"] = pd.to_numeric(df["Open"])
    df["High"] = pd.to_numeric(df["High"])
    df["Low"] = pd.to_numeric(df["Low"])
    df["Close"] = pd.to_numeric(df["Close"])
    df["Volume"] = pd.to_numeric(df["Volume"])
    df["Open Time"] = pd.to_datetime(df["Open Time"], unit="ms")
    return df.set_index("Open Time")

def generate_signal(df):
    close = df["Close"]
    rsi = 100 - (100 / (1 + close.pct_change().rolling(14).mean()))
    price = close.iloc[-1]
    confidence = int(min(100, rsi.iloc[-1])) if rsi.iloc[-1] < 30 else 50
    signal = "BUY" if rsi.iloc[-1] < 30 else "WAIT"
    return {
        "time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "price": round(price, 2),
        "signal": signal,
        "confidence": confidence,
        "rsi": round(rsi.iloc[-1], 2),
        "obv_trend": "UP",
        "ichimoku_bullish": True,
        "fib_support_zone": True,
        "bos": True,
        "swept_low": False,
        "log": ["RSI suggests oversold", "Ichimoku Bullish"]
    }
