import LinRegLearner as lrl
import BagLearner as bl
import numpy as np
class InsaneLearner(object):
    def __init__(self,verbose=False):
        self.insane_learner=None
        self.verbose=verbose
    def author(self):
        return "yyang3052"
    def add_evidence(self,data_x,data_y):
        self.insane_learner=[bl.BagLearner(learner=lrl.LinRegLearner,kwargs = {}, bags = 20,verbose=False,boost=False) for i in range(20)]
        for learner in self.insane_learner:
            learner.add_evidence(data_x,data_y)
    def query(self,points):
        aggregated_predictions = np.zeros((points.shape[0], 20))
        for i, learner in enumerate(self.insane_learner):
            aggregated_predictions[:, i] = learner.query(points)
        return np.mean(aggregated_predictions, axis=1)

