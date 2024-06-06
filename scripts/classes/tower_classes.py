from classes.tower import Tower
from classes.projectile import Projectile
import math
import data
import funcs
from classes.ability import MoabAssassin, MoabElim


class DummyTower(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 0)

    def tick(self):
        Tower.tick(self)


    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size = tower_data

        if self.upgrade[0] >= 1:
            pass
        if self.upgrade[0] >= 2:
            pass
        if self.upgrade[0] >= 3:
            pass
        if self.upgrade[0] >= 4:
            pass
        if self.upgrade[0] >= 5:
            pass

        if self.upgrade[1] >= 1:
            pass
        if self.upgrade[1] >= 2:
            pass
        if self.upgrade[1] >= 3:
            pass
        if self.upgrade[1] >= 4:
            pass
        if self.upgrade[1] >= 5:
            pass

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size]


class DubstepCat(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 0)
        self.current_projectile_id = 4
        self.base_lead = True
        self.base_bomb = True

    def tick(self):
        Tower.tick(self)

    def on_bought_upgrade(self, path):
        super().on_bought_upgrade(path)
        if path == 1:
            if self.upgrade[1] == 4:
                self.give_ability(MoabAssassin)
            if self.upgrade[1] == 5:
                self.give_ability(MoabElim)

    def shoot(self, target):
        angle = self.get_angle_towards_target(target)
        self.summon_projectile(_angle = angle, _bomb = True)

    def on_target_hit(self, projectile, target):
        super().on_target_hit(projectile, target)
        if projectile.bomb:
            self.summon_projectile(_x = projectile.x, _y = projectile.y, _projectile_id = 2, _speed = 0,
                                _damage = projectile.damage, _pierce = projectile.pierce, _lifetime = 15, _size = 30)
            projectile.pierce = 0

    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size = tower_data


        if self.upgrade[0] >= 1:
            pierce += 6
            projectile_size += 10
        if self.upgrade[0] >= 2:
            damage += 1
            pierce += 10
        if self.upgrade[0] >= 3:
            projectile_size += 18
            damage = 3
            pierce += 30
        if self.upgrade[0] >= 4:
            range += 50
        if self.upgrade[0] >= 5:
            damage += 9

        if self.upgrade[1] >= 1:
            attack_speed = self.base_attack_speed * 0.75
        if self.upgrade[1] >= 2:
            attack_speed *= 0.73333
            range += 20
        if self.upgrade[1] >= 3:
            moab_bonus = 16
            range += 10
        if self.upgrade[1] >= 4:
            range += 20
            ceramic_bonus = 5
            moab_bonus = 31
        if self.upgrade[1] >= 5:
            moab_bonus = 100
             

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size]


class Salt(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 1)
        self.current_projectile_id = 2
        

    def tick(self):
        Tower.tick(self)
        #self.tick_attack_speed_timer()

    def attempt_shot(self):
        target = self.strong_infinite_range_targeting()
        if target is not None:
            self.target_location_shoot(target)

    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size = tower_data

        if self.upgrade[0] >= 1:
            pierce += 1
        if self.upgrade[0] >= 2:
            pierce += 2
        if self.upgrade[0] >= 3:
            pierce += 22
            lifetime = 100
            projectile_id = 1
        if self.upgrade[0] >= 4:
            pierce = 50
            damage += 1
            speed += 5
        if self.upgrade[0] >= 5:
            pierce = 200
            damage = 5
            speed += 5

        if self.upgrade[1] >= 1:
            damage += 1
            pierce += 1
        if self.upgrade[1] >= 2:
            pierce += 3
            lead = True
        if self.upgrade[1] >= 3:
            targeting = 1
            projectile_id = 2
            pierce += 50
            damage = 3
        if self.upgrade[1] >= 4:
            damage = 6
        if self.upgrade[1] >= 5:
            damage = 10
            pierce += 50

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus,
                ceramic_bonus, projectile_size]


class Spood(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 2)

    def tick(self):
        Tower.tick(self)
        #self.tick_attack_speed_timer()

    def attempt_shot(self):
        if self.upgrade[0] > 2:
            target = self.strong_infinite_range_targeting()
        else:
            target = self.first_infinite_range_targeting()
        if target is not None:
            self.target_location_shoot(target)

    def on_target_hit(self, projectile, target):
        if self.upgrade[0] == 4:
            if target.id == 11:
                target.stun(3)
            if target.id == 12:
                target.stun(1.5)
            if target.id == 13 or target.id == 14:
                target.stun(0.75)

        if self.upgrade[0] == 5:
            if target.id == 11:
                target.cripple(7)
                target.stun(7)
            if target.id == 12:
                target.cripple(6)
                target.stun(6)
            if target.id == 13:
                target.cripple(3)
                target.stun(3)
            if target.id == 14:
                target.cripple(4)
                target.stun(4)
            if target.id == 15:
                target.cripple(0.75)


        return super().on_target_hit(projectile, target)


    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size = tower_data

        targeting = 2
        if self.upgrade[0] >= 1:
            damage = 4
        if self.upgrade[0] >= 2:
            damage = 7
        if self.upgrade[0] >= 3:
            damage = 20
            ceramic_bonus = 15
        if self.upgrade[0] >= 4:
            damage = 30
            ceramic_bonus = 15
        if self.upgrade[0] >= 5:
            damage = 280
            ceramic_bonus = 15

        if self.upgrade[1] >= 1:
            attack_speed = 1.11
        if self.upgrade[1] >= 2:
            attack_speed = 0.8874
        if self.upgrade[1] >= 3:
            attack_speed = 0.2597
        if self.upgrade[1] >= 4:
            attack_speed = 0.1299
            moab_bonus = 2
        if self.upgrade[1] >= 5:
            attack_speed = 0.0449
            moab_bonus = 4

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus,
                ceramic_bonus, projectile_size]


class Balou(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 3)
        self.wof_timer = 99999
        self.wof_timer_max = 12

    def tick(self):
        Tower.tick(self)
        #self.tick_attack_speed_timer()
        self.handle_wof()

    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size = tower_data

        if self.upgrade[0] >= 1:
            damage = 2
        if self.upgrade[0] >= 2:
            damage = 3
        if self.upgrade[0] >= 3:
            damage = 5
            attack_speed *= 0.5
        if self.upgrade[0] >= 4:
            moab_bonus = 12
            damage = 8
        if self.upgrade[0] >= 5:
            moab_bonus = 24
            damage = 12
            attack_speed *= 0.5

        if self.upgrade[1] >= 1:
            lead = True
        if self.upgrade[1] >= 2:
            pass
        if self.upgrade[1] >= 3:
            damage = 2
        if self.upgrade[1] >= 4:
            damage = 4
            self.wof_timer_max = 10
            self.current_pierce = 500
        if self.upgrade[1] >= 5:
            damage = 10
            self.current_pierce = 1500
            self.wof_timer_max = 8

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus,
                ceramic_bonus, projectile_size]

    def handle_wof(self):
        """Function handling Balou's wall of fire, it checks he WOF timer and spawns it when ready"""
        if self.upgrade[1] >= 2:
            self.wof_timer += 1
            if self.wof_timer >= self.wof_timer_max * 60:
                bloons = data.CLIENT.scene.bloons
                if bloons:
                    min_distance = 9999
                    min_bloon = None
                    for i in bloons:
                        distance = math.dist([self.x, self.y], [i.x, i.y])
                        if distance < min_distance:
                            min_distance = distance
                            min_bloon = i
                    if min_distance <= self.current_range + 50:
                        spawn_pos_x = min_bloon.x
                        spawn_pos_y = min_bloon.y
                        data.CLIENT.scene.projectiles.append(Projectile(spawn_pos_x, spawn_pos_y, 3, 0, self.current_damage, 150, 8*60, 0, True, True, self))
                        self.wof_timer = 0


class Slav(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 4)

    def tick(self):
        Tower.tick(self)

    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size = tower_data

        if self.upgrade[0] >= 1:
            damage += 40
        if self.upgrade[0] >= 2:
            damage += 40
        if self.upgrade[0] >= 3:
            damage += 160
        if self.upgrade[0] >= 4:
            damage = 1500
        if self.upgrade[0] >= 5:
            damage = 10000

        if self.upgrade[1] >= 1:
            pass
        if self.upgrade[1] >= 2:
            pass
        if self.upgrade[1] >= 3:
            pass
        if self.upgrade[1] >= 4:
            pass
        if self.upgrade[1] >= 5:
            pass

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size]

    def generate_money(self):
        self.update_stats()
        gold_generated = self.current_damage
        data.CLIENT.scene.gold += gold_generated
        self.add_pops(gold_generated)


class Anonymous(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 5)
        self.knockback_force = 1

    def tick(self):
        Tower.tick(self)
        #self.tick_attack_speed_timer()


    def attempt_shot(self):
        self.get_bloons_in_range()
        for i in self.bloons_in_range:
            if "nebunu" not in i.effects:
                i.effects.append("nebunu")



    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size = tower_data

        if self.upgrade[0] >= 1:
            range += 50
        if self.upgrade[0] >= 2:
            range += 100
        if self.upgrade[0] >= 3:
            self.knockback_force = 2
        if self.upgrade[0] >= 4:
            moab_bonus = 1
        if self.upgrade[0] >= 5:
            self.knockback_force = 4

        if self.upgrade[1] >= 1:
            attack_speed *= 0.85
        if self.upgrade[1] >= 2:
            attack_speed *= 0.5
        if self.upgrade[1] >= 3:
            damage += 1
        if self.upgrade[1] >= 4:
            damage += 2
        if self.upgrade[1] >= 5:
            damage = 5

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size]


class Ajeaje(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 6)

    def tick(self):
        Tower.tick(self)


    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size = tower_data

        if self.upgrade[0] >= 1:
            pass
        if self.upgrade[0] >= 2:
            pass
        if self.upgrade[0] >= 3:
            pass
        if self.upgrade[0] >= 4:
            pass
        if self.upgrade[0] >= 5:
            pass

        if self.upgrade[1] >= 1:
            pass
        if self.upgrade[1] >= 2:
            pass
        if self.upgrade[1] >= 3:
            pass
        if self.upgrade[1] >= 4:
            pass
        if self.upgrade[1] >= 5:
            pass

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size]


class Speed(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 7)

    def tick(self):
        Tower.tick(self)


    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size = tower_data

        if self.upgrade[0] >= 1:
            pass
        if self.upgrade[0] >= 2:
            pass
        if self.upgrade[0] >= 3:
            pass
        if self.upgrade[0] >= 4:
            pass
        if self.upgrade[0] >= 5:
            pass

        if self.upgrade[1] >= 1:
            pass
        if self.upgrade[1] >= 2:
            pass
        if self.upgrade[1] >= 3:
            pass
        if self.upgrade[1] >= 4:
            pass
        if self.upgrade[1] >= 5:
            pass

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size]


class Abnormal(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 8)

    def tick(self):
        Tower.tick(self)


    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size = tower_data

        if self.upgrade[0] >= 1:
            pass
        if self.upgrade[0] >= 2:
            pass
        if self.upgrade[0] >= 3:
            pass
        if self.upgrade[0] >= 4:
            pass
        if self.upgrade[0] >= 5:
            pass

        if self.upgrade[1] >= 1:
            pass
        if self.upgrade[1] >= 2:
            pass
        if self.upgrade[1] >= 3:
            pass
        if self.upgrade[1] >= 4:
            pass
        if self.upgrade[1] >= 5:
            pass

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size]


class Videogames1000(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 9)

    def tick(self):
        Tower.tick(self)


    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size = tower_data

        if self.upgrade[0] >= 1:
            pass
        if self.upgrade[0] >= 2:
            pass
        if self.upgrade[0] >= 3:
            pass
        if self.upgrade[0] >= 4:
            pass
        if self.upgrade[0] >= 5:
            pass

        if self.upgrade[1] >= 1:
            pass
        if self.upgrade[1] >= 2:
            pass
        if self.upgrade[1] >= 3:
            pass
        if self.upgrade[1] >= 4:
            pass
        if self.upgrade[1] >= 5:
            pass

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size]


class Goga(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 10)

    def tick(self):
        Tower.tick(self)
        


    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size = tower_data

        if self.upgrade[0] >= 1:
            pass
        if self.upgrade[0] >= 2:
            pass
        if self.upgrade[0] >= 3:
            pass
        if self.upgrade[0] >= 4:
            pass
        if self.upgrade[0] >= 5:
            pass

        if self.upgrade[1] >= 1:
            pass
        if self.upgrade[1] >= 2:
            pass
        if self.upgrade[1] >= 3:
            pass
        if self.upgrade[1] >= 4:
            pass
        if self.upgrade[1] >= 5:
            pass

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size]


class Minion(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 11)
        

    def tick(self):
        Tower.tick(self)
        #self.tick_attack_speed_timer()


    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size = tower_data


        if self.upgrade[0] >= 1:
            pierce += 1
        if self.upgrade[0] >= 2:
            pierce += 2
        if self.upgrade[0] >= 3:
            pierce += 22
            lifetime = 100
            projectile_id = 1
        if self.upgrade[0] >= 4:
            pierce = 50
            damage += 1
            speed += 5
        if self.upgrade[0] >= 5:
            pierce = 200
            damage = 5
            speed += 5

        if self.upgrade[1] >= 1:
            attack_speed = self.base_attack_speed * 0.85
        if self.upgrade[1] >= 2:
            attack_speed = self.base_attack_speed * 0.67
        if self.upgrade[1] >= 3:
            range += 40
            pierce += 1
            damage = 3
            camo = True
        if self.upgrade[1] >= 4:
            attack_speed = self.base_attack_speed * 0.5
            range += 40
            damage = 6
        if self.upgrade[1] >= 5:
             pierce = 10
             attack_speed = self.base_attack_speed * 0.2
             range += 40
             lead = True


        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus, projectile_size]
    
class_list = [DubstepCat, Salt, Spood, Balou,
                                    Slav, Anonymous, Ajeaje, Speed,
                                    Abnormal, Videogames1000, Goga,
                                    Minion]