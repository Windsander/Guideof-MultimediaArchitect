precision mediump float;

varying vec4 fs_position;
varying vec2 fs_texcoord;

uniform vec2 pixel_bias;
uniform mat3 gaussian_matrix;
uniform float gaussian_range;
uniform sampler2D target_texture;

float variance(vec3 c1, vec3 c2){
    vec3 temp = c2 - c1;
    return temp[0] * temp[0] + temp[1] * temp[1] + temp[2] * temp[2];
}

void main()
{
    vec4 color_center = texture2D(target_texture, fs_texcoord.xy);
    float gauss_factor = gaussian_matrix[0][0]+gaussian_matrix[0][1];
    vec3 output_ = texture2D(target_texture, fs_texcoord.xy ).rgb * gaussian_matrix[1][1];
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            vec2 bias = vec2(1-2*i, 1-2*j) * pixel_bias;
            vec4 color_sample = texture2D(target_texture, fs_texcoord.xy + bias);
            float grey_variance = variance(color_center.rgb, color_sample.rgb) / (2.0 * gaussian_range * gaussian_range);
            float range_weight = exp(-grey_variance);
            output_ += color_sample.rgb * gauss_factor * range_weight;
        }
    }
    gl_FragColor = vec4(output_, 1.0);
}