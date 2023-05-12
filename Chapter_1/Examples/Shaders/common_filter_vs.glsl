
attribute vec3 position;
// attribute vec2 texcoord; // for fullscreen, can constantly calculated

varying vec4 fs_position;
varying vec2 fs_texcoord;

void main()
{
    fs_position = vec4(position.x, position.y, position.z, 1.0);
    //    fs_texcoord = vec4(texcoord.x, texcoord.y, 0.0, 1.0);
    fs_texcoord = (position.xy + vec2(1.0, 1.0)) / 2.0;
    gl_Position = fs_position;
}