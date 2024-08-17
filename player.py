from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina(title='SCP Simulator Beta 0.9.2', fullscreen=True, vsync=True)

class Controller(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.normal_speed = self.speed
        self.sprint_speed = 10

    def update(self):
        super().update()
        self.speed = self.sprint_speed if held_keys['shift'] else self.normal_speed
