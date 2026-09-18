#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include "isolation_forest_test.h"

// compilation: gcc program.c isolation_forest_test.c -lm -o main
// run: ./main

int main() {
    // this example should be predicted as anomaly
    float anomaly_example[] = {2.59, 0.20, 4.09, -1.86, 17.02, -11.17, 12.41, 35.71, 658.52, 5.00, 3.00, 3.00};
    // this not
    float proper_example[] = {0.70, 0.10, 1.17, -0.42, 1.03, -9.59, 0.75, 1.90, 2.02, 7.00, 3.00, 4.00};
    
    float anomaly_prediction = predict(anomaly_example);
    float proper_prediction = predict(proper_example);

    printf("Anomaly prediction: %f\n", anomaly_prediction);
    printf("Proper prediction: %f\n", proper_prediction);
    return 0;
}
