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


class TreeCodeGenerator(BaseGenerator):
    def __init__(self, clf):
        self.clf = clf

    def generate_statements(self):
        tree = self.clf.tree_

        def recurse(node, depth):
            indent = "  " * depth
            if tree.feature[node] >= 0:
                name = tree.feature[node]
                threshold = tree.threshold[node]
                # TODO: two version on method - for int and floats
                # return indent + "if (x[%d] <= " % name + "%d" % threshold + ") {\n" + \
                #        recurse(tree.children_left[node], depth + 1) + \
                #        indent + "}\n" + indent + "else {\n" + \
                #        recurse(tree.children_right[node], depth + 1) + \
                #        indent + "}\n"
                return indent + "if (x[%d] <= " % name + "%.10f" % threshold + ") {\n" + \
                       recurse(tree.children_left[node], depth + 1) + \
                       indent + "}\n" + indent + "else {\n" + \
                       recurse(tree.children_right[node], depth + 1) + \
                       indent + "}\n"
            else:
                return indent + 'return %s;\n' % str(self.clf.classes_[np.argmax(tree.value[node])])

        return recurse(0, 1)

    def generate(self, fname = 'tree_model.c', cname="classifier", **kwargs):
        with open(fname, 'w') as c_file:
            c_file.write(self.license_header())
            c_file.write("int %s(double * x){\n%s};\n" % (cname, self.generate_statements()))
