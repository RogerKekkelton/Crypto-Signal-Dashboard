from flask import Flask, jsonify, request
import requests
import pandas as pd

app = Flask(__name__)

@app.route("/data", methods=["GET"])
def get_binance_data():
    symbol = request.args.get("symbol", "BTCUSDT")
    interval = request.args.get("interval", "15m")
    limit = request.args.get("limit", "150")

    url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        df = pd.DataFrame(data, columns=[
            "Open Time", "Open", "High", "Low", "Close", "Volume",
            "Close Time", "Quote Asset Volume", "Number of Trades",
            "Taker Buy Base", "Taker Buy Quote", "Ignore"
        ])
        df["Open Time"] = pd.to_datetime(df["Open Time"], unit="ms")
        df["Open"] = pd.to_numeric(df["Open"])
        df["High"] = pd.to_numeric(df["High"])
        df["Low"] = pd.to_numeric(df["Low"])
        df["Close"] = pd.to_numeric(df["Close"])
        df["Volume"] = pd.to_numeric(df["Volume"])

        return df[["Open Time", "Open", "High", "Low", "Close", "Volume"]].to_json(orient="records")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
