from sklearn.ensemble import IsolationForest
import sklearn


class IsolationForestAnomalyDetector:
    def __init__(self, n_estimators=1, max_samples='auto', random_state=42):
        self.clf = IsolationForest(n_estimators=n_estimators, max_samples=max_samples,
                                   random_state=random_state)

    def fit(self, x):
        self.clf.fit(x)
        tree_text = export_text(self.clf.estimators_[0])
        print(tree_text)  

    def predict(self, x):
        return self.clf.predict(x)

    
    def treeToArray(self,tree, node_id=0, arr=[]):
        threshold = tree.threshold[node_id]
        feature = tree.feature[node_id]
        left_child = tree.children_left[node_id]
        right_child = tree.children_right[node_id]
        value = tree.value[node_id][0]
        
        arr.append({'id': node_id, 'threshold': threshold, 'feature': feature, 'value': value})
        
        if left_child != sklearn.tree._tree.TREE_LEAF:
            self.treeToArray(tree, left_child, arr)
        else:
            arr.append({'id': left_child})
        
        if right_child != sklearn.tree._tree.TREE_LEAF:
            self.treeToArray(tree, right_child, arr)
        else:
            arr.append({'id': right_child})
        
        return arr

    def forestToArray(self):
        forest = []
        estimators = self.clf.estimators_
        for i in range(len(estimators)):
            tree = self.treeToArray(estimators[i].tree_)
            forest.append(tree)

        return forest