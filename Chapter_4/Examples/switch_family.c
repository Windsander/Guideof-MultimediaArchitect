#include <math.h>
#include <stdio.h>

double swish(double x) { return x * tanh(x); }

double swish_beta(double x, double beta) { return x * tanh(beta * x); }

double h_swish(double x) { return x * tanh(log(1 + exp(x))); }

int main() {
  // Swish
  {
    double x = 0.5;
    double y = swish(x);
    printf("The swish of %f is %f\n", x, y);
  }

  // Swish-β
  {
    double x = 0.5;
    double beta = 1.0;
    double y = swish_beta(x, beta);
    printf("The swish-beta of %f with beta=%f is %f\n", x, beta, y);
  }

  // h-Swish
  {
    double x = 0.5;
    double y = h_swish(x);
    printf("The h-swish of %f is %f\n", x, y);
  }

  return 0;
}