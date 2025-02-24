import pygame
import data
from classes.projectile import Projectile
import funcs
import math
import variables

class Tower:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.base_damage = data.TOWER_DAMAGE_DATA[id]
        self.base_attack_speed = data.TOWER_AS_DATA[id]
        self.base_range = data.TOWER_RANGE_DATA[id]
        self.base_pierce = data.TOWER_PIERCE_DATA[id]
        self.current_range = self.base_range
        self.current_attack_speed = self.base_attack_speed
        self.current_damage = self.base_damage
        self.current_pierce = self.base_pierce
        self.current_lifetime = 30
        self.current_speed = 12
        self.current_projectile_id = 0
        self.base_projectile_size = 10
        self.current_projectile_size = self.base_projectile_size
        self.base_camo = False
        self.current_camo = False
        self.base_lead = False
        self.current_lead = False
        self.current_targeting = 0
        self.current_moab_bonus = 0
        self.current_ceramic_bonus = 0
        self.bonus = []
        self.bloons_in_range = []
        self.size = data.TOWER_SIZE_DATA[self.id]
        self.timer = 0
        self.upgrade = [0, 0]
        self.money_spent = data.TOWER_PRICE_DATA[self.id]
        self.pops = 0
        self.image_reference = data.TOWER_IMAGES[self.id]
        self.upgrade_images_array = data.TOWER_UPGRADE_IMAGES[self.id]
        self.base_bomb = False
        self.current_bomb = False
        self.ability = None
        self.update_stats()

    def draw(self):
        image = self.image_reference
        image = pygame.transform.rotate(self.image_reference, self.timer/10)
        image_rect = image.get_rect(center = (self.x, self.y))
        funcs.draw_image(image, self.x, self.y, rect=image_rect)
        #data.WINDOW.blit(image, image_rect)
        if data.CLIENT.scene.tower_menu.get_tower_select() == self:
            pygame.draw.circle(data.WINDOW, (255, 0, 0), (self.x, self.y), self.current_range, 3)
            pygame.draw.circle(data.WINDOW, (0, 0, 0), (self.x, self.y), self.size, 1)

    def tick(self):
        frame_time = 16.666
        self.timer += frame_time
        self.tick_attack_speed_timer()
        if self.ability is not None:
            self.ability.tick()
        self.draw()

    def tick_attack_speed_timer(self):
        if self.timer >= self.current_attack_speed * 1000:
            self.attempt_shot()

    def attempt_shot(self):
        target = self.get_target()
        if target is not None:
            self.update_stats()
            self.shoot(target)

    def add_pops(self, count):
        self.pops += count

    def default_targeting(self):
        """This is the default tower targeting, attempts to shoot the first bloon in range"""
        if self.current_targeting == 0:
            self.get_bloons_in_range()
            max = 0
            target = None
            for i in self.bloons_in_range:
                if i.distance_travelled > max:
                    max = i.distance_travelled
                    target = i
            if target is not None:
                self.timer = 0
                return target
            else:
                return None


    def strong_infinite_range_targeting(self):
        """This targeting mode targets the strongest bloon on screen"""
        max_RBE = 0
        target = None
        for i in data.CLIENT.scene.bloons:
            if data.BLOON_RBE_DATA[i.id] > max_RBE:
                max_RBE = data.BLOON_RBE_DATA[i.id]
                target = i
        if target is not None:
            self.timer = 0
            return target
        else:
            return None


    def first_infinite_range_targeting(self):
        """This targeting mode targets the first bloon on screen"""
        target = None
        max = 0
        for i in data.CLIENT.scene.bloons:
            if i.distance_travelled > max:
                max = i.distance_travelled
                target = i
        if target is not None:
            self.timer = 0
            return target
        else:
            return

    def get_target(self):
        target = self.default_targeting()
        return target
    
    def get_angle_towards_target(self, target):
        if target is None:
            return
        return math.atan2(target.y - self.y, target.x - self.x)

    def shoot(self, target):
        """Default shot, throw projectile into target direction"""
        angle = self.get_angle_towards_target(target)
        self.summon_projectile(_angle=angle)
        # data.CLIENT.scene.projectiles.append(
        #     Projectile(self.x, self.y, self.current_projectile_id, angle, self.current_damage,
        #                self.current_pierce, self.current_lifetime, self.current_speed, self.current_camo,
        #                self.current_lead, self))
        
    def summon_projectile(self, _x = None, _y = None, _projectile_id = None, _angle = None, _damage = None, _pierce = None, _lifetime = None, _speed = None, _camo = None, _lead = None, _owner = None, _bomb = False, _size = None):
        if _x is None: _x = self.x
        if _y is None: _y = self.y
        if _projectile_id is None: _projectile_id = self.current_projectile_id
        if _angle is None: _angle = 0
        if _damage is None: _damage = self.current_damage
        if _pierce is None: _pierce = self.current_pierce
        if _lifetime is None: _lifetime = self.current_lifetime
        if _speed is None: _speed = self.current_speed
        if _camo is None: _camo = self.current_camo
        if _lead is None: _lead = self.current_lead
        if _owner is None: _owner = self
        if _size is None: _size = 10

        data.CLIENT.scene.projectiles.append(
            Projectile(_x, _y, _projectile_id, _angle, _damage, _pierce, _lifetime, _speed, _camo, _lead, _owner, _bomb, _size))


    def target_location_shoot(self, target):
        """Summons the projectile at target location"""
        data.CLIENT.scene.projectiles.append(Projectile(target.x, target.y, self.current_projectile_id, 0, self.current_damage, self.current_pierce, self.current_lifetime, 0, self.current_camo, self.current_lead, self))

    def on_target_hit(self, projectile, target):
        """Function called on projectile hitting a target"""
        pass


    def get_bloons_in_range(self):
        self.bloons_in_range = []
        for i in data.CLIENT.scene.bloons:
            if i.camo and self.current_camo == False:
                continue
            #if math.dist((self.x, self.y), (i.x, i.y)) <= self.current_range:
            #    self.bloons_in_range.append(i)
            if funcs.circle_collision((self.x, self.y, self.current_range), (i.x, i.y, i.size)):
               self.bloons_in_range.append(i)

    def is_clicked(self, x, y):
        return funcs.is_in_circle((x, y), (self.x, self.y, self.size))

    def sell(self):
        scene = data.CLIENT.scene
        scene.towers.remove(self)
        scene.gold += self.money_spent / 100 * 75

    def on_bought_upgrade(self, path):
        if self.upgrade_images_array is not None:
            current_upgrade = self.upgrade[path]
            print("CURRENT UPGR " + str(current_upgrade))

            opposite_path = funcs.get_opposite_path(path)
            if self.upgrade[opposite_path] > self.upgrade[path]:
                return


            if self.upgrade_images_array[path][current_upgrade - 1] is not None:
                self.image_reference = self.upgrade_images_array[path][current_upgrade - 1]
            self.timer = 0
            pass

    
    def give_ability(self, ability_class):
        self.ability = ability_class(self)
        data.CLIENT.scene.on_bought_ability(self)


    def is_ability_ready(self):
        if self.ability is None:
            return False
        return self.ability.is_ready()
    

    def activate_ability(self):
        print("trying to activate ability")
        if self.is_ability_ready():
            self.ability.activate_ability()
        

    def buy_upgrade(self, path):
        scene = data.CLIENT.scene
        gold = scene.gold
        if path == 0:
            price = data.TOWER_FIRSTPATH_PRICE[self.id][self.upgrade[0]]
            if gold >= price:
                scene.gold -= price
                self.upgrade[0] += 1
                self.money_spent += price
            else:
                return

        if path == 1:
            price = data.TOWER_FIRSTPATH_PRICE[self.id][self.upgrade[1]]
            if gold >= price:
                scene.gold -= price
                self.upgrade[1] += 1
                self.money_spent += price
            else:
                return

        self.update_stats()
        self.on_bought_upgrade(path)
        data.CLIENT.scene.tower_menu.update_image()

    def update_stats(self):
        attack_speed = self.base_attack_speed
        range = self.base_range
        damage = self.base_damage
        pierce = self.base_pierce
        lifetime = 30
        speed = 12
        projectile_id = self.current_projectile_id
        projectile_size = self.base_projectile_size
        camo = self.base_camo
        lead = self.base_lead
        targeting = self.current_targeting
        moab_bonus = 0
        ceramic_bonus = 0
        

        default_tower_data = [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead,
                              targeting, moab_bonus, ceramic_bonus, projectile_size]

        new_tower_data = self.get_upgrade_stats(default_tower_data)

        self.current_attack_speed = new_tower_data[0]
        self.current_range = new_tower_data[1]
        self.current_damage = new_tower_data[2]
        self.current_pierce = new_tower_data[3]
        self.current_lifetime = new_tower_data[4]
        self.current_speed = new_tower_data[5]
        self.current_projectile_id = new_tower_data[6]
        self.current_camo = new_tower_data[7]
        self.current_lead = new_tower_data[8]
        self.current_targeting = new_tower_data[9]
        self.current_moab_bonus = new_tower_data[10]
        self.current_ceramic_bonus = new_tower_data[11]
