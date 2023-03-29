import numpy as np
from sklearn.base import ClassifierMixin
from sklearn.cluster import KMeans
from sklearn.metrics import euclidean_distances


class KMeansAnomalyDetector(ClassifierMixin):
    def __init__(self, n_clusters=3, z_score=99.7):
        self.n_clusters = n_clusters
        self.z_score = z_score

    def fit(self, X):
        # print("Clusters: ")
        # print(self.n_clusters)
        # print("---")

        kmeans = KMeans(n_clusters=self.n_clusters, random_state=0).fit(X)
        self.clusters = kmeans.cluster_centers_
        data_pred = kmeans.predict(X)

        self.z_scores = []

        for k in range(self.n_clusters):
            #print("Cluster: ")
            #print(k)

            elem_cluster = X[np.where(data_pred == k)]

            cluster_dist = euclidean_distances(elem_cluster, [self.clusters[k]])

            # print("Center: ")
            # print(kmeans.cluster_centers_[k])

            z_score = np.percentile(cluster_dist, [self.z_score], axis=0)[0][0]

            # print("Z-Score: ")
            # print(z_score)

            self.z_scores.append(z_score)

    def predict_proba(self, X):
        cluster_dist = euclidean_distances(X, self.clusters)

        results = []

        for row in cluster_dist:
            k = np.argmin(row)
            v = np.min(row)

            results.append(v - self.z_scores[k])

        return np.matrix(results)

    def predict(self, X):
        proba = self.predict_proba(X)

        proba[proba <= 0] = 0
        proba[proba > 0] = 1

        return proba

class IsolationForest():
    