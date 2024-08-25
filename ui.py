from ursina import *
import config

app = config.app_global

version = Text('SCP Slayer Alpha 0.1.2c', color=color.white, position=window.top_left, scale=1.5)

'''
Game Tester Help = gt_help
'''

list_spawnbuttons = ['spawn_scp096_button', 'delete_scp096_button']

gt_help = Panel(title='Game Tester',
                position=(0, 0),
                visible=False,
                color=color.gray,
                alpha=.5)

gt_help.scale_x = camera.aspect_ratio
gt_help.scale_y = 0.6

gt_logo = Entity(
    parent=gt_help,
    model='quad',
    position=(.35, 0),
    scale=(0.3 / gt_help.scale_x, 0.3 / gt_help.scale_y),
    texture='assets/player/classes/images/gt_logo.png',
    alpha=.5)

gt_logo2 = Animation(
    'assets/misc/loading.gif',
    parent=gt_help,
    position=(-.46, 0),
    scale=(0.1 / gt_help.scale_x, 0.1 / gt_help.scale_y),
    alpha=.5)

gt_help_title = Text(parent=gt_help,
                     text="Game Tester",
                     font='assets/fonts/OpenSansBold.ttf',
                     position=(0, .44),
                     origin=(0, 0),
                     scale=(2 / gt_help.scale_x, 2 / gt_help.scale_y),
                     color=color.red,
                     alpha=.5)

gt_help_text = Text(parent=gt_help,
                    text='You are a Game Tester, play the game and report any errors or bugs to the developer',
                    position=(-.4, 0),
                    scale=(1.1 / gt_help.scale_x, 1.1 / gt_help.scale_y),
                    color=color.white,
                    alpha=.5)


def fade_in_ui():
    gt_help.visible = True
    gt_help.fade_in(duration=.5)
    gt_help_text.fade_in(duration=.5)
    gt_logo.fade_in(duration=.5)
    gt_logo2.fade_in(duration=.5)
    gt_help_title.fade_in(duration=.5)

def fade_out_ui():
    gt_help.fade_out(duration=.5)
    gt_help_text.fade_out(duration=.5)
    gt_logo.fade_out(duration=.5)
    gt_logo2.fade_out(duration=.5)
    gt_help_title.fade_out(duration=.5)
    invoke(hide_ui, delay=.5)

def hide_ui():
    gt_help.visible = False

def toggle_ui_gt():
    # if class_text.role == 'Game Tester':
    if gt_help.visible:
        fade_out_ui()
    else:
        fade_in_ui()

class GameTesterHelp(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(self, **kwargs)
        self.player = player

    def input(self, key):
        if key == 'f1':
            toggle_ui_gt()

# =================== Spawn menu ====================
# Import every SCP First
from scps.scp096 import SpawnScp096
# Spawn menu
class SpawnMenu(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(**kwargs)
        self.player = player

        # Background for the spawn menu
        self.bg = Panel(origin=(0, 0), position=(0, 0), alpha=0.5, visible=False)
        self.bg.scale_x = camera.aspect_ratio
        self.bg.scale_y = camera.aspect_ratio
        # --------- init SCPs ---------
        # SCP 096
        self.scp096_manager = self.SCP096Manager(player)

    class SCP096Manager:
        def __init__(self, player):
            self.player = player
            self.scp096_instance = None  # Placeholder for SCP-096 entity

            # SCP-096 Spawn Button
            self.spawn_button = Button(text='Spawn SCP-096', origin=(0, 0), position=(-.2, 0), scale=(.2, .1), visible=False)
            self.spawn_button.on_click = self.spawn

            # SCP-096 Remove Button
            self.remove_button = Button(text='Remove SCP-096', origin=(0, 0), position=(.2, 0), scale=(.2, .1), visible=False)
            self.remove_button.on_click = self.remove

        def spawn(self):
            if not self.scp096_instance:
                # Spawn SCP-096 in the world
                self.scp096_instance = SpawnScp096(target=self.player, scramble=False, active=True)

        def remove(self):
            if self.scp096_instance:
                # Remove SCP-096 from the world
                self.scp096_instance.toggle(False)
                destroy(self.scp096_instance.anim_sit)
                destroy(self.scp096_instance.anim_rage)
                destroy(self.scp096_instance.anim_run)
                self.scp096_instance.stop_all_audio()
                self.scp096_instance = None

    # ------------- OPEN THE MENU WHEN Q IS HELD ---------------
    def input(self, key):
        # Show or hide the spawn menu with 'q'
        if held_keys['q']:
            self.bg.visible = True
            mouse.locked = False
            mouse.enabled = True
            # SCP-096 
            self.scp096_manager.spawn_button.visible = True
            self.scp096_manager.remove_button.visible = True
        else:
            self.bg.visible = False
            mouse.locked = True
            mouse.enabled = True
            # SCP-096 
            self.scp096_manager.spawn_button.visible = False
            self.scp096_manager.remove_button.visible = False
