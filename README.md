# FogML

Due to the development of IoT solutions, we can observe the constantly growing number of these devices in almost every aspect of our lives. The machine learning may improve increase their intelligence and smartness. Unfortunately, the highly regarded programming libraries consume to much resources to be ported to the embedded processors.

The structure of the project is as follows:
* the `src` folder contains the source code generators for machine learning models i.e.: naive bayes, decision trees/forrest and neural nets;
* the `example` folder contains the simple examples and the MNIST digit recognition for Arduino board and the simple TFT touchscreen.

Examples of anomaly detection and classification algorithms provided by the FogML project for embedded devices:
* FogML-SDK [https://github.com/tszydlo/fogml_sdk]
* FogML Arduino [https://github.com/tszydlo/FogML-Arduino]

## Usage

`pip install fogml`


## Example

```
from sklearn import datasets, tree

from fogml.generators import GeneratorFactory

iris = datasets.load_iris()
X = iris.data
y = iris.target

clf = tree.DecisionTreeClassifier(random_state=3456)
clf.fit(X, y)
print( 'accuracy: ',clf.score(X,y))

factory = GeneratorFactory()
generator = factory.get_generator(clf)
generator.generate()
```

## Reinforcement Learning

```
import gym

from fogml.generators import GeneratorFactory
from fogml.rl.qlearning import QLearning, QStatesIntervals

env = gym.make('MountainCar-v0')

#create QStates discretizer table using QStatesIntervals()
stateSpace = [
    [-1.2, 0.6, 20],
    [-0.07, 0.07, 20]
]
qStates = QStatesIntervals(stateSpace)

#create QLearning agent
qAgent = QLearning(qStates.getStates(), env.action_space.n)

for episode in range(EPISODES):
    #TODO Train the model
    #see examples

factory = GeneratorFactory()

generatorQAgent = factory.get_generator(qAgent)
generatorQStates = factory.get_generator(qStates)

generatorQAgent.generate(fname='FogML_RL_Arduino\qlearning_model_test.c')
generatorQStates.generate(fname = 'FogML_RL_Arduino\qstates_discretizer_test.c')

```

See it in action:
https://www.youtube.com/watch?v=yEr5tjBrY70

## FogML research

If you think that the project is interesting to you, please cite the paper:
_Tomasz Szydlo, Joanna Sendorek, Robert Brzoza-Woch, Enabling machine learning on resource constrained devices by source code generation of the learned models, ICCS 2018_

_The research was supported by the National Centre for Research and Development (NCBiR) under Grant No. LIDER/15/0144 /L-7/15/NCBR/2016._
