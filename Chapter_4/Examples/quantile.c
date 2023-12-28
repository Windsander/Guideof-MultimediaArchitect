#include <math.h>
#include <stdio.h>

double quantile_loss(double *y_true, double *y_pred, int size, double q) {
  double sum = 0;
  for (int i = 0; i < size; i++) {
    double error = y_true[i] - y_pred[i];
    if (error > 0) {
      sum += q * error;
    } else {
      sum += (1 - q) * error;
    }
  }
  return sum / size;
}

int main() {
  int size = 3;
  double y_true[] = {0.5, 0.75, 1.0};
  double y_pred[] = {0.6, 0.8, 0.9};
  double q = 0.5;
  double quantile_loss_value = quantile_loss(y_true, y_pred, size, q);
  printf("The quantile loss is %f\n", quantile_loss_value);
  return 0;
}