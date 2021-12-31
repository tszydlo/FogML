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

from .utils import generate_c_array

class ArduinoGenerator:
    @staticmethod
    def generate_loop_vector_mul_matrix(neurons=10, result_name="r", vector_size=10, vector_name="x", matrix_type="int",
                                        matrix_name="m"):
        return "for(int n=0; n<%d; n++){\n" \
               "%s[n]=0;\n" \
               "for(int i=0;i<%d;i++){" \
               "%s[n]+=(%s)pgm_read_%s_near(%s+i*%d+n) * (%s)%s[i];}\n" \
               "}\n" % (neurons, result_name, vector_size, result_name, matrix_type, matrix_type, matrix_name, neurons,
                        matrix_type, vector_name)

    @staticmethod
    def generate_decomposed_loop_vector_mul_matrix(neurons=10, result_name="r", vector_size=10, vector_name="x",
                                                   matrix_type="int", matrix_name="m"):
        result = ""
        for k in range(neurons):
            result += "%s[%d]=0;\n" \
                      "for(int i=0;i<%d;i++){" \
                      "%s[%d]+=(%s)pgm_read_%s_near(%s%d+i) * (%s)%s[i];}\n" % (
                          result_name, k, vector_size, result_name, k, matrix_type, matrix_type, matrix_name, k,
                          matrix_type, vector_name
                      )
        return result

    @staticmethod
    def get_progmem_array(array, arr_type="float", name="arr"):
        return "const %s %s[] PROGMEM = %s;\n" % (arr_type, name, generate_c_array(array))

    @staticmethod
    def get_arduino_header():
        return "#include <Arduino.h>\n"
