from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from shaders import apply_blur_shader, remove_blur_shader
from viewbobbing import ViewBobbing
from footsteps import FootSteps
import config

app = config.app_global

played_sounds = set()
player_death_sfx = 'assets/player/death2.ogg'
player_spawn_sfx = 'assets/player/spawn.ogg'
player_death_sfx = 'assets/player/death2.ogg'
is_player_alive = True

class Controller(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.normal_speed = self.speed
        self.sprint_speed = 10
        self.vb = ViewBobbing(player=self)
        self.fs = FootSteps(player=self)

    def update(self):
        super().update()
        self.speed = self.sprint_speed if held_keys['shift'] else self.normal_speed
        if is_player_alive:
            self.vb.update()
            self.fs.update()
        
    def Death(self):
        global is_player_alive
        if player_death_sfx not in played_sounds:
            death = Audio(player_death_sfx, loop=False, autoplay=True)
            death.play()
            played_sounds.add(player_death_sfx)
            apply_blur_shader()
            camera.rotation_x -= 100 * time.dt
            if camera.rotation_x < -90:
                camera.rotation_x = -90
            elif camera.rotation_x > 90:
                camera.rotation_x = 90
            camera.position.y -= 10 * time.dt
            is_player_alive = False
            
    def Respawn(self):
        if is_player_alive == False:
            Controller.Death(self)
            def call_respawn_thesecond():
                Controller.Spawn(self)
                Controller()
                self.position = Vec3(50, 0, 0)
                self.enable()
                remove_blur_shader()
                destroy(respawn_button)

            respawn_button = Button(text="Respawn", scale=(.2, .1), position=(0, 0), origin=(0, 0), color=color.black)
            respawn_button.on_click = call_respawn_thesecond

    def Spawn(self):
        global player_health, class_text, is_player_alive
        is_player_alive = True
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
