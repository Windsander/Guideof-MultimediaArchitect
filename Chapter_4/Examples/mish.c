#include <math.h>
#include <stdio.h>

double mish(double x) { return x * tanh(log(1 + exp(x))); }

int main() {
  double x = 0.5;
  double y = mish(x);
  printf("The mish of %f is %f\n", x, y);
  return 0;
}