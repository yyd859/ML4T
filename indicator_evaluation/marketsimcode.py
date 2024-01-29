import datetime as dt
import numpy as np
import pandas as pd
from util import get_data


def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "yyang3052"  # replace tb34 with your Georgia Tech username.

def compute_portvals(
    input_df,
    start_val=100000,
    commission=9.95,
    impact=0.005,
    start_date = dt.datetime(2008, 1, 1),
    end_date = dt.datetime(2009, 12, 31)
):
    df=input_df
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
            new_df = new_df.append({'Date': date, 'Symbol': symbol, 'Order': order, 'Shares': shares},
                                   ignore_index=True)
    new_df.set_index('Date', inplace=True)
    orders_df=new_df
    symbols = list(set(orders_df['Symbol'].tolist()))
    prices = get_data(symbols, pd.date_range(start_date, end_date))
    prices = prices[symbols]  # remove SPY
    prices = prices.assign(cash=1.00)
    start_date = prices.index.min().strftime("%Y-%m-%d")
    end_date = prices.index.max().strftime("%Y-%m-%d")
    trades = pd.DataFrame(0, index=prices.index, columns=prices.columns)
    for date in prices.index:
        if date in orders_df.index:
            date = date.strftime("%Y-%m-%d")
            orders_today = orders_df.loc[date]
            if isinstance(orders_today, pd.Series):
                orders_today = orders_today.to_frame().T
                orders_today.index.name = 'Date'
            for index, order_info in orders_today.iterrows():
                symbol = order_info['Symbol']
                shares = order_info['Shares']
                order_type = order_info['Order']
                price = prices.loc[date, symbol]
                transaction_cost = price * shares * impact + commission
                if order_type == 'BUY':
                    trades.loc[date, 'cash'] = trades.loc[date, 'cash'] - 1 * price * shares - transaction_cost
                    trades.loc[date, symbol] = trades.loc[date, symbol] + shares
                else:
                    trades.loc[date, 'cash'] = trades.loc[date, 'cash'] + price * shares - transaction_cost
                    trades.loc[date, symbol] = trades.loc[date, symbol] - shares
    holdings = pd.DataFrame(0, index=prices.index, columns=prices.columns)
    holdings.loc[start_date, 'cash'] = start_val
    holdings.iloc[0] = holdings.iloc[0] + trades.iloc[0]
    for i in range(1, len(trades)):
        holdings.iloc[i] = holdings.iloc[i - 1] + trades.iloc[i]
    values = prices * holdings
    portfolio_value = values.sum(axis=1)
    return portfolio_value

