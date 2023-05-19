precision mediump float;

varying vec4 fs_position;
varying vec2 fs_texcoord;

uniform bool only_edge;
uniform vec2 pixel_bias;
uniform mat3 sobel_matrix_x;
uniform mat3 sobel_matrix_y;
uniform sampler2D target_texture;

void main()
{
    vec3 output_ = only_edge? vec3(0) : texture2D(target_texture, fs_texcoord.xy).rgb;
    vec3 color_center_x;
    vec3 color_center_y;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            vec2 bias = vec2(i-1, j-1) * pixel_bias;
            vec4 color_sample = texture2D(target_texture, fs_texcoord.xy + bias);
            color_center_x += color_sample.rgb * sobel_matrix_x[i][j];
            color_center_y += color_sample.rgb * sobel_matrix_y[i][j];
        }
    }
    output_ += vec3(
        length(vec2(color_center_x.r, color_center_y.r)),
        length(vec2(color_center_x.g, color_center_y.g)),
        length(vec2(color_center_x.b, color_center_y.b))
    );
    gl_FragColor = vec4(output_, 1.0);
}
