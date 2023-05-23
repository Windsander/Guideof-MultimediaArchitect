attribute vec3 position;
attribute vec2 texcoord;

uniform float u_time;
uniform int u_type;
uniform mat4 u_wvp;
uniform vec4 u_color_major;
uniform vec4 u_color_minor;
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

vec3 auto_rotate(vec3 v, float o) {
    return rotateZ(
        rotateX(
            rotateY(v, -u_time + o * 9.35),
            -u_time * 0.4 + o * 6.4
        ),
        -u_time * 0.6 + o * 8.26
    );
}

void main() {
    fs_texcoord = texcoord;
    fs_texcolor = mix(u_color_major, u_color_minor, texcoord.x);
    fs_texcolor *= fs_texcolor.w;
    float roatate_axis =
    (u_type == 1) ? texcoord.x :
    (u_type == 2) ? texcoord.y :
    1.0;
    gl_Position = u_wvp * vec4(auto_rotate(position, roatate_axis), 1.0);
}