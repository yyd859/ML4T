""""""
"""  		  	   		  		 		  		  		    	 		 		   		 		  
A simple wrapper for linear regression.  (c) 2015 Tucker Balch  		  	   		  		 		  		  		    	 		 		   		 		  

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

import numpy as np
import pandas as pd
import LinRegLearner as lrl

class BagLearner(object):
    """
    This is a Bagstrap Learner.
    """

    def __init__(self,learner,kwargs=None,bags=10, boost=False, verbose=False):
        self.learner=learner
        self.kwargs=kwargs
        self.bags=bags
        self.boost=boost
        self.verbose=verbose
        self.learners=[]


    def author(self):
        """
        :return: The GT username of the student
        :rtype: str
        """
        return "yyang3052"  # replace tb34 with your Georgia Tech username

    def remove_header(self, array):
        # Check if the first row seems like a header (all strings)
        first_row = array[0]
        if all(np.isnan(array[0])):
            return array[1:]
        else:
            # If the first row is all ints, there's no header to remove
            return array

    def remove_date(self, array):
        # Check if the first row seems like a header (all strings)
        first_column = array[:, 0]
        if all(np.isnan(array[:, 0])):
            return array[:, 1:]
        else:
            # If the first col is all ints, there's no date to remove
            return array
    def add_evidence(self, data_x, data_y):
        data_y = data_y.tolist()
        array_1 = np.column_stack([data_x, data_y])
        array_2 = self.remove_header(array_1)
        array = self.remove_date(array_2)
        data_x=array[:,:-1]
        data_y=array[:,-1]
        for i in range(self.bags):
            # Create a new instance of the base learner with optional arguments
            learner = self.learner(**self.kwargs)
            # Generate a random sample with replacement
            indices = np.random.choice(data_x.shape[0], size=round(data_x.shape[0] * 0.6), replace=True)
            x_bag, y_bag = data_x[indices], data_y[indices]
            # Train data
            learner.add_evidence(x_bag,y_bag)
            # Add the trained learner to the list
            self.learners.append(learner)

    def query(self, points):
        """
        Estimate a set of test points given the model we built.

        :param points: A numpy array with each row corresponding to a specific query.
        :type points: numpy.ndarray
        :return: The predicted result of the input data according to the trained model
        :rtype: numpy.ndarray
        """
        predictions = np.zeros((points.shape[0], len(self.learners)))
        for i, learner in enumerate(self.learners):
            predictions[:, i] = learner.query(points)
        aggregated_predictions = np.mean(predictions, axis=1)
        return aggregated_predictions

if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")
