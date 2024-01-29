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



class DTLearner(object):
    """
    This is a Decision Regression Tree Learner.

    :param verbose: If “verbose” is True, your code can print out information for debugging.
        If verbose = False your code should not generate ANY output. When we test your code, verbose will be False.
    :type verbose: bool
    """

    def __init__(self, leaf_size=1, verbose=False):
        """
                Constructor method
                """
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = None


    def author(self):
        """
        :return: The GT username of the student
        :rtype: str
        """
        return "yyang3052"  # replace tb34 with your Georgia Tech username

    def remove_header(self,array):
        # Check if the first row seems like a header (all strings)
        first_row = array[0]
        if all(np.isnan(array[0])):
            return array[1:]
        else:
            # If the first row is all ints, there's no header to remove
            return array

    def remove_date(self,array):
        # Check if the first row seems like a header (all strings)
        first_column = array[:, 0]
        if all(np.isnan(array[:,0])):
            return array[:, 1:]
        else:
            # If the first col is all ints, there's no date to remove
            return array
    # Calculate mean squared error
    def calculate_mean_squared_error(self,labels):
        mean = np.mean(labels)
        mse = np.mean((labels - mean) ** 2)
        return mse

    # Split the dataset based on a feature and value
    def split_dataset(self,array, column, value):
        left = array[array[:,column] <= value]
        right = array[array[:,column] > value]
        return left, right

    # Determine the best split for a dataset using mean squared error
    def determine_best_split(self,array):
        x=array[:,:-1]
        y=array[:,-1]
        best_mse = float('inf')
        best_split_column = None
        best_split_value = None
        for column in range(0,x.shape[1]):
            unique_values = np.unique(x[:,column])
            for value in unique_values:
                left, right = self.split_dataset(array, column, value)
                mse = (left.shape[0] / x.shape[0]) * self.calculate_mean_squared_error(left[:,-1]) \
                      + (right.shape[0] / x.shape[0]) * self.calculate_mean_squared_error(right[:,-1])

                if mse < best_mse:
                    best_mse = mse
                    best_split_column = column
                    best_split_value = value

        return best_split_column, best_split_value

    def build_decision_tree(self,array):
        leaf_size=self.leaf_size
        if array.shape[0] <= leaf_size:
            mean_target = np.mean(array[:,-1])
            return np.array([mean_target])

        best_split_column, best_split_value = self.determine_best_split(array)
        if best_split_column is None:
            mean_target = np.mean(array[:, -1])
            return np.array([mean_target])

        left, right = self.split_dataset(array, best_split_column, best_split_value)

        # Recur for left and right subtrees
        left_subtree = self.build_decision_tree(left)
        right_subtree = self.build_decision_tree(right)

        return np.array([best_split_column, best_split_value, left_subtree, right_subtree])
    def add_evidence(self, data_x, data_y):
        """
        Add training data to learner

        :param data_x: A set of feature values used to train the learner
        :type data_x: numpy.ndarray
        :param data_y: The value we are attempting to predict given the X data
        :type data_y: numpy.ndarray
        """
        data_y = data_y.tolist()
        array_1 = np.column_stack([data_x, data_y])
        array_2=self.remove_header(array_1)
        array=self.remove_date(array_2)
        self.tree = self.build_decision_tree(array)

    def predict(self, tree, sample):
        # If we've reached a leaf node, return the predicted value
        if tree.size == 1:
            return tree[0]
        # Traverse left or right based on the sample's feature value
        if sample[int(tree[0])] <= tree[1]:
            return self.predict(tree[2], sample)
        else:
            return self.predict(tree[3], sample)

    def query(self, points):
        """
        Estimate a set of test points given the model we built.

        :param points: A numpy array with each row corresponding to a specific query.
        :type points: numpy.ndarray
        :return: The predicted result of the input data according to the trained model
        :rtype: numpy.ndarray
        """
        list=[]
        for i in range(0,points.shape[0]):
            list.append(self.predict(tree=self.tree,sample=points[i]))
            query=np.array(list)
        return query

if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")
