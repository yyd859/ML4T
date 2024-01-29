import pandas as pd
import datetime as dt
from util import get_data, plot_data
symbols = ['JPM','AAPL']
if isinstance(symbols, str):
    symbols=[symbols]
sd=dt.datetime(2008, 1, 1)
ed=dt.datetime(2009,12,31)
prices = get_data(symbols, pd.date_range(sd, ed))
prices=prices[symbols]
df_trades = pd.DataFrame(index=prices.index, data=0, columns=symbols)
holdings = {symbol: 0 for symbol in symbols}



for i in range(1, len(prices)):
    for symbol in symbols:
        # Knowing the future, buy low sell high
        if prices[symbol].iloc[i] > prices[symbol].iloc[i - 1] and holdings[symbol] != 1000:
            df_trades[symbol].iloc[i] = 1000 - holdings[symbol]  # Buy to hold 1000 if price will go up
            holdings[symbol] = 1000  # update holding
        elif prices[symbol].iloc[i] < prices[symbol].iloc[i - 1] and holdings[symbol] != -1000:
            df_trades[symbol].iloc[i] = -1000 - holdings[symbol]  # Sell to hold -1000 if price will go down
            holdings[symbol] = -1000  # update holding

df=df_trades
new_df = pd.DataFrame(columns=['Date', 'Symbol', 'Order', 'Shares'])

# Iterate through the rows of the original DataFrame
for date, row in df.iterrows():
    for symbol, value in row.items():
        if value > 0:
            order = 'BUY'
        elif value < 0:
            order = 'SELL'
        else:
            continue

        shares = abs(value)  # Take the absolute value of the change
        new_df = new_df.append({'Date': date, 'Symbol': symbol, 'Order': order, 'Shares': shares}, ignore_index=True)

# Print the new DataFrame
print(prices)
import pandas as pd
import numpy as np
