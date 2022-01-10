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
import serial.tools.list_ports
from serial import Serial

def fformat(float):
    return str("{:.2f}".format(float))

env = gym.make('CartPole-v1')

print("Available serial ports:")
for i in serial.tools.list_ports.comports():
    print(i)

ser = Serial('COM11', baudrate=115200)  # open serial port
print("Selected port:")
print(ser.name)         # check which port was really used

while True:
    observation = env.reset()

    for step in range(500):
        env.render()
        # send observation to the device
        obs_str = ';'.join(map(fformat, observation))
        # For debug purposes
        #print("-> " + obs_str)
        obs_str = obs_str + "\n"
        ser.write(obs_str.encode())  # write a string

        #read action from the device
        line = ser.readline()  # read a '\n' terminated line
        action = int(line)
        # For debug purposes
        #print("<- " + str(line))

        observation, reward, done, info = env.step(action)

        if done:
            print("    Steps: {}".format(step))
            break

env.close()

ser.close()             # close port