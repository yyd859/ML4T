import datetime as dt
import pandas as pd
import numpy as np
from util import get_data, plot_data
orders_df_1 = pd.read_csv('/Users/yyd/Documents/ML4T_2023Fall/marketsim/orders/orders-01.csv',
                            index_col='Date', parse_dates=True, na_values=['nan'])
orders_df_5 = pd.read_csv('/Users/yyd/Documents/ML4T_2023Fall/marketsim/orders/orders-05.csv',
                            index_col='Date', parse_dates=True, na_values=['nan'])
for date in orders_df_1.index:
    date=date.strftime("%Y-%m-%d")
    orders_today = orders_df_1.loc[date]
    print(orders_today)
    break
for date in orders_df_5.index:
    date=date.strftime("%Y-%m-%d")
    orders_today = orders_df_5.loc[date]
    orders_today = orders_today.to_frame().T
    orders_today.index.name = 'Date'
    print(orders_today)
    break
# start_val = 1000000
# commission = 9.95
# impact = 0.005
# start_date = orders_df.index.min().strftime("%Y-%m-%d")
# end_date = orders_df.index.max().strftime("%Y-%m-%d")
# symbols=list(set(orders_df['Symbol'].tolist()))
# prices = get_data(symbols, pd.date_range(start_date, end_date))
# prices = prices[symbols]  # remove SPY
# prices=prices.assign(cash=1.00)
# trades=pd.DataFrame(0,index=prices.index,columns=prices.columns)
# for date in prices.index:
#     if date in orders_df.index:
#         date=date.strftime("%Y-%m-%d")
#         orders_today = orders_df.loc[date]
#         print(orders_today)
#         for index, order_info in orders_today.iterrows():
#             symbol = order_info['Symbol']
#             shares = order_info['Shares']
#             order_type = order_info['Order']
#             price=prices.loc[date,symbol]
#             transaction_cost=price*shares*impact+commission
#             if order_type == 'BUY':
#                 trades.loc[date,'cash']=trades.loc[date,'cash']-1*price*shares-transaction_cost
#                 trades.loc[date,symbol] = trades.loc[date,symbol]+shares
#             else:
#                 trades.loc[date, 'cash'] = trades.loc[date, 'cash']+price * shares - transaction_cost
#                 trades.loc[date, symbol] = trades.loc[date, symbol]-shares
# holdings=pd.DataFrame(0,index=prices.index,columns=prices.columns)
# holdings.loc[start_date,'cash']=start_val
# holdings.iloc[0]=holdings.iloc[0]+trades.iloc[0]
# for i in range(1, len(trades)):
#     holdings.iloc[i] = holdings.iloc[i - 1] + trades.iloc[i]
# values = prices * holdings
# portfolio_value = values.sum(axis=1)
# print(portfolio_value)