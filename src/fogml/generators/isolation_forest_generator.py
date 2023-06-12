from src.fogml.generators.base_generator import BaseGenerator


class IsolationForestAnomalyDetectorGenerator(BaseGenerator):
    skeleton_path = 'skeletons/isolation_forest_skeleton.txt'

    def __init__(self, anomaly_detector):
        self.anomaly_detector = anomaly_detector

    # TODO: check if generation code is generating correct C code
    # TODO: probably needs refactor
    def generate(self, fname='isolation_forest_test.c'):
        n_estimators = self.anomaly_detector.clf.n_estimators
        n_features = self.anomaly_detector.clf.n_features_in_
        n_samples = self.anomaly_detector.clf._n_samples
        trees = self.anomaly_detector.clf.estimators_
        max_depth = max(estimator.tree_.max_depth for estimator in trees)

        total_nodes = 0
        trees_indexes = [0]
        for tree in trees:
            tree = tree.tree_
            node_count = tree.node_count
            total_nodes += node_count
            trees_indexes.append(total_nodes)

        # Build C code
        code = "#include <math.h>\n"
        code += "#include <stdio.h>\n"
        code += "#include <stdbool.h>\n"
        code += "#include \"{}.h\"\n\n".format(fname[:-2])
        code += "const int n_estimators = {};\n".format(n_estimators)
        code += "const int n_features = {};\n".format(n_features)
        code += "const int max_depth = {};\n\n".format(max_depth)

        code += "typedef struct {\n"
        code += "    int feature_index;\n"
        code += "    float threshold;\n"
        code += "    int left_child;\n"
        code += "    int right_child;\n"
        code += "    float leaf_value;\n"
        code += "} decision_node;\n\n"

        code += f"const decision_node trees_nodes[{total_nodes}] = {{\n"
        for i, tree in enumerate(trees):
            code += "    // Tree {}\n".format(i)
            # code += "    {\n"
            stack = [(0, 0)]
            j = 0
            print(len(tree.tree_.feature))
            while len(stack) > 0:
                node_id, depth = stack.pop()
                if depth > max_depth or tree.tree_.children_left[node_id] == tree.tree_.children_right[node_id]:
                    code += "    {{-1, 0.0, -1, -1, {} }}, // Tree {} node {} \n".format(tree.tree_.value[node_id][0][0],i,node_id)
                else:
                    code += "    {{ {}, {}, {}, {}, 0.0 }}, // Tree {} node {} \n".format(
                        tree.tree_.feature[node_id],
                        tree.tree_.threshold[node_id],
                        tree.tree_.children_left[node_id],
                        tree.tree_.children_right[node_id],
                        i,node_id
                    )
                    stack.append((tree.tree_.children_right[node_id], depth + 1))
                    stack.append((tree.tree_.children_left[node_id], depth + 1))
                j += 1
            # code += "    },\n"
        code += "};\n\n"

        formatted_indexes = str(trees_indexes).replace("[", "{").replace("]", "}")
        code += f"const int trees[n_estimators] = {formatted_indexes};\n\n"

        code += "float predict(float x[{}]) {{\n".format(n_features)
        code += "    float y = 0.0;\n"
        code += "    for (int i = 0; i < n_estimators; i++) {\n"
        code += "        int node = 0;\n"
        code += "        int depth = 0;\n"
        code += "        while (true) {\n"
        code += "            if (depth >= max_depth) {\n"
        code += "                break;\n"
        code += "            }\n"
        code += "            decision_node decision = trees_nodes[i + node];\n"
        code += "            if (decision.feature_index == -1) {\n"
        code += "                y += depth;\n"
        code += "                break;\n"
        code += "            }\n"
        code += "            float value = x[decision.feature_index];\n"
        code += "            if (value <= decision.threshold) {\n"
        code += "                node = decision.left_child;\n"
        code += "            } else {\n"
        code += "                node = decision.right_child;\n"
        code += "            }\n"
        code += "            depth += 1;\n"
        code += "        }\n"
        code += "    }\n"
        code += "    float n = 80.0;\n"
        code += "    float avg_depth = y / n_estimators;\n"
        code += "    float c = 2.0 * (log((float) n_features) + 0.5772156649) - 2.0 * (float) n_features / (float) n;\n"
        code += "    float AS = pow(2, -avg_depth / c);\n"
        code += "    return AS;\n"
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