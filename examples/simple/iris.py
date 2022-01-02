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

import pickle
import sys

from sklearn import datasets, tree, naive_bayes
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier

sys.path.append("../../src/fogml/")

from generators import GeneratorFactory

factory = GeneratorFactory()

iris = datasets.load_iris()
X = iris.data
y = iris.target

# clf = tree.DecisionTreeClassifier(random_state=3456)
# clf = naive_bayes.GaussianNB()
# clf = MLPClassifier(
#     hidden_layer_sizes=(4,), random_state=34, solver="adam", max_iter=1500
# )
# clf = RandomForestClassifier(n_estimators=10)
clf = KNeighborsClassifier(
    n_neighbors=5, weights="uniform", algorithm="auto", metric="minkowski", p=2
)

generator = factory.get_generator(clf)

clf.fit(X, y)

print("accuracy: ", clf.score(X, y))

dumped = pickle.dumps(clf)
print("SIZE: " + str(len(dumped)))

generator.generate()
