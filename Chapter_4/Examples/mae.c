#include <math.h>
#include <stdio.h>

double mae(double *y_true, double *y_pred, int size) {
  double sum = 0;
  for (int i = 0; i < size; i++) {
    sum += fabs(y_true[i] - y_pred[i]);
  }
  return sum / size;
}

int main() {
  int size = 3;
  double y_true[] = {0.5, 0.75, 1.0};
  double y_pred[] = {0.6, 0.8, 0.9};
  double mae_value = mae(y_true, y_pred, size);
  printf("The MAE is %f\n", mae_value);
  return 0;
}