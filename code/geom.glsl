#version 330 core
layout(points) in;
layout(triangle_strip, max_vertices = 36) out;

uniform mat4 m_proj;
uniform mat4 m_view;

in vec3 v_vert[];
in float v_texture_id[];

out vec2 g_texcoord;

const vec3[8] cube_vertices = vec3[8](
    vec3(0, 0, 0),
    vec3(1, 0, 0),
    vec3(1, 1, 0),
    vec3(0, 1, 0),
    vec3(0, 0, 1),
    vec3(1, 0, 1),
    vec3(1, 1, 1),
    vec3(0, 1, 1)
);

const int[36] cube_indices = int[36](
    0, 1, 2, 2, 3, 0,
    4, 5, 6, 6, 7, 4,
    0, 1, 5, 5, 4, 0,
    2, 3, 7, 7, 6, 2,
    0, 3, 7, 7, 4, 0,
    1, 2, 6, 6, 5, 1
);

const float n_textures = 3;

void main() {
    float texture_id = v_texture_id[0];
    vec2 tex_coords[6] = vec2[6](
        vec2((0.0+texture_id)/n_textures, 0.0),
        vec2((1.0+texture_id)/n_textures, 0.0),
        vec2((1.0+texture_id)/n_textures, 1.0),
        vec2((1.0+texture_id)/n_textures, 1.0),
        vec2((0.0+texture_id)/n_textures, 1.0),
        vec2((0.0+texture_id)/n_textures, 0.0)
    );

    for (int i = 0; i < 36; i++) {
        g_texcoord = tex_coords[i % 6];
        vec3 g_vert = v_vert[0] + cube_vertices[cube_indices[i]];
        gl_Position = m_proj * m_view * vec4(g_vert, 1.0);
        EmitVertex();
        if (i % 3 == 2) {
            EndPrimitive();
        }
    }
}