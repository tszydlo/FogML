"""
   Copyright 2021 FogML

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import os
from .base_generator import BaseGenerator


class KMeansAnomalyDetectorGenerator(BaseGenerator):
    skeleton_path = 'skeletons/kmeans_anomaly_skeleton.txt'

    def __init__(self, clf):
        self.clf = clf

    @staticmethod
    def generate_c_array(array):
        size = len(array)
        result = "{"
        for pos in range(size):
            result += "%.6f" % array[pos]
            if (pos < size - 1):
                result += ", "
        result += "}"
        return result

    @staticmethod
    def generate_clusters_array(array):
        size = len(array)
        result = "{"
        for pos in range(size):
            cluster = array[pos]
            for elem in range(len(cluster)):
                result += "%.6f" % cluster[elem]
                if not (pos == size - 1 and elem == len(cluster) - 1):
                    result += ", "
            if (pos < size - 1):
                result += "\n                         "
        result += "}"
        return result

    def generate(self, fname='kmeans_anomaly_test.c', **kwargs):
        with open(os.path.join(os.path.dirname(__file__), self.skeleton_path)) as skeleton:
            code = skeleton.read()
            code = self.license_header() + code
            code = code.replace('<centroids_tab>', self.generate_clusters_array(self.clf.clusters))
            code = code.replace('<zscores_tab>', self.generate_c_array(self.clf.z_scores))
            code = code.replace('<vector_size>', str(len(self.clf.clusters[0])))
            code = code.replace('<clusters>', str(len(self.clf.clusters)))

            with open(fname, 'w') as output_file:
                output_file.write(code)
