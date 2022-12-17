import os

from .base_generator import BaseGenerator
from sklearn.neighbors import KNeighborsClassifier


class KNClassifierGenerator(BaseGenerator):

    skeleton_path = 'skeletons/knn_skeleton.txt'

    def __init__(self, clf: KNeighborsClassifier):
        if not isinstance(clf, KNeighborsClassifier):
            raise ValueError("Expected instance of KNeighborsClassifier")

        self.clf = clf

    def generate(self, fname = "k_neighbors.c", cname="classifier", **kwargs):

        samples_num = self.clf.n_samples_fit_
        features_num = self.clf.n_features_in_


        X = self.clf._fit_X
        X = X.astype(str)

        y = self.clf._y
        y = y.astype(str)

        X_str = "{{" + "},{".join([",".join(row) for row in X]) + "}}"
        y_str = "{" + ",".join(y) + "}"
        classes_str = self.clf.classes_.astype(str)
        classes_str = "{" + ",".join(classes_str) + "}"


        with open(os.path.join(os.path.dirname(__file__), self.skeleton_path)) as skeleton:
            code = skeleton.read()
            code = self.license_header() + code
            code = code.replace('<n_samples>', str(samples_num))
            code = code.replace('<features>', str(features_num))
            code = code.replace('<n_neighbors>', str(self.clf.n_neighbors))
            code = code.replace('<cname>', cname)
            code = code.replace('<train_data>', X_str)





            with open(fname, 'w') as output_file:
                output_file.write(code)
    
    
