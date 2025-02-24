import pygame
import data
import variables

class Ability:
    def __init__(self, owner):
        self.id = 0
        self.owner = owner
        self.timer = 0
        self.cooldown_max = 0
        self.update_stats()



    def tick(self):
        step = 16.6666
        if variables.speedup:
            step *= 2.0
        self.timer += step

    def activate_ability(self):
        self.timer = 0

    def is_ready(self):
        return self.timer > self.cooldown_max * 1000
    
    def update_stats(self):
        self.cooldown_max = data.ABILITY_COOLDOWN[self.id]

    def refresh_cooldown(self):
        self.timer = self.cooldown_max + 1
            



class MoabAssassin(Ability):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 0
        self.timer = self.cooldown_max * 1000
        self.update_stats()

    def activate_ability(self):
        if self.owner is None:
            return
        target = self.owner.strong_infinite_range_targeting()

        if target is None:
            return
        
        angle = self.owner.get_angle_towards_target(target)
        self.owner.summon_projectile(_angle=angle, _projectile_id=5, _damage = 750, _pierce = 1, _lifetime = 9999, _speed = 50)
        self.timer = 0


class MoabElim(Ability):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 1
        self.timer = self.cooldown_max * 1000
        self.update_stats()


    def activate_ability(self):
        if self.owner is None:
            return
        target = self.owner.strong_infinite_range_targeting()

        if target is None:
            return
        
        angle = self.owner.get_angle_towards_target(target)
        self.owner.summon_projectile(_angle=angle, _projectile_id=6, _damage = 4500, _pierce = 1, _lifetime = 9999, _speed = 50)
        self.timer = 0