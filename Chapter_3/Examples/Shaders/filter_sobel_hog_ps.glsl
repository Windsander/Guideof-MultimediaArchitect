precision mediump float;

const float PI = 3.1415927;

const int n = 8;
const int N = 2;
const int SIZE_CV = (n + 1);
const int SIZE_BV = /*N * N **/ SIZE_CV; // for orientation weight sum

const float ANGLE_GAP = 20.0 * PI / 180.0;
const vec3 ANGLE_0   = vec3(cos(ANGLE_GAP * 0.0), sin(ANGLE_GAP * 0.0), 100);
const vec3 ANGLE_20  = vec3(cos(ANGLE_GAP * 1.0), sin(ANGLE_GAP * 1.0), 2.74747742);
const vec3 ANGLE_40  = vec3(cos(ANGLE_GAP * 2.0), sin(ANGLE_GAP * 2.0), 1.19175359);
const vec3 ANGLE_60  = vec3(cos(ANGLE_GAP * 3.0), sin(ANGLE_GAP * 3.0), 0.57735027);
const vec3 ANGLE_80  = vec3(cos(ANGLE_GAP * 4.0), sin(ANGLE_GAP * 4.0), 0.17632698);
const vec3 ANGLE_100 = vec3(cos(ANGLE_GAP * 5.0), sin(ANGLE_GAP * 5.0), -0.17632698);
const vec3 ANGLE_120 = vec3(cos(ANGLE_GAP * 6.0), sin(ANGLE_GAP * 6.0), -0.57735027);
const vec3 ANGLE_140 = vec3(cos(ANGLE_GAP * 7.0), sin(ANGLE_GAP * 7.0), -1.19175359);
const vec3 ANGLE_160 = vec3(cos(ANGLE_GAP * 8.0), sin(ANGLE_GAP * 8.0), -2.74747742);
const vec3 ANGLE_180 = vec3(cos(ANGLE_GAP * 9.0), sin(ANGLE_GAP * 9.0), -100);

const float CELL_TILE_SIZE      = 8.0;  //pixels
const float BLOCK_TILE_SIZE     = 2.0;   //cells

const float HOG_TILE_SIZE       = 16.0;  //pixels(n*N)
const float HOG_SHAFT_LENGTH    = 14.0;
const float HOG_SHAFT_THICKNESS = 0.5;
const float HOG_SHAFT_HEAD_RATE = 64.0;
const vec3  HOG_COLOR           = vec3(1.0, 1.0, 0.0);
const float HOG_MIN_MAGNITUDE   = 0.1;

varying vec4 fs_position;
varying vec2 fs_texcoord;

uniform bool only_edge;
uniform vec2 pixel_bias;
uniform mat3 sobel_matrix_x;
uniform mat3 sobel_matrix_y;
uniform float hog_magnitude_limit;
uniform sampler2D target_texture;

/* Simple Grey */
float grey(vec3 c)
{
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2];
}

/* Calucate HOG Orient-hog Density (pixel by pixel) */
float hog_density(vec2 target_coord, vec3 field_vector) {
    vec2 ori_pos = target_coord.xy / pixel_bias;
    vec2 tile_center = (floor(ori_pos / HOG_TILE_SIZE) + 0.5) * HOG_TILE_SIZE;
    float magnitude = abs(field_vector.z);
    if (magnitude > max(HOG_MIN_MAGNITUDE, hog_magnitude_limit)) {
        float distance = clamp(magnitude * HOG_SHAFT_LENGTH, 0.1, HOG_SHAFT_LENGTH);
        vec2 normalizer = normalize(field_vector.xy);
        vec2 tile_offset = ori_pos - tile_center;
        float density = HOG_SHAFT_THICKNESS / HOG_SHAFT_HEAD_RATE - max(
        abs(dot(tile_offset, vec2(+normalizer.y, -normalizer.x))),
        abs(dot(tile_offset, vec2(+normalizer.x, +normalizer.y))) - distance
        );
        return clamp(1.0 + density, 0.0, 1.0);
    }
    return 0.0;
}

/* Calucate Sobel Field at target center */
vec3 sobel_edge_detection(vec2 target_coord) {
    float gradient_center_x;
    float gradient_center_y;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            vec2 bias = vec2(i-1, j-1) * pixel_bias;
            vec4 color_sample = texture2D(target_texture, fs_texcoord.xy + bias);
            float check_grey = grey(color_sample.rgb);
            gradient_center_x += check_grey * sobel_matrix_x[i][j];
            gradient_center_y += check_grey * sobel_matrix_y[i][j];
        }
    }
    // float rectangle = (atan(gradient_center_y, gradient_center_x) + 2.0 * PI) / (PI);
    vec2  orientate = vec2(gradient_center_x, gradient_center_y);
    float magnitude = length(orientate);
    return vec3(orientate, magnitude);
}

/* Calucate Cell Feature at target center */
mat3 cell_feature_extraction(vec2 target_coord) {
    mat3  result;
    float bias_unit = float(n-1)/2.0;
    vec2 ori_pos = target_coord.xy / pixel_bias;
    vec2 cell_center = (floor(ori_pos / CELL_TILE_SIZE) + 0.5) * CELL_TILE_SIZE;

    float normalization_factor = 0.0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            vec2 bias = vec2(float(i)-bias_unit, float(j)-bias_unit) * pixel_bias;
            vec3 field_vector = sobel_edge_detection(cell_center.xy + bias);
            float seek_to =  (field_vector.x+ 0.0001)  / (field_vector.y + 0.0001) ;
            float wight = 0.0;
            float wight_as = 0.0;
            {
                wight = field_vector[2] * wight_as;
                if (ANGLE_0.z>= seek_to && seek_to >= ANGLE_20.z){
                    wight_as = abs((seek_to - ANGLE_0.z)/(ANGLE_20.z - ANGLE_0.z));
                    result[0][0] += field_vector[2] *wight_as;
                    result[0][1] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_20.z>= seek_to && seek_to >= ANGLE_40.z){
                    wight_as = abs((seek_to - ANGLE_20.z)/(ANGLE_40.z - ANGLE_20.z));
                    result[0][1] += field_vector[2] * wight_as;
                    result[0][2] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_40.z>= seek_to && seek_to >= ANGLE_60.z){
                    wight_as = abs((seek_to - ANGLE_40.z)/(ANGLE_60.z - ANGLE_40.z));
                    result[0][2] += field_vector[2] * wight_as;
                    result[1][0] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_60.z>= seek_to && seek_to >= ANGLE_80.z){
                    wight_as = abs((seek_to - ANGLE_60.z)/(ANGLE_80.z - ANGLE_60.z));
                    result[1][0] += field_vector[2] * wight_as;
                    result[1][1] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_80.z>= seek_to && seek_to >= ANGLE_100.z){
                    wight_as = abs((seek_to - ANGLE_80.z)/(ANGLE_100.z - ANGLE_80.z));
                    result[1][1] += field_vector[2] * wight_as;
                    result[1][2] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_100.z>= seek_to && seek_to >= ANGLE_120.z){
                    wight_as = abs((seek_to - ANGLE_100.z)/(ANGLE_120.z - ANGLE_100.z));
                    result[1][2] += field_vector[2] * wight_as;
                    result[2][0] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_120.z>= seek_to && seek_to >= ANGLE_140.z){
                    wight_as = abs((seek_to - ANGLE_120.z)/(ANGLE_140.z - ANGLE_120.z));
                    result[2][0] += field_vector[2] * wight_as;
                    result[2][1] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_140.z>= seek_to && seek_to >= ANGLE_160.z){
                    wight_as = abs((seek_to - ANGLE_140.z)/(ANGLE_160.z - ANGLE_140.z));
                    result[2][1] += field_vector[2] * wight_as;
                    result[2][2] += field_vector[2] * (1.0 - wight_as);
                } else if (ANGLE_160.z>= seek_to && seek_to >= ANGLE_180.z){
                    wight_as = abs((seek_to - ANGLE_160.z)/(ANGLE_180.z - ANGLE_160.z));
                    result[2][2] += field_vector[2] * wight_as;
                    result[0][0] += field_vector[2] * (1.0 - wight_as);
                }
            }
        }
    }
    return result;
}

/* Calucate Block Feature at target center */
float block_feature_extraction(vec2 target_coord) {
    float orient_hog_density = 0.0;
    float block_feature_vector[SIZE_BV];

    vec2 cell_bias = vec2(n, n) * pixel_bias;
    mat3 cell_lt = cell_feature_extraction(target_coord);
    mat3 cell_rt = cell_feature_extraction(target_coord + vec2(cell_bias.x, 0.0));
    mat3 cell_lb = cell_feature_extraction(target_coord + vec2(0.0, cell_bias.y));
    mat3 cell_rb = cell_feature_extraction(target_coord + cell_bias);

    float normalization_factor = 0.0;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            normalization_factor += cell_lt[i][j] + cell_rt[i][j] + cell_lb[i][j] + cell_rb[i][j];
            block_feature_vector[i*3+j] = cell_lt[i][j] + cell_rt[i][j] + cell_lb[i][j] + cell_rb[i][j];
            // block_feature_vector[i*3+j+SIZE_CV*0] = cell_lt[i][j];
            // block_feature_vector[i*3+j+SIZE_CV*1] = cell_rt[i][j];
            // block_feature_vector[i*3+j+SIZE_CV*2] = cell_lb[i][j];
            // block_feature_vector[i*3+j+SIZE_CV*3] = cell_rb[i][j];
        }
    }
    for (int i = 0; i < SIZE_BV; i++) {
        // block_feature_vector[i] = block_feature_vector[i] / normalization_factor;
        vec3 field_vector;
        int at = int(mod(float(i) , 9.0));
        float weight = block_feature_vector[i] / normalization_factor;
        if (at == 0){
            field_vector = vec3(ANGLE_0.xy, weight);
        } else if (at == 1){
            field_vector = vec3(ANGLE_20.xy, weight);
        } else if (at == 2){
            field_vector = vec3(ANGLE_40.xy, weight);
        } else if (at == 3){
            field_vector = vec3(ANGLE_60.xy, weight);
        } else if (at == 4){
            field_vector = vec3(ANGLE_80.xy, weight);
        } else if (at == 5){
            field_vector = vec3(ANGLE_100.xy, weight);
        } else if (at == 6){
            field_vector = vec3(ANGLE_120.xy, weight);
        } else if (at == 7){
            field_vector = vec3(ANGLE_140.xy, weight);
        } else if (at == 8){
            field_vector = vec3(ANGLE_160.xy, weight);
        }
        orient_hog_density += hog_density(target_coord, field_vector);
    }
    return orient_hog_density;
}

void main()
{
    vec3 output_ = only_edge? vec3(0) : texture2D(target_texture, fs_texcoord.xy).rgb;
    float orient_hog_density = block_feature_extraction(fs_texcoord.xy);
    vec3 hogs_ = orient_hog_density * HOG_COLOR;
    gl_FragColor = vec4(output_ + hogs_, 1.0);
}
