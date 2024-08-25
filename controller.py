from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from shaders import apply_blur_shader, remove_blur_shader
import config

app = config.app_global

footstep_sounds = [f'assets/steps/Step{i}.ogg' for i in range(1, 8)]
footstep_interval = 0.9
last_footstep_time = 0
played_sounds = set()
player_death_sfx = 'assets/player/death2.ogg'
player_spawn_sfx = 'assets/player/spawn.ogg'
player_death_sfx = 'assets/player/death2.ogg'
bob_amount_vertical = .1
# bob_amount_horizontal = 0.2
bob_amount_rotation = 1
bob_speed = 4.4
bob_phase = 0
is_moving = False

class FootSteps(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(**kwargs)
        self.player = player
        self.last_position = self.player.position

    def update(self):
        global last_footstep_time
        if self.player.grounded:
            movement = distance(self.player.position, self.last_position)
            if movement > 0.01:
                current_time = time.time()
                if current_time - last_footstep_time > footstep_interval:
                    footstep_sound = random.choice(footstep_sounds)
                    Audio(footstep_sound, loop=False, autoplay=True)
                    last_footstep_time = current_time

        self.last_position = self.player.position

    def input(self, key):
        global footstep_interval, footstep_sounds
        if held_keys['shift']:
            footstep_interval = 0.5
            footstep_sounds = [f'assets/steps/Run{i}.ogg' for i in range(1, 8)]
        else:
            footstep_interval = 0.9
            footstep_sounds = [f'assets/steps/Step{i}.ogg' for i in range(1, 8)]


class ViewBobbing(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(**kwargs)
        self.player = player
        self.bob_phase = 0
        self.previous_position = self.player.position

    def update(self):
        global bob_phase, previous_position
        is_moving = self.player.position != self.previous_position

        if is_moving:
            bob_phase += bob_speed * time.dt
            self.player.camera_pivot.y = 1.5 + math.sin(bob_phase) * bob_amount_vertical
            self.player.camera_pivot.rotation_z = math.sin(bob_phase) * bob_amount_rotation

        if not self.player.grounded:
            bob_phase = 0
            self.player.camera_pivot.y = 1.5
            self.player.camera_pivot.rotation_z = 0

        self.previous_position = self.player.position

    def input(self, key):
        global bob_speed
        if held_keys['shift']:
            bob_speed = 6
        else:
            bob_speed = 4.4

class Controller(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.normal_speed = self.speed
        self.sprint_speed = 10
        self.vb = ViewBobbing(player=self)
        self.fs = FootSteps(player=self)
        self.is_player_alive = True

    def update(self):
        super().update()
        self.speed = self.sprint_speed if held_keys['shift'] else self.normal_speed
        self.fs.update()
        self.vb.update()
        if not self.is_player_alive:
            self.Death()
            print("Player is dead. Triggering death sequence.")
        
    def Death(self):
            if player_death_sfx not in played_sounds:
                death = Audio(player_death_sfx, loop=False, autoplay=True)
                death.play()
                played_sounds.add(player_death_sfx)
                apply_blur_shader()
                self.Respawn()

    def Respawn(self):
        respawn_button = Button(text="Respawn", scale=(.2, .1), position=(0, 0), origin=(0, 0), color=color.black)
        def call_respawn():
            self.Spawn() 
            self.position = Vec3(50, 0, 0) 
            self.is_player_alive = True 
            remove_blur_shader()  
            destroy(respawn_button)  
        respawn_button.on_click = call_respawn

    def Spawn(self):
        self.is_player_alive = True
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
            color=color.red,
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
                youare_text.alpha -= 0.001
                invoke(fade_out_text, delay=0.1)
            if class_text.alpha > 0:
                class_text.alpha -= 0.001
                invoke(fade_out_text, delay=0.1)
            if help_text.alpha > 0:
                help_text.alpha -= 0.001
                invoke(fade_out_text, delay=0.1)
    
        invoke(fade_out_text, delay=4)
