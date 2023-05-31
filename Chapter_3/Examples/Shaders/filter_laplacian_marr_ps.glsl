precision mediump float;

const int n = 3;
const int m = 5;

varying vec4 fs_position;
varying vec2 fs_texcoord;

uniform bool only_edge;
uniform bool marr_blur;
uniform vec2 pixel_bias;
uniform float gaussian_matrix[n * n];
uniform float marr_matrix[m * m];
uniform float marr_factor;
uniform sampler2D target_texture;

float grey(vec3 c){
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2];
}

vec3 gauss_operation()
{
    vec3 output_;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            vec2 bias = vec2(i-1, j-1) * pixel_bias;
            output_ += texture2D(target_texture, fs_texcoord.xy + bias).rgb * gaussian_matrix[i + j * n];
        }
    }
    return texture2D(target_texture, fs_texcoord.xy).rgb;
}

vec3 edge_operation()
{
    vec3 output_;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) {
            vec2 bias = vec2(i-1, j-1) * pixel_bias;
            vec4 color_sample = texture2D(target_texture, fs_texcoord.xy + bias);
            float check_grey = grey(color_sample.rgb);
            output_ += color_sample.rgb * marr_matrix[i + j * m];
        }
    }
    return output_;
}

void main()
{
    vec3 output_;
    if (only_edge) {
        output_ = edge_operation();
    } else if (marr_blur) {
        output_ = gauss_operation() - marr_factor * edge_operation();
    } else {
        output_ = texture2D(target_texture, fs_texcoord.xy).rgb - marr_factor * edge_operation();
    }
    gl_FragColor = vec4(output_, 1.0);
}
