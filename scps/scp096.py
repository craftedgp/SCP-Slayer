from ursina import *
from direct.actor.Actor import Actor
import death
from death import Death

app = Ursina(title='SCP Simulator Beta 0.9.2', fullscreen=True, vsync=True)

# ==================== Assets ======================
trigger = Audio('assets/096/Triggered.ogg', loop=False, autoplay=False)
angered = Audio('assets/096/096Angered.ogg', loop=False, autoplay=False)
raging = Audio('assets/096/096Rage.ogg', loop=True, autoplay=False)
raging.volume = 0
chasing_music = Audio('assets/096/096Chase.ogg', loop=True, autoplay=False)
calmdown = Audio('assets/096/096CalmDown.ogg', loop=False, autoplay=False)
calm = Audio('assets/096/096.ogg', loop=True, autoplay=True)
calm.volume = 0

trigger_area = Entity(model='wireframe_cube',
                      color=color.blue,
                      scale=(60, 10, 60),
                      position=(0, .6, 0))

played_sounds = set()


class SpawnScp096(Entity):  # Inheriting from Entity
    def __init__(self, player, scramble):
        super().__init__()
        self.player = player
        self.scramble = scramble

        # ------- Sit animation --------
        global anim_sit
        anim_sit_actor = Actor('assets/096/anim_sit.gltf')
        anim_sit_actor.loop('scp096_skeleton|scp096_skeleton|scp096_sit')
        anim_sit = Entity(model=anim_sit_actor, scale=(.5, .5, .5), collider='box', position=(0, .6, 0))

    def seen(self):
        global raging, anim_sit
        trigger.play()
        played_sounds.add(trigger)
        calm.stop()
        anim_sit.disable()
        if calm and calmdown in played_sounds:
            played_sounds.remove(calm, calmdown)

    def seen2(self):
        global anim_rage
        angered.play()
        played_sounds.add(angered)
        anim_rage_actor = Actor('assets/096/anim_rage.gltf')
        anim_rage_actor.loop('scp096_skeleton|scp096_skeleton|scp096_panic')
        anim_rage = Entity(model=anim_rage_actor, scale=(.5, .5, .5), position=(0, .6, 0), collider='box')

    def seen3(self):
        global anim_run, anim_rage
        raging.play()
        played_sounds.add(raging)
        chasing_music.play()
        played_sounds.add(chasing_music)
        anim_rage.disable()
        anim_run_actor = Actor('assets/096/anim_run.gltf')
        anim_run_actor.setHpr(180, 0, 0)
        anim_run = Entity(model=anim_run_actor, scale=(.4, .4, .4), position=(0, .5, 0), collider='box')
        anim_run_actor.loop('scp096_skeleton|scp096_skeleton|scp096attackrun')
        anim_run.look_at_2d(self.player, 'y')

    def calm_down(self):
        global anim_run
        if calmdown and calm not in played_sounds:
            calmdown.play()
            calm.play()
            anim_sit.enable()
            anim_sit.position = anim_run.position
            # anim_clamdown_actor = Actor('assets/096/anim_sit.gltf')
            # anim_clamdown_actor.loop('scp096_skeleton|scp096_skeleton|scp096_sit')
            # anim_clamdown = Entity(model=anim_clamdown_actor,
            #                        scale=(.5, .5, .5),
            #                        position=anim_run.position,
            #                        collider='box')
            raging.stop()
            chasing_music.stop()
            anim_run.disable()
        played_sounds.add(calmdown)
        played_sounds.add(calm)

    def update(self):
        # ---------- SCP 096 mechanics ----------
        global anim_sit, direction_to_096

        try:
            direction_to_096 = (anim_sit.position - self.player.position).normalized()
        except ValueError:
            pass

        player_forward = get_forward_direction(self.player)
        angle = math.acos(player_forward.dot(direction_to_096))
        angle_threshold = math.radians(10)  # Adjust this if you want

        hit_info = boxcast(origin=anim_sit.position,
                           direction=(0, 0, -1),
                           thickness=(6, 6),
                           distance=20,
                           ignore=[anim_sit, self.player if self.scramble == True else None],
                           debug=False)

        # ----------- Noise Distance ------------
        max_distance = 30
        dist_anim_sit = distance(self.player.position, anim_sit.position)
        volume_anim_sit = max(0, 1 - (dist_anim_sit / max_distance))
        calm.volume = volume_anim_sit

        if 'anim_rage' in globals() and 'anim_run' in globals():
            dist_anim_rage = distance(self.player.position, anim_rage.position)
            volume_anim_rage = max(0, 1 - (dist_anim_rage / max_distance))
            raging.volume = volume_anim_rage

            dist_anim_run = distance(self.player.position, anim_run.position)
            volume_anim_run = max(0, 1 - (dist_anim_run / max_distance))
            raging.volume = volume_anim_run

        # ---------- Trigger --------------------
        if hit_info.hit and hit_info.entity == self.player:
            if angle < angle_threshold:
                if trigger not in played_sounds:
                    SpawnScp096.seen(self)
                    SpawnScp096.seen2(self)

                    def invokeSeen3():
                        SpawnScp096.seen3(self)

                    invoke(invokeSeen3, delay=6)

        if 'anim_run' in globals():
            anim_run.position += anim_run.forward * time.dt * 30
            anim_run.look_at_2d(self.player, 'y')
            if self.player.intersects(anim_run).hit:
                self.player.disable()
                Text(text='You died', position=(0, .5), origin=(0, 1), scale=3, color=color.white)
                Text(text='You were killed by SCP 096', origin=(0, 0), position=(0, .3))
                Death()
                def invokeCalmDown():
                    SpawnScp096.calm_down(self)

                invoke(invokeCalmDown, delay=2)

def get_forward_direction(entity):
    forward = entity.camera.forward if hasattr(entity, 'camera') else entity.forward
    return forward.normalized()
