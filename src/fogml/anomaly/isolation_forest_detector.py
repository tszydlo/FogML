from sklearn.ensemble import IsolationForest


class IsolationForestAnomalyDetector:
    def __init__(self, n_estimators=100, max_samples='auto', random_state=42):
        self.n_estimators = n_estimators
        self.max_samples = max_samples
        self.random_state = random_state
        self.n_features_in_ = None
        self.estimators_ = None
        self.clf = None

    def fit(self, x):
        self.clf = IsolationForest(n_estimators=self.n_estimators, max_samples=self.max_samples,
                                   random_state=self.random_state)
        self.clf.fit(x)
        self.n_features_in_ = self.clf.n_features_in_
        self.estimators_ = self.clf.estimators_

    def predict(self, x):
        return self.clf.predict(x)
