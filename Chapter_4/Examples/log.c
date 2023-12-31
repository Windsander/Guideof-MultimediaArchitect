#include <math.h>
#include <stdio.h>

double log_loss(double *y_true, double *y_pred, int size) {
  double sum = 0;
  for (int i = 0; i < size; i++) {
    sum += y_true[i] * log(y_pred[i]) + (1 - y_true[i]) * log(1 - y_pred[i]);
  }
  return -sum / size;
}

int main() {
  int size = 3;
  double y_true[] = {0.5, 0.75, 1.0};
  double y_pred[] = {0.6, 0.8, 0.9};
  double log_loss_value = log_loss(y_true, y_pred, size);
  printf("The log loss is %f, for object class 'apple'", log_loss_value);
  return 0;
}