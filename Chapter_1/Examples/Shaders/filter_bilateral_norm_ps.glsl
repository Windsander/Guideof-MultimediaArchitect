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
    float total_range_weight = 0.0;
    vec3 output_;
    vec4 color_center = texture2D(target_texture, fs_texcoord.xy);
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            vec2 bias = vec2(i-1, j-1) * pixel_bias;
            vec4 color_sample = texture2D(target_texture, fs_texcoord.xy + bias);
            float grey_variance = variance(color_center.rgb, color_sample.rgb) / (2.0 * gaussian_range * gaussian_range);
            float range_weight = exp(-grey_variance);
            total_range_weight += range_weight;
            output_ += color_sample.rgb  * range_weight;
        }
    }
    gl_FragColor = vec4(output_, 1.0) / total_range_weight;
}