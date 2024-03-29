import numpy as np
import random as rd


class RTLearner(object):
    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose

    def author(self):
        return 'tsu35'  # replace tb34 with your Georgia Tech username

    def built_tree(self, dataX, dataY):
        leaf = -1000
        # if the data points in a branch has equal or less than the leaf size
        # average the Y's  of data points in a leaf
        if dataX.shape[0] <= self.leaf_size:
            self.tree = np.asarray([[leaf, np.mean(dataY), np.nan, np.nan]])
            return self.tree

        # if all the Y values are the same, then just return Y
        elif len(set(dataY)) == 1:
            self.tree = np.asarray([[leaf, np.mean(dataY), np.nan,
                                     np.nan]])
            return self.tree

        else:
            # randomly order the features in a list
            # select the first feature in the list to split on
            randomList = rd.sample(xrange(0, dataX.shape[1]), dataX.shape[1])
            i = randomList[0]
            z = 1
            # check if the feature has any information,
            # if all data points in that feature is the same pick another feature
            while len(set(dataX[:, i])) == 1 and z <= dataX.shape[1]:
                i = randomList[z]
                z = z + 1
            if len(set(dataX[:,
                       i])) == 1:  # if selected feature has all the same values then make it a leaf and return the mean of the data points
                return [[leaf, np.mean(dataY), np.nan, np.nan]]
            else:
                SplitVal = np.mean(np.random.choice(dataX[:, i], size=2,
                                                    replace=False))  # if selected feature has information, find two data points to split on
                while SplitVal == np.amax(dataX[:,
                                          i]):  # if split value is greater than all data points you need to select another split value to prevent the right branch from eing blank
                    SplitVal = np.mean(np.random.choice(dataX[:, i], size=2,
                                                        replace=False))
                a = dataX[:, i] <= SplitVal  # data on the left
                dataxl = dataX[a]
                datayl = dataY[a]
                leftTree = self.built_tree(dataxl,
                                      datayl)  # recursively build the left tree
                dataxr = dataX[~a]  # data on the right
                datayr = dataY[~a]
                rightTree = self.built_tree(dataxr,
                                       datayr)  # recursively build the right tree
                root = [i, SplitVal, 1, len(leftTree) + 1]
                self.tree = np.vstack((root, leftTree, rightTree))

                return self.tree

    def addEvidence(self, dataX, dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        return self.built_tree(dataX, dataY)

    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        i = 0
        sh = points.shape[0]
        result = np.empty([sh])  # create an empty array
        while i < sh:
            arrayIndex = 0
            while ~np.isnan(self.tree[
                                arrayIndex, 3]):  # checks if the row in "decision tree" array is a leaf
                val = self.tree[arrayIndex, 1]  # finds the split value
                if points[i, int(self.tree[
                                     arrayIndex, 0])] <= val:  # compares the split value of the feature with the value of the same feature in test set
                    arrayIndex = arrayIndex + 1  # goes to the right ree
                else:
                    arrayIndex = arrayIndex + int(
                        self.tree[arrayIndex, 3])  # goes to the left tree
            value = self.tree[arrayIndex, 1]
            result[i] = value
            i = i + 1
        return result


if __name__ == "__main__":
    print "the secret clue is 'zzyzx'"
