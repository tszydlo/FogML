from src.fogml.generators.base_generator import BaseGenerator
import os


class IsolationForestAnomalyDetectorGenerator(BaseGenerator):
    skeleton_path = 'skeletons/isolation_forest_skeleton.txt'

    def __init__(self, anomaly_detector):
        self.anomaly_detector = anomaly_detector

    @staticmethod
    def generate_trees_nodes(trees, max_depth):
        code = "{\n"
        for i, tree in enumerate(trees):
            code += "    // Tree {}\n".format(i)
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
                        i, node_id
                    )
                    stack.append((tree.tree_.children_right[node_id], depth + 1))
                    stack.append((tree.tree_.children_left[node_id], depth + 1))
                j += 1
        code += "};"
        return code

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
        with open(os.path.join(os.path.dirname(__file__), self.skeleton_path)) as skeleton:
            code = skeleton.read()
            code = self.license_header() + code
            code = code.replace('<n_estimators>', str(n_estimators))
            code = code.replace('<n_features>', str(n_features))
            code = code.replace('<max_depth>', str(max_depth))
            code = code.replace('<total_nodes>', str(total_nodes))
            code = code.replace('<trees_nodes>', self.generate_trees_nodes(trees, max_depth))
            formatted_indexes = str(trees_indexes).replace("[", "{").replace("]", "}")
            code = code.replace('<trees>', formatted_indexes)

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