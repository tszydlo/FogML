import pickle

from sklearn import datasets, tree, naive_bayes
from sklearn.neural_network import MLPClassifier

from generators.generator import GeneratorFactory

factory = GeneratorFactory()

iris = datasets.load_iris()
X = iris.data
y = iris.target

# clf = tree.DecisionTreeClassifier(random_state=3456)
clf = naive_bayes.GaussianNB()
# clf = MLPClassifier(hidden_layer_sizes=(8,), random_state=34)

generator = factory.get_generator(clf)

clf.fit(X, y)

dumped = pickle.dumps(clf)
print("SIZE: " + str(len(dumped)))

generator.generate()