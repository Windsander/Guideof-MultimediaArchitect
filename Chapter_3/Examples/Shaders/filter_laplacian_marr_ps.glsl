precision mediump float;

const int n = 3;

varying vec4 fs_position;
varying vec2 fs_texcoord;

uniform bool only_edge;
uniform vec2 pixel_bias;
uniform float marr_matrix[n * n];
uniform sampler2D target_texture;

float grey(vec3 c){
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2];
}

vec4 edge_operation()
{
    vec3 output_;
    float marr_factor = 0.0;
    float normalize_div = 0.0;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            vec2 bias = vec2(i-1, j-1) * pixel_bias;
            vec4 color_sample = texture2D(target_texture, fs_texcoord.xy + bias);
            float check_grey = grey(color_sample.rgb);
            normalize_div += check_grey;
            marr_factor += check_grey * marr_matrix[i + j * n];
        }
    }
    output_ = texture2D(target_texture, fs_texcoord.xy).rgb * (1.0 - marr_factor/normalize_div);
    return vec4(output_, 1.0);
}

void main()
{
    if (only_edge){
        gl_FragColor = edge_operation();
        return;
    }
    vec3 output_;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            vec2 bias = vec2(i-1, j-1) * pixel_bias;
            output_ += texture2D(target_texture, fs_texcoord.xy + bias).rgb * marr_matrix[i + j * n];
        }
    }
    gl_FragColor = vec4(output_, 1.0);
}
