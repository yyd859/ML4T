import datetime as dt
import numpy as np
import pandas as pd
from util import get_data
import matplotlib.pyplot as plt
import TheoreticallyOptimalStrategy as tos
from marketsimcode import compute_portvals
import matplotlib.dates as mdates
from pathlib import Path
import indicators as ind
def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "yyang3052"  # replace tb34 with your Georgia Tech username.
def plot_tos():
    script_directory = Path(__file__).resolve().parent
    #Plot TOS
    a= compute_portvals(tos.testPolicy(),commission=0,impact=0)
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    benchmark = get_data(['JPM'], pd.date_range(sd, ed))
    benchmark = benchmark['JPM']
    benchmark_trades = pd.DataFrame(index=benchmark.index, data=0, columns=['JPM'])
    benchmark_trades.iloc[0]=1000
    b=compute_portvals(benchmark_trades,commission=0,impact=0)
    normed_prices_b = b/b.iloc[0]
    normed_prices_a = a / a.iloc[0]
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(benchmark.index, normed_prices_a, color='m', label='Benchmark')
    ax.plot(benchmark.index, normed_prices_b, color='r', label='Theoretically Optimal Strategy')
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.xticks(rotation=45)
    plt.xlim(benchmark.index[0], benchmark.index[-1])  # Set x-axis limits
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Value')
    plt.title('Theoretically Optimal Strategy vs. Benchmark for JPM')
    plt.savefig(script_directory/'images/TOS.png')
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
def df_tos():
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    a = compute_portvals(tos.testPolicy(), commission=0, impact=0)
    benchmark = get_data(['JPM'], pd.date_range(sd, ed))
    benchmark = benchmark['JPM']
    benchmark_trades = pd.DataFrame(index=benchmark.index, data=0, columns=['JPM'])
    benchmark_trades.iloc[0] = 1000
    b = compute_portvals(benchmark_trades, commission=0, impact=0)
    df=dataframe_statistics(a, b)
    return df
def plot_bollinger_bands_1(prices):
    prices = prices / prices.iloc[0]
    upper_band, sma, lower_band = ind.bollinger_bands(prices)
    script_directory = Path(__file__).resolve().parent
    plt.figure(figsize=(12, 6))
    plt.plot(prices.index, prices, color='blue', label='Price')
    plt.plot(prices.index, sma, color='red', label='SMA')
    plt.plot(prices.index, lower_band, color='y', label='lower band', linestyle='--')
    plt.plot(prices.index, upper_band, color='g', label='upper_band', linestyle='--')
    lower_band = lower_band.iloc[:, 0]
    upper_band = upper_band.iloc[:, 0]
    plt.fill_between(prices.index, lower_band, upper_band, color='gray', alpha=0.3)
    plt.xlabel('Date')
    plt.ylabel('Normalized Price')
    plt.title('Stock Price with Bollinger Bands')
    plt.legend()
    plt.savefig(script_directory / 'images/BB_1.png')
def plot_bollinger_bands_2(prices):
    bbp, signals = ind.bollinger_bands_percent(prices)
    script_directory = Path(__file__).resolve().parent
    plt.figure(figsize=(12, 6))
    plt.plot(bbp.index, bbp, color='blue', label='BBP')
    plt.axhline(y=100, color='black', linestyle='--')
    plt.axhline(y=0, color='black', linestyle='--')
    bbp = bbp.iloc[:, 0]
    plt.fill_between(bbp.index, bbp, 100, where=(bbp > 100), interpolate=True, color='green', label='Buy Zone',
                     alpha=0.5)
    plt.fill_between(bbp.index, bbp, 0, where=(bbp < 0), interpolate=True, color='red', label='Sell Zone', alpha=0.5)
    plt.fill_between(bbp.index, bbp, 100, where=(bbp <= 100), interpolate=True, color='grey', alpha=0.3)
    plt.fill_between(bbp.index, bbp, 0, where=(bbp >= 0), interpolate=True, color='grey', alpha=0.3)
    plt.xlabel('Date')
    plt.ylabel('Bollinger Bands Percentage (%)')
    plt.title('Bollinger Bands Percentage (BBP)')
    plt.legend()
    plt.savefig(script_directory / 'images/BB_2.png')
def plot_rsi(prices):
    rsi,signals=ind.rsi_signals(prices)
    script_directory = Path(__file__).resolve().parent
    plt.figure(figsize=(12, 6))
    plt.plot(rsi.index, rsi, color='blue', label='RSI')
    plt.axhline(y=70, color='black', linestyle='--')
    plt.axhline(y=30, color='black', linestyle='--')
    rsi=rsi.iloc[:,0]
    plt.fill_between(rsi.index, rsi, 70, where=(rsi > 70), interpolate=True, color='red', label='Sell Zone', alpha=0.5)
    plt.fill_between(rsi.index, rsi, 30, where=(rsi < 30), interpolate=True, color='green', label='Buy Zone', alpha=0.5)
    plt.fill_between(rsi.index, rsi, 70, where=(rsi <= 70), interpolate=True, color='grey', alpha=0.3)
    plt.fill_between(rsi.index, rsi, 30, where=(rsi >= 30), interpolate=True, color='grey', alpha=0.3)
    plt.xlabel('Date')
    plt.ylabel('Relative Strength Index')
    plt.title('Relative Strength Index (RSI)')
    plt.legend()
    plt.savefig(script_directory / 'images/RSI.png')
def plot_ema_1(prices):
    prices=prices/prices.iloc[0]
    script_directory = Path(__file__).resolve().parent
    ema_values=ind.ema(prices)
    prices = prices.iloc[:, 0]
    ema_values=ema_values.iloc[:,0]
    prices_on_ema=prices/ema_values
    plt.figure(figsize=(12, 6))
    plt.plot(prices.index, prices, label='Prices', color='blue', alpha=0.8)
    plt.plot(ema_values.index, ema_values, label='EMA', color='orange', alpha=0.8)
    plt.fill_between(prices.index, prices, ema_values, where=(ema_values > prices), color='green', alpha=0.3,
                     label='EMA > Prices')
    plt.fill_between(prices.index, prices, ema_values, where=(ema_values < prices), color='red', alpha=0.3,
                     label='EMA < Prices')
    plt.title('EMA vs. Prices')
    plt.xlabel('Date')
    plt.ylabel('EMA')
    plt.legend()
    plt.savefig(script_directory / 'images/EMA_1.png')
def plot_ema_2(prices):
    prices = prices / prices.iloc[0]
    script_directory = Path(__file__).resolve().parent
    ema_values = ind.ema(prices)
    prices = prices.iloc[:, 0]
    ema_values = ema_values.iloc[:, 0]
    prices_on_ema = prices / ema_values * 100
    plt.figure(figsize=(12, 6))
    plt.plot(prices_on_ema.index, prices_on_ema, color='blue', label='Price to EMA')
    plt.fill_between(prices_on_ema.index, prices_on_ema, 100, where=(prices_on_ema > 100), interpolate=True,
                     color='red', label='Sell Zone', alpha=0.5)
    plt.fill_between(prices_on_ema.index, prices_on_ema, 100, where=(prices_on_ema < 100), interpolate=True,
                     color='green', label='Buy Zone', alpha=0.5)
    plt.legend()
    plt.title('Price to EMA')
    plt.xlabel('Date')
    plt.ylabel('Price to EMA (%)')
    plt.savefig(script_directory / 'images/EMA_2.png')
def plot_std_jpm(prices):
    prices=prices/prices.iloc[0]
    script_directory = Path(__file__).resolve().parent
    prices = prices.iloc[:, 0]
    plt.figure(figsize=(12, 6))
    plt.plot(prices.index, prices, label='Prices', color='blue', alpha=0.8)
    plt.xlabel('Date')
    plt.ylabel('Normalized Price')
    plt.title('JPM Normalized Price')
    plt.legend()
    plt.savefig(script_directory / 'images/JPM_standard.png')
def plot_stochastic(prices):
    prices = prices.iloc[:, 0]
    script_directory = Path(__file__).resolve().parent
    k=ind.stochastic(prices)
    plt.figure(figsize=(12, 6))
    plt.plot(k.index, k, color='blue', label='Stochastic Indicator')
    plt.axhline(y=70, color='black', linestyle='--')
    plt.axhline(y=30, color='black', linestyle='--')
    plt.fill_between(k.index, k, 70, where=(k > 70), interpolate=True, color='red', label='Sell Zone', alpha=0.5)
    plt.fill_between(k.index, k, 30, where=(k < 30), interpolate=True, color='green', label='Buy Zone', alpha=0.5)
    plt.fill_between(k.index, k, 70, where=(k <= 70), interpolate=True, color='grey', alpha=0.3)
    plt.fill_between(k.index, k, 30, where=(k >= 30), interpolate=True, color='grey', alpha=0.3)
    plt.xlabel('Date')
    plt.ylabel('Stochastic Oscillator')
    plt.title('Stochastic Indicator')
    plt.legend()
    plt.savefig(script_directory / 'images/Stochastic.png')
def plot_momentum(prices):
    momentum,signals=ind.momentum_signals(prices)
    script_directory = Path(__file__).resolve().parent
    plt.figure(figsize=(12, 6))
    plt.plot(momentum.index, momentum, color='blue', label='Momentum')
    momentum=momentum.iloc[:,0]
    plt.fill_between(momentum.index, momentum, 0, where=(momentum > 0), interpolate=True, color='green', label='Buy Zone', alpha=0.5)
    plt.fill_between(momentum.index, momentum, 0, where=(momentum < 0), interpolate=True, color='red', label='Sell Zone', alpha=0.5)
    plt.xlabel('Date')
    plt.ylabel('Momentum Value')
    plt.title('Momentum')
    plt.legend()
    plt.savefig(script_directory / 'images/Momentum.png')
if __name__ == "__main__":
    plot_tos()
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)
    symbols = ['JPM']
    prices = get_data(symbols, pd.date_range(sd, ed))[symbols]
    plot_bollinger_bands_1(prices)
    plot_bollinger_bands_2(prices)
    plot_rsi(prices)
    plot_ema_1(prices)
    plot_ema_2(prices)
    plot_std_jpm(prices)
    plot_stochastic(prices)
    plot_momentum(prices)