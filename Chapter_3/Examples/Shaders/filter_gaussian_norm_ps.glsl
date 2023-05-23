precision mediump float;

const int n = 3;

varying vec4 fs_position;
varying vec2 fs_texcoord;

uniform vec2 pixel_bias;
uniform float gaussian_matrix[n * n];
uniform sampler2D target_texture;

void main()
{
    vec3 output_;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            vec2 bias = vec2(i-1, j-1) * pixel_bias;
            output_ += texture2D(target_texture, fs_texcoord.xy + bias).rgb * gaussian_matrix[i + j * n];
        }
    }
    gl_FragColor = vec4(output_, 1.0);
}