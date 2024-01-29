import numpy as np
import pandas as pd
import DTLearner as dt
import RTLearner as rt
import BagLearner as bl
import resource
import LinRegLearner as lrl
import InsaneLearner as it
# def remove_header(array):
#     # Check if the first row seems like a header (all strings)
#     first_row = array[0]
#     if any(isinstance(item,int ) for item in first_row)==False:
#         # If any of the first row is a non-int, consider it as a header and remove it
#         return array[1:]
#     else:
#         # If the first row is all ints, there's no header to remove
#         return array
# def remove_date(array):
#     # Check if the first row seems like a header (all strings)
#     first_column = array[:,0]
#     if any(isinstance(item,int ) for item in first_column)==False:
#         # If any of the first column is a non-int, consider it as a date and remove it
#         return array[:,1:]
#     else:
#         # If the first col is all ints, there's no date to remove
#         return array
data = np.genfromtxt('/Users/yyd/Documents/ML4T_2023Fall/assess_learners/Data/Istanbul.csv', delimiter=',')
data_x=data[:,:-1]
data_y=data[:,-1]
print(data_y)

# # data_1_reshaped = np.tile(data_1, (data_1.shape[0], 1))
# # data_z=np.hstack((data_y,data_1_reshaped))
# # print(data_z)
# learner = rt.RTLearner(leaf_size = 1, verbose = False) # constructor
# array=learner.remove_date(learner.remove_header(data))
# # array=np.array([[2,2,3],[2,5,3],[1,8,5],[7,11,9]])
# # data_x=array[:,:-1]
# # data_y=array[:,-1].tolist()
# # array_1 = np.column_stack([data_x, data_y])
# # array_2 = learner.remove_header(array_1)
# # array = learner.remove_date(array_2)
# # learner.add_evidence(data_x,data_y)
# # data_y = data_y.tolist()
# # array_1 = np.column_stack([data_x, data_y])
# # array_2 = learner.remove_header(array_1)
# # array = learner.remove_date(array_2)
# Xtest=np.array([data[111,1:-1],data[2,1:-1]])
# # print(learner.query(Xtest))
# learner = bl.BagLearner(
#     learner=rt.RTLearner,
#     kwargs={"leaf_size": 1},
#     bags=1,
#     boost=False,
#     verbose=False,
# )
# # data_y = data_y.tolist()
# # array_1 = np.column_stack([data_x, data_y])
# # array_2 = self.remove_header(array_1)
# # array = self.remove_date(array_2)
# # data_x = array[:, :-1]
# # data_y = array[:, -1]
# # print(data_x)
# # data_y=learner.remove_header(data_y)
#
# learner.add_evidence(data_x, data_y)
# Y = learner.query(Xtest)
# def memory_usage():
#     return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
# print(memory_usage())
#
#
# print(learner.build_decision_tree(array))