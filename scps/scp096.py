from ursina import *
from direct.actor.Actor import Actor
from controller import Controller
import controller
import config

app = config.app_global


class SpawnScp096(Entity):
    def __init__(self, target, scramble, active=True):
        super().__init__()
        self.target = target
        self.scramble = scramble
        self.active = active
        self.anim_sit = None
        self.anim_rage = None
        self.anim_run = None
        self.played_sounds = set()
        
        # ------- Audio Assets --------
        self.trigger = Audio('assets/096/Triggered.ogg', loop=False, autoplay=False)
        self.angered = Audio('assets/096/096Angered.ogg', loop=False, autoplay=False)
        self.raging = Audio('assets/096/096Rage.ogg', loop=True, autoplay=False)
        self.raging.volume = 0
        self.chasing_music = Audio('assets/096/096Chase.ogg', loop=True, autoplay=False)
        self.calmdown = Audio('assets/096/096CalmDown.ogg', loop=False, autoplay=False)
        self.calm = Audio('assets/096/096.ogg', loop=True, autoplay=True)
        self.calm.volume = 0

        # ------- Trigger Area --------
        self.trigger_area = Entity(
            model='wireframe_cube',
            color=color.blue,
            scale=(60, 10, 60),
            position=(0, .6, 0)
        )
        
        # ------- Sit animation --------
        anim_sit_actor = Actor('assets/096/anim_sit.gltf')
        anim_sit_actor.loop('scp096_skeleton|scp096_skeleton|scp096_sit')
        self.anim_sit = Entity(model=anim_sit_actor, scale=(.5, .5, .5), collider='box', position=(0, .6, 0))

    def toggle(self, state):
        self.active = state
        if not self.active:
            if self.anim_sit:
                self.anim_sit.disable()
            if self.anim_rage:
                self.anim_rage.disable()
            if self.anim_run:
                self.anim_run.disable()
        else:
            if self.anim_sit:
                self.anim_sit.enable()

    def seen(self):
        if not self.active:
            return
        self.trigger.play()
        self.played_sounds.add(self.trigger)
        self.calm.stop()
        self.anim_sit.disable()
        if self.calm and self.calmdown in self.played_sounds:
            self.played_sounds.remove(self.calm, self.calmdown)

    def seen2(self):
        if not self.active:
            return
        self.angered.play()
        self.played_sounds.add(self.angered)
        anim_rage_actor = Actor('assets/096/anim_rage.gltf')
        anim_rage_actor.loop('scp096_skeleton|scp096_skeleton|scp096_panic')
        self.anim_rage = Entity(model=anim_rage_actor, scale=(.5, .5, .5), position=(0, .6, 0), collider='box')

    def seen3(self):
        if not self.active:
            return
        self.raging.play()
        self.played_sounds.add(self.raging)
        self.chasing_music.play()
        self.played_sounds.add(self.chasing_music)
        if self.anim_rage:
            self.anim_rage.disable()
        anim_run_actor = Actor('assets/096/anim_run.gltf')
        anim_run_actor.setHpr(180, 0, 0)
        self.anim_run = Entity(model=anim_run_actor, scale=(.4, .4, .4), position=(0, .5, 0), collider='box')
        anim_run_actor.loop('scp096_skeleton|scp096_skeleton|scp096attackrun')
        self.anim_run.look_at_2d(self.target, 'y')

    def calm_down(self):
        if not self.active:
            return
        if self.calmdown and self.calm not in self.played_sounds:
            self.calmdown.play()
            self.calm.play()
            self.anim_sit.enable()
            if self.anim_run:
                self.anim_sit.position = self.anim_run.position
                self.anim_run.disable()
            self.raging.stop()
            self.chasing_music.stop()
        self.played_sounds.add(self.calmdown)
        self.played_sounds.add(self.calm)

    def stop_all_audio(self):
        self.trigger.stop()
        self.angered.stop()
        self.raging.stop()
        self.chasing_music.stop()
        self.calmdown.stop()
        self.calm.stop()

    def update(self):
        if not self.active:
            return
        # ----------------- Sound ----------------------
        max_distance = 30
        dist_anim_sit = distance(self.target.position, self.anim_sit.position)
        volume_anim_sit = max(0, 1 - (dist_anim_sit / max_distance))
        self.calm.volume = volume_anim_sit       
        if self.anim_rage:
            dist_anim_rage = distance(self.target.position, self.anim_rage.position)
            volume_anim_rage = max(0, 1 - (dist_anim_rage / max_distance))
            self.raging.volume = volume_anim_rage        
        if self.anim_run:
            dist_anim_run = distance(self.target.position, self.anim_run.position)
            volume_anim_run = max(0, 1 - (dist_anim_run / max_distance))
            self.raging.volume = volume_anim_run     

        if controller.is_player_alive:
            if self.anim_run:
                self.anim_run.look_at_2d(self.target, 'y')
                self.anim_run.position += self.anim_run.forward * 10 * time.dt
            try:
                direction_to_096 = (self.anim_sit.position - self.target.position).normalized()
            except ValueError:
                return      
            player_forward = get_forward_direction(self.target)
            angle = math.acos(player_forward.dot(direction_to_096))
            angle_threshold = math.radians(10)      
            hit_info = boxcast(
                origin=self.anim_sit.position,
                direction=(0, 0, -1),
                thickness=(6, 6),
                distance=60,
                ignore=[self.anim_sit, self.target if self.scramble else None],
                debug=False
            )      
            # ----------------- Trigger --------------------
            if hit_info.hit and hit_info.entity == self.target:
                if angle < angle_threshold:
                    if self.trigger not in self.played_sounds:
                        self.seen()
                        self.seen2()
                        invoke(self.seen3, delay=6)

            if self.anim_run and self.target.intersects(self.anim_run).hit:
                self.target.disable()
                global text1, text2
                text1 = Text(text='You died', position=(0, .5), origin=(0, 1), scale=3, color=color.white)
                text2 = Text(text='You were killed by SCP 096', origin=(0, 0), position=(0, .3))
                controller.is_player_alive = False     
                invoke(self.calm_down, delay=2)     
                Controller.Respawn(self)

            if controller.is_player_alive == True:
                if 'text1' and 'text2' in globals():
                    destroy(text1)
                    destroy(text2)

            elif not controller.is_player_alive:
                invoke(self.calm_down)


def get_forward_direction(entity):
    forward = entity.camera.forward if hasattr(entity, 'camera') else entity.forward
    return forward.normalized()

