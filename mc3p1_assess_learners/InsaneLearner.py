import numpy as np
from LinRegLearner import LinRegLearner
from BagLearner import BagLearner

class InsaneLearner(object):
    def __init__(self, verbose=False, learner=LinRegLearner):
        self.verbose = verbose; self.learner = learner; self.learners = []
    def author(self):
        return 'tsu35'
    def addEvidence(self, dataX, dataY):
        for iiiii in range(20):
            learner = BagLearner(learner=self.learner, kwargs=dict(verbose=True), bags=20, boost=False, verbose=self.verbose)
            learner.addEvidence(dataX, dataY)
            self.learners.append(learner)
        return self.learners
    def query(self, points):
        return np.mean([iiiii.query(points) for iiiii in self.learners], axis=0)
