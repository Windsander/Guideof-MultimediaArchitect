#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define BATCH_SIZE 10     // Batch_size = Samples_of_Person x Data/Person
#define VECTOR_SIZE 128   // Extract output layer Feature vector's dimissions
#define DEVIDE_SAFE 1e-12 // protect when gridant at 0 will be to lage

// Pairwise Distance Calculation
void pairwise_distance(double embeddings[BATCH_SIZE][VECTOR_SIZE],
                       double distances[BATCH_SIZE][BATCH_SIZE], bool squared) {
  for (int i = 0; i < BATCH_SIZE; i++) {
    for (int j = 0; j < BATCH_SIZE; j++) {
      double dot_product = 0.0;
      double square_norm_i = 0.0;
      double square_norm_j = 0.0;

      for (int k = 0; k < VECTOR_SIZE; k++) {
        dot_product += embeddings[i][k] * embeddings[j][k];
        square_norm_i += embeddings[i][k] * embeddings[i][k];
        square_norm_j += embeddings[j][k] * embeddings[j][k];
      }

      distances[i][j] = square_norm_i - (2.0 * dot_product) + square_norm_j;

      if (!squared) {
        if (distances[i][j] < 0.0) {
          distances[i][j] = 0.0;
        } else {
          distances[i][j] = sqrt(distances[i][j]);
        }
      }
    }
  }
}

// Contrastive Loss Calculation
double contrastive_loss(int labels[BATCH_SIZE],
                        double embeddings[BATCH_SIZE][VECTOR_SIZE],
                        double margin) {
  // So, this only caused once per epoch for certain storage space
  double pairwise_distances[BATCH_SIZE][BATCH_SIZE];

  // Pairwise distance calculation
  pairwise_distance(embeddings, pairwise_distances, false);

  // Contrastive loss calculation
  double contrastive_cost = 0.0;
  for (int i = 0; i < BATCH_SIZE; i++) {
    for (int j = 0; j < BATCH_SIZE; j++) {
      if (i != j) {
        double current_loss = 0.0;
        if (labels[i] == labels[j]) {
          current_loss = fmax(0, margin - pairwise_distances[i][j]);
        } else {
          current_loss = fmax(0, pairwise_distances[i][j] - margin);
        }
        contrastive_cost += current_loss;
      }
    }
  }
  return contrastive_cost / (double)(BATCH_SIZE * (BATCH_SIZE - 1));
}

int main() {
  // Example input (fulfill to BATCH_SIZE x VECTOR_SIZE)
  // Use Random labels and embeddings for testing
  // Use three classes as different type, to generate labels
  int labels[BATCH_SIZE];
  double embeddings[BATCH_SIZE][VECTOR_SIZE];
  for (int i = 0; i < BATCH_SIZE; i++) {
    labels[i] = rand() % 3;
    for (int j = 0; j < VECTOR_SIZE; j++) {
      embeddings[i][j] = (double)rand() / (double)RAND_MAX;
    }
  }

  double margin = 0.2;
  double contrastive_cost_value = contrastive_loss(labels, embeddings, margin);
  printf("The contrastive loss is %f \n", contrastive_cost_value);
  return 0;
}
