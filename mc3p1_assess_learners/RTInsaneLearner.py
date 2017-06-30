import numpy as np
from LinRegLearner import LinRegLearner
from BagLearner import BagLearner

class RTInsaneLearner(object):
    def __init__(self, verbose=False):
        self.verbose = verbose # not really used to shorten the code.
        self.learners = []

    def addEvidence(self, dataX, dataY):
        for iiiii in range(20):
            learner = BagLearner(learner=LinRegLearner, kwargs=dict(verbose=True), bags=20, boost=False, verbose=self.verbose)
            learner.addEvidence(dataX, dataY)
            self.learners.append(learner)
        return self.learners

    def query(self, points):
        return np.mean([iiiii.query(points) for iiiii in self.learners], axis=0)
