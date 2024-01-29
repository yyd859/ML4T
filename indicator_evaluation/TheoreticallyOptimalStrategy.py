
import pandas as pd
import datetime as dt
from util import get_data, plot_data

def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "yyang3052"  # replace tb34 with your Georgia Tech username.

def testPolicy(symbols = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000):
    if isinstance(symbols, str):
        symbols = [symbols]
    prices = get_data(symbols, pd.date_range(sd, ed))
    prices = prices[symbols]
    df_trades = pd.DataFrame(index=prices.index, data=0, columns=symbols)
    holdings = {symbol: 0 for symbol in symbols}
    for i in range(1, len(prices)):
        for symbol in symbols:
            if prices[symbol].iloc[i] > prices[symbol].iloc[i - 1] and holdings[symbol] != 1000:
                df_trades[symbol].iloc[i-1] = 1000 - holdings[symbol]
                holdings[symbol] = 1000
            elif prices[symbol].iloc[i] < prices[symbol].iloc[i - 1] and holdings[symbol] != -1000:
                df_trades[symbol].iloc[i-1] = -1000 - holdings[symbol]
                holdings[symbol] = -1000
            # print('new price', prices[symbol].iloc[i], 'old price', prices[symbol].iloc[i - 1],
            #       holdings[symbol],df_trades[symbol].iloc[i-1])
    return df_trades
