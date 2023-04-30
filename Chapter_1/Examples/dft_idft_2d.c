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

#include "stdio.h"
#include "math.h"

#define PI 3.1415926f

typedef struct FBasis {
    double re_;
    double im_;
    double w_[2];
} FBasis;

typedef struct Signal2DOriginal {
    int GW_;
    int GH_;
    double *Fo_;
} Signal2DOriginal;

typedef struct Signal2DAnalyzed {
    int NU_;
    int NV_;
    FBasis *Fn_;
} Signal2DAnalyzed;

/**
 * 2D-DFT [Discrete Fourier Transform]
 * [How to Use]
 *   <case:>
 *     Fo[W][H] = {...};
 *     Fn[U][V] = {};
 *     dft_2d(&Fo, &Fn);
 * [logistic]
 * {
 *   result[U][V] = []; // as byte 2D-array
 *   // do SDD:
 *   for u in range(NU-Horizontal_Slices) {
 *   for v in range(NV-Vertical_Slices)   {
 *     An = 0; Bn = 0;
 *     // do FDD:
 *     for y in Range(Height) {
 *     for x in Range(Wight)  {
 *       Wn = (2 * PI) * Vec< (u / U , v / V)>;
 *       An = Re += Cos(Wn · Vec<x,y>T) * Fo(t);
 *       Bn = Im += Sin(Wn · Vec<x,y>T) * Fo(t);
 *     }}
 *     result[u][v] = Fn.to_complex_angular_form(An, Bn)
 *   }}
 *   return result;
 * }
 * @param original_ Original Function input 2D-array
 *           (image include width & height)
 * @param analyzed_ Fourier Basis info in 2D
 */
void dft_2d(Signal2DOriginal *original_, Signal2DAnalyzed *analyzed_) {
    for (int u = 0; u < analyzed_->NU_; ++u) {
        for (int v = 0; v < analyzed_->NV_; ++v) {
            double An = 0;
            double Bn = 0;
            double Un = (2 * PI / analyzed_->NU_) * u  ;
            double Vn = (2 * PI / analyzed_->NV_) * v  ;
            for (int y = 0; y < original_->GH_; ++y) {
                for (int x = 0; x < original_->GW_; ++x) {
                    An += cos(Un * x + Vn * y) * original_->Fo_[y * original_->GW_ + x];
                    Bn += sin(Un * x + Vn * y) * original_->Fo_[y * original_->GW_ + x];
                }
            }
            FBasis e_ = {An, Bn, {Un, Vn}};
            analyzed_->Fn_[u * analyzed_->NV_ + v] = e_;
        }
    }
}

/**
 * 2D-IDFT [Inverse Discrete Fourier Transform]
 * [How to Use]
 *   <case:>
 *     Fo[W][H] = {};
 *     Fn[U][V] = {...};
 *     idft_2d(&Fo, &Fn);
 * [logistic]
 * {
 *   result[W][H] = []; // as byte 2D-array
 *   // do SDD:
 *   for y in Range(Height) {
 *   for x in Range(Wight)  {
 *     Re = 0; Im = 0;
 *     // do FDD:
 *     for u in range(NU-Horizontal_Slices) {
 *     for v in range(NV-Vertical_Slices)   {
 *       Wn = (2 * PI) * Vec< (u / U , v / V)>;;
 *       An = Re * (Fn[n] · Vec<x,y>T);
 *       Bn = Im * (Fn[n] · Vec<x,y>T);
 *       result[t] += Fn[n].to_value(Wn, An, Bn) / (U * V);
 *     }}
 *   }
 *   return result;
 * }
 * @param original_ Original Function input 2D-array
 *           (image include width & height)
 * @param analyzed_ Fourier Basis analyzed info in 2D
 */
void idft_2d(Signal2DOriginal *original_, Signal2DAnalyzed *analyzed_) {
    for (int y = 0; y < original_->GH_; ++y) {
        for (int x = 0; x < original_->GW_; ++x) {
            for (int u = 0; u < analyzed_->NU_; ++u) {
                for (int v = 0; v < analyzed_->NV_; ++v) {
                    FBasis e_ = analyzed_->Fn_[u * analyzed_->NV_ + v];
                    original_->Fo_[y * original_->GW_ + x] += (
                        e_.re_ * cos(e_.w_[0] * x + e_.w_[1] * y) +
                        e_.im_ * sin(e_.w_[0] * x + e_.w_[1] * y)
                    ) / (analyzed_->NU_ * analyzed_->NV_);
                }
            }
        }
    }
}


int main(void) {
    double input_data_[36] = {
        1.0f, 2.0f, 3.0f, 4.0f, 5.0f, 6.0f,
        2.0f, 3.0f, 4.0f, 5.0f, 6.0f, 1.0f,
        3.0f, 4.0f, 5.0f, 6.0f, 1.0f, 2.0f,
        4.0f, 5.0f, 6.0f, 1.0f, 2.0f, 3.0f,
        5.0f, 6.0f, 1.0f, 2.0f, 3.0f, 4.0f,
        6.0f, 1.0f, 2.0f, 3.0f, 4.0f, 5.0f
    };
    FBasis output_data_[36] = {};
    double versed_data_[36] = {};

    Signal2DOriginal Fo = {
        6, 6,
        input_data_
    };
    Signal2DAnalyzed Fn = {
        6, 6,
        output_data_
    };
    Signal2DOriginal iFo = {
        6, 6,
        versed_data_
    };

    printf("\n Original_data: \n");
    for (int y = 0; y < Fo.GH_; ++y) {
        for (int x = 0; x < Fo.GW_; ++x) {
            printf("%f  ", Fo.Fo_[x + y * Fo.GW_]);
        }
        printf("\n");
    }

    printf("\n DFT_result: \n");
    dft_2d(&Fo, &Fn);
    for (int v = 0; v < Fn.NV_; ++v) {
        for (int u = 0; u < Fn.NU_; ++u) {
            printf("%.3f + i %.3f   ", Fn.Fn_[u + v * Fn.NU_].re_, Fn.Fn_[u + v * Fn.NU_].im_);
        }
        printf("\n");
    }

    printf("\n IDFT_result: \n");
    idft_2d(&iFo, &Fn);
    for (int y = 0; y < iFo.GH_; ++y) {
        for (int x = 0; x < iFo.GW_; ++x) {
            printf("%f  ", iFo.Fo_[x + y * Fo.GW_]);
        }
        printf("\n");
    }

    return 0;
}
