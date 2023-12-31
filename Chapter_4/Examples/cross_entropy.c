#include <math.h>
#include <stdio.h>

double cross_entropy_loss(double *y_true, double *y_pred, int size,
                          int num_classes) {
  double sum = 0;
  for (int i = 0; i < size; i++) {
    for (int j = 0; j < num_classes; j++) {
      sum += y_true[i * num_classes + j] * log(y_pred[i * num_classes + j]);
    }
  }
  return -sum / size;
}

int main() {
  int size = 3;
  double y_true[] = {0.5, 0.75, 1.0}; // single sample base 'cat' 'puppy' 'dog'
  double y_pred[] = {0.6, 0.8, 0.9};  // single sample pred 'cat' 'puppy' 'dog'
  int num_classes = 3;
  double loss_value = cross_entropy_loss(y_true, y_pred, size, num_classes);
  printf("The cross entropy loss is %f, for 'cat' 'puppy' 'dog' ", loss_value);
  return 0;
}