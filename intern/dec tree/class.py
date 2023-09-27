from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import json


@dataclass
class Node:
    """Decision tree node."""
    feature: int = 0
    threshold: float = 0
    n_samples: int = 0
    value: int = 0
    mse: float = 0
    left: Node = None
    right: Node = None


@dataclass
class DecisionTreeRegressor:
    """Decision tree regressor."""
    max_depth: int
    min_samples_split: int = 2

    def fit(self, X: np.ndarray, y: np.ndarray) -> DecisionTreeRegressor:
        """Build a decision tree regressor from the training set (X, y)."""
        self.n_features_ = X.shape[1]
        self.tree_ = self._split_node(X, y, depth=0)
        return self

    def _mse(self, y: np.ndarray) -> float:
        """Compute the mse criterion for a given set of target values."""
        y_pred = np.mean(y)
        mse = np.sum((y - y_pred) ** 2) / len(y)
        return mse

    def _weighted_mse(self, y_left: np.ndarray, y_right: np.ndarray) -> float:
        """Compute the weighted mse criterion for two given sets of target values."""
        if len(y_left) + len(y_right) == 0:
            mse_weighted = 0
        else:
            mse_weighted = (self._mse(y_left) * len(y_left) +
                            self._mse(y_right) * len(y_right)) / (len(y_left) + len(y_right))
        return mse_weighted

    def _split(self, X: np.ndarray, y: np.ndarray, feature: int, threshold: float) -> float:
        """Calculate the mse for splitting on a feature and threshold."""
        y_left = y[X[:, feature] <= threshold]
        y_right = y[X[:, feature] > threshold]
        mse_split = self._weighted_mse(y_left, y_right)
        return mse_split

    def _best_split(self, X: np.ndarray, y: np.ndarray) -> tuple[int, float]:
        """Find the best split for a node."""
        best_feature = None
        best_threshold = None
        best_mse = float('inf')

        for feature in range(self.n_features_):
            unique_values = np.unique(X[:, feature])
            for threshold in unique_values:
                mse_split = self._split(X, y, feature, threshold)
                if mse_split < best_mse:
                    best_feature = feature
                    best_threshold = threshold
                    best_mse = mse_split

        return best_feature, best_threshold

    def _split_node(self, X: np.ndarray, y: np.ndarray, depth: int = 0) -> Node:
        """Recursively split a node and build the tree."""
        n_samples, n_features = X.shape

        # Create a leaf node if the stopping criteria are met
        if depth >= self.max_depth or n_samples < self.min_samples_split:
            node = Node(n_samples=n_samples,
                        value=round(np.mean(y)), mse=self._mse(y))
            return node

        # Find the best split for this node
        best_feature, best_threshold = self._best_split(X, y)

        # If no valid split is found, create a leaf node
        if best_feature is None:
            node = Node(n_samples=n_samples,
                        value=round(np.mean(y)), mse=self._mse(y))
            return node

        # Split the data based on the best feature and threshold
        left_mask = X[:, best_feature] <= best_threshold
        right_mask = ~left_mask

        X_left, y_left = X[left_mask], y[left_mask]
        X_right, y_right = X[right_mask], y[right_mask]

        # Recursively build the left and right subtrees
        left_subtree = self._split_node(X_left, y_left, depth + 1)
        right_subtree = self._split_node(X_right, y_right, depth + 1)

        # Create the current node with the splitting information
        node = Node(
            feature=best_feature,
            threshold=best_threshold,
            n_samples=n_samples,
            value=round(np.mean(y)),
            mse=self._mse(y),
            left=left_subtree,
            right=right_subtree
        )

        return node
    
    def as_json(self, decimals: int = 2) -> str:
        """Return the decision tree as a JSON-like string."""
        if self.tree_ is None:
            return "{}"
        return self._as_json(self.tree_, decimals=decimals)

    def _as_json(self, node: Node, decimals: int = 2) -> str:
        """Return the decision tree as a JSON-like string. Execute recursively."""
        if node is None:
            return "{}"

        if node.left is None and node.right is None:
            # If it's a leaf, create a JSON-like string for the leaf
            return f'{{"value": {int(node.value)}, "n_samples": {node.n_samples}, "mse": {round(float(node.mse), decimals)}}}'

        # Convert NumPy integers to Python integers
        feature = int(node.feature)
        threshold = int(node.threshold)
        n_samples = int(node.n_samples)

        # Create a JSON-like string for the current node and recursively for left and right subtrees
        return f'{{"feature": {feature}, "threshold": {round(threshold, decimals)}, "n_samples": {n_samples}, "mse": {round(float(node.mse), decimals)}, ' \
               f'"left": {self._as_json(node.left, decimals=decimals)}, "right": {self._as_json(node.right, decimals=decimals)}}}'

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict regression target for X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        y : array of shape (n_samples,)
            The predicted values.
        """
        if self.tree_ is None:
            raise ValueError("The model has not been fitted yet.")

        n_samples, n_features = X.shape
        predictions = np.empty(n_samples, dtype=float)

        for i in range(n_samples):
            predictions[i] = self._predict_one_sample(X[i])

        return predictions

    def _predict_one_sample(self, features: np.ndarray) -> float:
        """Predict the target value of a single sample."""
        node = self.tree_
        while node.left is not None and node.right is not None:
            if features[node.feature] <= node.threshold:
                node = node.left
            else:
                node = node.right
        return node.value


