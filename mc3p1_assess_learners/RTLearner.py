import numpy as np


class RTLearner(object):
    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = None

    def author(self):
        return 'tsu35'

    def select_split_value(self, dataX, i):
        while True:
            split_value = np.mean(
                np.random.choice(dataX[:, i], size=2, replace=False))
            if split_value != np.amax(dataX[:, i]) \
                    and split_value != np.amin(dataX[:, i]):
                break
        return split_value

    def built_tree(self, dataX, dataY):

        ###############
        # Initialization
        ###############
        # randomly order the features in a list
        random_feature_list = np.random.choice(dataX.shape[1],
                                               dataX.shape[1],
                                               replace=False)
        leaf = -999

        ###############
        # Corner cases
        ###############

        # if all Ys are the same, return Y
        if np.unique(dataY).shape[0] == 1:
            self.tree = np.array([[leaf, np.mean(dataY), np.nan, np.nan]])
            return self.tree

        # if the data points a branch has <= the defined leaf size
        # average the Ys in a leaf
        elif dataX.shape[0] <= self.leaf_size:
            self.tree = np.array([[leaf, np.mean(dataY), np.nan, np.nan]])
            return self.tree

        else:

            ###############
            # find a feature to split on until all features are used up.
            ###############
            for feature in random_feature_list:
                if np.unique(dataX[:, feature]).shape[0] != 1:
                    break

            ###############
            # split
            ###############
            if np.unique(dataX[:, feature]).shape[0] == 1:
                # if have no feature to split on
                # make it a leaf and return the mean of the data points
                return [[leaf, np.mean(dataY), np.nan, np.nan]]

            else:
                # find split value: average of two random points
                split_value = self.select_split_value(dataX, feature)

                # index for data on the left split
                left_index = dataX[:, feature] <= split_value

                # recursively build the left tree
                dataX_left = dataX[left_index]
                dataY_left = dataY[left_index]
                left_tree = self.built_tree(dataX_left, dataY_left)

                # recursively build the right tree
                dataX_right = dataX[~left_index]
                dataY_right = dataY[~left_index]
                right_tree = self.built_tree(dataX_right, dataY_right)

                # add the split into the table
                root = [feature, split_value, 1, len(left_tree) + 1]
                self.tree = np.vstack((root, left_tree, right_tree))

                return self.tree

    def addEvidence(self, dataX, dataY):

        return self.built_tree(dataX, dataY)

    def query(self, points):

        pred_len = points.shape[0]
        pred = np.empty([pred_len])

        for point_ind in range(pred_len):
            tree_index = 0
            # checks if the row is a leaf
            while ~np.isnan(self.tree[tree_index, 3]):
                # get the split value
                split_value = self.tree[tree_index, 1]

                # compares to the split value
                if points[
                    point_ind, int(self.tree[tree_index, 0])] > split_value:
                    # goes to the left
                    tree_index += int(self.tree[tree_index, 3])

                else:
                    # goes to the right
                    tree_index += 1

            pred[point_ind] = self.tree[tree_index, 1]

        return pred


if __name__ == "__main__":
    print "the secret clue is 'zzyzx'"
