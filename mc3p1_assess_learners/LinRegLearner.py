"""
A simple wrapper for linear regression.  (c) 2015 Tucker Balch
"""

import numpy as np

class LinRegLearner(object):

    def __init__(self, verbose = False):
        self.verbose = verbose

    def author(self):
        return 'tsu35' # replace tb34 with your Georgia Tech username

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """

        # slap on 1s column so linear regression finds a constant term
        newdataX = np.ones([dataX.shape[0],dataX.shape[1]+1])
        newdataX[:,0:dataX.shape[1]]=dataX

        # build and save the model
        self.model_coefs, residuals, rank, s = np.linalg.lstsq(newdataX, dataY)
        
    def query(self,points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        result = (self.model_coefs[:-1] * points).sum(axis = 1) + self.model_coefs[-1]
        return result

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"
