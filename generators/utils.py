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
