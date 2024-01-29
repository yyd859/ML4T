import matplotlib.pyplot as plt
import numpy as np
import StrategyLearner as sl
import pandas as pd
import datetime as dt
from marketsimcode import compute_portvals
from pathlib import Path
def author():
  return 'yyang3052'
def compute_statistics(prices):
    daily_returns = prices.pct_change().dropna()
    cumulative_return = (prices.iloc[-1] / prices.iloc[0]) - 1
    stdev_daily_returns = daily_returns.std()
    return cumulative_return, stdev_daily_returns

def run_experiment(symbol, sd, ed, impacts, commission):
    metrics = {"cumulative_return": [], "std_dev": []}
    for impact in impacts:
        learner = sl.StrategyLearner(impact=impact, commission=commission)
        learner.add_evidence(symbol=symbol, sd=sd, ed=ed, sv=100000)
        df_trades = learner.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=100000)
        value = compute_portvals(df_trades)
        cr,std=compute_statistics(value)
        metrics["cumulative_return"].append(cr)
        metrics["std_dev"].append(std)
    return metrics

def plot_results(impacts, metrics):
    script_directory = Path(__file__).resolve().parent
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('Impact')
    ax1.set_ylabel('Cumulative Return', color=color)
    ax1.plot(impacts, metrics["cumulative_return"], color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('Std Dev of Daily Returns', color=color)
    ax2.plot(impacts, metrics["std_dev"], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.title('Impact of "Impact" on Trading Strategy')
    plt.savefig(script_directory / 'images/experiment_2.png')
def exp_2():
    symbol = "JPM"
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    impacts = np.arange(0, 0.21, 0.05)
    commission = 0.00
    experiment_results = run_experiment(symbol, sd, ed, impacts, commission)
    plot_results(impacts, experiment_results)
if __name__ == "__main__":
    print('yes')