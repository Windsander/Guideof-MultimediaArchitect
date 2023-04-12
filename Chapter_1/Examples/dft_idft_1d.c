/*
 * Copyright (c) 2023 Arikan.Li [Updated]
 * Created by Arikan.Li on 2014/7/12.
 * <last modified at> 2023/1/26 [commit:: encapsulated all old-coded-resources for Project_M]
 *
 * DFT & IDFT Theorem-Version
 *
 * [theorem::definitions]
 *   Fo meanings Original Function
 *   Fn meanings Fourier Basis at [n]
 *   pi meanings π
 *   T  meanings Periodic of Fo
 *   N  meanings Slice of Frequency
 *   Wn meanings Angular Frequency of Basis Fn is Wn = ((2*pi*n)/T)
 * [theorem::formula]
 *   Fo[t] = sum_{n=0}^{N-1} x Fn[t] * exp(  i * ((2*pi*n)/T) * t), 0<=n<N
 *   Fn[t] = sum_{t=0}^{T-1} x Fo[t] * exp( -i * ((2*pi*n)/T) * t), 0<=t<T
 *         = sum_{t=0}^{T-1} x Fo[t] * (An * cos(Wn * t) + Bn * sin(Wn * t)), 0<=t<T
 *         = All_in_one(An) * cos(Wn * t) + All_in_one(Bn) * sin(Wn * t), 0<=t<T
 *   So:
 *     An = Re(Fn[t]);  Bn = Im(Fn[t])
 */

#include "math.h"

#define PI 3.1415926f

typedef struct FBasis {
    double re_;
    double im_;
    double w_;
} FBasis;

/**
 * 1D-DFT [Discrete Fourier Transform]
 * [How to Use]
 *   <case:>
 *     Fo[T] = {...};
 *     Fn[N] = {};
 *     dft_1d(&Fo, &Fn, T, N);
 * [logistic]
 * {
 *   result = []; // as byte array
 *   // do TDD:
 *   for n in range(N) {
 *     An = 0; Bn = 0;
 *     // do FDD:
 *     for t in Range(T) {
 *       Wn = (2 * pi * n) / T;
 *       An = Re += Cos(Wn * t) * Fo(t);
 *       Bn = Im += Sin(Wn * t) * Fo(t);
 *     }
 *     result[n] = Fn.to_complex_angular_form(An, Bn)
 *   }
 *   return result;
 * }
 * @param Fo Original Function input array
 *           (already sampled by T as count-of-time-slice)
 * @param Fn Fourier Basis
 *           (already sampled by N as count-of-frequency-slice)
 * @param T  Periodic of Fo, Number of Time Slice
 * @param N  Number of Frequency Slice
 */
void dft_1d(double *Fo, FBasis *Fn, size_t T, size_t N) {
    for (int n = 0; n < N; ++n) {
        double An = 0;
        double Bn = 0;
        double Wn = (2 * PI * n) / T;
        for (int t = 0; t < T; ++t) {
            An += cos(Wn * t) * Fo[t];
            Bn += sin(Wn * t) * Fo[t];
        }
        FBasis e_ = {An, Bn, Wn};
        Fn[n] = e_;
    }
}

/**
 * 1D-IDFT [Inverse Discrete Fourier Transform]
 * [How to Use]
 *   <case:>
 *     Fo[T] = {};
 *     Fn[N] = {...};
 *     dft_1d(&Fo, &Fn, T, N);
 * [logistic]
 * {
 *   result = []; // as byte array
 *   // do TDD:
 *   for t in range(T) {
 *     Re = 0; Im = 0;
 *     // do FDD:
 *     for n in Range(N) {
 *       Wn = (2 * pi * n) / T;
 *       An = Re(Fn[n]);
 *       Bn = Im(Fn[n]);
 *       result[t] += Fn[n].to_value(Wn, An, Bn) / N;
 *     }
 *   }
 *   return result;
 * }
 * @param Fo Original Function input array
 *           (already sampled by T as count-of-time-slice)
 * @param Fn Fourier Basis
 *           (already sampled by N as count-of-frequency-slice)
 * @param T  Periodic of Fo, Number of Time Slice
 * @param N  Number of Frequency Slice
 */
void idft_1d(double *Fo, FBasis *Fn, size_t T, size_t N) {
    for (int t = 0; t < T; ++t) {
        for (int n = 0; n < N; ++n) {
            FBasis e_ = Fn[n];
            Fo[t] += (e_.re_ * cos(e_.w_ * t) + e_.im_ * sin(e_.w_ * t)) / N;
        }
    }
}

int main(void) {
    FBasis Fn[6] = {};
    double Fo[6] = {1, 2, 3, 4, 5, 6};
    double iFo[6] = {};
    size_t T = sizeof(Fo) / sizeof(double);
    size_t N = sizeof(Fn) / sizeof(FBasis);
    printf("\n Original_data: \n");
    for (int t = 0; t < T; ++t) {
        printf("%f  ", Fo[t]);
    }

    printf("\n DFT_result: \n");
    dft_1d(Fo, Fn, T, N);
    for (int n = 0; n < N; ++n) {
        printf("%f + i %f \n", Fn[n].re_, Fn[n].im_);
    }

    printf("\n IDFT_result: \n");
    idft_1d(iFo, Fn, T, N);
    for (int t = 0; t < T; ++t) {
        printf("%f  ", iFo[t]);
    }

    return 0;
}
