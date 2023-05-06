precision mediump float;

varying vec4 fs_position;
varying vec2 fs_texcoord;

uniform mat3 gaussian_matrix;
uniform sampler2D target_texture;

void main()
{
    vec3 output_;
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            output_ += texture2D(target_texture, fs_texcoord.xy).rgb * gaussian_matrix[i][j];
        }
    }
    gl_FragColor = vec4(output_, 1.0);
}