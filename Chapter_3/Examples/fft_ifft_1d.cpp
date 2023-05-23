/*
 * Copyright (c) 2023 Arikan.Li [Updated]
 * Created by Arikan.Li on 2014/7/12.
 * <last modified at> 2023/4/30 [commit:: encapsulated all old-coded-resources for Project_M]
 *
 * FFT & IFFT Theorem-Version
 *
 * [theorem::definitions]
 *   Fo meanings Original Function
 *   Fn meanings Fourier Basis at [n]
 *   pi meanings π
 *   T  meanings Periodic of Fo
 *   N  meanings Slice of Frequency
 *   Wn meanings Angular Frequency of Basis Fn is Wn = ((2*pi*n)/T)
 * [theorem::formula]
 *   See below at Algorithmic Practical Function(FFT/IFFT)
 *   So:
 *     An = Re(Fn[t]);  Bn = Im(Fn[t])
 */

#include "stdio.h"
#include "math.h"

#define PI 3.1415926f

typedef struct Complex {
    double re_;
    double im_;

    Complex operator+(const Complex &b_) const {
        Complex result_;
        result_.re_ = re_ + b_.re_;
        result_.im_ = im_ + b_.im_;
        return result_;
    }

    Complex operator-(const Complex &b_) const {
        Complex result_;
        result_.re_ = re_ - b_.re_;
        result_.im_ = im_ - b_.im_;
        return result_;
    }

    Complex operator*(const Complex &b_) const {
        Complex result_;
        result_.re_ = re_ * b_.re_ - im_ * b_.im_;
        result_.im_ = re_ * b_.im_ + im_ * b_.re_;
        return result_;
    }

} Rotator, FBasis;

void digital_convert(double *digital_, Complex *complex_, size_t size_, bool inverse = false) {
    if (!inverse) {
        for (int i = 0; i < size_; i++) {
            complex_[i] = {digital_[i], 0};
        }
    } else {
        for (int i = 0; i < size_; i++) {
            digital_[i] = complex_[i].re_ / size_;
        }
    }
}

void bit_reversal(Complex *input_, FBasis *result_, size_t size_, bool inverse = false) {
    for (int i = 0; i < size_; i++) {
        int k = i, j = 0;
        double level_ = (log(size_) / log(2));
        while ((level_--) > 0) {
            j = j << 1;
            j |= (k & 1);
            k = k >> 1;
        }
        if (j > i) {
            Complex temp = input_[i];
            result_[i] = input_[j];
            result_[j] = temp;
        }
    }
}

void butterfly(Complex *target_, int step_, int slice_idx_, bool inverse = false) {
    int start_at_ = slice_idx_ * 2 * step_;
    for (int inner_idx_ = 0; inner_idx_ < step_; inner_idx_++) {
        Rotator R_ = {
            cos(2 * PI * inner_idx_ / (2.0f * step_)),
            (inverse ? -1 : +1) * sin(2 * PI * inner_idx_ / (2.0f * step_))
        };
        // printf("R_ at %i :: %f + i %f \n", inner_idx_, R_.re_, R_.im_);
        Complex temp_t_ = target_[start_at_ + inner_idx_];
        Complex temp_b_ = target_[start_at_ + inner_idx_ + step_] * R_;
        target_[start_at_ + inner_idx_] = temp_t_ + temp_b_;
        target_[start_at_ + inner_idx_ + step_] = temp_t_ - temp_b_;
    }
}

/**
 * 1D-FFT [Fast Fourier Transform]
 * [How to Use]
 *   <case:>
 *     Fo[T] = {...};
 *     Fn[T] = {};
 *     fft_1d(&Fo, &Fn, T);
 * [logistic]
 * {
 *   result = []; // as byte array
 *   // do Bit-Reversal
 *   Fo_sorted = bit_reversal(Fn, Fn, T);
 *   // do DIT:
 *   for (int layer_at_ = 0; layer_at_ < max_layer; layer_at_++) {
 *     layer_step_ = 2 ^ layer_at;
 *     // do Butterfly (each layer):
 *     for (int slice_idx_ = 0; slice_idx_ * 2 * step_ < size_; slice_idx_++) {
 *       for (int inner_idx_ = 0; inner_idx_ < step_; inner_idx_++) {
 *          Rotator Rn = complex_from_angle(PI * inner_idx_ / layer_step_)
 *          then Calculate Cross(Butterfly-2x2 Matrix):
 *              slice_out_[inner_idx_] = {
 *                  slice_data_[inner_idx_] + slice_data_[inner_idx_ + step_] * R_
 *              };
 *              slice_out_[inner_idx_ + step_] = {
 *                  slice_data_[inner_idx_] - slice_data_[inner_idx_ + step_] * R_
 *              };
 *       }
 *       layer_out_[slice_idx_] = slice_out_;
 *     }
 *   }
 *   return result;
 * }
 * @param Fo Original Function input array
 *           (already sampled by T as count-of-time-slice)
 * @param Fn Fourier Basis
 *           (already sampled by N as count-of-frequency-slice)
 * @param T  Periodic of Fo, Number of Time Slice,
 *           (also as Number of Frequency Slice for FFT)
 */
void fft_1d(double *Fo, FBasis *Fn, size_t size_) {
    digital_convert(Fo, Fn, size_);
    bit_reversal(Fn, Fn, size_);
    for (int layer_at_ = 0; layer_at_ < log(size_) / log(2); layer_at_++) {
        int step_ = 1 << layer_at_;
        for (int slice_idx_ = 0; slice_idx_ * 2 * step_ < size_; slice_idx_++) {
            butterfly(Fn, step_, slice_idx_);
        }
    }
}

/**
 * 1D-IFFT [Inverse Fast Fourier Transform]
 * [How to Use]
 *   <case:>
 *     Fo[T] = {};
 *     Fn[T] = {...};
 *     fft_1d(&Fo, &Fn, T);
 * [logistic]
 * {
 *   result = []; // as byte array
 *   // do Bit-Reversal
 *   Fo_sorted = bit_reversal(Fn, Fn, T) / T; dont forget divide N(num equal T)  [<= key]
 *   // do DIT:
 *   for (int layer_at_ = 0; layer_at_ < max_layer; layer_at_++) {
 *     layer_step_ = 2 ^ layer_at;
 *     // do Inverse Butterfly (each layer):
 *     for (int slice_idx_ = 0; slice_idx_ * 2 * step_ < size_; slice_idx_++) {
 *       for (int inner_idx_ = 0; inner_idx_ < step_; inner_idx_++) {
 *          Rotator Rn = complex_from_angle(-i * PI * inner_idx_ / layer_step_)  [<= key]
 *          then Calculate Cross(Butterfly-2x2 Matrix):
 *              slice_out_[inner_idx_] = {
 *                  slice_data_[inner_idx_] + slice_data_[inner_idx_ + step_] * R_
 *              };
 *              slice_out_[inner_idx_ + step_] = {
 *                  slice_data_[inner_idx_] - slice_data_[inner_idx_ + step_] * R_
 *              };
 *       }
 *       layer_out_[slice_idx_] = slice_out_;
 *     }
 *   }
 *   return result;
 * }
 * @param Fo Original Function input array
 *           (already sampled by T as count-of-time-slice)
 * @param Fn Fourier Basis
 *           (already sampled by N as count-of-frequency-slice)
 * @param T  Periodic of Fo, Number of Time Slice,
 *           (also as Number of Frequency Slice for FFT)
 */
void ifft_1d(double *Fo, FBasis *Fn, size_t size_) {
    bit_reversal(Fn, Fn, size_);
    for (int layer_at_ = 0; layer_at_ < log(size_) / log(2); layer_at_++) {
        int step_ = 1 << layer_at_;
        for (int slice_idx_ = 0; slice_idx_ * 2 * step_ < size_; slice_idx_++) {
            butterfly(Fn, step_, slice_idx_, true);
        }
    }
    digital_convert(Fo, Fn, size_, true);
}

int main(void) {
    FBasis Fn[8] = {};
    double Fo[8] = {0, 1, 2, 3, 4, 5, 6, 7};
    double iFo[8] = {};
    size_t T = sizeof(Fo) / sizeof(double);
    size_t N = sizeof(Fn) / sizeof(FBasis);
    printf("\n Original_data: \n");
    for (int t = 0; t < T; ++t) {
        printf("%f  ", Fo[t]);
    }

    printf("\n FFT_result: \n");
    fft_1d(Fo, Fn, T);
    for (int n = 0; n < N; ++n) {
        printf("%f + i %f \n", Fn[n].re_, Fn[n].im_);
    }

    printf("\n IFFT_result: \n");
    ifft_1d(iFo, Fn, T);
    for (int t = 0; t < T; ++t) {
        printf("%f  ", iFo[t]);
    }

    return 0;
}