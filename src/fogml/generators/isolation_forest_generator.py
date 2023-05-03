from src.fogml.generators.base_generator import BaseGenerator


class IsolationForestAnomalyDetectorGenerator(BaseGenerator):
    skeleton_path = 'skeletons/isolation_forest_skeleton.txt'

    def __init__(self, clf):
        self.clf = clf

    def generate(self, fname='isolation_forest_test.c'):
        n_estimators = self.clf.n_estimators
        max_features = self.clf.max_samples
        n_outputs = self.clf.n_features_in_
        trees = self.clf.estimators_

        # Write header file
        header_file = fname[:-2] + ".h"
        with open(header_file, "w") as f:
            f.write("#ifndef EXTREMELY_RANDOMIZED_TREES_H\n")
            f.write("#define EXTREMELY_RANDOMIZED_TREES_H\n\n")
            f.write("#ifdef __cplusplus\n")
            f.write("extern \"C\" {\n")
            f.write("#endif\n\n")
            f.write("void predict(float x[{}], float y[{}]);\n\n".format(max_features, n_outputs))
            f.write("#ifdef __cplusplus\n")
            f.write("}\n")
            f.write("#endif\n\n")
            f.write("#endif /* EXTREMELY_RANDOMIZED_TREES_H */\n")

        # Write C file
        with open(fname, "w") as f:
            f.write("#include <math.h>\n")
            f.write("#include \"{}\"\n\n".format(header_file))
            f.write("const int n_estimators = {};\n".format(n_estimators))
            f.write("const int max_features = {};\n".format(max_features))
            f.write("const int n_outputs = {};\n\n".format(n_outputs))

            # Write predict function
            f.write("void predict(float x[{}], float y[{}]) {{\n".format(max_features, n_outputs))
            for i in range(n_outputs):
                f.write("    y[{}] = 0.0;\n".format(i))
            for i, tree in enumerate(trees):
                f.write("    // Tree {}\n".format(i))
                f.write("    int node = 0;\n")
                f.write("    while (true) {\n")
                f.write("        if (node >= {} || node < 0) {{\n".format(tree.tree_.node_count))
                f.write("            break;\n")
                f.write("        }\n")
                f.write("        int feature = tree.tree_.feature[node];\n")
                f.write("        if (feature < 0) {{\n")
                for j in range(n_outputs):
                    f.write("            y[{}] += tree.tree_.value[node][{}];\n".format(j, i))
                f.write("            break;\n")
                f.write("        }\n")
                f.write("        float threshold = tree.tree_.threshold[node];\n")
                f.write("        if (x[feature] <= threshold) {\n")
                f.write("            node = tree.tree_.children_left[node];\n")
                f.write("        } else {\n")
                f.write("            node = tree.tree_.children_right[node];\n")
                f.write("        }\n")
            f.write("}\n")
