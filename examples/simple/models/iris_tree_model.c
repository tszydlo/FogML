int classify(double * x){
  if (x[3] <= 0.8000000119) {
    return 0;
  }
  else {
    if (x[3] <= 1.7500000000) {
      if (x[2] <= 4.9499998093) {
        if (x[3] <= 1.6500000954) {
          return 1;
        }
        else {
          return 2;
        }
      }
      else {
        if (x[3] <= 1.5499999523) {
          return 2;
        }
        else {
          if (x[0] <= 6.9499998093) {
            return 1;
          }
          else {
            return 2;
          }
        }
      }
    }
    else {
      if (x[2] <= 4.8500003815) {
        if (x[0] <= 5.9499998093) {
          return 1;
        }
        else {
          return 2;
        }
      }
      else {
        return 2;
      }
    }
  }
};
