#include <math.h>
#include <stdio.h>

double hinge_loss(double *y_true, double *y_pred, int size) {
  double sum = 0;
  for (int i = 0; i < size; i++) {
    double margin = 1 - y_true[i] * y_pred[i];
    sum += fmax(0, margin);
  }
  return sum / size;
}

int main() {
  int size = 4;
  double y_true[] = {0.5, 0.75, 1.0, 1.0};
  double y_pred[] = {0.6, 0.8, 0.9, 0.3};
  double hinge_loss_value = hinge_loss(y_true, y_pred, size);
  printf("The hinge loss is %f\n", hinge_loss_value);
  return 0;
}