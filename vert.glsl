#version 330 core

uniform mat4 m_proj;
uniform mat4 m_view;

in vec3 vert;
in float texture_id;

out vec3 v_vert;
out float v_texture_id;

void main(){
    v_vert = vert;
    v_texture_id = texture_id;
    gl_Position = vec4(vert, 1.0);
}