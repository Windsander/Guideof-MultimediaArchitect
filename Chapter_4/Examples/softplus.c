#include <math.h>
#include <stdio.h>

double softplus(double x) { return log(1 + exp(x)); }

int main() {
  double x = 0.5;
  double y = softplus(x);
  printf("The softplus of %f is %f\n", x, y);
  return 0;
}