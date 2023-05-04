from sklearn.ensemble import IsolationForest


class IsolationForestAnomalyDetector:
    def __init__(self, n_estimators=100, max_samples='auto', random_state=42):
        self.clf = IsolationForest(n_estimators=n_estimators, max_samples=max_samples,
                                   random_state=random_state)

    def fit(self, x):
        self.clf.fit(x)

    def predict(self, x):
        # TODO: change to decision_function and add threshold
        return self.clf.predict(x)
