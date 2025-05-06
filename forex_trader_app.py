import pandas as pd
import numpy as np
import pythoncom
import win32com.client
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import streamlit as st

# MT4 Connector
class MT4Bridge:
    def __init__(self):
        pythoncom.CoInitialize()
        self.mt4 = win32com.client.Dispatch("MT4.Terminal")
    
    def connect(self, server="Forex.com-UK", login=12345, password="your_password"):
        self.mt4.Connect(server, login, password)
    
    def get_rates(self, symbol="EURUSD", timeframe=15, count=1000):
        rates = self.mt4.CopyRatesFromPos(symbol, timeframe, 0, count)
        return pd.DataFrame(list(rates), columns=['time','open','high','low','close','volume'])

# LSTM Predictor
class ForexPredictor:
    def __init__(self):
        self.model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(60, 1)),
            LSTM(50),
            Dense(1)
        ])
        self.model.compile(optimizer='adam', loss='mse')
    
    def predict_next(self, data):
        last_60 = data[-60:].values.reshape(1, 60, 1)
        return self.model.predict(last_60)[0][0]

# Streamlit UI
st.title("Forex.com AI Trader")
bridge = MT4Bridge()
predictor = ForexPredictor()

if st.button("Get Prediction"):
    df = bridge.get_rates()
    prediction = predictor.predict_next(df['close'])
    st.metric("Next EUR/USD Close", f"{prediction:.5f}")
    st.line_chart(df.set_index('time')['close'])