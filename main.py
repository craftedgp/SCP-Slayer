from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import time
from direct.actor.Actor import Actor

app = Ursina(fullscreen=False, borderless=True, vsync=True)

# ==================== Map and player ==========================================
ground = Entity(model='plane', scale=(1000, 1, 1000), texture='grass', texture_scale=(1000, 1000), collider='box')
Sky(texture='assets/sky.jpg')

def spawn():
    global player_health
    player_health = 100
    Audio(player_spawn_sfx, loop=False, autoplay=True)

class SprintFirstPersonController(FirstPersonController):
    FirstPersonController()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.normal_speed = self.speed
        self.sprint_speed = 10

    def update(self):
        super().update()
        self.speed = self.sprint_speed if held_keys['shift'] else self.normal_speed

player = SprintFirstPersonController()
player.position = Vec3(50, 0, 0)
player.collider = 'box'
player_death_sfx = 'assets/player/death2.ogg'
player_spawn_sfx = 'assets/player/spawn.ogg'
player_health = 100
invoke(spawn)

def death():
    if not player_death_sfx in played_sounds:
        death = Audio(player_death_sfx, loop=False, autoplay=True)
        death.play()
        played_sounds.add(player_death_sfx)
        camera.shader = blur_shader
        player.disable()
        camera.rotation_x -= 100 * time.dt
        if camera.rotation_x < -90:
            camera.rotation_x = -90
        elif camera.rotation_x > 90:
            camera.rotation_x = 90
        camera.position.y -= 10 * time.dt
# =================== footstep Mechanics ============================
footstep_sounds = [f'assets/steps/Step{i}.ogg' for i in range(1, 8)]
footstep_interval = 0.9
last_footstep_time = 0
last_position = player.position
# ================== SCP 096 mechanics ===================
follower = Entity(model='cube', color=color.clear, scale=(.5, .5, .5), position=(0, .6, 0), collider='box')
trigger = 'assets/096/Triggered.ogg'
angered = 'assets/096/096Angered.ogg'
hella_angry = 'assets/096/096Rage.ogg'
broiscomming = 'assets/096/096Chase.ogg'
calm_down = 'assets/096/096calmdown.ogg'
broischill_ambience = Audio('assets/096/096.ogg', loop=True, autoplay=True)
kill = 'assets/player/death.ogg'
# ------- Sit animation --------
anim_sit = Actor('assets/096/anim_sit.gltf')
anim_sit.reparent_to(follower)
anim_sit.loop('scp096_skeleton|scp096_skeleton|scp096_sit')
# ------- After seeing his face ----

def seen():
    global hella_angry2
    Audio(trigger, loop=False, autoplay=True)
    played_sounds.add(trigger)
    broischill_ambience.stop()
    anim_sit.cleanup()
    anim_sit.removeNode()

def seen2():
    Audio(angered, loop=False, autoplay=True)
    played_sounds.add(angered)
    global anim_rage
    anim_rage = Actor('assets/096/anim_rage.gltf')
    anim_rage.reparent_to(follower)
    anim_rage.loop('scp096_skeleton|scp096_skeleton|scp096_panic')

def seen3():
    global hella_angry2
    global broiscomming2
    hella_angry2 = Audio(hella_angry, loop=True, autoplay=True)
    played_sounds.add(hella_angry)
    broiscomming2 = Audio(broiscomming, loop=True, autoplay=True)
    played_sounds.add(broiscomming)
    global anim_run
    anim_rage.cleanup()
    anim_rage.removeNode()
    anim_run = Actor('assets/096/anim_run.gltf')
    anim_run.reparent_to(follower)
    anim_run.loop('scp096_skeleton|scp096_skeleton|scp096_run')
    follower.add_script(SmoothFollow(target=player, speed=0.4))
    follower.look_at_2d(player, 'y')


kill_area = Entity(model='wireframe_cube',
                   color=color.green, 
                   scale=(4, 7, 4), 
                   position=(0, .6, 0), 
                   parent=follower,
                   collider='box')

trigger_area = Entity(model='wireframe_cube', 
                      color=color.blue, 
                      scale=(60, 10, 60), 
                      position=(0, .6, 0),
                      parent=follower)

# ============= Played Sounds shall not be played again =============
played_sounds = set()
played_sounds2 = False
# ========================= Blur mechanics ==========================
blur_shader = Shader(fragment=open('blur_shader.glsl').read(), default_input={'resolution': Vec2(window.size)})
# =================== View Bobbing mechanics ========================
bob_amount_vertical = 0.1  
# bob_amount_horizontal = 0.2
bob_amount_rotation = 1
bob_speed = 4.4
bob_phase = 0  
is_moving = False
previous_position = player.position
# =================== Update and some other functions================
def update():
    # --------- Footstep updates ---------
    global last_footstep_time, last_position, direction_to_follower

    if player.grounded:
        movement = distance(player.position, last_position)
        if movement > 0.01:
            current_time = time.time()
            if current_time - last_footstep_time > footstep_interval:
                footstep_sound = random.choice(footstep_sounds)
                Audio(footstep_sound, loop=False, autoplay=True)
                last_footstep_time = current_time

    last_position = player.position
    # ------------------- View Bobbing --------------------
    global bob_phase, previous_position
    is_moving = player.position != previous_position

    if is_moving:
        bob_phase += bob_speed * time.dt
        player.camera_pivot.y = 1.5 + math.sin(bob_phase) * bob_amount_vertical
        player.camera_pivot.rotation_z = math.sin(bob_phase) * bob_amount_rotation

    if not player.grounded:
        bob_phase = 0
        player.camera_pivot.y = 1.5  
        player.camera_pivot.rotation_z = 0

    previous_position = player.position
    # ---------- SCP 096 mechanics ----------
    global follower
    try:
        direction_to_follower = (follower.position - player.position).normalized()
    except ValueError:
        pass
    player_forward = get_forward_direction(player)
    angle = math.acos(player_forward.dot(direction_to_follower))
    angle_threshold = math.radians(10)  # Adjust this if you want

    hit_info = boxcast(origin=follower.position, 
                       direction=(0, 0, -1), 
                       thickness=(6, 6), 
                       distance=20, 
                       ignore=[follower], 
                       debug=False)
    
    dist = distance(player.position, follower.position)
    max_distance = 20
    volume = max (0, 1 - (dist / max_distance))
    broischill_ambience.volume = volume
    
    if hit_info.hit and hit_info.entity == player:
        if angle < angle_threshold:
            if trigger not in played_sounds:
                invoke(seen)
                invoke(seen2)
                invoke(seen3, delay=6)
                follower.look_at_2d(player, 'y')

        if player.intersects(kill_area).hit:
            invoke(death)

def get_forward_direction(entity):
    forward = entity.camera.forward if hasattr(entity, 'camera') else entity.forward
    return forward.normalized()

def input(key):
    global footstep_interval
    global footstep_sounds
    global bob_speed
    if held_keys['shift']:
        footstep_interval = 0.5
        footstep_sounds = [f'assets/steps/Run{i}.ogg' for i in range(1, 8)]
        bob_speed = 6
    else :
        footstep_interval = 0.9
        footstep_sounds = [f'assets/steps/Step{i}.ogg' for i in range(1, 8)]
        bob_speed = 4.4
# ---------------------- RUN -----------------------------
app.run()
