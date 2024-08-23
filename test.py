from ursina import *

app = Ursina(fullscreen=True, vsync=False, borderless=True)

EditorCamera()

ground = Entity(model='assets/map/untitled.gltf', position=(0, 0, 0), )

app.run()
