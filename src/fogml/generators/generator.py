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

import sklearn.ensemble

from sklearn import *
from sklearn.neural_network import *

import fogml.rl
from .bayes_code_generator import BayesCodeGenerator
from .mlp_code_generator import MlpCodeGenerator
from .qlearning_code_generator import QLearningCodeGenerator
from .qstatesintervals_code_generator import QStatesIntervalsCodeGenerator
from .random_forest_generator import RandomForestCodeGenerator
from .tree_code_generator import TreeCodeGenerator


class GeneratorFactory:

    recognized_classifiers = {
        sklearn.tree.DecisionTreeClassifier: TreeCodeGenerator,
        sklearn.naive_bayes.GaussianNB: BayesCodeGenerator,
        sklearn.neural_network.MLPClassifier: MlpCodeGenerator,
        sklearn.ensemble.RandomForestClassifier: RandomForestCodeGenerator,
        fogml.rl.QLearning: QLearningCodeGenerator,
        fogml.rl.QStatesIntervals: QStatesIntervalsCodeGenerator
    }

    def get_generator(self, clf):
        if clf.__class__ in self.recognized_classifiers.keys():
            return self.recognized_classifiers[clf.__class__](clf)
        else:
            print("Sorry, but this is not recognized type of classifier")
            return None
