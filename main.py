from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import time
from direct.actor.Actor import Actor
from ursina.shaders import lit_with_shadows_shader

app = Ursina(fullscreen=True, borderless=True, vsync=True)

# ==================== Map and player ==========================================
ground = Entity(model='plane', scale=(1000, 1, 1000), texture='grass', texture_scale=(1000, 1000), collider='box')
Sky(texture='assets/sky.jpg')
# -------------- Played Sounds shall not be played again --------------
played_sounds = set()
played_sounds2 = False

def spawn():
    global player_health, class_text
    player_health = 100
    Audio(player_spawn_sfx, loop=False, autoplay=True)
    if player_death_sfx in played_sounds:
        played_sounds.remove(player_death_sfx)

    youare_text = Text(
    text='You are',  
    position=(0, .2),     
    origin=(0, 0),         
    scale=4,   
    font='assets/fonts/OliversBarney.ttf'     
    )
    class_text = Text(
    text='Game Tester',  
    position=(0, .1),     
    origin=(0, 0),         
    scale=5,   
    font='assets/fonts/OliversBarney.ttf',  
    color = color.random_color(),
    role='Game Tester'
    )
    help_text = Text(
    text='Press F1 for help',  
    position=(0, 0),     
    origin=(0, 0),         
    scale=2,   
    font='assets/fonts/OliversBarney.ttf'
    )

    def fade_out_text():
        if youare_text.alpha > 0:
            youare_text.alpha -= 0.01  
            invoke(fade_out_text, delay=0.5)  
        if class_text.alpha > 0:
            class_text.alpha -= 0.01
            invoke(fade_out_text, delay=0.5)
        if help_text.alpha > 0:
            help_text.alpha -= 0.01
            invoke(fade_out_text, delay=0.5)

    # Start fading out the text after 2 seconds
    invoke(fade_out_text, delay=2)

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
invoke(spawn, delay=2)

# ----------------- Player Death mechanis | What happens when the player's health is zero or when special events are met ---------------
def death():
    if not player_death_sfx in played_sounds:
        death = Audio(player_death_sfx, loop=False, autoplay=True)
        death.play()
        played_sounds.add(player_death_sfx)
        blur_amount = 100
        apply_blur_shader()
        player.disable()
        camera.rotation_x -= 100 * time.dt
        if camera.rotation_x < -90:
            camera.rotation_x = -90
        elif camera.rotation_x > 90:
            camera.rotation_x = 90
        camera.position.y -= 10 * time.dt
# =================== Player classes and help =======================
'''
Game Tester Help = gt_help
'''
gt_help = WindowPanel(scale=(0.5, 0.5), position=(0, 0), visible=False, color=color.gray)
gt_help_text = Text(parent=gt_help, 
                    text='Help stuff comming soon \n Im going to sleep \n if i continue coding im might ruin all this', 
                    position=(-.4, 0), 
                    scale=2, 
                    color=color.white)

# gt_help = Panel(scale=(2, 1), color=color.gray, visible=False)
# gt_help_text = Text(text='This is the UI Panel', origin=(.43, .43), scale=1, parent=gt_help)
# ------------------- Functions ---------------------
def fade_in_ui():
    gt_help.visible = True
    gt_help.fade_in(duration=.5)
    # gt_help_text.fade_in(duration=.5)

def fade_out_ui():
    gt_help.fade_out(duration=.5)
    # gt_help_text.fade_out(duration=.5)
    invoke(hide_ui, delay=.5)

def hide_ui():
    gt_help.visible = False

def toggle_ui_gt():
    if class_text.role == 'Game Tester':
        if gt_help.visible:
            fade_out_ui()
        else:
            fade_in_ui()

# =================== footstep Mechanics ============================
footstep_sounds = [f'assets/steps/Step{i}.ogg' for i in range(1, 8)]
footstep_interval = 0.9
last_footstep_time = 0
last_position = player.position
# ================== SCP 096 mechanics ===================
trigger = Audio('assets/096/Triggered.ogg', loop=False, autoplay=False)
angered = Audio('assets/096/096Angered.ogg', loop=False, autoplay=False)
raging = Audio('assets/096/096Rage.ogg', loop=True, autoplay=False)
raging.volume = 0
chasing_music = Audio('assets/096/096Chase.ogg', loop=True, autoplay=False)
calm_down = Audio('assets/096/096calmdown.ogg', loop=False, autoplay=False)
calm = Audio('assets/096/096.ogg', loop=True, autoplay=True)
calm.volume = 0
kill = 'assets/player/death.ogg'
# ------- Sit animation --------
anim_sit_actor = Actor('assets/096/anim_sit.gltf')
anim_sit_actor.loop('scp096_skeleton|scp096_skeleton|scp096_sit')
anim_sit = Entity(model=anim_sit_actor, scale=(.5, .5, .5), position=(0, .6, 0), collider='box')
# ------- After seeing his face -------
def seen():
    global raging
    trigger.play()
    played_sounds.add(trigger)
    calm.stop()
    anim_sit.disable()

def seen2():
    angered.play()
    played_sounds.add(angered)
    global anim_rage
    anim_rage_actor = Actor('assets/096/anim_rage.gltf')
    anim_rage_actor.loop('scp096_skeleton|scp096_skeleton|scp096_panic')
    anim_rage = Entity(model=anim_rage_actor, scale=(.5, .5, .5), position=(0, .6, 0), collider='box')

def seen3():
    global anim_run
    raging.play()
    played_sounds.add(raging)
    chasing_music.play()
    played_sounds.add(chasing_music)
    anim_rage.disable()
    anim_run_actor = Actor('assets/096/anim_run.gltf')
    anim_run_actor.setHpr(180, 0, 0)
    anim_run = Entity(model=anim_run_actor, scale=(.4, .4, .4), position=(0, .5, 0), collider='box')
    anim_run_actor.loop('scp096_skeleton|scp096_skeleton|scp096attackrun')
    anim_run.look_at_2d(player, 'y')

trigger_area = Entity(model='wireframe_cube', 
                      color=color.blue, 
                      scale=(60, 10, 60), 
                      position=(0, .6, 0))

# ========================= Blur mechanics ==========================
blur_shader = Shader(language=Shader.GLSL, 
                     vertex='blur_vertex_shader.glsl', 
                     fragment='blur_fragment_shader.glsl')

blur_amount = 0
def apply_blur_shader():
    camera.shader = blur_shader
    camera.set_shader_input('blur_amount', blur_amount)
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
    global last_footstep_time, last_position
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
    global anim_sit, direction_to_096
    try:
        direction_to_096 = (anim_sit.position - player.position).normalized()
    except ValueError:
        pass
    player_forward = get_forward_direction(player)
    angle = math.acos(player_forward.dot(direction_to_096))
    angle_threshold = math.radians(10)  # Adjust this if you want

    hit_info = boxcast(origin=anim_sit.position, 
                       direction=(0, 0, -1), 
                       thickness=(6, 6), 
                       distance=20, 
                       ignore=[anim_sit], 
                       debug=False)
    # ----------- Noise Distance ------------
    if 'anim_rage' and 'anim_run' in globals():
        max_distance = 20

        dist_anim_rage = distance(player.position, anim_rage.position)
        volume_anim_rage = max (0, 1 - (dist_anim_rage / max_distance))
        raging.volume = volume_anim_rage

        dist_anim_run = distance(player.position, anim_run.position)
        volume_anim_run = max (0, 1 - (dist_anim_run / max_distance))
        chasing_music.volume = volume_anim_run
    # ---------- Trigger --------------------
    if hit_info.hit and hit_info.entity == player:
        if angle < angle_threshold:
            if trigger not in played_sounds:
                invoke(seen)
                invoke(seen2)
                invoke(seen3, delay=6)
    if 'anim_run' in globals():
        anim_run.position += anim_run.forward * time.dt * 20
        anim_run.look_at_2d(player, 'y')
        if player.intersects(anim_run).hit:
            invoke(death)

def get_forward_direction(entity):
    forward = entity.camera.forward if hasattr(entity, 'camera') else entity.forward
    return forward.normalized()

# ========== Input ===========
def input(key):
    global footstep_interval
    global footstep_sounds
    global bob_speed
    if held_keys['shift']:
        footstep_interval = 0.5
        footstep_sounds = [f'assets/steps/Run{i}.ogg' for i in range(1, 8)]
        bob_speed = 6
    else:
        footstep_interval = 0.9
        footstep_sounds = [f'assets/steps/Step{i}.ogg' for i in range(1, 8)]
        bob_speed = 4.4
    if key == 'f1':
        toggle_ui_gt()
# ---------------------- RUN -----------------------------
app.run()
