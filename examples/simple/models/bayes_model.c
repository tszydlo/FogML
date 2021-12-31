int evaluate_bayes(double* x){

    double sigma[3][4] = {
{0.121764, 0.140816, 0.029556, 0.010884, },
{0.261104, 0.096500, 0.216400, 0.038324, },
{0.396256, 0.101924, 0.298496, 0.073924, },
};
    double theta[3][4] = {
{5.006000, 3.428000, 1.462000, 0.246000, },
{5.936000, 2.770000, 4.260000, 1.326000, },
{6.588000, 2.974000, 5.552000, 2.026000, },
};
    double log_sigma[3][4] = {
{-0.267793, -0.122424, -1.683591, -2.682584, },
{0.495041, -0.500335, 0.307250, -1.423802, },
{0.912182, -0.445651, 0.628878, -0.766841, },
};

    double prior[3] = {-1.098612, -1.098612, -1.098612, };

    double n_ij;
    double temp_sum;
    double joint_log_likelihood[3];

    for (int i = 0; i < 3; i++){
        temp_sum = 0;
        for (int j = 0; j < 4; j++){
            temp_sum += log_sigma[i][j];
        }
        n_ij = -0.5 * temp_sum;

        temp_sum = 0;
        for (int j = 0; j < 4; j++){
            temp_sum += ((x[j] - theta[i][j]) * (x[j] - theta[i][j])) / (sigma[i][j]);
        }
        n_ij -= 0.5 * temp_sum;
        joint_log_likelihood[i] = prior[i] + n_ij;
    }

    int max_index = 0;
    for (int i = 0; i < 3; i++){
        printf("%lf\n", joint_log_likelihood[i]);
        if (joint_log_likelihood[i] > joint_log_likelihood[max_index]){
            max_index = i;
        }
    }
    return max_index;
}