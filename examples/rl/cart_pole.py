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
import math

import gym
import numpy as np

from fogml.generators import GeneratorFactory
from fogml.rl.qlearning import QLearning, QStatesIntervals

env = gym.make('CartPole-v1')

#After optimization
#stateSpace = [
#    [-1.6, 1.6, 1],
#    [-0.17, 0.17, 1],
#    [-0.28, 0.28, 4],
#    [-0.58, 0.58, 4],
#]

stateSpace = [
    [-1.6, 1.6, 1],
    [-0.17, 0.17, 1],
    [-0.42, 0.42, 6],
    [-0.87, 0.87, 6],
]

print(stateSpace)
qStates = QStatesIntervals(stateSpace)

print("Number of states = {}".format(qStates.getStates()))

#create QLearning agent
qAgent = QLearning(qStates.getStates(), env.action_space.n, learning_rate=0.2, discount=1.0, zeros=True)

EXPLOITATION_EPISODE = 800
EPISODES = 1200
STEPS = 500

mean_reward = 0

obs_track=[]

for episode in range(EPISODES):
    if episode < EXPLOITATION_EPISODE:
        epsilon = max(0.1, min(1., 1. - math.log10((episode + 1) / 25)))
    else:
        epsilon = 0
    qAgent.setEpsilon(epsilon)
    qAgent.setLearningRate(epsilon)

    if episode % 100 == 0:
        print("Episode {}".format(episode))
        print("     Mean reward {}".format(mean_reward/100))
        print("     Epsilon {}".format(epsilon))
        mean_reward = 0
    observation = env.reset()

    qAgent.updateState(qStates.getState(observation))

    for step in range(STEPS):
        if episode % 100 == 0:
            env.render()

        if episode < EXPLOITATION_EPISODE:
            action = qAgent.selectActionWithExploration()
        else:
            action = qAgent.selectAction()

        observation, reward, done, info = env.step(action)

        obs_track.append(observation)

        new_state = qStates.getState(observation)

        mean_reward = mean_reward + reward

        if episode < EXPLOITATION_EPISODE:
            #reward
            qAgent.update(action, new_state, reward)
        else:
            qAgent.updateState(new_state)

        if done:
            break

env.close()

print("Statistics to optimize the state discretizer function:")
obs_track = np.array(obs_track)
percentiles = np.percentile(obs_track, [2.5,97.5], axis=0)
print("    min        :" + str(obs_track.min(axis=0)))
print("    low 95% CI :" + str(percentiles[0]))
print("    mean       :" + str(obs_track.mean(axis=0)))
print("    high 95% CI:" + str(percentiles[1]))
print("    max        :" + str(obs_track.max(axis=0)))

factory = GeneratorFactory()

generatorQAgent = factory.get_generator(qAgent)
generatorQStates = factory.get_generator(qStates)

generatorQAgent.generate(fname='FogML_RL_Arduino\qlearning_model_test.c')
generatorQStates.generate(fname = 'FogML_RL_Arduino\qstates_discretizer_test.c')

