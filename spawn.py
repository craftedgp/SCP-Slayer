from ursina import *

app = Ursina(title='SCP Simulator Beta 0.9.2', fullscreen=True, vsync=True)
played_sounds = set()
player_spawn_sfx = 'assets/player/spawn.ogg'
player_death_sfx = 'assets/player/death2.ogg'


def Spawn():
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
