import sklearn

from generators.bayes_code_generator import BayesCodeGenerator
from generators.mlp_code_generator import MlpCodeGenerator
from generators.tree_code_generator import TreeCodeGenerator


class GeneratorFactory:

    recognized_classifiers = {
        sklearn.tree.tree.DecisionTreeClassifier: TreeCodeGenerator,
        sklearn.naive_bayes.GaussianNB: BayesCodeGenerator,
        sklearn.neural_network.MLPClassifier: MlpCodeGenerator
    }

    def get_generator(self, clf):
        if clf.__class__ in self.recognized_classifiers.keys():
            return self.recognized_classifiers[clf.__class__](clf)
        else:
            print("Sorry, but this is not recognized type of classifier")
            return None
