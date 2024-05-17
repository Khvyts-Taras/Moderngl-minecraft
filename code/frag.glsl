#version 330 core

uniform sampler2D tex;

in vec2 g_texcoord;

out vec4 f_color;

void main(){
    float depth = gl_FragCoord.z / gl_FragCoord.w;
    f_color = vec4(texture(tex, g_texcoord).xyz*(1-depth/800), 1.0);
}