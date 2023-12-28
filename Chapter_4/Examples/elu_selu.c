#include <math.h>
#include <stdio.h>

double elu(double x, double alpha) { return x >= 0 ? x : alpha * (exp(x) - 1); }

double selu(double x, double alpha, double lambda) {
  return lambda * (x >= 0 ? x : alpha * (exp(x) - 1));
}

int main() {
  // ELU
  {
    double x = -0.5;
    double alpha = 1.0;
    double y = elu(x, alpha);
    printf("The ELU of %f with alpha=%f is %f\n", x, alpha, y);
  }

  // SELU
  {
    double x = -0.5;
    double alpha = 1.6732632423543772848170429916717;
    double lambda = 1.0507009873554804934193349650124;
    double y = selu(x, alpha, lambda);
    printf("The SELU of %f with alpha=%f and lambda=%f is %f\n", x, alpha,
           lambda, y);
  }

  return 0;
}