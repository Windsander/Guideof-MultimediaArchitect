#include <math.h>
#include <stdbool.h>
#include <stdio.h>

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

// Get Triplet Mask
void get_triplet_mask(int labels[BATCH_SIZE],
                      bool mask[BATCH_SIZE][BATCH_SIZE][BATCH_SIZE]) {
  for (int i = 0; i < BATCH_SIZE; i++) {
    for (int j = 0; j < BATCH_SIZE; j++) {
      for (int k = 0; k < BATCH_SIZE; k++) {
        // indices_equal
        bool i_not_j = (i == j);
        bool i_not_k = (i == k);
        bool j_not_k = (j == k);
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

// Batch All Triplet Loss
double triplet_loss(int labels[BATCH_SIZE],
                    double embeddings[BATCH_SIZE][VECTOR_SIZE], double margin,
                    bool squared, double *fraction_positives) {

  // So, this only caused once per epoch for certain storage space
  double pairwise_distances[BATCH_SIZE][BATCH_SIZE];
  bool triplets_avail_masks[BATCH_SIZE][BATCH_SIZE][BATCH_SIZE];

  // Pairwise distance calculation
  pairwise_distance(embeddings, pairwise_distances, squared);

  // Get triplet mask
  get_triplet_mask(labels, triplets_avail_masks);

  // Triplet loss calculation
  int num_positive = 0;
  int num_validate = 0;
  double triplet_cost = 0.0;
  {
    for (int i = 0; i < BATCH_SIZE; i++) {     // i for Anchor
      for (int j = 0; j < BATCH_SIZE; j++) {   // j for positive
        for (int k = 0; k < BATCH_SIZE; k++) { // k for negative
          double current_mask = triplets_avail_masks[i][j][k];
          double current_loss =
              fmax(0, current_mask * (pairwise_distances[i][j] -
                                      pairwise_distances[i][k] + margin));
          triplet_cost += current_loss;

          // Calculate number of positive triplets and valid triplets
          if (current_loss > 0) {
            num_positive++;
          }
          if (current_mask > 0) {
            num_validate++;
          }
        }
      }
    }
    // Calculate fraction of positive triplets
    *fraction_positives =
        (double)num_positive / ((double)num_validate + DEVIDE_SAFE);
    return triplet_cost / (double)(num_positive + DEVIDE_SAFE);
  }
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
  double fraction_positives = 0.0;
  double triplet_cost_value =
      triplet_loss(labels, embeddings, margin, false, &fraction_positives);
  printf("The triplet loss is %f with positives %f \n", triplet_cost_value,
         fraction_positives);
  return 0;
}