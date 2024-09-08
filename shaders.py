from ursina import *
import config

app = config.app_global

blur_shader = Shader(language=Shader.GLSL,
                     vertex='blur_vertex_shader.glsl',
                     fragment='blur_fragment_shader.glsl')

blur_amount = 90

def apply_blur_shader():
    camera.shader = blur_shader
    camera.set_shader_input('blur_amount', blur_amount)

def remove_blur_shader():
    camera.shader = None 
