precision mediump float;

varying vec4 fs_position;
varying vec2 fs_texcoord;

uniform vec2 pixel_bias;
uniform mat3 laplacian_matrix;
uniform sampler2D target_texture;

void main()
{
    vec3 output_;
    output_ += texture2D(target_texture, fs_texcoord.xy).rgb * (1.0 + laplacian_matrix[1][1]);
    output_ += texture2D(target_texture, fs_texcoord.xy + vec2(-1, -1) * pixel_bias).rgb * laplacian_matrix[0][0];
    output_ += texture2D(target_texture, fs_texcoord.xy + vec2(-1, +1) * pixel_bias).rgb * laplacian_matrix[2][0];
    output_ += texture2D(target_texture, fs_texcoord.xy + vec2(+1, -1) * pixel_bias).rgb * laplacian_matrix[0][2];
    output_ += texture2D(target_texture, fs_texcoord.xy + vec2(+1, +1) * pixel_bias).rgb * laplacian_matrix[2][2];
    gl_FragColor = vec4(output_, 1.0);
}
