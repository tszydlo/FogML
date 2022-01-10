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

import os
from .base_generator import BaseGenerator


class QLearningCodeGenerator(BaseGenerator):
    skeleton_path = 'skeletons/qlearning_model_skeleton.txt'

    def __init__(self, clf):
        self.clf = clf

    @staticmethod
    def generate_c_array(array):
        states, actions = array.shape
        result = "{"
        for state in range(states):
            for action in range(actions):
                result += "%.6f, " % array[state][action]
            result += "\n"
        result += "}"
        return result

    def generate_q_table(self):
        return self.generate_c_array(self.clf.Q)

    def generate(self, fname='qlearning_model_test.c', **kwargs):
        with open(os.path.join(os.path.dirname(__file__), self.skeleton_path)) as skeleton:
            code = skeleton.read()
            code = self.license_header() + code
            code = code.replace('<q_table>', self.generate_q_table())

            code = code.replace('<states>', str(self.clf.states))
            code = code.replace('<actions>', str(self.clf.actions))

            with open(fname, 'w') as output_file:
                output_file.write(code)
