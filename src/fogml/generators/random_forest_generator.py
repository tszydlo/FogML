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

import numpy as np

from .base_generator import BaseGenerator


class RandomForestCodeGenerator(BaseGenerator):
    def __init__(self, clf):
        self.clf = clf

    def generate_statements(self, tree, index):

        def recurse(node, depth):
            indent = "  " * depth
            if tree.feature[node] >= 0:
                name = tree.feature[node]
                threshold = tree.threshold[node]
                return indent + "if (x[%d] <= " % name + "%.10f" % threshold + ") {\n" + \
                       recurse(tree.children_left[node], depth + 1) + \
                       indent + "}\n" + indent + "else {\n" + \
                       recurse(tree.children_right[node], depth + 1) + \
                       indent + "}\n"
            else:
                return indent + 'results[%s] = %s;\n' % (index, str(self.clf.classes_[np.argmax(tree.value[node])]))

        return recurse(0, 1)

    def generate(self, fname = 'random_forest_model.c', cname="classifier", **kwargs):
        result = self.license_header()
        result += "int %s(float * x){\n" % cname
        result += "  int results[%s];\n" % len(self.clf.estimators_)
        index = 0
        for estimator in self.clf.estimators_:
            result += self.generate_statements(estimator.tree_, index)
            index += 1
        result += "  int classes_amount = 0;\n"
        result += "  for(int i=0; i<%s; i++){\n" % len(self.clf.estimators_)
        result += "  	if(results[i]+1 > classes_amount) classes_amount = results[i]+1;"
        result += "  }\n"
        result += "  int result_class = -1;\n"
        result += "  int max_apperance = 0;\n"
        result += "  for(int i=0; i<classes_amount; i++){\n"
        result += "   int apperance = 0;\n"
        result += "  	for(int j=0; j<%s; j++) if(results[j] == i) apperance++;\n" % len(self.clf.estimators_)
        result += "  	if(apperance > max_apperance){\n"
        result += "  		max_apperance = apperance;\n"
        result += "  		result_class = i;\n"
        result += "  	}\n"
        result += "  }\n"
        result += "  return result_class;\n"
        result += "}\n"
        with open(fname, 'w') as c_file:
            c_file.write(result)