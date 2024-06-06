# import funcs
# import data
# import variables
# import math
# import pygame
# from classes.tower import Tower
# from classes.ui import BuyIcon, Sidebar, TowerMenu


# class Client:
#     def __init__(self):
#         self.scene = MainMenu()

#     def tick(self):
#         self.scene.tick()
#         update_speed = 120 if variables.speedup else 60
#         data.CLOCK.tick(update_speed)
        


# class Scene:
#     def scene_tick(self):
#         pygame.display.update()

#     def add_buttons_to_scene(self, buttons_id):
#         for i in buttons_id:
#             self.buttons.append(Button(i))


# class MainMenu(Scene):
#     def __init__(self):
#         self.id = 0
#         self.buttons = []
#         Scene.add_buttons_to_scene(self, range(0, 5))

#     def tick(self):
#         self.scene_tick()
#         funcs.draw_image(data.MENU_SCREEN, 0, 0)


# class MapSelect(Scene):
#     def __init__(self):
#         self.id = 1
#         self.buttons = []
#         Scene.add_buttons_to_scene(self, range(5, 15))

#     def tick(self):
#         self.scene_tick()
#         funcs.draw_image(data.MAP_SELECT_SCREEN, 0, 0)

#         for i in range(0, 10):
#             for j in range(0, 3):
#                 x = 30+j*80 + i * 270 if i < 5 else 30+j*80 + (i-5) * 270
#                 y = 200 if i < 5 else 480
#                 if variables.completed_maps[i][j] == 0:
#                     funcs.draw_image(data.STAR_EMPTY, x, y)
#                 else:
#                     funcs.draw_image(data.STAR_FULL, x, y)


# class DifficultySelect(Scene):
#     def __init__(self, map_id=0):
#         self.buttons = []
#         self.id = 2
#         Scene.add_buttons_to_scene(self, range(15, 19))
#         self.map_id = map_id

#     def tick(self):
#         self.scene_tick()
#         funcs.draw_image(data.DIFFICULTY_SELECT_SCREEN, 0, 0)


# class Game(Scene):
#     def __init__(self, map_id=0, difficulty=0):
#         self.buttons = []
#         self.id = 3
#         Scene.add_buttons_to_scene(self, range(19, 37))
#         self.map_id = map_id
#         self.difficulty = difficulty
#         self.bloons = []
#         self.towers = []
#         self.waypoints = []
#         self.projectiles = []
#         self.timer = 0
#         self.lives = 100
#         self.gold = 650
#         self.buy_icons = []
#         self.win = False
#         for i in range(0, 12):
#             self.buy_icons.append(BuyIcon(i))
#         self.sidebar = Sidebar()
#         self.tower_menu = TowerMenu()
#         self.round_paid = True

#         funcs.draw_image(data.SIDEBAR, 1169, 0)
#         for i in self.buy_icons:
#             i.tick()


#         self.get_waypoints()

#         self.spawner = self.waypoints[0]
#         self.despawner = self.waypoints[-1]
#         self.round_spawner = RoundSpawner(self.spawner, self.difficulty)
#         self.round_spawner = RoundSpawner(self.spawner, self.difficulty)

#         pygame.display.update()



#     def tick(self):
#         funcs.draw_image(data.MAPS[self.map_id], 0, 0)
#         self.timer += 1

#         self.round_spawner.tick()

#         for i in self.bloons:
#             i.tick()

#         for i in self.towers:
#             i.tick()

#         for i in self.projectiles:
#             i.tick()

#         if not self.round_paid:
#             if len(self.bloons) == 0 and len(self.round_spawner.current_list) == 0:
#                 self.gold += 100 + self.round_spawner.round + 1
#                 self.round_paid = True
#                 for i in self.towers:
#                     if i.id == 4:
#                         i.generate_money()
#                 if self.win == False and self.round_spawner.round+1 == self.round_spawner.max_rounds:
#                     self.win = True



#         self.sidebar.tick()
#         self.tower_menu.tick()

#         funcs.draw_image(data.HEART, 0, 5)
#         funcs.draw_image(data.GOLD, 0, 50)
#         funcs.draw_text(self.lives, 55, 0, size=45, shadow=True)
#         funcs.draw_text(int(self.gold), 55, 45, size=45, shadow=True)
#         funcs.draw_text("Round "+str(self.round_spawner.round+1)+"/"+str(self.round_spawner.max_rounds), 900, 0, size=40, shadow=True)
#         if self.win:
#             funcs.draw_image(data.WIN_SCREEN, 200, 300)



#         pygame.display.update(0, 0, 1169, 768)

#     def spawn_bloon(self, id, camo=False, lead=False):
#         self.bloons.append(Bloon(id, self.spawner, camo=camo, lead=lead))

#     def get_waypoints(self):
#         n = 0
#         for i in data.WAYPOINTS_DATA[self.map_id]:
#             if n == 0:
#                 self.waypoints.append(Waypoint(i[0], i[1], is_spawn=True))
#             elif n == len(data.WAYPOINTS_DATA[self.map_id]):
#                 self.waypoints.append(Waypoint(i[0], i[1], is_despawn=True))
#             else:
#                 self.waypoints.append(Waypoint(i[0], i[1]))
#             n += 1
#         for i in range(0, len(self.waypoints)-1):
#             if i != 0:
#                 self.waypoints[i].previous = self.waypoints[i-1]
#             if i != len(self.waypoints)-1:
#                 self.waypoints[i].ahead = self.waypoints[i+1]


# class Button:
#     def __init__(self, id):
#         button_data = data.BUTTON_DATA[id]
#         self.id = id
#         self.x, self.y, self.w, self.h = button_data
#         self.active = True

#     def tick(self):
#         print(self.id)
#         scene = data.CLIENT.scene
#         # Play button
#         if self.id == 0:
#             data.CLIENT.scene = MapSelect()

#         # Exit button
#         if self.id == 4:
#             variables.running = False

#         # Map button
#         if 4 < self.id < 15:
#             data.CLIENT.scene = DifficultySelect(self.id-5)

#         if 15 < self.id < 19:
#             data.CLIENT.scene = Game(map_id=data.CLIENT.scene.map_id, difficulty=self.id-16)

#         # Go back to menu button
#         if self.id == 15:
#             data.CLIENT.scene = MainMenu()

#         if 19 <= self.id <= 30:
#             select = self.id - 19
#             data.CLIENT.scene.sidebar.select = select

#         if 31 <= self.id <= 33:
#             if data.CLIENT.scene.tower_menu.get_tower_select() is not None:
#                 select = data.CLIENT.scene.tower_menu.get_tower_select()
#                 if self.id == 33:
#                     select.sell()
#                     data.CLIENT.scene.tower_menu.set_tower_select(None)
#                 if self.id == 31:
#                     # Upgrade 1st path
#                     if select.upgrade[1] > 2:
#                         if select.upgrade[0] < 2:
#                             select.buy_upgrade(0)
#                     elif select.upgrade[0] < 5:
#                         select.buy_upgrade(0)

#                 if self.id == 32:
#                     # Upgrade 2nd path
#                     if select.upgrade[0] > 2:
#                         if select.upgrade[1] < 2:
#                             select.buy_upgrade(1)
#                     elif select.upgrade[1] < 5:
#                         select.buy_upgrade(1)
                

#         if self.id == 34:
#             if not scene.round_spawner.round_playing:
#                 scene.round_spawner.round_playing = True
#                 scene.round_spawner.round += 1
#                 scene.round_paid = False
#                 if scene.round_spawner.round > len(data.ROUND_DATA)-1:
#                     scene.round_spawner.round = len(data.ROUND_DATA)-1
#                     print("REACHED MAX ROUND")
#                 scene.round_spawner.current_list = data.ROUND_DATA[scene.round_spawner.round]
#         if self.id == 35:
#             variables.speedup = not variables.speedup
#         if self.id == 36:
#             if scene.win:
#                 map_id = scene.map_id
#                 difficulty = scene.difficulty
#                 variables.completed_maps[map_id][difficulty] = 1
#                 funcs.update_savefile()
#                 data.CLIENT.scene = MainMenu()


#     def is_inside(self, x, y):
#         return self.x < x < self.x + self.w and self.y < y < self.y + self.h

#     def check_click(self, x, y):
#         if self.active:
#             if self.is_inside(x, y):
#                 self.tick()


# class Waypoint:
#     def __init__(self, x, y, previous=None, ahead=None, is_spawn=False, is_despawn=False):
#         self.x = x
#         self.y = y
#         self.previous = previous
#         self.ahead = ahead
#         self.is_spawn = is_spawn
#         self.is_despawn = is_despawn


# class Bloon:
#     def __init__(self, id, waypoint=None, x=None, y=None, lifetime=0, distance_travelled=0, camo=False, lead=False):
#         self.id = id
#         self.angle = 0
#         self.last_waypoint = waypoint
#         self.current_waypoint = waypoint.ahead
#         #self.w = 49
#         #self.h = 63
#         self.size = 20
#         self.speed = data.BLOON_SPEED_DATA[self.id] * data.BLOON_SPEED_MULTIPLIER
#         self.lifetime = lifetime
#         self.distance_travelled = distance_travelled
#         self.health = data.BLOON_HP_DATA[self.id]
#         self.camo = camo
#         self.lead = lead
#         self.effects = []
#         if self.id == 7 or self.id == 14:
#             self.lead = True
#         #BLOON_IMAGES = []
#         #for i in range(0, 16):
#         #    BLOON_IMAGES.append((pygame.image.load("assets/bloons/bloon_" + str(i) + ".png")).convert_alpha())
#         if x is None:
#             self.spawn()
#         else:
#             self.x = x
#             self.y = y
#             self.angle = math.atan2(self.current_waypoint.y - self.last_waypoint.y,
#                                     self.current_waypoint.x - self.last_waypoint.x)


#     def tick(self):
#         self.lifetime += 1
#         self.distance_travelled += self.speed
#         modifier = 1
#         if "nebunu" in self.effects:
#             modifier = -0.2

#         self.x += math.cos(self.angle) * self.speed * modifier
#         self.y += math.sin(self.angle) * self.speed * modifier

#         if math.dist((self.x, self.y), (self.current_waypoint.x, self.current_waypoint.y)) < 3:
#             if self.current_waypoint.ahead is None:
#                 self.despawn()
#                 return
#             self.x = self.current_waypoint.x
#             self.y = self.current_waypoint.y
#             self.last_waypoint = self.current_waypoint
#             self.current_waypoint = self.last_waypoint.ahead
#             self.angle = math.atan2(self.current_waypoint.y - self.last_waypoint.y,
#                                     self.current_waypoint.x - self.last_waypoint.x)


#         self.draw()

#     def spawn(self):
#         self.x = self.last_waypoint.x
#         self.y = self.last_waypoint.y
#         self.angle = math.atan2(self.current_waypoint.y - self.last_waypoint.y, self.current_waypoint.x - self.last_waypoint.x)


#     def despawn(self):
#         data.CLIENT.scene.bloons.remove(self)
#         data.CLIENT.scene.lives -= data.BLOON_RBE_DATA[self.id]
#         del self


#     def pop(self):
#         data.CLIENT.scene.bloons.remove(self)
#         del self


#     def spawn_children(self, projectile, children=None):
#         if children is not None:
#             for i in range(0, len(children)):
#                 distance = i * 10
#                 bloon = Bloon(children[i], self.last_waypoint,
#                               self.x - math.cos(self.angle) * distance, self.y - math.sin(self.angle) * distance,
#                               self.lifetime)
#                 projectile.already_hit.append(bloon)
#                 data.CLIENT.scene.bloons.append(bloon)
#             return

#         for i in range(0, len(data.BLOON_CHILDREN_DATA[self.id])):
#             distance = 10+i*10
#             bloon = Bloon(data.BLOON_CHILDREN_DATA[self.id][i], self.last_waypoint, self.x-math.cos(self.angle)*distance, self.y-math.sin(self.angle)*distance, self.lifetime, self.distance_travelled)
#             projectile.already_hit.append(bloon)
#             data.CLIENT.scene.bloons.append(bloon)

#     def draw(self):
#         if self.camo:
#             funcs.draw_image(data.CAMO_BLOON_IMAGES[self.id], self.x, self.y, center=True)
#         else:
#             funcs.draw_image(data.BLOON_IMAGES[self.id], self.x, self.y, center=True)
#         if "nebunu" in self.effects:
#             funcs.draw_image(data.NEBUNU, self.x, self.y)
#         pygame.draw.circle(data.WINDOW, (0, 0, 0), (self.x, self.y), self.size, 1)


# class RoundSpawner:
#     def __init__(self, waypoint, difficulty):
#         self.waypoint = waypoint
#         default_rounds = [-1, 3, 6]
#         self.round = default_rounds[difficulty]
#         b = [40, 80, 100]
#         self.max_rounds = b[difficulty]
#         self.round_playing = False
#         self.timer = 0
#         self.current_list = None


#     def tick(self):
#         if self.round_playing:

#             if not self.current_list:
#                 self.round_playing = False
#             else:
#                 self.timer += 1
#                 if self.timer >= self.current_list[0][1]:
#                     camo = False
#                     if len(self.current_list[0]) == 3:
#                         camo = True
#                     data.CLIENT.scene.spawn_bloon(self.current_list[0][0], camo=camo)
#                     self.current_list.pop(0)
#                     self.timer = 0
#                     if len(self.current_list) == 0:
#                         print(len(self.current_list))
#                         print(self.current_list)
#                         self.round_playing = False


# class Effect:
#     def __init__(self):
#         self.id = 0

# class Nebunu(Effect):
#     def __init__(self):
#         Effect.__init__()
#         self.timer = 60
#         self.owner = None