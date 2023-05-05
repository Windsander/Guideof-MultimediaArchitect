attribute vec3 position;
attribute vec2 texcoord;

uniform float u_time;
uniform vec4 u_color_major;
uniform vec4 u_color_minor;
uniform mat4 u_wvp;
varying vec4 fs_texcolor;
varying vec2 fs_texcoord;

vec3 rotateX(vec3 v, float angle) {
    float s = sin(angle);
    float c = cos(angle);
    return vec3(v.x, c * v.y + s * v.z, -s * v.y + c * v.z);
}

vec3 rotateY(vec3 v, float angle) {
    float s = sin(angle);
    float c = cos(angle);
    return vec3(c * v.x + s * v.z, v.y, -s * v.x + c * v.z);
}

vec3 rotateZ(vec3 v, float angle) {
    float s = sin(angle);
    float c = cos(angle);
    return vec3(c * v.x + s * v.y, -s * v.x + c * v.y, v.z);
}

vec3 auto_rotate(vec3 v,vec2 tc) {
    return rotateZ(
        rotateX(
            rotateY(v, -u_time + tc.x * 6.1),
            -u_time * 0.6 + tc.x * 8.1
        ),
        -u_time * 0.7 + tc.x * 7.12
    );
}

void main(void) {
    fs_texcoord = texcoord;
    fs_texcolor = mix(u_color_major, u_color_minor, texcoord.x);
    fs_texcolor *= fs_texcolor.w;
    vec3 pos = auto_rotate(position, texcoord);
    gl_Position = u_wvp * vec4(pos, 1.0);
}