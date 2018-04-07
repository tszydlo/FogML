from generators.utils import generate_c_array


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
