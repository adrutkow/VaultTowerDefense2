import pygame
import data
import funcs
import variables
from classes.ui import Button, BuyIcon, Sidebar, TowerMenu, FloatingText
from classes.bloon import Bloon

class Scene:
    def scene_tick(self):
        pygame.display.update()

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

                try:
                
                    if variables.completed_maps[i][j] == 0:
                        funcs.draw_image(data.STAR_EMPTY, x, y)
                    else:
                        funcs.draw_image(data.STAR_FULL, x, y)
                except:
                    continue




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
        Scene.add_buttons_to_scene(self, range(19, 44))
        self.map_id = map_id
        self.difficulty = difficulty
        self.bloons = []
        self.towers = []
        self.ability_towers = []
        self.grouped_abilities = []
        self.waypoints = []
        self.projectiles = []
        self.particles = []
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

        self.draw_sidebar()
        self.get_waypoints()

        self.spawner = self.waypoints[0]
        self.despawner = self.waypoints[-1]
        self.round_spawner = RoundSpawner(self.spawner, self.difficulty)

        pygame.display.update()


    def draw_sidebar(self):
        funcs.draw_image(data.SIDEBAR, 1169, 0)
        for i in self.buy_icons:
            i.tick()

    def tick(self):
        funcs.draw_image(data.MAPS[self.map_id], 0, 0)
        self.timer += 1

        self.round_spawner.tick()

        for i in self.bloons:
            i.tick()

        for i in self.towers:
            i.tick()

        for i in self.projectiles:
            i.tick()

        for i in self.particles:
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

        funcs.draw_image(data.HEART, 0, 5)
        funcs.draw_image(data.GOLD, 0, 50)
        funcs.draw_text(self.lives, 55, 0, size=45, shadow=True)
        funcs.draw_text(int(self.gold), 55, 45, size=45, shadow=True)
        funcs.draw_text("Round "+str(self.round_spawner.round+1)+"/"+str(self.round_spawner.max_rounds), 900, 0, size=40, shadow=True)
        if self.win:
            funcs.draw_image(data.WIN_SCREEN, 200, 300)

        self.draw_abilities()



        pygame.display.update(0, 0, 1169, 768)

    def add_floating_text(self, text, x, y, size=30, speed=1, lifetime=3, color=(255,255,255)):
        self.particles.append(FloatingText(text, x, y, size=size, speed=speed, lifetime=lifetime, color=color))

    def activate_ability(self, slot):
        print("trying to active ability number "+str(slot))
        for tower in self.grouped_abilities[slot][1]:
            if tower.is_ability_ready():
                tower.activate_ability()
                break



    def on_bought_ability(self, tower):
        if not tower in self.ability_towers:
            self.ability_towers.append(tower)
        self.grouped_abilities = self.get_grouped_ability_list()
        print("BOUGHT ABILITY")



    def get_grouped_ability_list(self):
        grouped_abilities = []

        for i, tower in enumerate(self.ability_towers):
            current_tower_ability_id = tower.ability.id

            ability_already_accounted = False
            for ability_slot in grouped_abilities:
                ability_id = ability_slot[0]
                ability_tower_list = ability_slot[1]

                if current_tower_ability_id == ability_id:
                    ability_tower_list.append(tower)
                    ability_already_accounted = True
            
            if not ability_already_accounted:
                grouped_abilities.append([current_tower_ability_id, [tower]])
        return grouped_abilities

    def draw_abilities(self):
        
        # ID  [Tower list]
        # [[1, [tower, tower, tower]], [2, [tower]]]

        i = 0
        for ability_id, tower_list in self.grouped_abilities:

            ability_count = len(tower_list)
            ready_ability_count = 0

            for tower in tower_list:
                if tower.is_ability_ready():
                    ready_ability_count += 1

            x = 100 + i * 100
            y = 700
            funcs.draw_image(data.ABILITY_IMAGES[ability_id], x, y, final_x=75, final_y=75)

            if ready_ability_count > 1:
                funcs.draw_text(ready_ability_count, x, y, 20, (255, 255, 255), True)
            if ready_ability_count == 0:
                # Get lowest ability cooldown
                min_value = 9999999
                min_value_tower = None
                
                for tower in tower_list:

                    remaining_time = max(0, tower.ability.cooldown_max * 1000 - tower.ability.timer) / 1000
                    if remaining_time < min_value:
                        min_value = remaining_time
                        min_value_tower = tower

                funcs.draw_text(str(int(min_value)) + "s", x, y, 20, (255, 255, 255), True)



            i += 1


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


    def next_round_button(self):
        if self.round_playing:
            variables.speedup = not variables.speedup
            return
        scene = data.CLIENT.scene
        self.round_playing = True
        self.round += 1
        scene.round_paid = False
        if scene.round_spawner.round > len(data.ROUND_DATA)-1:
            scene.round_spawner.round = len(data.ROUND_DATA)-1
            print("REACHED MAX ROUND")
        self.current_list = data.ROUND_DATA[scene.round_spawner.round].copy()


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


class Waypoint:
    def __init__(self, x, y, previous=None, ahead=None, is_spawn=False, is_despawn=False):
        self.x = x
        self.y = y
        self.previous = previous
        self.ahead = ahead
        self.is_spawn = is_spawn
        self.is_despawn = is_despawn