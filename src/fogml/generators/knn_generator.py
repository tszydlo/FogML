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
        X = self.clf._fit_X
        X = X.astype(str)
        result = "float X[][] = [[" + "],[".join([",".join(row) for row in X]) + "]]\n"

        y = self.clf._y
        y = y.astype(str)
        result += "float y[] = [" + ",".join(y) + "]"

        X_str = "[[" + "],[".join([",".join(row) for row in X]) + "]]"
        y_str = "[" + ",".join(y) + "]"
        classes_str = self.clf.classes_.astype(str)
        classes_str = "[" + ",".join(classes_str) + "]"
        # print(result)
        # with open(fname, 'w') as c_file:
        #     c_file.write(result)
        samples_num = self.clf.n_samples_fit_
        features_num = self.clf.n_features_in_
        print("hi")
        with open(os.path.join(os.path.dirname(__file__), self.skeleton_path)) as skeleton:
            code = skeleton.read()
            code = self.license_header() + code
            code = code.replace('<n_samples>', str(samples_num))
            code = code.replace('<features>', str(features_num))
            code = code.replace('<n_neighbors>', str(self.clf.n_neighbors))
            code = code.replace('<cname>', cname)
            code = code.replace('<X_train>', X_str)
            code = code.replace('<Y_train>', y_str)
            code = code.replace('<n_classes>', str(len(self.clf.classes_)))
            code = code.replace('<classes>', classes_str)





            with open(fname, 'w') as output_file:
                output_file.write(code)
    
    
