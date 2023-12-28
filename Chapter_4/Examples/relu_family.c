#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

double relu(double x) { return fmax(0, x); }

double prelu(double x, double tau) { return fmax(0, x) + tau * fmin(0, x); }

double lrelu(double x, double alpha) { return fmax(alpha * x, x); }

double rrelu(double x, double alpha, double lower, double upper) {
  double r = (double)rand() / (double)RAND_MAX;
  double alpha_rand = lower + r * (upper - lower);
  return fmax(alpha_rand * x, x);
}

int main() {
  // ReLU
  {
    double x = -0.5;
    double y = relu(x);
    printf("The ReLU of %f is %f\n", x, y);
  }
  {
    double x = +0.5;
    double y = relu(x);
    printf("The ReLU of %f is %f\n", x, y);
  }

  // PReLU
  {
    double x = -0.5;
    double tau = 0.1;
    double y = prelu(x, tau);
    printf("The PReLU of %f with alpha=%f is %f\n", x, tau, y);
  }

  // LReLU
  {
    double x = -0.5;
    double alpha = 0.1;
    double y = lrelu(x, alpha);
    printf("The LReLU of %f with alpha=%f is %f\n", x, alpha, y);
  }

  // RReLU
  {
    // Set the random seed
    srand(time(NULL));

    double x = -0.5;
    double alpha = 0.1;
    double lower = 0.0;
    double upper = 1.0;
    double y = rrelu(x, alpha, lower, upper);
    printf("The RReLU of %f with alpha=%f, lower=%f, and upper=%f is %f\n", x,
           alpha, lower, upper, y);
  }

  return 0;
}