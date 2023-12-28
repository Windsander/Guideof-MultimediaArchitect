#include <math.h>
#include <stdio.h>

double mse(double *y_true, double *y_pred, int size) {
  double sum = 0;
  for (int i = 0; i < size; i++) {
    sum += pow(y_true[i] - y_pred[i], 2);
  }
  return sum / size;
}

int main() {
  int size = 3;
  double y_true[] = {0.5, 0.75, 1.0};
  double y_pred[] = {0.6, 0.8, 0.9};
  double mse_value = mse(y_true, y_pred, size);
  printf("The MSE is %f\n", mse_value);
  return 0;
}