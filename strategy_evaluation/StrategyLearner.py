""""""
"""  		  	   		  		 		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		  		 		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		  		 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		  		 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		  		 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 		  		  		    	 		 		   		 		  
or edited.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		  		 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		  		 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		  	   		  		 		  		  		    	 		 		   		 		  
GT User ID: tb34 (replace with your User ID)  		  	   		  		 		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		  	   		  		 		  		  		    	 		 		   		 		  
"""

import datetime as dt
import random
import RTLearner as RT
from indicators import bbp, rsi, ema
import pandas as pd
import util as ut


class StrategyLearner(object):
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		  		 		  		  		    	 		 		   		 		  
        If verbose = False your code should not generate ANY output.  		  	   		  		 		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		  		 		  		  		    	 		 		   		 		  
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		  		 		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		  		 		  		  		    	 		 		   		 		  
    :param commission: The commission amount charged, defaults to 0.0  		  	   		  		 		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		  		 		  		  		    	 		 		   		 		  
    """

    # constructor  		  	   		  		 		  		  		    	 		 		   		 		  
    def author():
        return 'yyang3052'

    def __init__(self, verbose=False, impact=0.0, commission=0.0):
        """  		  	   		  		 		  		  		    	 		 		   		 		  
        Constructor method  		  	   		  		 		  		  		    	 		 		   		 		  
        """
        self.verbose = verbose
        self.impact = impact
        self.commission = commission
        self.learner = RT.RTLearner(leaf_size=5)

    def calculate_Y(self,prices, N=10, YBUY=0.05, YSELL=0.05):
        future_returns = (prices.shift(-N) / prices) - 1.0
        Y = pd.Series(index=prices.index, data=0)  # Default to CASH
        Y[future_returns > YBUY] = 1  # LONG
        Y[future_returns < YSELL] = -1  # SHORT
        return Y[:-N]

    def calculate_features(self,prices):
        features = pd.DataFrame(index=prices.index)
        features['BBP'] = bbp(prices)
        features['RSI'] = rsi(prices)
        features['EMA'] = ema(prices)
        return features

    def add_evidence(
            self,
            symbol="IBM",
            sd=dt.datetime(2008, 1, 1),
            ed=dt.datetime(2009, 1, 1),
            sv=100000,
    ):
        prices = ut.get_data([symbol], pd.date_range(sd, ed))
        X = self.calculate_features(prices[symbol])[:-10] # remove the rows without Y values
        Y = self.calculate_Y(prices[symbol])
        self.learner.add_evidence(X, Y)

    def generate_trades(self,signals):
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
    def testPolicy(self, symbol, sd, ed, sv):
        prices = ut.get_data([symbol], pd.date_range(sd, ed))
        X = self.calculate_features(prices[symbol])
        raw_predictions = self.learner.query(X)
        predictions = pd.DataFrame(raw_predictions, index=X.index)
        # Convert predictions to trades DataFrame
        trades = self.generate_trades(predictions)
        trades.columns=[symbol]
        return trades

if __name__ == "__main__":
    print("One does not simply think up a strategy")
