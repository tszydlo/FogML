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


class QStatesIntervalsCodeGenerator(BaseGenerator):
    skeleton_path = 'skeletons/qstates_discretizer_skeleton.txt'

    def __init__(self, clf):
        self.clf = clf

    @staticmethod
    def generate_c_array(array):
        size = len(array)
        result = "{"
        for pos in range(size):
            for elem in range(3):
                result += "%.6f, " % array[pos][elem]
            result += "\n"
        result += "}"
        return result

    def generate_q_states_table(self):
        return self.generate_c_array(self.clf.stateSpace)

    def generate(self, fname = 'qstates_discretizer_test.c', **kwargs):
        with open(os.path.join(os.path.dirname(__file__), self.skeleton_path)) as skeleton:
            code = skeleton.read()
            code = self.license_header() + code
            code = code.replace('<q_states>', self.generate_q_states_table())

            code = code.replace('<rl_observation_size>', str(len(self.clf.stateSpace)))

            with open(fname, 'w') as output_file:
                output_file.write(code)
