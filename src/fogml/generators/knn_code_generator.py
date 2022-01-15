import numpy as np
import os

from sklearn.neighbors import KNeighborsClassifier

from .base_generator import BaseGenerator


class KNNCodeGenerator(BaseGenerator):
    skeleton_path = "skeletons/knn_skeleton.txt"

    def __init__(self, clf: KNeighborsClassifier):
        self.clf = clf

    @staticmethod
    def generate_c_matrix(matrix):
        result = "{\n"
        for i in range(matrix.shape[0]):
            result += "{"
            for j in range(matrix.shape[1]):
                result += "%.6f, " % matrix[i][j]
            result += "},\n"
        result += "}"
        return result

    @staticmethod
    def generate_c_array(array):
        result = "{"
        for i in range(len(array)):
            result += "%.6f, " % array[i]
        result += "}"
        return result

    def generate_zero_array(self, size):
        zero_array = np.zeros(size)
        return self.generate_c_array(zero_array)

    def metric_calculation(self, metric):
        if metric == "euclidean":
            return "res += pow2(x[j] - attributes[i][j])"
        elif metric == "manhattan":
            return "res += abs2(x[j] - attributes[i][j])"
        elif metric == "chebyshev":
            return "res = max2(res, abs2(x[j] - attributes[i][j]))"
        pass

    def generate(self, fname="knn_model.c", cname="classifier", **kwargs):

        classes = len(self.clf.classes_)
        features = self.clf.n_features_in_
        k = self.clf.n_neighbors
        fit_X = np.array(self.clf._fit_X)
        Y = np.array(self.clf._y)

        with open(os.path.join(os.path.dirname(__file__), self.skeleton_path)) as skeleton:
            code = skeleton.read()
            code = self.license_header() + code
            code = code.replace('<class_count>', str(classes))
            code = code.replace('<features>', str(features))
            code = code.replace('<k_neighbours>', str(k))
            code = code.replace('<members>', str(len(self.clf._fit_X)))
            code = code.replace('<dataset_features>', self.generate_c_matrix(fit_X))
            code = code.replace('<member_class>', self.generate_c_array(Y))
            code = code.replace('<class_count_empty>', self.generate_zero_array(classes))
            code = code.replace('<cname>', cname)
            code = code.replace('<metric>', self.metric_calculation(self.clf.metric))

            with open(fname, 'w') as output_file:
                output_file.write(code)
