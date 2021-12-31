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

def generate_c_matrix(matrix):
    result = "{\n"
    for i in range(matrix.shape[0]):
        result += "{"
        for j in range(matrix.shape[1]):
            result += "%.6f, " % matrix[i][j]
        result += "},\n"
    result += "}"
    return result


def generate_c_array(array):
    result = "{"
    for i in range(len(array)):
        result += "%.6f, " % array[i]
    result += "}"
    return result


def generate_c_function(function_body="", return_type="void", name="fun", args=""):
    return "%s %s(%s){\n %s\n }; \n " % (return_type, name, args, function_body)
