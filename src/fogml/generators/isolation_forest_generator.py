from src.fogml.generators.base_generator import BaseGenerator


class IsolationForestAnomalyDetectorGenerator(BaseGenerator):
    skeleton_path = 'skeletons/isolation_forest_skeleton.txt'

    def __init__(self, anomaly_detector):
        self.anomaly_detector = anomaly_detector

    # TODO: y is probability, change it with thresold?
    def generate(self, fname='isolation_forest_test.c'):
        n_estimators = self.anomaly_detector.clf.n_estimators
        n_features = self.anomaly_detector.clf.n_features_in_
        trees = self.anomaly_detector.clf.estimators_

        # Build C code
        code = "#include <math.h>\n"
        code += "#include \"{}.h\"\n\n".format(fname[:-2])
        code += "const int n_estimators = {};\n".format(n_estimators)
        code += "const int n_features = {};\n\n".format(n_features)

        code += "float predict(float x[{}]) {{\n".format(n_features)
        code += "    float y = 0.0;\n"
        for i, tree in enumerate(trees):
            code += "    // Tree {}\n".format(i)
            code += "    int node = 0;\n"
            code += "    while (true) {\n"
            code += "        if (node >= {} || node < 0) {{\n".format(tree.tree_.node_count)
            code += "            break;\n"
            code += "        }\n"
            code += "        int feature = tree.tree_.feature[node];\n"
            code += "        if (feature < 0) {{\n"
            code += "            y += tree.tree_.value[node][0];\n"
            code += "            break;\n"
            code += "        }\n"
            code += "        float threshold = tree.tree_.threshold[node];\n"
            code += "        if (x[feature] <= threshold) {\n"
            code += "            node = tree.tree_.children_left[node];\n"
            code += "        } else {\n"
            code += "            node = tree.tree_.children_right[node];\n"
            code += "        }\n"
        code += "    return y;\n"
        code += "}\n"

        # Write C code to file
        with open(fname, "w") as f:
            f.write(code)

        # Write header file
        header_file = fname[:-2] + ".h"
        with open(header_file, "w") as f:
            f.write("#ifndef ISOLATION_FOREST_H\n")
            f.write("#define ISOLATION_FOREST_H\n\n")
            f.write("#ifdef __cplusplus\n")
            f.write("extern \"C\" {\n")
            f.write("#endif\n\n")
            f.write("float predict(float x[{}]);\n\n".format(n_features))
            f.write("#ifdef __cplusplus\n")
            f.write("}\n")
            f.write("#endif\n\n")
            f.write("#endif /* ISOLATION_FOREST_H */\n")
