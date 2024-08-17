from ursina import *
from player import Controller
from scps.scp096 import SpawnScp096
from spawn import Spawn
from viewbobbing import ViewBobbing
from ursina.shaders import lit_with_shadows_shader
from footsteps import FootSteps
from ui import GameTesterHelp

app = Ursina(title='SCP Simulator Beta 0.9.2', fullscreen=True, vsync=True)
# ==================== Initializing Map and Player ==========================================
Entity.default_shader = lit_with_shadows_shader
ground = Entity(model='plane', scale=(1000, 1, 1000), texture='brick', texture_scale=(1000, 1000), collider='box')
Sky(texture='assets/sky.jpg')
directional_light = DirectionalLight(shadow=True)
directional_light.look_at(Vec3(1, -1, -1))
player = Controller()
player.position = Vec3(50, 0, 0)
player.collider = 'box'
player_health = 100
invoke(Spawn, delay=1)
# ================== Player help and class ==========================
def gt_help():
    GameTesterHelp(player=player)

invoke(gt_help, delay=5)
# =================== footstep Mechanics ============================
fs = FootSteps(player=player)
# ================== SCP 096 mechanics ==============================
scp096 = SpawnScp096(player=player, scramble=False)
# =================== View Bobbing mechanics ========================
vb = ViewBobbing(player=player)
# =================== Update and some other functions================
def update():
    # --------- Call the ViewBobbing update method ----------
    vb.update()
    # --------- Call the FootStep update method ----------
    fs.update()

# ---------------------- RUN -----------------------------
app.run()
