import numpy as np
from sklearn.tree import DecisionTreeRegressor


class GradientBoostingRegressor:
    def __init__(
        self,
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        min_samples_split=2,
        loss="mse",
        verbose=False,
        subsample_size=0.5,
        replace=False

    ):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.verbose = verbose
        self.subsample_size = subsample_size
        self.replace = replace
        self.loss = loss
        if loss == 'mse':
            self.loss = self._mse
        self.trees_ = []

    def _mse(self, y_true, y_pred):

        loss = np.mean((y_pred - y_true)**2)
        grad = y_pred - y_true
        if self.verbose is True:
            print(loss)

        return loss, grad

    def _subsample(self, X, y):

        mask = np.random.choice(range(len(y)), int(len(y) * self.subsample_size),
                                replace=self.replace)
        sub_x = X[mask]
        sub_y = y[mask]

        return sub_x, sub_y

    def fit(self, X, y):
        """
        Fit the model to the data.

        Args:
            X: array-like of shape (n_samples, n_features)
            y: array-like of shape (n_samples,)

        Returns:
            GradientBoostingRegressor: The fitted model.
        """
        self.base_pred_ = np.mean(y)
        y_pred = np.full(len(y), self.base_pred_)
        grad = -1 * self.loss(y, y_pred)[1]

        for estim in range(self.n_estimators):
            model = DecisionTreeRegressor(max_depth=self.max_depth,
                                          min_samples_split=self.min_samples_split).fit(X, grad)
            self.trees_.append(model)

            X_sub, y_sub = self._subsample(X, y_pred)

            y_pred = y_pred + model.predict(X) * self.learning_rate

            grad = -1 * self.loss(y, y_pred)[1]

        return self

    def predict(self, X):
        """Predict the target of new data.

        Args:
            X: array-like of shape (n_samples, n_features)

        Returns:
            y: array-like of shape (n_samples,)
            The predict values.

        """
        predictions = np.zeros(X.shape[0])

        y = self.base_pred_ + predictions
        for model in self.trees_:
            y = y + model.predict(X) * self.learning_rate

        return y