import numpy as np
import RTLearner as rt
import LinRegLearner as lr


class BagLearner(object):
    def __init__(self, learner, kwargs, bags, boost,
                 verbose):
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.boost = boost
        assert (not self.boost), "Boosting method is not implemented."
        self.verbose = verbose
        self.learners = []

    def author(self):
        return 'tsu35'  # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):  # train the dataset

        if not self.boost:
            for iiiii in range(0, self.bags):
                learner = self.learner(**self.kwargs)
                ind = np.random.randint(0,
                                        high=dataX.shape[0],
                                        size=dataX.shape[0]
                                        )
                X = dataX[ind]
                Y = dataY[ind]
                learner.addEvidence(X, Y)
                self.learners.append(learner)
        else:
            print "Boosting method is not implemented."

        if self.verbose:
            print "number of learners in bag: ", len(self.learners)
        return self.learners

    def query(self, points):

        Result_ls = [iiiii.query(points) for iiiii in self.learners]
        # average the Y's of all bags.
        Result = np.mean(Result_ls, axis=0)

        if self.verbose:
            print Result[:5]
        return Result
