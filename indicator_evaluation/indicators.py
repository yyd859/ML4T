import pandas as pd
from util import get_data, plot_data
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "yyang3052"  # replace tb34 with your Georgia Tech username.


def bollinger_bands(prices, n=14, k=2):
    sma = prices.rolling(window=n).mean()
    rolling_std = prices.rolling(window=n).std()
    upper_band = sma + (rolling_std * k)
    lower_band = sma - (rolling_std * k)
    return upper_band, sma, lower_band
def bollinger_bands_percent(prices, n=14, k=2):
    upper_band, sma, lower_band = bollinger_bands(prices, n, k)
    bbp = (prices - lower_band) / (upper_band - lower_band)*100
    bbp[:n - 1] = np.nan
    signals = bbp.applymap(lambda x: -1 if x > 1 else (1 if x < 0 else (0 if not np.isnan(x) else np.nan)))
    return bbp, signals
def rsi(prices, n=10):
    delta = prices.diff().dropna()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.rolling(window=n).mean()
    avg_loss = loss.rolling(window=n).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
def rsi_signals(prices, n=10,ul=70,ll=30):
    rsi_values = rsi(prices, n)
    signals = rsi_values.applymap(lambda x: -1 if x > ul else (1 if x < ll else 0))
    return rsi_values, signals

def ema(prices, window=12):
    ema = prices.ewm(span=window, adjust=False).mean()
    return ema

def generate_ema_signals(prices, window=12):
    ema_values = ema(prices, window)
    signals = pd.Series(0, index=prices.index)
    signals[prices > ema_values] = 1
    signals[prices < ema_values] = -1
    return signals



