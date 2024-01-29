from ManualStrategy import aggregate_signals, generate_trades
from marketsimcode import compute_portvals
import StrategyLearner as sl
import numpy as np
import pandas as pd
from util import get_data
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

def author():
  return 'yyang3052'
def exp_1_is():
    script_directory = Path(__file__).resolve().parent
    symbol="JPM"
    if isinstance(symbol, str):
        symbol=[symbol]
    sd=dt.datetime(2008,1,1)
    ed=dt.datetime(2009,12,31)
    prices = get_data(symbol, pd.date_range(sd, ed))
    signals = aggregate_signals(prices)
    trades = generate_trades(signals)
    a = compute_portvals(trades, start_date=sd, end_date=ed)
    benchmark = get_data(symbol, pd.date_range(sd, ed))[symbol]
    benchmark_trades = pd.DataFrame(index=benchmark.index, data=0, columns=symbol)
    benchmark_trades.iloc[0] = 1000
    b = compute_portvals(benchmark_trades, start_date=sd, end_date=ed)
    learner = sl.StrategyLearner(verbose=False, impact=0.005, commission=9.95)  # constructor
    learner.add_evidence(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31),
                         sv=100000)  # training phase
    df_trades = learner.testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31),
                                   sv=100000)  # testing phase
    c=compute_portvals(df_trades,start_date=sd,end_date=ed)
    normed_prices_b = b / b.iloc[0]
    normed_prices_a = a / a.iloc[0]
    normed_prices_c= c/c.iloc[0]
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(benchmark.index, normed_prices_a, color='m', label='ManualStrategy')
    ax.plot(benchmark.index, normed_prices_b, color='r', label='Benchmark')
    ax.plot(benchmark.index, normed_prices_c, color='g', label='StrategyLearner')
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    plt.xlim(benchmark.index[0], benchmark.index[-1])  # Set x-axis limits
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Value')
    plt.title('In-sample performance')
    plt.savefig(script_directory / 'images/experiment_1_in_sample.png')

def exp_1_os():
    script_directory = Path(__file__).resolve().parent
    symbol="JPM"
    if isinstance(symbol, str):
        symbol=[symbol]
    sd=dt.datetime(2010,1,1)
    ed=dt.datetime(2011,12,31)
    prices = get_data(symbol, pd.date_range(sd, ed))
    signals = aggregate_signals(prices)
    trades = generate_trades(signals)
    a = compute_portvals(trades, start_date=sd, end_date=ed)
    benchmark = get_data(symbol, pd.date_range(sd, ed))[symbol]
    benchmark_trades = pd.DataFrame(index=benchmark.index, data=0, columns=symbol)
    benchmark_trades.iloc[0] = 1000
    b = compute_portvals(benchmark_trades, start_date=sd, end_date=ed)
    learner = sl.StrategyLearner(verbose=False, impact=0.005, commission=9.95)  # constructor
    learner.add_evidence(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31),
                         sv=100000)  # training phase
    df_trades = learner.testPolicy(symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31),
                                   sv=100000)  # testing phase
    c=compute_portvals(df_trades,start_date=sd,end_date=ed)
    normed_prices_b = b / b.iloc[0]
    normed_prices_a = a / a.iloc[0]
    normed_prices_c= c/c.iloc[0]
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(benchmark.index, normed_prices_a, color='m', label='ManualStrategy')
    ax.plot(benchmark.index, normed_prices_b, color='r', label='Benchmark')
    ax.plot(benchmark.index, normed_prices_c, color='g', label='StrategyLearner')
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    plt.xlim(benchmark.index[0], benchmark.index[-1])  # Set x-axis limits
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Value')
    plt.title('Out-sample performance')
    plt.savefig(script_directory / 'images/experiment_1_out_sample.png')
if __name__ == "__main__":
    # np.random.seed(903952220)
    # exp_1_is()
    # exp_1_os()
    print('Yes')