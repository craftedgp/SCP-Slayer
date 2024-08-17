from ursina import *
from shaders import apply_blur_shader

app = Ursina(title='SCP Simulator Beta 0.9.2', fullscreen=True, vsync=True)

played_sounds = set()
player_death_sfx = 'assets/player/death2.ogg'


def Death():
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
