#include <math.h>
#include <stdio.h>

double contrastive_loss(double *y_true, double *y_pred, int size,
                        double margin) {
  double sum = 0;
  for (int i = 0; i < size; i++) {
    double distance = y_pred[i];
    sum += y_true[i] * pow(distance, 2) +
           (1 - y_true[i]) * pow(fmax(0, margin - distance), 2);
  }
  return sum / size;
}

int main() {
  int size = 3;
  double y_true[] = {0.5, 0.75, 1.0}; // single sample base 'cat' 'puppy' 'dog'
  double y_pred[] = {0.6, 0.8, 0.9};  // single sample pred 'cat' 'puppy' 'dog'
  // int num_classes = 3;
  double margin = 0.2;
  double loss_value = contrastive_loss(y_true, y_pred, size, margin);
  printf("The contrastive loss is %f\n", loss_value);
  return 0;
}