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

from sklearn import tree, naive_bayes
from sklearn.neural_network import MLPClassifier
from sklearn.tree import export_graphviz
import pandas as pd
import numpy as np

from fogml.generators import GeneratorFactory

for data_chunk in pd.read_csv('./mldata/dataset.arff', sep=',', chunksize=10 ** 6):
    clf = tree.DecisionTreeClassifier()
    # clf = naive_bayes.GaussianNB()
    # clf = MLPClassifier(hidden_layer_sizes=(15,), random_state=34)

    clf.fit(data_chunk.iloc[:, 0:5], data_chunk.iloc[:, 5:6])

    factory = GeneratorFactory()

    generator = factory.get_generator(clf)
    generator.generate(fname="models\classifier_moa.c")

    # print(clf.predict(np.array([0.3, 0.3, 0.4, 0.5, 0.6]).reshape(1, -1)))
    print(clf.predict(np.array([5.7, 0.9, 0.4, 0.5, 0.6]).reshape(1, -1)))

    export_graphviz(clf, out_file="tree.dot", max_depth=3,
                    filled=True, rotate=True, rounded=True
                    )
