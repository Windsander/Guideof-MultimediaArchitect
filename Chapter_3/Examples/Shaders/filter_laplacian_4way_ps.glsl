precision mediump float;

varying vec4 fs_position;
varying vec2 fs_texcoord;

uniform bool only_edge;
uniform vec2 pixel_bias;
uniform mat3 laplacian_matrix;
uniform sampler2D target_texture;

void main()
{
    vec3 output_ = only_edge? vec3(0) : texture2D(target_texture, fs_texcoord.xy).rgb;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            vec2 bias = vec2(i-1, j-1) * pixel_bias;
            vec4 color_sample = texture2D(target_texture, fs_texcoord.xy + bias);
            output_ += color_sample.rgb * laplacian_matrix[i][j];
        }
    }
    gl_FragColor = vec4(output_, 1.0);
}