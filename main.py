import pygame
import moderngl
import numpy as np
import glm
import random

FOV = 80
NEAR = 0.01
FAR = 600
SENSITIVITY = 0.1
SPEED = 0.03
window_size = [1200, 800]
aspect_ratio = window_size[0] / window_size[1]

screen = pygame.display.set_mode(window_size, pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)
ctx = moderngl.create_context()
ctx.enable(moderngl.DEPTH_TEST | moderngl.BLEND)
ctx.blend_func = (moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA)
ctx.gc_mode = 'auto'

def load(filename):
    with open(filename+'.glsl', 'r') as file:
        return file.read()

vert_shader = load('vert')
geom_shader = load('geom')
frag_shader = load('frag')

default_program = ctx.program(vertex_shader=vert_shader, geometry_shader=geom_shader, fragment_shader=frag_shader)

texture = pygame.image.load('atlas.png')
tex = ctx.texture(size=texture.get_size(), components=3, data=pygame.image.tostring(texture, 'RGB'))
tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
tex.use(0)
default_program['tex'] = 0

positions = np.array([[x, y, z, random.randint(0, 2)] for x in range(128) for y in range(32) for z in range(128)], dtype='f4')
buffer = ctx.buffer(data=positions)
program = default_program
render_object = ctx.vertex_array(program, [(buffer, '3f 1f', 'vert', 'texture_id')])

m_proj = glm.perspective(glm.radians(FOV), aspect_ratio, NEAR, FAR)
default_program['m_proj'].write(m_proj)

up = glm.vec3(0, 1, 0)
right = glm.vec3(1, 0, 0)
forward = glm.vec3(0, 0, -1)
cam_pos = glm.vec3([0, 0, 0])
cam_yaw = 90
cam_pitch = 0
delta_time = 1

while True:
    time = pygame.time.get_ticks()
    screen.fill((0, 0, 0))
    ctx.clear(color=(0.0, 0.0, 0.0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ctx.release()
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.event.set_grab(True)
            pygame.mouse.set_visible(False)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.event.set_grab(False)
        pygame.mouse.set_visible(True)
    
    velocity = SPEED * delta_time
    if keys[pygame.K_w]:
        cam_pos += forward * velocity
    if keys[pygame.K_s]:
        cam_pos -= forward * velocity
    if keys[pygame.K_a]:
        cam_pos -= right * velocity
    if keys[pygame.K_d]:
        cam_pos += right * velocity
    if keys[pygame.K_LSHIFT]:
        cam_pos -= up * velocity
    if keys[pygame.K_SPACE]:
        cam_pos += up * velocity
    
    rel_x, rel_y = pygame.mouse.get_rel()
    cam_yaw += rel_x * SENSITIVITY
    cam_pitch -= rel_y * SENSITIVITY
    cam_pitch = max(-89, min(89, cam_pitch))
    yaw, pitch = glm.radians(cam_yaw), glm.radians(cam_pitch)
    
    forward.x = glm.cos(yaw) * glm.cos(pitch)
    forward.y = glm.sin(pitch)
    forward.z = glm.sin(yaw) * glm.cos(pitch)
    forward = glm.normalize(forward)
    right = glm.normalize(glm.cross(forward, glm.vec3(0, 1, 0)))
    
    m_view = glm.lookAt(cam_pos, cam_pos + forward, up)
    default_program['m_view'].write(m_view)
    
    render_object.render(mode=moderngl.POINTS)
    delta_time = clock.tick(60)
    pygame.display.flip()