precision mediump float;

varying vec4 fs_position;
varying vec2 fs_texcoord;

uniform vec2 pixel_bias;
uniform mat3 gaussian_matrix;
uniform sampler2D target_texture;

void main()
{
    float gauss_factor = gaussian_matrix[0][0]+gaussian_matrix[0][1];
    vec3 output_;
    output_ += texture2D(target_texture, fs_texcoord.xy ).rgb * gaussian_matrix[1][1];
    output_ += texture2D(target_texture, fs_texcoord.xy + vec2(-1, -1) * pixel_bias).rgb * gauss_factor;
    output_ += texture2D(target_texture, fs_texcoord.xy + vec2(-1, +1) * pixel_bias).rgb * gauss_factor;
    output_ += texture2D(target_texture, fs_texcoord.xy + vec2(+1, -1) * pixel_bias).rgb * gauss_factor;
    output_ += texture2D(target_texture, fs_texcoord.xy + vec2(+1, +1) * pixel_bias).rgb * gauss_factor;
    gl_FragColor = vec4(output_, 1.0);
}
