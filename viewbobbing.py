from ursina import *

app = Ursina(title='SCP Simulator Alpha 0.1.2', fullscreen=True, vsync=True, icon='assets/favicon.ico')

bob_amount_vertical = .1
# bob_amount_horizontal = 0.2
bob_amount_rotation = 1
bob_speed = 4.4
bob_phase = 0
is_moving = False

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
