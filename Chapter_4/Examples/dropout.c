#include <stdio.h>
#include <stdlib.h>
#include <time.h>

double dropout(double x, double p) {
  if (drand48() < p) {
    return 0;
  } else {
    return x;
  }
}

int main() {
  double x = 0.5;
  double p = 0.5;
  double y_1 = dropout(x, p);
  double y_2 = dropout(x, p);
  printf("The dropout of %f with p=%f is %f\n", x, p, y_1);
  printf("The dropout of %f with p=%f is %f\n", x, p, y_2);
  return 0;
}