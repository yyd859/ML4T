import pandas as pd
import numpy as np
import indicators as ind
from marketsimcode import compute_portvals
import datetime as dt
from util import get_data
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

def author():
  return 'yyang3052'

def aggregate_signals(prices, bb_n=14, bb_k=2, rsi_n=10, rsi_ul=70, rsi_ll=30, ema_window=12):
    # Calculate signals from each indicator
    _, bb_signals = ind.bollinger_bands_percent(prices, bb_n, bb_k)
    _, rsi_signals = ind.rsi_signals(prices, rsi_n, rsi_ul, rsi_ll)
    ema_signals = ind.generate_ema_signals(prices, ema_window)
    stocks = set(col.split('_')[0] for col in bb_signals.columns).union(
              col.split('_')[0] for col in rsi_signals.columns).union(
              col.split('_')[0] for col in ema_signals.columns)

    all_signals = {}

    for stock in stocks:
        # Retrieve signals for each indicator, using 0 if not available
        bb_signal = bb_signals[stock].fillna(-999)
        rsi_signal = rsi_signals[stock].fillna(-999)
        ema_signal = ema_signals[stock].fillna(-999)

        # Store the signals in the dictionary
        all_signals[stock] = {
            'BB': bb_signal,
            'RSI': rsi_signal,
            'EMA': ema_signal
        }
    aggregated_signals = pd.DataFrame(index=bb_signals.index)
    for stock, indicators in all_signals.items():
        # Aggregate signals for the stock
        stock_signals = sum(indicators.values())
        final_signals = stock_signals.apply(lambda x: 1 if x > 0 else (-1 if (x>-5 and x < 0) else 0))
        # Add to the aggregated signals DataFrame
        aggregated_signals[stock] = final_signals
    return aggregated_signals
def generate_trades(signals):
    trades = pd.DataFrame(0, index=signals.index, columns=signals.columns)

    # Previous state initialization
    prev_state = {stock: 0 for stock in signals.columns}

    for date, row in signals.iterrows():
        for stock in signals.columns:
            current_signal = row[stock]
            # Record a trade only if there is a state change
            if current_signal != prev_state[stock] and current_signal != 0:
                trades.at[date, stock] = current_signal
                prev_state[stock] = current_signal

    # Remove rows where all elements are zero (no trade for any stock)
    trades = trades[(trades != 0).any(axis=1)]
    for stock in trades.columns:
        prev_state = 0
        for date, signal in trades[stock].iteritems():
            if signal != 0:
                trade_size = 2000 if prev_state != 0 else 1000
                trades.at[date, stock] = signal * trade_size
                prev_state = signal
    return trades
def compute_statistics(prices):
    daily_returns = prices.pct_change().dropna()
    # Calculate statistics
    cumulative_return = (prices.iloc[-1] / prices.iloc[0]) - 1
    stdev_daily_returns = daily_returns.std()
    mean_daily_returns = daily_returns.mean()
    return cumulative_return, stdev_daily_returns, mean_daily_returns
def dataframe_statistics(portfolio, benchmark):
    portfolio_stats = compute_statistics(portfolio)
    benchmark_stats = compute_statistics(benchmark)
    df = pd.DataFrame(index=['Cumulative Return', 'Stdev of Daily Returns', 'Mean of Daily Returns'],
                      columns=['Portfolio', 'Benchmark'])
    df['Portfolio'] = portfolio_stats
    df['Benchmark'] = benchmark_stats
    pd.set_option('display.float_format', '{:.6f}'.format)
    return(df)
def testPolicy(symbol='JPM',sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000,
               verbose=False):
    script_directory = Path(__file__).resolve().parent
    if isinstance(symbol, str):
        symbol=[symbol]
    prices=get_data(symbol, pd.date_range(sd, ed))[symbol]
    signals=aggregate_signals(prices)
    trades= generate_trades(signals)

    a = compute_portvals(trades,start_date=sd,end_date=ed)
    benchmark = get_data(symbol, pd.date_range(sd, ed))[symbol]
    benchmark_trades = pd.DataFrame(index=benchmark.index, data=0, columns=symbol)
    benchmark_trades.iloc[0]=1000
    b=compute_portvals(benchmark_trades,start_date=sd,end_date=ed)
    normed_prices_b = b/b.iloc[0]
    normed_prices_a = a / a.iloc[0]
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(benchmark.index, normed_prices_a, color='m', label='ManualStrategy')
    ax.plot(benchmark.index, normed_prices_b, color='r', label='Benchmark')
    for date, trade in trades.iterrows():
        if trade[symbol[0]] > 0:  # Buy signal
            ax.axvline(x=date, color='blue', linestyle='--', linewidth=0.7)
        elif trade[symbol[0]] < 0:  # Sell signal
            ax.axvline(x=date, color='black', linestyle='--', linewidth=0.7)
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    plt.xlim(benchmark.index[0], benchmark.index[-1])  # Set x-axis limits
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Value')
    plt.title('In-sample performance')
    plt.savefig(script_directory / 'images/manual_strategy_1.png')
    df_stats_1=dataframe_statistics(normed_prices_b,normed_prices_a)
    if verbose:
        print(df_stats_1)



    sd=dt.datetime(2010,1,1)
    ed=dt.datetime(2011,12,31)
    prices=get_data(symbol, pd.date_range(sd, ed))[symbol]
    signals=aggregate_signals(prices)
    trades= generate_trades(signals)
    a = compute_portvals(trades,start_date=sd,end_date=ed)
    benchmark = get_data(symbol, pd.date_range(sd, ed))[symbol]
    benchmark_trades = pd.DataFrame(index=benchmark.index, data=0, columns=symbol)
    benchmark_trades.iloc[0]=1000
    b=compute_portvals(benchmark_trades,start_date=sd,end_date=ed)
    normed_prices_b = b/b.iloc[0]
    normed_prices_a = a / a.iloc[0]
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(benchmark.index, normed_prices_a, color='m', label='ManualStrategy')
    ax.plot(benchmark.index, normed_prices_b, color='r', label='Benchmark')
    for date, trade in trades.iterrows():
        if trade[symbol[0]] > 0:  # Buy signal
            ax.axvline(x=date, color='blue', linestyle='--', linewidth=0.7)
        elif trade[symbol[0]] < 0:  # Sell signal
            ax.axvline(x=date, color='black', linestyle='--', linewidth=0.7)
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    plt.xlim(benchmark.index[0], benchmark.index[-1])  # Set x-axis limits
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Value')
    plt.title('Out-sample performance')
    plt.savefig(script_directory / 'images/manual_strategy_2.png')
    df_stats_2 = dataframe_statistics(normed_prices_b, normed_prices_a)
    if verbose:
        print(df_stats_2)
    return trades

if __name__ == "__main__":
    print('yes')