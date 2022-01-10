import numpy as np


class QLearning():
    def __init__(self, states, actions, learning_rate=0.1, discount=0.8, epsilon=0.2, zeros=True):
        self.states = states
        self.actions = actions
        self.learning_rate = learning_rate
        self.discount = discount
        self.epsilon = epsilon

        if zeros:
            self.Q = np.zeros((states, actions))
        else:
            self.Q = np.random.rand(states, actions)

    def setEpsilon(self, epsilon):
        self.epsilon = epsilon

    def selectActionWithExploration(self):
        if np.random.random() > self.epsilon:
            action = np.argmax(self.Q[self.state])
        else:
            action = np.random.randint(0, self.actions)
        return action

    def selectAction(self):
        action = np.argmax(self.Q[self.state])
        return action

    def updateState(self, state):
        self.state = state

    def update(self, action, newState, reward):
        self.Q[self.state][action] = self.Q[self.state][action] + self.learning_rate * (
                reward +
                self.discount * np.max(self.Q[newState]) - self.Q[self.state][action]
        )
        self.state = newState

    def updateQ(self, state, action, reward):
        self.Q[state][action] = reward

    def getQ(self):
        return self.Q


class QStatesCustom():
    def __init__(self, stateSpace):
        self.stateSpace = stateSpace

        self.states = 1
        self.nums = []

        for feature in stateSpace:
            self.nums.append(len(feature) + 1)
            self.states = self.states * (len(feature) + 1)

    def getStates(self):
        return self.states

    def getState(self, features):
        features_states = []

        for index in range(len(features)):
            for index_val in range(len(self.stateSpace[index])):
                found = False
                if features[index] <= self.stateSpace[index][index_val]:
                    features_states.append(index_val)
                    found = True
                    break
            if not found:
                features_states.append(len(self.stateSpace[index]))

        result = 0
        mul = 1
        for index in range(len(features_states)):
            result = result + mul * features_states[index]

            mul = mul * self.nums[index]

        return result


class QStatesIntervals():
    def __init__(self, stateSpace):
        self.stateSpace = stateSpace

        self.states = 1
        self.nums = []

        for feature in stateSpace:
            self.nums.append(feature[2])
            self.states = self.states * (feature[2] + 2)

    def getStates(self):
        return self.states

    def getState(self, observation):
        observation_states = []

        for index in range(len(observation)):
            window = (self.stateSpace[index][1] - self.stateSpace[index][0]) / self.stateSpace[index][2]  # (max-min) / num
            state = int((observation[index] - self.stateSpace[index][0]) / window) + 1

            if state < 0:
                state = 0
            if state > self.stateSpace[index][2] + 1:
                state = self.stateSpace[index][2] + 1

            observation_states.append(state)

        result = 0
        mul = 1
        for index in range(len(observation_states)):
            result = result + mul * observation_states[index]

            mul = mul * (self.nums[index] + 2)

        return result
