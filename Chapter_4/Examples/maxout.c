#include <stdio.h>
#include <stdlib.h>

double maxout(double *x, int size) {
  double max_value = x[0];
  for (int i = 1; i < size; i++) {
    if (x[i] > max_value) {
      max_value = x[i];
    }
  }
  return max_value;
}

int main() {
  int size = 3;
  double vecx[] = {0.5, 0.75, 1.0};
  double w = maxout(vecx, size);
  printf("The maxout of the input vector is %f\n", w);
  return 0;
}