import pygame
import data
import math
import funcs
import random



class Bloon:
    def __init__(self, id, waypoint=None, x=None, y=None, lifetime=0, distance_travelled=0, camo=False, lead=False):
        self.id = id
        self.angle = 0
        self.last_waypoint = waypoint
        self.current_waypoint = waypoint.ahead
        #self.w = 49
        #self.h = 63
        self.size = data.BLOON_SIZE_DATA[self.id]
        self.speed = data.BLOON_SPEED_DATA[self.id] * data.BLOON_SPEED_MULTIPLIER
        self.lifetime = lifetime
        self.distance_travelled = distance_travelled
        self.health = data.BLOON_HP_DATA[self.id]
        self.camo = camo
        self.lead = lead
        self.effects = []
        self.moab_class = False
        if self.id >= 11:
            self.moab_class = True
        if self.id == 7 or self.id == 14:
            self.lead = True
        #BLOON_IMAGES = []
        #for i in range(0, 16):
        #    BLOON_IMAGES.append((pygame.image.load("assets/bloons/bloon_" + str(i) + ".png")).convert_alpha())
        if x is None:
            self.spawn()
        else:
            self.x = x
            self.y = y
            self.angle = math.atan2(self.current_waypoint.y - self.last_waypoint.y,
                                    self.current_waypoint.x - self.last_waypoint.x)
        self.image_reference = None
        self.image = None
        self.update_image()

    def tick(self):
        self.lifetime += 1
        self.distance_travelled += self.speed
        modifier = 1
        if "nebunu" in self.effects:
            modifier = -0.2

        for effect in self.effects:
            effect.tick()

        is_stunned = False
        if Stun in [type(i) for i in self.effects]:
            is_stunned = True

        if not is_stunned:
            self.x += math.cos(self.angle) * self.speed * modifier
            self.y += math.sin(self.angle) * self.speed * modifier

        if math.dist((self.x, self.y), (self.current_waypoint.x, self.current_waypoint.y)) < 4:
            self.on_current_waypoint_reached()
            # if self.current_waypoint.ahead is None:
            #     self.despawn()
            #     return
            # self.x = self.current_waypoint.x
            # self.y = self.current_waypoint.y
            # self.last_waypoint = self.current_waypoint
            # self.current_waypoint = self.last_waypoint.ahead
            # self.angle = math.atan2(self.current_waypoint.y - self.last_waypoint.y,
            #                         self.current_waypoint.x - self.last_waypoint.x)


        self.draw()

    def on_current_waypoint_reached(self):
        if self.current_waypoint.ahead is None:
            self.despawn()
            return
        self.x = self.current_waypoint.x
        self.y = self.current_waypoint.y
        self.last_waypoint = self.current_waypoint
        self.current_waypoint = self.last_waypoint.ahead
        self.angle = math.atan2(self.current_waypoint.y - self.last_waypoint.y,
                                self.current_waypoint.x - self.last_waypoint.x)
        self.update_image()


    def spawn(self):
        self.x = self.last_waypoint.x
        self.y = self.last_waypoint.y
        self.angle = math.atan2(self.current_waypoint.y - self.last_waypoint.y, self.current_waypoint.x - self.last_waypoint.x)


    def despawn(self):
        data.CLIENT.scene.bloons.remove(self)
        data.CLIENT.scene.lives -= data.BLOON_RBE_DATA[self.id]
        del self

    def get_current_rbe(self):
        default_hp = data.BLOON_HP_DATA[self.id]
        default_rbe = data.BLOON_RBE_DATA[self.id]
        missing_health = default_hp - self.health
        return default_rbe - missing_health
        # if default_hp == 1:
        #     return default_rbe

    def pop(self):
        pop_sounds = [data.SOUND_BLOON_POP1, data.SOUND_BLOON_POP2, data.SOUND_BLOON_POP3]
        random.choice(pop_sounds).play()
        data.CLIENT.scene.bloons.remove(self)
        del self


    def spawn_children(self, projectile, children=None):
        if children is not None:
            for i in range(0, len(children)):
                distance = i * 10
                bloon = Bloon(children[i], self.last_waypoint,
                              self.x - math.cos(self.angle) * distance, self.y - math.sin(self.angle) * distance,
                              self.lifetime)
                projectile.already_hit.append(bloon)
                data.CLIENT.scene.bloons.append(bloon)
            return

        for i in range(0, len(data.BLOON_CHILDREN_DATA[self.id])):
            distance = 8+i*8
            bloon = Bloon(data.BLOON_CHILDREN_DATA[self.id][i], self.last_waypoint, self.x-math.cos(self.angle)*distance, self.y-math.sin(self.angle)*distance, self.lifetime, self.distance_travelled)
            projectile.already_hit.append(bloon)
            data.CLIENT.scene.bloons.append(bloon)

    def update_image(self):
        if self.camo:
            self.image_reference = data.CAMO_BLOON_IMAGES[self.id]
        else:
            self.image_reference = data.BLOON_IMAGES[self.id]
        self.image = self.image_reference
        if self.moab_class:
            self.image = funcs.rotate_image(self.image_reference, -math.degrees(self.angle))

    def draw(self):
        # if self.camo:
        #     funcs.draw_image(data.CAMO_BLOON_IMAGES[self.id], self.x, self.y, center=True)
        # else:
        #     funcs.draw_image(data.BLOON_IMAGES[self.id], self.x, self.y, center=True)
        funcs.draw_image(self.image, self.x, self.y, center=True)
        if "nebunu" in self.effects:
            funcs.draw_image(data.NEBUNU, self.x, self.y)
        pygame.draw.circle(data.WINDOW, (0, 0, 0), (self.x, self.y), self.size, 1)

    def get_bonus_damage(self):
        bonus_damage = 0
        for e in self.effects:
            if type(e) is Cripple:
                bonus_damage += 5

        print(bonus_damage)
        print(self.effects)
        return bonus_damage

    def stun(self, duration):
        for e in self.effects:
            if type(e) is Stun:
                self.effects.remove(e)

        self.effects.append(Stun(self, duration))

    def cripple(self, duration):
        for e in self.effects:
            if type(e) is Cripple:
                self.effects.remove(e)

        self.effects.append(Cripple(self, duration))




class Effect:
    def __init__(self, owner, duration=3):
        self.id = 0
        self.owner = owner
        self.duration = duration
        self.timer = 0

    def tick(self):
        self.timer += 16.666
        if self.timer > self.duration * 1000:
            self.owner.effects.remove(self)    
    


    

class Nebunu(Effect):
    def __init__(self, owner, duration):
        Effect.__init__()
        self.timer = 60
        self.owner = None
        self.duration

class Stun(Effect):
    def __init__(self, owner, duration=3):
        super().__init__(owner, duration)    


class Cripple(Effect):
    def __init__(self, owner, duration=3):
        super().__init__(owner, duration)