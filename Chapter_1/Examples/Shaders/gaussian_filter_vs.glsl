#include "common_header.glsl"

VertexInput();
VertexOutput();

uniform mat4 textures_matrix;
uniform mat4 position_matrix;

void main()
{
    vec4 temp_pos = vec4(position.x, position.y, position.z, 1.0);
    vec4 temp_tex = vec4(texcoord.x, texcoord.y, texcoord.z, 1.0);

    fs_position = position_matrix * temp_pos;
    fs_texcoord = textures_matrix * temp_tex;
    fs_texcolor = texcolor;

    gl_Position = fs_position;
}