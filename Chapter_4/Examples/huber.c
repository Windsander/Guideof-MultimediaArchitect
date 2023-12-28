#include <math.h>
#include <stdio.h>

double huber_loss(double *y_true, double *y_pred, int size, double delta) {
  double sum = 0;
  for (int i = 0; i < size; i++) {
    double error = y_true[i] - y_pred[i];
    if (fabs(error) <= delta) {
      sum += 0.5 * pow(error, 2);
    } else {
      sum += delta * (fabs(error) - 0.5 * delta);
    }
  }
  return sum / size;
}

int main() {
  int size = 3;
  double y_true[] = {0.5, 0.75, 1.0};
  double y_pred[] = {0.6, 0.8, 0.9};
  double delta = 1.0;
  double huber_loss_value = huber_loss(y_true, y_pred, size, delta);
  printf("The Huber loss is %f\n", huber_loss_value);
  return 0;
}