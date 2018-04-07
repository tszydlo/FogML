import math

import numpy as np
import os

from generators.base_generator import BaseGenerator


class BayesCodeGenerator(BaseGenerator):

    skeleton_path = 'skeletons/bayes_skeleton.txt'

    def __init__(self, clf):
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

    def generate_sigma_code(self):
        return self.generate_c_matrix(self.clf.sigma_)

    def generate_theta_code(self):
        return self.generate_c_matrix(self.clf.theta_)

    def generate_log_sigma_code(self):
        return self.generate_c_matrix(self.calculate_log_sigma())

    def generate_log_priors_code(self):
        return self.generate_c_array(self.calculate_log_priors())

    def calculate_log_sigma(self):
        log_sigma = np.copy(self.clf.sigma_)
        for i in range(log_sigma.shape[0]):
            for j in range(log_sigma.shape[1]):
                log_sigma[i][j] = math.log(2 * math.pi * self.clf.sigma_[i][j])
        return log_sigma

    def calculate_log_priors(self):
        log_priors = []
        for prior in self.clf.class_prior_:
            log_priors.append(math.log(prior))
        return log_priors

    def generate(self):
        classes_num = len(self.clf.classes_)
        features_num = self.clf.sigma_.shape[1]

        with open(os.path.join(os.path.dirname(__file__), self.skeleton_path)) as skeleton:
            code = skeleton.read()
            code = code.replace('<classes>', str(classes_num))
            code = code.replace('<features>', str(features_num))
            code = code.replace('<sigma>', self.generate_sigma_code())
            code = code.replace('<theta>', self.generate_theta_code())
            code = code.replace('<log_sigma>', self.generate_log_sigma_code())
            code = code.replace('<prior>', self.generate_log_priors_code())
            with open('./models/bayes_model.c', 'w') as output_file:
                output_file.write(code)
