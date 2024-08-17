from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from direct.actor.Actor import *

app = Ursina()

ground = Entity(model='plane', scale=(1000, 1, 1000), texture='grass', texture_scale=(1000, 1000), collider='box')
Sky()
player = FirstPersonController()
player.position = Vec3(1, 0, 3)
player.collider = 'box'

test_actor = Actor('assets/player/playerwalk.gltf')
test_actor.loop('classd_skeleton|classd_skeleton|classd_skeleton|classd_walk')
test_entity = Entity(model=test_actor, scale=(0.026, 0.026, 0.026), collider='box', rotation=(0, 90, 0))
test_entity.add_script(SmoothFollow(target=player, speed=0.4))

killzone = Entity(model='cube',
                  position=(3, 0, 3), 
                  scale=(1, 1, 1), 
                  texture='brick', 
                  collider='box')

soundzone = Entity(model='wireframe_cube', 
                      color=color.blue, 
                      scale=(60, 10, 60), 
                      position=(0, .6, 0))

blur_shader = Shader(language=Shader.GLSL, 
                     vertex='blur_vertex_shader.glsl', 
                     fragment='blur_fragment_shader.glsl')

# Set the blur amount
blur_amount = 0
def apply_blur_shader():
    camera.shader = blur_shader
    camera.set_shader_input('blur_amount', blur_amount)

bob_amount_vertical = 0.1  
# bob_amount_horizontal = 0.2
bob_amount_rotation = 1
bob_speed = 4.4 
bob_phase = 0  
is_moving = False
previous_position = player.position

def update():
    test_entity.look_at_2d(player, 'y')
    # ====================== Death Effect =======================
    global blur_amount
    if player.intersects(killzone).hit:
        camera.shader = blur_shader
        player.disable()
        blur_amount = 1
        apply_blur_shader()
        camera.rotation_x -= 100 * time.dt
        if camera.rotation_x < -90:
            camera.rotation_x = -90
        elif camera.rotation_x > 90:
            camera.rotation_x = 90
        camera.position.y -= 10 * time.dt
    # ===================== View Bobbing =======================
    global bob_phase, previous_position
    is_moving = player.position != previous_position

    if is_moving:
        bob_phase += bob_speed * time.dt
        player.camera_pivot.y = 1.5 + math.sin(bob_phase) * bob_amount_vertical
        # player.camera_pivot.x = math.sin(bob_phase * 2) * bob_amount_horizontal
        player.camera_pivot.rotation_z = math.sin(bob_phase) * bob_amount_rotation

    if not player.grounded:
        bob_phase = 0
        player.camera_pivot.y = 1.5  
        # player.camera_pivot.x = 0 
        player.camera_pivot.rotation_z = 0

    previous_position = player.position

app.run()