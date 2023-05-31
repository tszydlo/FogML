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

    
    def treeToArray(self, tree, parent_id = 0, node_id=0, arr=[0]*208):
        threshold = tree.threshold[node_id]
        feature = tree.feature[node_id]
        left_child = tree.children_left[node_id]
        right_child = tree.children_right[node_id]
        value = tree.value[node_id][0]

        if node_id == 0:
            arr[node_id] = {'id': node_id, 'threshold': threshold, 'feature': feature, 'value': value}
        elif(node_id%2 == 1):
            arr[2*parent_id + 1] = {'id': node_id, 'threshold': threshold, 'feature': feature, 'value': value}
        else:
            arr[2*parent_id + 2] = {'id': node_id, 'threshold': threshold, 'feature': feature, 'value': value}

    
        if left_child != sklearn.tree._tree.TREE_LEAF:
            self.treeToArr(tree, node_id, left_child, arr)
        else: 
            arr[2*node_id + 1] = ({'id': left_child})
        
        if right_child != sklearn.tree._tree.TREE_LEAF:
            self.treeToArr(tree, node_id, right_child, arr)
        else: 
            arr[2*node_id + 2] = ({'id': left_child})

        return arr


    def forestToArray(self):
        forest = []
        estimators = self.clf.estimators_
        for i in range(len(estimators)):
            tree = self.treeToArray(estimators[i].tree_)
            forest.append(tree)

        return forest