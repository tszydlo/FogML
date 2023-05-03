#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include "isolation_forest_test.h"

int main() {
    float example[] = {0.08577195, 0.44609929, 0.17940467, 0.42611499, 1.2588785, 0.08970673, 0.00911895,
    0.04256261, 1.44378307, 0.75, 0.28571429, 0.25};
    float prediction = predict(example);

    printf("Prediction: %f\n", prediction);
    return 0;
}
