from ursina import *

app = Ursina(title='SCP Simulator Beta 0.9.2', fullscreen=True, vsync=True)

version = Text('SCP:Simulator version Beta 0.9.x', color=color.white, position=window.top_left, scale=1.5)

'''
Game Tester Help = gt_help
'''

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
