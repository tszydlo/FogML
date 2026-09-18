#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include "isolation_forest_test.h"

// compilation: gcc program.c isolation_forest_test.c -lm -o main
// run: ./main

int main() {
    // this example should be predicted as anomaly
    // float example[] = {0.08577195, 0.44609929, 0.17940467, 0.42611499, 1.2588785, 0.08970673, 0.00911895, 0.04256261, 1.44378307, 0.75, 0.28571429, 0.25};
    // float example[] = {2.19, 0.22, 0.95, -0.52, 1.73, -9.48, 7.54, 0.93, 4.80, 4.00, 5.00, 4.00};
    // float example[] = {0.70, 0.10, 1.17, -0.42, 1.03, -9.59, 0.75, 1.90, 2.02, 7.00, 3.00, 4.00};
    // float example[] = {2.59, 0.20, 4.09, -1.86, 17.02, -11.17, 12.41, 35.71, 658.52, 5.00, 3.00, 3.00};
    // float example[] = {2.59, 0.20, 4.09, -1.86, 17.02, -11.17, 12.41, 35.71, 658.52, 5.00, 3.00, 3.00};
    float example[] = {12313123.70, 123123.10, 123123.17, -1231231.42, 123132.03, -123132.59, 123123.75, 123123.90, 12123.02, 12313.00, 123123.00, 123132.00};
    // anomaly score
    float prediction = predict(example);
    printf("Prediction: %f\n", prediction);
    return 0;
}
