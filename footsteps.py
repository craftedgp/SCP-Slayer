from ursina import *

footstep_sounds = [f'assets/steps/Step{i}.ogg' for i in range(1, 8)]
footstep_interval = 0.9
last_footstep_time = 0

class FootSteps(Entity):
    def __init__(self, player, **kwargs):
        super().__init__(**kwargs)
        self.player = player
        last_position = self.player.position

    def update(self):
        global last_footstep_time, last_position
        if self.player.grounded:
            movement = distance(self.player.position, last_position)
            if movement > 0.01:
                current_time = time.time()
                if current_time - last_footstep_time > footstep_interval:
                    footstep_sound = random.choice(footstep_sounds)
                    Audio(footstep_sound, loop=False, autoplay=True)
                    last_footstep_time = current_time

        last_position = self.player.position

    def input(self, key):
        global footstep_interval, footstep_sounds
        if held_keys['shift']:
            footstep_interval = 0.5
            footstep_sounds = [f'assets/steps/Run{i}.ogg' for i in range(1, 8)]
        else:
            footstep_interval = 0.9
            footstep_sounds = [f'assets/steps/Step{i}.ogg' for i in range(1, 8)]
