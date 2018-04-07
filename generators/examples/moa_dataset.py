import pandas
from sklearn import tree, naive_bayes
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.tree import export_graphviz

from generators.generator import GeneratorFactory

for data_chunk in pandas.read_csv('./mldata/dataset.arff', sep=',', chunksize=10 ** 6):
    clf = tree.DecisionTreeClassifier()
    # clf = naive_bayes.GaussianNB()
    # clf = MLPClassifier(hidden_layer_sizes=(15,), random_state=34)

    clf.fit(data_chunk.iloc[:, 0:5], data_chunk.iloc[:, 5:6])

    factory = GeneratorFactory()

    generator = factory.get_generator(clf)
    generator.generate()

    # print(clf.predict(np.array([0.3, 0.3, 0.4, 0.5, 0.6]).reshape(1, -1)))
    print(clf.predict(np.array([5.7, 0.9, 0.4, 0.5, 0.6]).reshape(1, -1)))

    export_graphviz(clf, out_file="tree.dot", max_depth=3,
                    filled=True, rotate=True, rounded=True
                    )

