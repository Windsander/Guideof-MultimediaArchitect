/*
 * Copyright (c) 2023 Arikan.Li [Updated]
 * Created by Arikan.Li on 2014/7/12.
 * <last modified at> 2023/4/30 [commit:: encapsulated all old-coded-resources for Project_M]
 *
 * IoU & GIoU Theorem-Version
 *
 * [theorem::definitions]
 *   M_area_ meanings Original Function
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

#include <glm/ext.hpp>

#include "stdio.h"
#include "math.h"

typedef glm::vec2 Vector_2f;
typedef glm::vec3 Vector_3f;
typedef glm::vec4 Vector_4f;
typedef glm::mat2 Matrix_2x2f;
typedef glm::mat3 Matrix_3x3f;
typedef glm::mat4 Matrix_4x4f;

#define XC_PI 3.14159265358979323846
#define XC_RADIAN(d_) (XC_PI * d_ / 180.0f)
#define XC_VECTOR_NORMALIZE(v_) glm::normalize(v_)
#define XC_VECTOR_CROSS(vl_, vr_) glm::cross(vl_, vr_)
#define XC_VECTOR_DOT(vl_, vr_) glm::dot(vl_, vr_)
#define XC_MATRIX_INVERSE(m_) glm::inverse(m_)
#define XC_MATRIX_TRANSPOSE(m_) glm::transpose(m_)
#define XC_MATRIX_DOT(ml_, mr_) dot_m4x4(ml_, mr_)
#define XC_V4_M44_DOT(vl_, mr_) dot_v4_m4x4(vl_, mr_)

Vector_4f
dot_v4_m4x4(Vector_4f v4_, Matrix_4x4f m4x4_)
{
    return m4x4_[0] * v4_[0] + m4x4_[1] * v4_[1] + m4x4_[2] * v4_[2] + m4x4_[3] * v4_[3];
}

Matrix_4x4f
dot_m4x4(Matrix_4x4f ml_, Matrix_4x4f mr_)
{
    Matrix_4x4f result_;
    result_[0] = mr_[0] * ml_[0][0] + mr_[1] * ml_[0][1] + mr_[2] * ml_[0][2] + mr_[3] * ml_[0][3];
    result_[1] = mr_[0] * ml_[1][0] + mr_[1] * ml_[1][1] + mr_[2] * ml_[1][2] + mr_[3] * ml_[1][3];
    result_[2] = mr_[0] * ml_[2][0] + mr_[1] * ml_[2][1] + mr_[2] * ml_[2][2] + mr_[3] * ml_[2][3];
    result_[3] = mr_[0] * ml_[3][0] + mr_[1] * ml_[3][1] + mr_[2] * ml_[3][2] + mr_[3] * ml_[3][3];
    return result_;
}

bool static IoU_simple(
    Vector_4f anchor_box_,
    Vector_4f ground_box_,
    float threshold_ = 0.8f
) {
    float M_area_, T_area_, I_area_, U_area_;
    float IoU_mark_;
    {
        Vector_2f I_lt = {
            MAX(anchor_box_[0], ground_box_[0]),
            MAX(anchor_box_[1], ground_box_[1])
        };
        Vector_2f I_rb = {
            MIN(anchor_box_[2], ground_box_[2]),
            MIN(anchor_box_[3], ground_box_[3])
        };
        if (I_rb.x < I_lt.x || I_rb.y < I_lt.y) {
            return false;
        }
        M_area_ = MAX(ABS(anchor_box_[2] - anchor_box_[0]), 0) *
                  MAX(ABS(anchor_box_[3] - anchor_box_[1]), 0);
        T_area_ = MAX(ABS(ground_box_[2] - ground_box_[0]), 0) *
                  MAX(ABS(ground_box_[3] - ground_box_[1]), 0);
        I_area_ = MAX(ABS(I_lt.x - I_rb.x), 0) * MAX(ABS(I_lt.y - I_rb.y), 0);
        U_area_ = M_area_ + T_area_ - I_area_;
        IoU_mark_ = I_area_ / U_area_;
    }
    return (1.0 - IoU_mark_ > threshold_);
}

bool static GIoU_simple(
    Vector_4f anchor_box_,
    Vector_4f ground_box_,
    float threshold_ = 0.8f
) {
    float M_area_, T_area_, I_area_, U_area_, C_area_;
    float IoU_mark_, GIoU_mark_;
    {
        Vector_2f I_lt = {
            MAX(anchor_box_[0], ground_box_[0]),
            MAX(anchor_box_[1], ground_box_[1])
        };
        Vector_2f I_rb = {
            MIN(anchor_box_[2], ground_box_[2]),
            MIN(anchor_box_[3], ground_box_[3])
        };
        if (I_rb.x < I_lt.x || I_rb.y < I_lt.y) {
            return false;
        }
        M_area_ = MAX(ABS(anchor_box_[2] - anchor_box_[0]), 0) *
                  MAX(ABS(anchor_box_[3] - anchor_box_[1]), 0);
        T_area_ = MAX(ABS(ground_box_[2] - ground_box_[0]), 0) *
                  MAX(ABS(ground_box_[3] - ground_box_[1]), 0);
        I_area_ = MAX(ABS(I_lt.x - I_rb.x), 0) * MAX(ABS(I_lt.y - I_rb.y), 0);
        U_area_ = M_area_ + T_area_ - I_area_;
        IoU_mark_ = I_area_ / U_area_;
    }
    {
        Vector_2f C_lt = {
            MIN(anchor_box_[0], ground_box_[0]),
            MIN(anchor_box_[1], ground_box_[1])
        };
        Vector_2f C_rb = {
            MAX(anchor_box_[2], ground_box_[2]),
            MAX(anchor_box_[3], ground_box_[3])
        };
        if (C_rb.x < C_lt.x || C_rb.y < C_lt.y) {
            return false;
        }
        C_area_ = MAX(ABS(C_lt.x - C_rb.x), 0) * MAX(ABS(C_lt.y - C_rb.y), 0);
        GIoU_mark_ = IoU_mark_ - (C_area_ - U_area_) / C_area_;
    }
    return ((1.0 - GIoU_mark_) * 0.5f > threshold_);
}

bool static simple_cover_check(
    Matrix_4x4f marked_matrix_,
    Matrix_4x4f target_matrix_,
    Matrix_4x4f observer_matrix_,
    bool enable_GIoU_mode = false
) {
    Matrix_4x4f marked_converter_matrix = observer_matrix_ * marked_matrix_;
    Matrix_4x4f target_converter_matrix = observer_matrix_ * target_matrix_;

    std::initializer_list <Vector_4f> marked_pt_list_ = {
        XC_V4_M44_DOT(OBJ_SPACE_CUBE[0], marked_converter_matrix),
        XC_V4_M44_DOT(OBJ_SPACE_CUBE[1], marked_converter_matrix),
        XC_V4_M44_DOT(OBJ_SPACE_CUBE[2], marked_converter_matrix),
        XC_V4_M44_DOT(OBJ_SPACE_CUBE[3], marked_converter_matrix),
        XC_V4_M44_DOT(OBJ_SPACE_CUBE[4], marked_converter_matrix),
        XC_V4_M44_DOT(OBJ_SPACE_CUBE[5], marked_converter_matrix),
        XC_V4_M44_DOT(OBJ_SPACE_CUBE[6], marked_converter_matrix),
        XC_V4_M44_DOT(OBJ_SPACE_CUBE[7], marked_converter_matrix),
    };
    std::initializer_list <Vector_4f> covers_pt_list_ = {
        XC_V4_M44_DOT(OBJ_SPACE_CUBE[0], target_converter_matrix),
        XC_V4_M44_DOT(OBJ_SPACE_CUBE[1], target_converter_matrix),
        XC_V4_M44_DOT(OBJ_SPACE_CUBE[2], target_converter_matrix),
        XC_V4_M44_DOT(OBJ_SPACE_CUBE[3], target_converter_matrix),
        XC_V4_M44_DOT(OBJ_SPACE_CUBE[4], target_converter_matrix),
        XC_V4_M44_DOT(OBJ_SPACE_CUBE[5], target_converter_matrix),
        XC_V4_M44_DOT(OBJ_SPACE_CUBE[6], target_converter_matrix),
        XC_V4_M44_DOT(OBJ_SPACE_CUBE[7], target_converter_matrix),
    };

    Vector_4f marked_plane_range = {
        min(marked_pt_list_, [](Vector_4f l, Vector_4f r) -> bool { return l.x < r.x; }).x,
        min(marked_pt_list_, [](Vector_4f l, Vector_4f r) -> bool { return l.y < r.y; }).y,
        max(marked_pt_list_, [](Vector_4f l, Vector_4f r) -> bool { return l.x < r.x; }).x,
        max(marked_pt_list_, [](Vector_4f l, Vector_4f r) -> bool { return l.y < r.y; }).y,
    };

    Vector_4f target_plane_range = {
        min(covers_pt_list_, [](Vector_4f l, Vector_4f r) -> bool { return l.x < r.x; }).x,
        min(covers_pt_list_, [](Vector_4f l, Vector_4f r) -> bool { return l.y < r.y; }).y,
        max(covers_pt_list_, [](Vector_4f l, Vector_4f r) -> bool { return l.x < r.x; }).x,
        max(covers_pt_list_, [](Vector_4f l, Vector_4f r) -> bool { return l.y < r.y; }).y,
    };

    return  enable_GIoU_mode?
            GIoU_simple(marked_plane_range, target_plane_range, 0.08f):
            IoU_simple(marked_plane_range, target_plane_range, 0.08f);
}

int main(void) {
    return 0;
}