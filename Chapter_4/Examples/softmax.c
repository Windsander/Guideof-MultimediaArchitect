#include <math.h>
#include <stdio.h>

double ori_softmax(double *x, int size) {
  double sum = 0;
  for (int i = 0; i < size; i++) {
    sum += exp(x[i]);
  }

  double y = exp(x[0]) / sum;
  for (int i = 1; i < size; i++) {
    y += exp(x[i]) / sum;
  }

  return y;
}

double ori_log_softmax(double *x, int size) {
  double sum = 0;
  for (int i = 0; i < size; i++) {
    sum += exp(x[i]);
  }

  double y = x[0] - log(sum);
  for (int i = 1; i < size; i++) {
    y += x[i] - log(sum);
  }

  return y;
}

double softmax(double *x, int size) {
  double max_value = x[0];
  for (int i = 1; i < size; i++) {
    if (x[i] > max_value) {
      max_value = x[i];
    }
  }

  double sum = 0;
  for (int i = 0; i < size; i++) {
    sum += exp(x[i] - max_value);
  }

  double y = exp(x[0] - max_value) / (sum);
  for (int i = 1; i < size; i++) {
    y += exp(x[i] - max_value) / (sum);
  }

  return y;
}

double log_softmax(double *x, int size) {
  double max_value = x[0];
  for (int i = 1; i < size; i++) {
    if (x[i] > max_value) {
      max_value = x[i];
    }
  }

  double sum = 0;
  for (int i = 0; i < size; i++) {
    sum += exp(x[i] - max_value);
  }

  double y = (x[0] - max_value) - log(sum);
  for (int i = 1; i < size; i++) {
    y += (x[i] - max_value) - log(sum);
  }

  return y;
}

int main() {
  // Softmax
  {
    int size = 3;
    double vecx[] = {0.5, 0.75, 1.0};
    double w = ori_softmax(vecx, size);
    printf("The softmax of the input vector is %f\n", w);
  }

  // log-Softmax
  {
    int size = 3;
    double vecx[] = {0.5, 0.75, 1.0};
    double w = ori_log_softmax(vecx, size);
    printf("The log-softmax of the input vector is %f\n", w);
  }

  // stable-Softmax, which we use most as Softmax
  {
    int size = 3;
    double vecx[] = {0.5, 0.75, 1.0};
    double w = softmax(vecx, size);
    printf("The stable-softmax of the input vector is %f\n", w);
  }

  // log-stable-Softmax, which we use most as log-Softmax
  {
    int size = 3;
    double vecx[] = {0.5, 0.75, 1.0};
    double w = log_softmax(vecx, size);
    printf("The log-stable-softmax of the input vector is %f\n", w);
  }

  return 0;
}