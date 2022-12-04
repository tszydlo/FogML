from .base_generator import BaseGenerator
from sklearn.neighbors import KNeighborsClassifier


class KNClassifierGenerator(BaseGenerator):
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

        print(result)
        # with open(fname, 'w') as c_file:
        #     c_file.write(result)
    
    
