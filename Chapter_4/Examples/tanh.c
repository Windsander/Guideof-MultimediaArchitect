#include <math.h>
#include <stdio.h>

double tanh(double x) { return (exp(x) - exp(-x)) / (exp(x) + exp(-x)); }

int main() {
  double x = 0.5;
  double y = tanh(x);
  printf("The tanh of %f is %f\n", x, y);
  return 0;
}