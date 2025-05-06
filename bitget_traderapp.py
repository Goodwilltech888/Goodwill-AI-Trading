import ccxt
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
import streamlit as st

# Initialize Bitget
def init_exchange():
    return ccxt.bitget({
        'apiKey': st.secrets["BITGET_API_KEY"],
        'secret': st.secrets["BITGET_SECRET"],
        'password': st.secrets["BITGET_PASSPHRASE"]
    })

# AI Trading Core
class AITrader:
    def __init__(self):
        self.exchange = init_exchange()
        self.model = GradientBoostingClassifier(n_estimators=100)
    
    def fetch_data(self, symbol='BTC/USDT', timeframe='1h', limit=500):
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp','open','high','low','close','volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    
    def train_model(self, df):
        df['target'] = np.where(df['close'].shift(-1) > df['close'], 1, 0)
        features = df[['open','high','low','close','volume']]
        self.model.fit(features, df['target'])
        return df

# Streamlit UI
st.title("Bitget AI Trader")
trader = AITrader()

if st.button("Run AI Trading"):
    df = trader.fetch_data()
    df = trader.train_model(df)
    df['signal'] = trader.model.predict(df[['open','high','low','close','volume']])
    
    st.line_chart(df.set_index('timestamp')['close'])
    st.write("Latest Signal:", "BUY" if df.iloc[-1]['signal'] == 1 else "SELL")