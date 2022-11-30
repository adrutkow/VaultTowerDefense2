import funcs
import data
import variables
import math
import pygame


class Client:
    def __init__(self):
        self.scene = MainMenu()

    def tick(self):
        self.scene.tick()
        pygame.display.update()
        update_speed = 120 if variables.speedup else 60
        data.CLOCK.tick(update_speed)


class Scene:
    def scene_tick(self):
        pass

    def add_buttons_to_scene(self, buttons_id):
        for i in buttons_id:
            self.buttons.append(Button(i))


class MainMenu(Scene):
    def __init__(self):
        self.id = 0
        self.buttons = []
        Scene.add_buttons_to_scene(self, range(0, 5))

    def tick(self):
        self.scene_tick()
        funcs.draw_image(data.MENU_SCREEN, 0, 0)


class MapSelect(Scene):
    def __init__(self):
        self.id = 1
        self.buttons = []
        Scene.add_buttons_to_scene(self, range(5, 15))

    def tick(self):
        self.scene_tick()
        funcs.draw_image(data.MAP_SELECT_SCREEN, 0, 0)

        for i in range(0, 10):
            for j in range(0, 3):
                x = 30+j*80 + i * 270 if i < 5 else 30+j*80 + (i-5) * 270
                y = 200 if i < 5 else 480
                if variables.completed_maps[i][j] == 0:
                    funcs.draw_image(data.STAR_EMPTY, x, y)
                else:
                    funcs.draw_image(data.STAR_FULL, x, y)


class DifficultySelect(Scene):
    def __init__(self, map_id=0):
        self.buttons = []
        self.id = 2
        Scene.add_buttons_to_scene(self, range(15, 19))
        self.map_id = map_id

    def tick(self):
        self.scene_tick()
        funcs.draw_image(data.DIFFICULTY_SELECT_SCREEN, 0, 0)


class Game(Scene):
    def __init__(self, map_id=0, difficulty=0):
        self.buttons = []
        self.id = 3
        Scene.add_buttons_to_scene(self, range(19, 37))
        self.map_id = map_id
        self.difficulty = difficulty
        self.bloons = []
        self.towers = []
        self.waypoints = []
        self.projectiles = []
        self.timer = 0
        self.lives = 100
        self.gold = 650
        self.buy_icons = []
        self.win = False
        for i in range(0, 12):
            self.buy_icons.append(BuyIcon(i))
        self.sidebar = Sidebar()
        self.tower_menu = TowerMenu()
        self.round_paid = True


        self.get_waypoints()

        self.spawner = self.waypoints[0]
        self.despawner = self.waypoints[-1]
        self.round_spawner = RoundSpawner(self.spawner, self.difficulty)
        self.round_spawner = RoundSpawner(self.spawner, self.difficulty)


    def tick(self):
        self.scene_tick()
        funcs.draw_image(data.MAPS[self.map_id], 0, 0)
        self.timer += 1

        self.round_spawner.tick()

        for i in self.bloons:
            i.tick()

        for i in self.towers:
            i.tick()

        for i in self.projectiles:
            i.tick()

        if not self.round_paid:
            if len(self.bloons) == 0 and len(self.round_spawner.current_list) == 0:
                self.gold += 100 + self.round_spawner.round + 1
                self.round_paid = True
                for i in self.towers:
                    if i.id == 4:
                        i.generate_money()
                if self.win == False and self.round_spawner.round+1 == self.round_spawner.max_rounds:
                    self.win = True



        self.sidebar.tick()
        self.tower_menu.tick()

        funcs.draw_image(data.SIDEBAR, 1169, 0)
        funcs.draw_image(data.HEART, 0, 5)
        funcs.draw_image(data.GOLD, 0, 50)
        funcs.draw_text(self.lives, 55, 0, size=45, shadow=True)
        funcs.draw_text(int(self.gold), 55, 45, size=45, shadow=True)
        funcs.draw_text("Round "+str(self.round_spawner.round+1)+"/"+str(self.round_spawner.max_rounds), 900, 0, size=40, shadow=True)
        if self.win:
            funcs.draw_image(data.WIN_SCREEN, 200, 300)

        for i in self.buy_icons:
            i.tick()

    def spawn_bloon(self, id, camo=False, lead=False):
        self.bloons.append(Bloon(id, self.spawner, camo=camo, lead=lead))

    def get_waypoints(self):
        n = 0
        for i in data.WAYPOINTS_DATA[self.map_id]:
            if n == 0:
                self.waypoints.append(Waypoint(i[0], i[1], is_spawn=True))
            elif n == len(data.WAYPOINTS_DATA[self.map_id]):
                self.waypoints.append(Waypoint(i[0], i[1], is_despawn=True))
            else:
                self.waypoints.append(Waypoint(i[0], i[1]))
            n += 1
        for i in range(0, len(self.waypoints)-1):
            if i != 0:
                self.waypoints[i].previous = self.waypoints[i-1]
            if i != len(self.waypoints)-1:
                self.waypoints[i].ahead = self.waypoints[i+1]


class Button:
    def __init__(self, id):
        button_data = data.BUTTON_DATA[id]
        self.id = id
        self.x, self.y, self.w, self.h = button_data
        self.active = True

    def tick(self):
        print(self.id)
        scene = data.CLIENT.scene
        # Play button
        if self.id == 0:
            data.CLIENT.scene = MapSelect()

        # Exit button
        if self.id == 4:
            variables.running = False

        # Map button
        if 4 < self.id < 15:
            data.CLIENT.scene = DifficultySelect(self.id-5)

        if 15 < self.id < 19:
            data.CLIENT.scene = Game(map_id=data.CLIENT.scene.map_id, difficulty=self.id-16)

        # Go back to menu button
        if self.id == 15:
            data.CLIENT.scene = MainMenu()

        if 19 <= self.id <= 30:
            select = self.id - 19
            data.CLIENT.scene.sidebar.select = select

        if 31 <= self.id <= 33:
            if data.CLIENT.scene.tower_menu.tower_select is not None:
                select = data.CLIENT.scene.tower_menu.tower_select
                if self.id == 33:
                    select.sell()
                    data.CLIENT.scene.tower_menu.tower_select = None
                if self.id == 31:
                    # Upgrade 1st path
                    if select.upgrade[1] > 2:
                        if select.upgrade[0] < 2:
                            select.buy_upgrade(0)
                    elif select.upgrade[0] < 5:
                        select.buy_upgrade(0)

                if self.id == 32:
                    # Upgrade 2nd path
                    if select.upgrade[0] > 2:
                        if select.upgrade[1] < 2:
                            select.buy_upgrade(1)
                    elif select.upgrade[1] < 5:
                        select.buy_upgrade(1)

        if self.id == 34:
            if not scene.round_spawner.round_playing:
                scene.round_spawner.round_playing = True
                scene.round_spawner.round += 1
                scene.round_paid = False
                if scene.round_spawner.round > len(data.ROUND_DATA)-1:
                    scene.round_spawner.round = len(data.ROUND_DATA)-1
                    print("REACHED MAX ROUND")
                scene.round_spawner.current_list = data.ROUND_DATA[scene.round_spawner.round]
        if self.id == 35:
            variables.speedup = not variables.speedup
        if self.id == 36:
            if scene.win:
                map_id = scene.map_id
                difficulty = scene.difficulty
                variables.completed_maps[map_id][difficulty] = 1
                funcs.update_savefile()
                data.CLIENT.scene = MainMenu()


    def is_inside(self, x, y):
        return self.x < x < self.x + self.w and self.y < y < self.y + self.h

    def check_click(self, x, y):
        if self.active:
            if self.is_inside(x, y):
                self.tick()


class Waypoint:
    def __init__(self, x, y, previous=None, ahead=None, is_spawn=False, is_despawn=False):
        self.x = x
        self.y = y
        self.previous = previous
        self.ahead = ahead
        self.is_spawn = is_spawn
        self.is_despawn = is_despawn


class Bloon:
    def __init__(self, id, waypoint=None, x=None, y=None, lifetime=0, distance_travelled=0, camo=False, lead=False):
        self.id = id
        self.angle = 0
        self.last_waypoint = waypoint
        self.current_waypoint = waypoint.ahead
        self.w = 49
        self.h = 63
        self.speed = data.BLOON_SPEED_DATA[self.id] * data.BLOON_SPEED_MULTIPLIER
        self.lifetime = lifetime
        self.distance_travelled = distance_travelled
        self.health = data.BLOON_HP_DATA[self.id]
        self.camo = camo
        self.lead = lead
        self.effects = []
        if self.id == 7 or self.id == 14:
            self.lead = True
        BLOON_IMAGES = []
        for i in range(0, 16):
            BLOON_IMAGES.append((pygame.image.load("assets/bloons/bloon_" + str(i) + ".png")).convert_alpha())
        if x is None:
            self.spawn()
        else:
            self.x = x
            self.y = y
            self.angle = math.atan2(self.current_waypoint.y - self.last_waypoint.y,
                                    self.current_waypoint.x - self.last_waypoint.x)


    def tick(self):
        self.lifetime += 1
        self.distance_travelled += self.speed
        modifier = 1
        if "nebunu" in self.effects:
            modifier = -1

        self.x += math.cos(self.angle) * self.speed * modifier
        self.y += math.sin(self.angle) * self.speed * modifier

        if math.dist((self.x+self.w/2, self.y+self.h/2), (self.current_waypoint.x, self.current_waypoint.y)) < 2:
            if self.current_waypoint.ahead is None:
                self.despawn()
                return
            self.x = self.current_waypoint.x - self.w/2
            self.y = self.current_waypoint.y - self.h/2
            self.last_waypoint = self.current_waypoint
            self.current_waypoint = self.last_waypoint.ahead
            self.angle = math.atan2(self.current_waypoint.y - self.last_waypoint.y,
                                    self.current_waypoint.x - self.last_waypoint.x)


        self.draw()

    def spawn(self):
        self.x = self.last_waypoint.x - self.w / 2
        self.y = self.last_waypoint.y - self.h / 2
        self.angle = math.atan2(self.current_waypoint.y - self.last_waypoint.y, self.current_waypoint.x - self.last_waypoint.x)


    def despawn(self):
        data.CLIENT.scene.bloons.remove(self)
        data.CLIENT.scene.lives -= data.BLOON_RBE_DATA[self.id]
        del self


    def pop(self):
        data.CLIENT.scene.bloons.remove(self)
        del self


    def spawn_children(self, projectile, children=None):
        if children is not None:
            for i in range(0, len(children)):
                distance = 10 + i * 10
                bloon = Bloon(children[i], self.last_waypoint,
                              self.x - math.cos(self.angle) * distance, self.y - math.sin(self.angle) * distance,
                              self.lifetime)
                projectile.already_hit.append(bloon)
                data.CLIENT.scene.bloons.append(bloon)
            return

        for i in range(0, len(data.BLOON_CHILDREN_DATA[self.id])):
            distance = 10+i*10
            bloon = Bloon(data.BLOON_CHILDREN_DATA[self.id][i], self.last_waypoint, self.x-math.cos(self.angle)*distance, self.y-math.sin(self.angle)*distance, self.lifetime, self.distance_travelled)
            projectile.already_hit.append(bloon)
            data.CLIENT.scene.bloons.append(bloon)

    def draw(self):
        if self.camo:
            funcs.draw_image(data.CAMO_BLOON_IMAGES[self.id], self.x, self.y)
        else:
            funcs.draw_image(data.BLOON_IMAGES[self.id], self.x, self.y)
        if "nebunu" in self.effects:
            funcs.draw_image(data.NEBUNU, self.x, self.y)


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
        self.current_camo = False
        self.current_lead = False
        self.current_targeting = 0
        self.current_moab_bonus = 0
        self.current_ceramic_bonus = 0
        self.bonus = []
        self.w = data.TOWER_IMAGES[self.id].get_width()
        self.h = data.TOWER_IMAGES[self.id].get_height()
        self.bloons_in_range = []
        self.size = 30
        self.timer = 0
        self.upgrade = [0, 0]
        self.money_spent = data.TOWER_PRICE_DATA[self.id]
        self.pops = 0

    def draw(self):
        image = data.TOWER_IMAGES[self.id]
        image = pygame.transform.rotate(image, self.timer)
        funcs.draw_image(image, self.x, self.y)
        if data.CLIENT.scene.tower_menu.tower_select == self:
            x = self.x + self.w/2
            y = self.y + self.h/2
            pygame.draw.circle(data.WINDOW, (255, 0, 0), (x, y), self.current_range, 3)

    def tick(self):
        self.timer += 1
        self.draw()

    def tick_attack_speed_timer(self):
        if self.timer >= self.current_attack_speed * 60:
            self.attempt_shot()

    def attempt_shot(self):
        target = self.get_target()
        if target is not None:
            self.get_stats()
            self.default_shoot(target)

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

    def default_shoot(self, target):
        """Default shot, throw projectile into target direction"""
        angle = math.atan2(target.y - self.y, target.x - self.x)
        data.CLIENT.scene.projectiles.append(
            Projectile(self.x + self.w / 2, self.y + self.h / 2, self.current_projectile_id, angle, self.current_damage,
                       self.current_pierce, self.current_lifetime, self.current_speed, self.current_camo,
                       self.current_lead, self))

    def target_location_shoot(self, target):
        """Summons the projectile at target location"""
        data.CLIENT.scene.projectiles.append(Projectile(target.x, target.y, self.current_projectile_id, 0, self.current_damage, self.current_pierce, self.current_lifetime, 0, self.current_camo, self.current_lead, self))

    def get_bloons_in_range(self):
        self.bloons_in_range = []
        for i in data.CLIENT.scene.bloons:
            if i.camo and self.current_camo == False:
                continue
            if math.dist((self.x, self.y), (i.x, i.y)) <= self.current_range:
                self.bloons_in_range.append(i)

    def is_clicked(self, x, y):
        return funcs.is_in_rect(x, y, self.x, self.y, self.w, self.h)

    def sell(self):
        scene = data.CLIENT.scene
        scene.towers.remove(self)
        scene.gold += self.money_spent / 100 * 75

    def buy_upgrade(self, path):
        scene = data.CLIENT.scene
        gold = scene.gold
        if path == 0:
            price = data.TOWER_FIRSTPATH_PRICE[self.id][self.upgrade[0]]
            if gold >= price:
                scene.gold -= price
                self.upgrade[0] += 1

        if path == 1:
            price = data.TOWER_FIRSTPATH_PRICE[self.id][self.upgrade[1]]
            if gold >= price:
                scene.gold -= price
                self.upgrade[1] += 1

    def get_stats(self):
        attack_speed = self.base_attack_speed
        range = self.base_range
        damage = self.base_damage
        pierce = self.base_pierce
        lifetime = 30
        speed = 12
        projectile_id = 0
        camo = False
        lead = False
        targeting = 0
        moab_bonus = 0
        ceramic_bonus = 0

        default_tower_data = [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead,
                              targeting, moab_bonus, ceramic_bonus]

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


class DummyTower(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 0)

    def tick(self):
        Tower.tick(self)


    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus = tower_data

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

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus]


class DubstepCat(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 0)

    def tick(self):
        Tower.tick(self)
        self.tick_attack_speed_timer()

    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus = tower_data


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
        if self.upgrade[1] >= 4:
            attack_speed = self.base_attack_speed * 0.5
            range += 40
            damage = 6
        if self.upgrade[1] >= 5:
             pierce = 10
             attack_speed = self.base_attack_speed * 0.2
             range += 40

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus]


class Salt(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 1)

    def tick(self):
        Tower.tick(self)
        self.tick_attack_speed_timer()

    def attempt_shot(self):
        target = self.strong_infinite_range_targeting()
        if target is not None:
            self.target_location_shoot(target)

    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus = tower_data

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
                ceramic_bonus]


class Spood(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 2)

    def tick(self):
        Tower.tick(self)
        self.tick_attack_speed_timer()

    def attempt_shot(self):
        target = self.strong_infinite_range_targeting()
        if target is not None:
            self.target_location_shoot(target)

    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus = tower_data

        targeting = 2
        if self.upgrade[0] >= 1:
            damage = 4
        if self.upgrade[0] >= 2:
            damage = 7
        if self.upgrade[0] >= 3:
            damage = 20
            ceramic_bonus = 15
        if self.upgrade[0] >= 4:
            moab_bonus = 35
            ceramic_bonus = 110
        if self.upgrade[0] >= 5:
            moab_bonus = 120

        if self.upgrade[1] >= 1:
            attack_speed = self.base_attack_speed * 0.70
        if self.upgrade[1] >= 2:
            attack_speed = self.base_attack_speed * 0.4
        if self.upgrade[1] >= 3:
            attack_speed /= 3
        if self.upgrade[1] >= 4:
            attack_speed /= 2
        if self.upgrade[1] >= 5:
            attack_speed /= 4

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus,
                ceramic_bonus]


class Balou(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 3)
        self.wof_timer = 99999
        self.wof_timer_max = 12

    def tick(self):
        Tower.tick(self)
        self.tick_attack_speed_timer()
        self.handle_wof()

    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus = tower_data

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
                ceramic_bonus]

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
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus = tower_data

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

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus]

    def generate_money(self):
        self.get_stats()
        gold_generated = self.current_damage
        data.CLIENT.scene.gold += gold_generated
        self.pops += gold_generated


class Glebu(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 5)
        self.knockback_force = 1

    def tick(self):
        Tower.tick(self)
        self.tick_attack_speed_timer()


    def attempt_shot(self):
        self.get_bloons_in_range()
        for i in self.bloons_in_range:
            if "nebunu" not in i.effects:
                i.effects.append("nebunu")



    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus = tower_data

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

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus]


class Ajeaje(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 6)

    def tick(self):
        Tower.tick(self)


    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus = tower_data

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

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus]


class Speed(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 7)

    def tick(self):
        Tower.tick(self)


    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus = tower_data

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

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus]


class Abnormal(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 8)

    def tick(self):
        Tower.tick(self)


    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus = tower_data

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

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus]


class Videogames1000(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 9)

    def tick(self):
        Tower.tick(self)


    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus = tower_data

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

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus]


class Goga(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 10)

    def tick(self):
        Tower.tick(self)


    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus = tower_data

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

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus]


class Minion(Tower):
    def __init__(self, x, y):
        Tower.__init__(self, x, y, 11)

    def tick(self):
        Tower.tick(self)


    def get_upgrade_stats(self, tower_data):
        attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus = tower_data

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

        return [attack_speed, range, damage, pierce, lifetime, speed, projectile_id, camo, lead, targeting, moab_bonus, ceramic_bonus]


class BuyIcon:
    def __init__(self, spot):
        self.spot = spot

    def tick(self):
        self.draw()

    def draw(self):
        x = 1177 + 82*(self.spot % 2)
        y = 115 + 96*int(self.spot/2)
        image = data.TOWER_IMAGES[self.spot]
        funcs.draw_image(image, x, y, 78, 92)
        funcs.draw_text(str(data.TOWER_PRICE_DATA[self.spot])+"$", x, y+70, 20)


class Sidebar:
    def __init__(self):
        self.select = None

    def tick(self):
        if self.select is not None:
            tower_image = data.TOWER_IMAGES[self.select]
            mouse_pos = pygame.mouse.get_pos()
            range = data.TOWER_RANGE_DATA[self.select]
            funcs.draw_image(tower_image, int(mouse_pos[0]-tower_image.get_width()/2), int(mouse_pos[1]-tower_image.get_height()/2))
            pygame.draw.circle(data.WINDOW, (255, 0, 0), (mouse_pos[0], mouse_pos[1]), range, 3)


class Projectile:
    def __init__(self, x, y, id, angle, damage, pierce, lifetime, speed, camo, lead, owner=None):
        self.x = x
        self.y = y
        self.angle = angle
        self.damage = damage
        self.pierce = pierce
        self.maxlifetime = lifetime
        self.lifetime = 0
        self.speed = speed
        self.already_hit = []
        self.id = id
        self.camo = camo
        self.lead = lead
        self.w = data.PROJECTILE_IMAGES[self.id].get_width()
        self.h = data.PROJECTILE_IMAGES[self.id].get_height()
        self.owner = owner

    def tick(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.lifetime += 1

        if self.lifetime > self.maxlifetime:
            self.die()
            return

        for i in data.CLIENT.scene.bloons:
            # if it's camo and we don't see camo, leave
            if i.camo and not self.camo:
                continue
            # if already hit, leave
            if i in self.already_hit:
                # if balou wof has 3rd upgrade, dont leave
                if self.owner.id == 3:
                    if self.owner.upgrade[1] >= 3:
                        pass
                    else:
                        continue
                else:
                    continue

            # if hit
            if funcs.rect_collision(self.x, self.y, self.w, self.h, i.x, i.y, i.w, i.h):
                scene = data.CLIENT.scene
                round = scene.round_spawner.round
                multiplier = 1
                if round > 100:
                    multiplier = 0.02
                elif round > 86:
                    multiplier = 0.1
                elif round > 61:
                    multiplier = 0.2
                elif round > 51:
                    multiplier = 0.5

                # if the bloon's RBE value is lower or equal to damage, pop it
                if data.BLOON_RBE_DATA[i.id] <= self.damage:
                    i.pop()
                    scene.gold += 1 * multiplier
                    self.owner.pops += data.BLOON_RBE_DATA[i.id]
                else:
                    # ALGORITHM FOR BLOONS
                    if i.id < 11:
                        children = []
                        # if the bloon has more hp than projectile has damage, just remove some hp from bloon
                        if i.health > self.damage:
                            i.health -= self.damage
                            self.owner.pops += self.damage
                            self.already_hit.append(i)
                        # if the hp and damage is exactly the same, simply spawn bloon's children
                        elif i.health == self.damage:
                            print("SPAWNED CHILDREN")
                            i.spawn_children(self)
                            i.pop()
                            scene.gold += 1 * multiplier
                            self.owner.pops += self.damage
                        # if the hp is lower than proj damage:
                        elif i.health < self.damage:
                            layer_down = 0
                            current_damage = self.damage
                            children = []
                            self.owner.pops += self.damage

                            while current_damage > 0:

                                i.health -= 1
                                current_damage -= 1

                                if i.health <= 0:
                                    layer_down += 1
                                    scene.gold += 1 * multiplier
                                    print("ADDED GOLD")
                                    i.health = data.BLOON_HP_DATA[i.id-layer_down]

                                    if i.id - layer_down == 0:
                                        if len(children) > 0:
                                            children.remove(children[-1])
                                    else:
                                        if children == []:
                                            children = data.BLOON_CHILDREN_DATA[i.id]
                                        else:
                                            new_children = []
                                            for j in children:
                                                for k in data.BLOON_CHILDREN_DATA[j]:
                                                    new_children.append(k)
                                            children = new_children

                            i.spawn_children(self, children)
                            i.pop()

                    # ALGORITHM FOR MOABS
                    else:
                        # if the moab has more hp than projectile has damage, just remove some hp from bloon
                        if i.health > self.damage:
                            i.health -= self.damage
                            self.already_hit.append(i)
                        # if the hp and damage is exactly the same, simply spawn moab's children
                        elif i.health == self.damage:
                            i.spawn_children(self)
                            i.pop()
                            scene.gold += 1 * multiplier
                        # if the hp is lower than projectile damage, spawn children anyway
                        elif i.health < self.damage:
                            i.spawn_children(self)
                            i.pop()
                            scene.gold += 1 * multiplier

                self.pierce -= 1
                if self.pierce <= 0:
                    self.die()
                    return


        self.draw()

    def die(self):
        data.CLIENT.scene.projectiles.remove(self)
        del self

    def draw(self):
        #pygame.draw.rect(data.WINDOW, (255, 255, 255), (self.x, self.y, 15, 15), 3)
        funcs.draw_image(data.PROJECTILE_IMAGES[self.id], self.x, self.y)


class TowerMenu:
    def __init__(self):
        self.tower_select = None

    def tick(self):
        if self.tower_select is not None:
            funcs.draw_image(data.TOWER_MENU, 0, 91)
            funcs.draw_text(data.TOWER_NAMES[self.tower_select.id]+str(self.tower_select.pops), 32, 104)
            funcs.draw_image(data.TOWER_IMAGES[self.tower_select.id], 65, 150, final_x=78, final_y=92)
            if self.tower_select.upgrade[0] < 5:
                funcs.draw_text(data.TOWER_FIRSTPATH_NAMES[self.tower_select.id][self.tower_select.upgrade[0]], 35, 255)
                funcs.draw_text(str(data.TOWER_FIRSTPATH_PRICE[self.tower_select.id][self.tower_select.upgrade[0]])+"$", 32, 300)
            else:
                funcs.draw_text("MAX!", 35, 255)
            if self.tower_select.upgrade[1] < 5:
                funcs.draw_text(data.TOWER_SECONDPATH_NAMES[self.tower_select.id][self.tower_select.upgrade[1]], 35, 346)
                funcs.draw_text(str(data.TOWER_SECONDPATH_PRICE[self.tower_select.id][self.tower_select.upgrade[1]])+"$", 32, 392)
            else:
                funcs.draw_text("MAX!", 35, 346)
            funcs.draw_text(str(int(self.tower_select.money_spent / 100 * 75))+"$", 26, 632)

            for i in range(0, self.tower_select.upgrade[1]):
                pygame.draw.rect(data.WINDOW, (0, 255, 0), (25, 374 - i*7, 6, 6))

            for i in range(0, self.tower_select.upgrade[0]):
                pygame.draw.rect(data.WINDOW, (0, 255, 0), (25, 284 - i*7, 6, 6))

            if self.tower_select.upgrade[1] > 2:
                funcs.draw_image(data.LIMIT, 25, 256)

            if self.tower_select.upgrade[0] > 2:
                funcs.draw_image(data.LIMIT, 25, 346)


class RoundSpawner:
    def __init__(self, waypoint, difficulty):
        self.waypoint = waypoint
        default_rounds = [-1, 3, 6]
        self.round = default_rounds[difficulty]
        b = [40, 80, 100]
        self.max_rounds = b[difficulty]
        self.round_playing = False
        self.timer = 0
        self.current_list = None


    def tick(self):
        if self.round_playing:

            if not self.current_list:
                self.round_playing = False
            else:
                self.timer += 1
                if self.timer >= self.current_list[0][1]:
                    camo = False
                    if len(self.current_list[0]) == 3:
                        camo = True
                    data.CLIENT.scene.spawn_bloon(self.current_list[0][0], camo=camo)
                    self.current_list.pop(0)
                    self.timer = 0
                    if len(self.current_list) == 0:
                        print(len(self.current_list))
                        print(self.current_list)
                        self.round_playing = False


class Effect:
    def __init__(self):
        self.id = 0




class Nebunu(Effect):
    def __init__(self):
        Effect.__init__()
        self.timer = 60
        self.owner = None