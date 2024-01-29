""""""  		  	   		  		 		  		  		    	 		 		   		 		  
"""  		  	   		  		 		  		  		    	 		 		   		 		  
Test a learner.  (c) 2015 Tucker Balch  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
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
"""  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
import math  		  	   		  		 		  		  		    	 		 		   		 		  
import sys  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
import numpy as np  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
import LinRegLearner as lrl
import RTLearner as rt
import DTLearner as dt
from pathlib import Path
import matplotlib.pyplot as plt
import BagLearner as bl
import time
import resource

def memory_usage():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
def data_prep(alldata):
    datasize = alldata.shape[0]
    cutoff = int(datasize * 0.6)
    permutation = np.random.permutation(alldata.shape[0])
    col_permutation = np.random.permutation(alldata.shape[1] - 1)
    train_data = alldata[permutation[:cutoff], :]
    train_x = train_data[:, col_permutation]
    train_y = train_data[:, -1]
    test_data = alldata[permutation[cutoff:], :]
    test_x = test_data[:, col_permutation]
    test_y = test_data[:, -1]
    return train_x,train_y,test_x,test_y
def test_learner(alldata,leaf_sizes,bagging=False,bag=20):
    train_x, train_y, test_x, test_y=data_prep(alldata)
    train_rmse = []
    test_rmse = []
    if bagging==False:
        for leaf_size in leaf_sizes:
            leaf_size={"leaf_size":leaf_size}
            learner = dt.DTLearner(**leaf_size)
            learner.add_evidence(train_x, train_y)
            train_predictions = learner.query(train_x)
            train_rmse.append(np.sqrt(np.mean((train_predictions - train_y) ** 2)))
            test_predictions = learner.query(test_x)
            test_rmse.append(np.sqrt(np.mean((test_predictions - test_y) ** 2)))
        min_test_rmse_leaf_size = leaf_sizes[np.argmin(test_rmse)]
        return train_rmse,test_rmse,min_test_rmse_leaf_size
    if bagging==True:
        for leaf_size in leaf_sizes:
            learner = bl.BagLearner(learner=dt.DTLearner, kwargs={'leaf_size': leaf_size}, bags=bag)
            learner.add_evidence(train_x, train_y)
            train_predictions = learner.query(train_x)
            train_rmse.append(np.sqrt(np.mean((train_predictions - train_y) ** 2)))
            test_predictions = learner.query(test_x)
            test_rmse.append(np.sqrt(np.mean((test_predictions - test_y) ** 2)))
        min_test_rmse_leaf_size = leaf_sizes[np.argmin(test_rmse)]
        return train_rmse,test_rmse,min_test_rmse_leaf_size

if __name__ == "__main__":
    #PYTHONPATH =../:.python testlearner.py Data / Istanbul.csv
    script_directory = Path(__file__).resolve().parent
    alldata = np.genfromtxt(script_directory/'Data/Istanbul.csv', delimiter=',')
    if all(np.isnan(alldata[0])):
        alldata=alldata[1:]
    if all(np.isnan(alldata[:,0])):
            alldata=alldata[:, 1:]
    leaf_sizes = range(0,50)
    #Experiment1
    train_rmse,test_rmse,min_test_rmse_leaf_size=test_learner(alldata, leaf_sizes)
    plt.figure()
    plt.plot(leaf_sizes, train_rmse, label='Training RMSE')
    plt.plot(leaf_sizes, test_rmse, label='Testing RMSE')
    plt.axvline(x=min_test_rmse_leaf_size, color='r', linestyle='--',
                label=f'Min Test RMSE Leaf Size ({min_test_rmse_leaf_size})')
    plt.xlabel('leaf_size')
    plt.ylabel('RMSE')
    plt.title('RMSE vs. leaf_size for DTLearner')
    plt.legend()
    plt.savefig(script_directory / 'images/E1')
    ##Experiment2
    train_rmse, test_rmse, min_test_rmse_leaf_size = test_learner(alldata, leaf_sizes, bagging=True)
    plt.figure()
    plt.plot(leaf_sizes, train_rmse, label='Training RMSE')
    plt.plot(leaf_sizes, test_rmse, label='Testing RMSE')
    plt.axvline(x=min_test_rmse_leaf_size, color='r', linestyle='--',
                label=f'Min Test RMSE Leaf Size ({min_test_rmse_leaf_size})')
    plt.xlabel('leaf_size')
    plt.ylabel('RMSE')
    plt.title('RMSE vs. leaf_size for DTLearner with bagging')
    plt.legend()
    plt.savefig(script_directory / 'images/E2')
    #Experiment 3
    #Measure time and ME for training DTLearner and RTLearner
    def time_me(data,decisiontree=False,randomtree=False):
        train_x, train_y, test_x, test_y = data_prep(data)
        training_time=[]
        me=[]
        for leaf_size in leaf_sizes:
            start_time = time.time()
            if decisiontree==True:
                learner = dt.DTLearner(leaf_size=leaf_size)
                learner.add_evidence(train_x, train_y)
                prediction=learner.query(test_x)
                training_time.append(time.time() - start_time)
                me.append(np.max(np.abs(test_y - prediction)))
            if randomtree==True:
                learner = rt.RTLearner(leaf_size=leaf_size)
                learner.add_evidence(train_x, train_y)
                prediction = learner.query(test_x)
                training_time.append(time.time() - start_time)
                me.append(np.max(np.abs(test_y - prediction)))
        return training_time,me
    training_time_dt,me_dt=time_me(alldata,decisiontree=True)
    training_time_rt, me_rt = time_me(alldata, randomtree=True)
    plt.figure()
    plt.plot(leaf_sizes, training_time_dt, label='DT training time')
    plt.plot(leaf_sizes, training_time_rt, label='RT Training time')
    plt.xlabel('leaf_size')
    plt.ylabel('Training time in secs')
    plt.title('DT vs RT in terms of Training Time')
    plt.legend()
    plt.savefig(script_directory / 'images/E3-1')

    plt.figure()
    plt.plot(leaf_sizes, me_dt, label='DT maximum error')
    plt.plot(leaf_sizes, me_rt, label='RT maximum error')
    plt.xlabel('leaf_size')
    plt.ylabel('Maximum error')
    plt.title('DT vs RT in terms of Maximum error')
    plt.legend()
    plt.savefig(script_directory / 'images/E3-2')