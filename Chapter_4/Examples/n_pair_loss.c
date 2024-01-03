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

// Get N-Pair Mask (Totally same with Triplet Mask)
void get_n_pair_mask(int labels[BATCH_SIZE],
                     bool mask[BATCH_SIZE][BATCH_SIZE][BATCH_SIZE]) {
  for (int i = 0; i < BATCH_SIZE; i++) {
    for (int j = 0; j < BATCH_SIZE; j++) {
      for (int k = 0; k < BATCH_SIZE; k++) {
        // indices_equal
        bool i_not_j = (i != j);
        bool i_not_k = (i != k);
        bool j_not_k = (j != k);
        bool distinct_indices = (i_not_j && i_not_k && j_not_k);

        // label_equal
        bool i_equal_j = (labels[i] == labels[j]);
        bool i_equal_k = (labels[i] == labels[k]);
        bool valid_labels = (i_equal_j && !i_equal_k);

        // mask depends on both
        mask[i][j][k] = (distinct_indices && valid_labels);
      }
    }
  }
}

// Batch All N-Pair Loss
double n_pair_loss(int labels[BATCH_SIZE],
                   double embeddings[BATCH_SIZE][VECTOR_SIZE], double margin,
                   bool squared, double *fraction_positives) {

  // So, this only caused once per epoch for certain storage space
  double pairwise_distances[BATCH_SIZE][BATCH_SIZE];
  bool n_paired_avail_masks[BATCH_SIZE][BATCH_SIZE][BATCH_SIZE];

  // Pairwise distance calculation
  pairwise_distance(embeddings, pairwise_distances, squared);

  // Get n_pair mask
  get_n_pair_mask(labels, n_paired_avail_masks);

  // n_pair loss calculation
  int num_positive = 0;
  int num_validate = 0;
  double n_pair_cost = 0.0;
  {
    for (int i = 0; i < BATCH_SIZE; i++) { // i for Anchor
      double n_pair_loss = 0.0;
      for (int j = 0; j < BATCH_SIZE; j++) {   // j for positive
        for (int k = 0; k < BATCH_SIZE; k++) { // k for negative
          double current_mask = n_paired_avail_masks[i][j][k];
          double current_loss = current_mask * exp(pairwise_distances[i][j] -
                                                   pairwise_distances[i][k]);
          n_pair_loss += current_loss;

          // Calculate number of positive n_pairs and valid n_pairs
          if (current_loss > margin) {
            num_positive++;
          }
          if (current_mask > 0) {
            num_validate++;
          }
        }
      }
      n_pair_cost += log(margin + n_pair_loss);
    }
  }
  // Calculate fraction of positive n_pairs
  *fraction_positives =
      (double)num_positive / ((double)num_validate + DEVIDE_SAFE);
  return n_pair_cost / (double)(num_positive + DEVIDE_SAFE);
}

int main() {
  // Example input (fulfill to BATCH_SIZE x VECTOR_SIZE)
  // Use Random labels and embeddings for testing
  // Use three classes as different type, to generate labels
  int type = 3;
  int labels[BATCH_SIZE];
  double embeddings[BATCH_SIZE][VECTOR_SIZE];
  for (int i = 0; i < BATCH_SIZE; i++) {
    labels[i] = rand() % type;
    for (int j = 0; j < VECTOR_SIZE; j++) {
      embeddings[i][j] = (double)rand() / (double)RAND_MAX;
    }
  }

  double margin = 1.0;
  double fraction_positives = 0.0;
  double n_pair_cost_value =
      n_pair_loss(labels, embeddings, margin, false, &fraction_positives);
  printf("The n_pair loss is %f with positives %f \n", n_pair_cost_value,
         fraction_positives);
  return 0;
}
