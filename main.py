from ursina import *
from controller import Controller
from ursina.shaders import lit_with_shadows_shader
from ui import GameTesterHelp, SpawnMenu
import config

app = config.app_global
# ==================== Initializing Map and Player ==========================================
Entity.default_shader = lit_with_shadows_shader
ground = Entity(model='plane', scale=(200, 2, 200), texture='brick', collider='box')
Sky(texture='assets/sky.jpg')
directional_light = DirectionalLight(shadow=True)
directional_light.look_at(Vec3(1, -1, -1))
player = Controller()
player.position = Vec3(50, 0, 0)
player.collider = 'box'
invoke(player.Spawn, delay=2)
# ================== Player help and class ==========================
def gt_help():
    GameTesterHelp(player=player)

invoke(gt_help, delay=5)
# ========================= SpawnMenu  ==============================
SpawnMenu(player=player)
# =================== Update and some other functions================
def update():
    pass

# ---------------------- RUN -----------------------------
app.run()
