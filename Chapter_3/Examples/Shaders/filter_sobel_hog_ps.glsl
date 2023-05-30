precision mediump float;

const float PI = 3.1415927;

const float ARROW_TILE_SIZE       = 16.0;  //pixels
const float ARROW_HEAD_ANGLE      = 45.0 * PI / 180.0;
const float ARROW_HEAD_LENGTH     = ARROW_TILE_SIZE / 6.0;
const float ARROW_SHAFT_THICKNESS = 3.0;
const float ARROW_SHAFT_HEAD_RATE = 16.0;
const vec3  ARROW_COLOR           = vec3(1.0, 1.0, 0.0);

varying vec4 fs_position;
varying vec2 fs_texcoord;

uniform bool only_edge;
uniform vec2 pixel_bias;
uniform mat3 sobel_matrix_x;
uniform mat3 sobel_matrix_y;
uniform sampler2D target_texture;

float grey(vec3 c)
{
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2];
}

/* Calucate Sobel Field at target center */
vec3 sobel_edge_detection(vec2 target_coord) {
    // Sobel HOG
    float gradient_center_x;
    float gradient_center_y;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            vec2 bias = vec2(i-1, j-1) * pixel_bias;
            vec4 color_sample = texture2D(target_texture, target_coord.xy + bias);
            float check_grey = grey(color_sample.rgb);
            gradient_center_x += check_grey * sobel_matrix_x[i][j];
            gradient_center_y += check_grey * sobel_matrix_y[i][j];
        }
    }
    // float orientate(in Angle mode) = atan2(gradient_center_y, gradient_center_x);
    vec2  orientate = vec2(gradient_center_x, gradient_center_y);
    float magnitude = length(orientate);
    return vec3(gradient_center_x, gradient_center_y, magnitude);
}

/* Calucate HOG Orient-Arrow Density (pixel by pixel) */
float arrow_density(vec2 target_coord) {
    vec2 ori_pos = target_coord.xy / pixel_bias;
    vec2 tile_center = (floor(ori_pos / ARROW_TILE_SIZE) + 0.5) * ARROW_TILE_SIZE;
    vec3 field_vector = sobel_edge_detection(tile_center * pixel_bias);
    float magnitude = field_vector.z;
    if (magnitude > 0.0) {
        float distance = clamp(magnitude * ARROW_TILE_SIZE, 5.0, ARROW_TILE_SIZE / 2.0);
        vec2 normalizer = vec2(field_vector.x, field_vector.y) / magnitude;
        vec2 tile_offset = ori_pos - tile_center;
        vec2 tile_orient = normalizer * distance;
        float density = max(
            // Shaft
            ARROW_SHAFT_THICKNESS / ARROW_SHAFT_HEAD_RATE - max(
                abs(dot(tile_offset, vec2(+normalizer.y, -normalizer.x))),                                         // Width
                abs(dot(tile_offset, vec2(+normalizer.x, +normalizer.y))) - distance + ARROW_HEAD_LENGTH / 2.0    // Length
            ),
            // Arrow head
            (
                min(0.0, dot(tile_orient - tile_offset, normalizer) - cos(ARROW_HEAD_ANGLE / 2.0) * length(tile_orient - tile_offset)) * 2.0 +
                min(0.0, dot(tile_offset, normalizer) + ARROW_HEAD_LENGTH - distance)
            )
        );
        return clamp(1.0 + density, 0.0, 1.0);
    }

    return 0.0;
}

void main()
{
    vec3 output_ = only_edge? vec3(0) : texture2D(target_texture, fs_texcoord.xy).rgb;
    vec3 arrows_ = arrow_density(fs_texcoord.xy) * ARROW_COLOR;
    gl_FragColor = vec4(output_ + arrows_, 1.0);
}
