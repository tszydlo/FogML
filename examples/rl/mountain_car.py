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

import gym

from fogml.generators import GeneratorFactory
from fogml.rl.qlearning import QLearning, QStatesCustom, QStatesIntervals

env = gym.make('MountainCar-v0')

#create QStates discretizer table using QStatesCustom()
#stateSpace = [
#    [x / 100 for x in range(-120, 60+1, 10)],
#    [x / 1000 for x in range(-70, 70+1, 10)]
#]
#print(stateSpace)
#qStates = QStatesCustom(stateSpace)

#create QStates discretizer table using QStatesIntervals()
stateSpace = [
    [-1.2, 0.6, 20],
    [-0.07, 0.07, 20]
]
print(stateSpace)
qStates = QStatesIntervals(stateSpace)

print("Number of states = {}".format(qStates.getStates()))

#create QLearning agent
qAgent = QLearning(qStates.getStates(), env.action_space.n)

mean_reward = 0
succesful = 0

EPSILON = 0.6
EPISODES = 6000
EXPLOITATION_EPISODE = 5500

epsilon = EPSILON

# env is created, now we can use it:
for episode in range(EPISODES):
    if epsilon > 0:
        epsilon = EPSILON - (episode / EXPLOITATION_EPISODE) * EPSILON
        qAgent.setEpsilon(epsilon)

    if episode % 100 == 0:
        print("Episode {}".format(episode))
        print("     Mean reward {}".format(mean_reward/100))
        print("     Succesfull {}".format(succesful))
        print("     Epsilon {}".format(epsilon))
        mean_reward = 0
        succesful = 0

    observation = env.reset()

    qAgent.updateState(qStates.getState(observation))

    for step in range(300):
        if episode % 100 == 0:
            env.render()

        if episode < EXPLOITATION_EPISODE:
            action = qAgent.selectActionWithExploration()
        else:
            action = qAgent.selectAction()

        observation, reward, done, info = env.step(action)

        new_state = qStates.getState(observation)

        if episode < EXPLOITATION_EPISODE:
            qAgent.update(action, new_state, reward)
        else:
            qAgent.updateState(new_state)

        mean_reward = mean_reward + reward

        if done:
            if (observation[0] >= 0.5):
                qAgent.updateQ(previous_state, action, 0)
                succesful = succesful + 1
            break

        previous_state = new_state

env.close()

print(qAgent.getQ())

factory = GeneratorFactory()

generatorQAgent = factory.get_generator(qAgent)
generatorQStates = factory.get_generator(qStates)

generatorQAgent.generate(fname='FogML_RL_Arduino\qlearning_model_test.c')
generatorQStates.generate(fname = 'FogML_RL_Arduino\qstates_discretizer_test.c')
