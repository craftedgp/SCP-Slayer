from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import time
from direct.actor.Actor import Actor

app = Ursina(title='SCP SIMULATOR', fullscreen=False, borderless=True, vsync=True)

# ==================== Map and player ==========================================
ground = Entity(model='plane', scale=(1000, 1, 1000), texture='grass', texture_scale=(1000, 1000), collider='box')
Sky(texture='assets/sky.jpg')

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
player.position = Vec3(70, 0, 70)
player.collider = 'box'
player_death_sfx = 'assets/player/death.ogg'
# =================== footstep Mechanics ============================
footstep_sounds = [f'assets/steps/StepForest{i}.ogg' for i in range(1, 3)]
footstep_interval = 0.5
last_footstep_time = 0
last_position = player.position
'''
Refer to update() to see the footsteps mechanics there
'''
# ================== SCP 096 mechanics ===================
follower = Entity(model='cube', color=color.clear, scale=(.5, .5, .5), position=(0, .6, 0), collider='box')
trigger = 'assets/096/Triggered.ogg'
angered = 'assets/096/096Angered.ogg'
hella_angry = 'assets/096/Scream.ogg'
broiscomming = 'assets/096/096Chase.ogg'
broischill_ambience = Audio('assets/096/096.ogg', loop=True, autoplay=True)
kill = 'assets/player/death.ogg'
# ------- Sit animation --------
anim_sit = Actor('assets/096/anim_sit.gltf')
anim_sit.reparent_to(follower)
anim_sit.loop('scp096_skeleton|scp096_skeleton|scp096_sit')
# ------- After seeing his face ----

def seen():
    Audio(trigger, loop=False, autoplay=True)
    played_sounds.add(trigger)
    broischill_ambience.stop()
    anim_sit.cleanup()
    anim_sit.removeNode()
    global anim_standup
    anim_standup = Actor('assets/096/anim_standup.gltf')
    anim_standup.reparent_to(follower)
    anim_standup.play('scp096_skeleton|scp096_skeleton|scp096_situp')


def seen2():
    Audio(angered, loop=False, autoplay=True)
    played_sounds.add(angered)
    global anim_rage
    anim_rage = Actor('assets/096/anim_rage.gltf')
    anim_rage.reparent_to(follower)
    anim_rage.loop('scp096_skeleton|scp096_skeleton|scp096_panic')
    anim_standup.cleanup()
    anim_standup.removeNode()


def seen3():
    Audio(hella_angry, loop=True, autoplay=True)
    played_sounds.add(hella_angry)
    Audio(broiscomming, loop=True, autoplay=True)
    played_sounds.add(broiscomming)
    global anim_run
    anim_rage.cleanup()
    anim_rage.removeNode()
    anim_run = Actor('assets/096/anim_run.gltf')
    anim_run.reparent_to(follower)
    anim_run.loop('scp096_skeleton|scp096_skeleton|scp096_run')
    follower.add_script(SmoothFollow(target=player, speed=0.4))
    follower.look_at(player)


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

'''
Refer to update() to see the SCP mechanics there
'''
# =================== Played Sounds shall not be played again =======
played_sounds = set()
played_sounds2 = False
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
    
    if hit_info.hit and hit_info.entity == player:
        if angle < angle_threshold:
            if trigger not in played_sounds:
                invoke(seen)
                invoke(seen2, delay=4.5)
                invoke(seen3, delay=35)

            if player.intersects(kill_area).hit:
                global played_sounds2
                if played_sounds2 == False:
                    Audio(kill, loop=False, autoplay=True)
                    played_sounds2 = True
                    player.disable()
                    move_speed = 1.0
                    camera.position.y -= move_speed * time.dt

def get_forward_direction(entity):
    forward = entity.camera.forward if hasattr(entity, 'camera') else entity.forward
    return forward.normalized()
# ---------------------- RUN -----------------------------
app.run()
