#include <math.h>
#include <stdio.h>

double sigmoid(double x) { return 1 / (1 + exp(-x)); }

int main() {
  double x = 0.5;
  double y = sigmoid(x);
  printf("The sigmoid of %f is %f\n", x, y);
  return 0;
}