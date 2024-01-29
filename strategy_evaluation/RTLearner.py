import numpy as np

class RTLearner(object):
    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size
        self.verbose = verbose
        self.tree = None

    def author(self):
        return "yyang3052"

    def add_evidence(self, data_x, data_y):
        data = np.column_stack([data_x, data_y])
        self.tree = self.build_tree(data)

    def build_tree(self, data):
        if data.shape[0] <= self.leaf_size:
            return np.array([[-1, self.majority_class(data[:, -1]), -1, -1]])

        if len(set(data[:, -1])) == 1:
            return np.array([[-1, data[0, -1], -1, -1]])

        split_col, split_val = self.random_split(data)
        left_data = data[data[:, split_col] <= split_val]
        right_data = data[data[:, split_col] > split_val]

        if left_data.size == 0 or right_data.size == 0:
            return np.array([[-1, self.majority_class(data[:, -1]), -1, -1]])

        left_tree = self.build_tree(left_data)
        right_tree = self.build_tree(right_data)
        root = np.array([[split_col, split_val, 1, left_tree.shape[0] + 1]])
        return np.vstack([root, left_tree, right_tree])

    def random_split(self, data):
        features = np.random.choice(data.shape[1] - 1, size=2, replace=False)
        feature = np.random.choice(features)
        values = np.unique(data[:, feature])
        value = np.random.choice(values)
        return feature, value

    def majority_class(self, y):
        values, counts = np.unique(y, return_counts=True)
        index = np.argmax(counts)
        return values[index]

    def query(self, points):
        predictions = np.apply_along_axis(self.predict, axis=1, arr=points)
        return predictions

    def predict(self, record):
        node = 0
        while self.tree[node, 0] != -1:
            feature, value = self.tree[node, 0], self.tree[node, 1]
            if record[int(feature)] <= value:
                node += int(self.tree[node, 2])
            else:
                node += int(self.tree[node, 3])
        return self.tree[node, 1]

if __name__ == "__main__":
    print("RTLearner for classification initialized.")
