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

from .arduino_generator import ArduinoGenerator
from .base_generator import BaseGenerator
from .utils import generate_c_matrix, generate_c_array, generate_c_function


class MlpCodeGenerator(BaseGenerator):
    def __init__(self, clf):
        self.clf = clf

    @staticmethod
    def generate_list_of_matrixes(matrixes_list):
        result = "{"
        for i in range(len(matrixes_list)):
            result += generate_c_matrix(matrixes_list[i]) + ", "
        result += "}"
        return result

    @staticmethod
    def generate_list_of_arrays(arrays_list):
        result = "{"
        for i in range(len(arrays_list)):
            result += generate_c_array(arrays_list[i]) + ", "
        result += "}"
        return result

    @staticmethod
    def generate_vector_mul_matrix(matrix, vector_name="x", result_name="r"):
        instruction = ""
        for j in range(matrix.shape[1]):
            instruction += "%s[%d] = " % (result_name, j)
            for p in range(matrix.shape[0]):
                if abs(matrix[p][j] - 0.0) > 1e-5:
                    instruction += " + (%f) * %s[%d]" % (matrix[p][j], vector_name, p)
                if p == matrix.shape[0] - 1:
                    instruction += ";\n"
        return instruction

    @staticmethod
    def generate_vector_add_vector(vector1, vector2_name="x", result_name="r"):
        instruction = ""
        for i in range(vector1.shape[0]):
            instruction += "%s[%d] = %s[%d] + (%f);\n" % (result_name, i, vector2_name, i, vector1[i])
        return instruction

    @staticmethod
    def generate_vector_declaration(name="v", size=10, vector_type="int"):
        return "%s %s[%d];\n" % (vector_type, name, size)

    @staticmethod
    def generate_relu_activation_on_vector(size=10, vector_name="v"):
        return "for (int i=0; i < %d; i++){ if (%s[i] < 0) { %s[i] = 0;}}\n" % (size, vector_name, vector_name)

    @staticmethod
    def generate_softmax_activation_on_vector(size=10, vector_name="v"):
        return "double max_el = %s[0];" \
               "for (int i=1; i < %d; i++){max_el = max(max_el, %s[i]);}" \
               "double exp_sum = 0.0; \n" \
               "for (int i=0; i<%d; i++){ exp_sum += exp(%s[i]-max_el); } \n" \
               "for (int i=0; i<%d; i++){ %s[i] = exp(%s[i]-max_el) / exp_sum; }\n" \
               % (vector_name, size, vector_name, size, vector_name, size, vector_name, vector_name)

    @staticmethod
    def generate_max_index_return(classes, vector_name="v"):
        return "int max_index = 0;\n" \
               "for (int i = 0; i < %d; i++){ if (%s[i] > %s[max_index]){ max_index = i; }}\n" \
               "return max_index;\n" % (classes, vector_name, vector_name)

    def generate_code_expanded(self):
        code = self.generate_vector_declaration(name="result0", size=self.clf.coefs_[0].shape[1],
                                                vector_type="double")
        code += self.generate_vector_mul_matrix(self.clf.coefs_[0], result_name="result0")
        code += self.generate_vector_add_vector(self.clf.intercepts_[0], vector2_name="result0", result_name="result0")
        code += self.generate_relu_activation_on_vector(size=self.clf.coefs_[0].shape[1], vector_name="result0")

        code += self.generate_vector_declaration(name="result1", size=self.clf.coefs_[1].shape[1], vector_type="double")
        code += self.generate_vector_mul_matrix(self.clf.coefs_[1], result_name="result1", vector_name="result0")
        code += self.generate_vector_add_vector(self.clf.intercepts_[1], vector2_name="result1", result_name="result1")
        code += self.generate_softmax_activation_on_vector(size=self.clf.coefs_[0].shape[1], vector_name="result1")

        code += self.generate_max_index_return(len(self.clf.classes_), vector_name="result1")
        return code

    def generate_layer_transformation(self, layer, vector_name="x", decomposed=False):
        result = self.generate_vector_declaration(
            name="result%d" % layer,
            size=self.clf.coefs_[layer].shape[1], vector_type="float"
        )
        if decomposed:
            result += ArduinoGenerator.generate_decomposed_loop_vector_mul_matrix(
                neurons=self.clf.coefs_[layer].shape[1],
                result_name="result%d" % layer,
                vector_size=self.clf.coefs_[layer].shape[0],
                vector_name=vector_name, matrix_type="float",
                matrix_name="pmdata_%d" % layer
            )
        else:
            result += ArduinoGenerator.generate_loop_vector_mul_matrix(
                neurons=self.clf.coefs_[layer].shape[1],
                result_name="result%d" % layer,
                vector_size=self.clf.coefs_[layer].shape[0],
                vector_name=vector_name, matrix_type="float",
                matrix_name="pmdata_%d" % layer
            )
        return result + self.generate_vector_add_vector(
            self.clf.intercepts_[layer],
            vector2_name="result%d" % layer,
            result_name="result%d" % layer
        )

    def generate_code_for_arduino(self, cname):
        code = self.license_header()

        code += ArduinoGenerator.get_arduino_header()
        #code += "#include \"neural_nets.h\"\n"
        for layer in range(self.clf.n_layers_ - 1):
            for col in range(self.clf.coefs_[layer].shape[1]):
                code += ArduinoGenerator.get_progmem_array(self.clf.coefs_[layer][:, [col]],
                                                           name="pmdata_%d%d" % (layer, col))

        vector_names = ["x", "result0"]
        hidden_layers = len(self.clf.hidden_layer_sizes)
        function_body = ""
        for layer in range(hidden_layers):
            function_body += self.generate_layer_transformation(layer, vector_name=vector_names[layer], decomposed=True)
            function_body += self.generate_relu_activation_on_vector(size=self.clf.coefs_[layer].shape[1],
                                                                     vector_name="result%d" % layer)
        function_body += self.generate_layer_transformation(hidden_layers, vector_name=vector_names[hidden_layers],
                                                            decomposed=True)
        function_body += self.generate_softmax_activation_on_vector(
            size=self.clf.coefs_[hidden_layers].shape[1], vector_name="result%d" % hidden_layers)

        function_body += self.generate_max_index_return(len(self.clf.classes_), vector_name="result1")
        code += generate_c_function(function_body=function_body, return_type="int",
                                    name=cname, args="uint8_t * x")
        return code

    def generate(self, fname = 'mlp_model.c', cname="classifier", **kwargs):
        with open(fname, 'w') as output_file:
            output_file.write(self.generate_code_for_arduino(cname))
