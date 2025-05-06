import streamlit as st
import ccxt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from sklearn.ensemble import RandomForestClassifier

# Initialize Binance API
exchange = ccxt.binance()

# App title
st.title("🚀 AI Trading Dashboard")
st.sidebar.header("Settings")

# User inputs
symbol = st.sidebar.selectbox("Select Crypto", ["BTC/USDT", "ETH/USDT", "SOL/USDT"])
timeframe = st.sidebar.selectbox("Timeframe", ["1m", "5m", "15m", "1h"])
initial_balance = st.sidebar.number_input("Initial Balance (USDT)", 1000)

# Fetch OHLCV data
@st.cache_data(ttl=60)  # Cache for 1 minute
def get_data(symbol, timeframe, limit=500):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

df = get_data(symbol, timeframe)

# Technical Indicators
def add_indicators(df):
    # RSI
    df["rsi"] = RSIIndicator(df["close"], window=14).rsi()
    
    # Bollinger Bands
    indicator_bb = BollingerBands(df["close"], window=20, window_dev=2)
    df["bb_upper"] = indicator_bb.bollinger_hband()
    df["bb_lower"] = indicator_bb.bollinger_lband()
    
    # Target (1 if next candle is green, 0 if red)
    df["target"] = np.where(df["close"].shift(-1) > df["close"], 1, 0)
    return df

df = add_indicators(df)

# Train AI Model
features = ["rsi", "bb_upper", "bb_lower", "close"]
X = df[features].dropna()
y = df["target"].dropna()

model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# Generate predictions
df["prediction"] = model.predict(X)

# Trading Simulation
balance = initial_balance
position = 0
trades = []

for i in range(1, len(df)):
    if df["prediction"].iloc[i] == 1 and position <= 0:  # Buy signal
        position = balance / df["close"].iloc[i]
        balance = 0
        trades.append({"type": "BUY", "price": df["close"].iloc[i], "time": df["timestamp"].iloc[i]})
    elif df["prediction"].iloc[i] == 0 and position > 0:  # Sell signal
        balance = position * df["close"].iloc[i]
        position = 0
        trades.append({"type": "SELL", "price": df["close"].iloc[i], "time": df["timestamp"].iloc[i]})

# Calculate final portfolio value
final_value = balance if balance > 0 else position * df["close"].iloc[-1]
profit_pct = ((final_value - initial_balance) / initial_balance) * 100

# Display Results
col1, col2 = st.columns(2)
col1.metric("Initial Balance", f"${initial_balance:,.2f}")
col2.metric("Final Value", f"${final_value:,.2f}", f"{profit_pct:.2f}%")

# Price Chart with Signals
fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=df["timestamp"],
    open=df["open"],
    high=df["high"],
    low=df["low"],
    close=df["close"],
    name="Price"
))

# Add Bollinger Bands
fig.add_trace(go.Scatter(
    x=df["timestamp"],
    y=df["bb_upper"],
    line=dict(color="rgba(255, 0, 0, 0.5)"),
    name="Upper Band"
))
fig.add_trace(go.Scatter(
    x=df["timestamp"],
    y=df["bb_lower"],
    line=dict(color="rgba(0, 255, 0, 0.5)"),
    name="Lower Band"
))

# Add buy/sell markers
buy_signals = df[df["prediction"] == 1]
sell_signals = df[df["prediction"] == 0]

fig.add_trace(go.Scatter(
    x=buy_signals["timestamp"],
    y=buy_signals["close"],
    mode="markers",
    marker=dict(color="green", size=10, symbol="triangle-up"),
    name="Buy Signal"
))
fig.add_trace(go.Scatter(
    x=sell_signals["timestamp"],
    y=sell_signals["close"],
    mode="markers",
    marker=dict(color="red", size=10, symbol="triangle-down"),
    name="Sell Signal"
))

fig.update_layout(title=f"{symbol} Price with AI Signals")
st.plotly_chart(fig, use_container_width=True)

# Trade History
st.subheader("Trade Log")
trades_df = pd.DataFrame(trades)
st.dataframe(trades_df)

# Feature Importance
st.subheader("AI Model Insights")
feature_importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
}).sort_values("Importance", ascending=False)
st.bar_chart(feature_importance.set_index("Feature"))