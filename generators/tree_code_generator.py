import numpy as np

from generators.base_generator import BaseGenerator


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
                #TODO: two version on method - for int and floats
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

    def generate(self):
        with open('../examples/models/tree_model.c', 'w') as c_file:
            c_file.write("int classify(double * x){\n%s};\n" % self.generate_statements())
