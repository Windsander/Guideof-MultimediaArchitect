#ifndef _COMMON__GLSL__
#define _COMMON__GLSL__

precision highp float;

#ifndef _VERSION__IO__
#define _VERSION__IO__
#if __VERSION__ >= 330
    #define VS_IN(x) layout(location = x) in
    #define VS_OUT out
    #define PS_IN in
#elif __VERSION__ >= 140
    #define VS_IN(x) in
    #define VS_OUT out
    #define PS_IN in
#else
    #define VS_IN(x) attribute
    #define VS_OUT varying
    #define PS_IN varying
#endif
#endif /* _VERSION__IO__ */

#define VertexInput()       \
VS_IN(0) vec3 position;     \
VS_IN(1) vec3 texcoord;     \
VS_IN(2) vec4 texcolor

#define VertexOutput()      \
VS_OUT vec4 fs_position;    \
VS_OUT vec4 fs_texcoord;    \
VS_OUT vec4 fs_texcolor

#define PixelInput()        \
PS_IN vec4 fs_position;     \
PS_IN vec4 fs_texcoord;     \
PS_IN vec4 fs_texcolor

#endif /* _COMMON__GLSL__ */
