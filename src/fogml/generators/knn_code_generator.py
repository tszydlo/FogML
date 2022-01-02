import math

import numpy as np
import os

from sklearn.neighbors import KNeighborsClassifier

from .base_generator import BaseGenerator


class KNNCodeGenerator(BaseGenerator):

    skeleton_path = "skeletons/knn_skeleton.txt"

    def __init__(self, clf: KNeighborsClassifier):
        self.clf = clf

    def generate(self, fname="knn_model.c", cname="classifier", **kwargs):
        print(self.clf.classes_)
        print(self.clf.get_params())
        print('neighbors')
        print(self.clf.kneighbors())
        # classes_num = len(self.clf.classes_)
        # features_num = self.clf.var_.shape[1]

        # with open(os.path.join(os.path.dirname(__file__), self.skeleton_path)) as skeleton:
        #     code = skeleton.read()
        #     code = self.license_header() + code
        #     code = code.replace('<classes>', str(classes_num))
        #     code = code.replace('<features>', str(features_num))
        #     code = code.replace('<sigma>', self.generate_sigma_code())
        #     code = code.replace('<theta>', self.generate_theta_code())
        #     code = code.replace('<log_sigma>', self.generate_log_sigma_code())
        #     code = code.replace('<prior>', self.generate_log_priors_code())

        #     code = code.replace('<cname>', cname)

        #     with open(fname, 'w') as output_file:
        #         output_file.write(code)
