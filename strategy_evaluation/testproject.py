import StrategyLearner as sl
import datetime as dt
import ManualStrategy as ms
import experiment1
import experiment2
def author():
  return 'yyang3052'

if __name__ == "__main__":
  ms.testPolicy(verbose=False)
  experiment1.exp_1_is()
  experiment1.exp_1_os()
  experiment2.exp_2()