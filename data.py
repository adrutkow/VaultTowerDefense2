import pygame
import classes

BUTTON_DATA = [
    [580, 370, 200, 42],  #0 Play button
    [580, 420, 200, 42],  # Shop button
    [580, 470, 200, 42],  # Stats button
    [580, 520, 200, 42],  # Settings button
    [580, 570, 200, 42],  # Exit button
    [16, 16, 250, 250],  # Map select 0
    [286, 16, 250, 250],
    [556, 16, 250, 250],
    [826, 16, 250, 250],
    [1096, 16, 250, 250],
    [16, 287, 250, 250],  #10
    [286, 287, 250, 250],
    [556, 287, 250, 250],
    [826, 287, 250, 250],
    [1096, 287, 250, 250],  # Map select 9
    [44, 550, 200, 200],  # Go back button from map select
    [200, 220, 250, 250],  # Easy button
    [570, 220, 250, 250],  # Normal button
    [920, 220, 250, 250],  # Hard button
    [1179, 114, 77, 91], # buy slot 0
    [1262, 114, 77, 91], #20 buy slot 1
    [1179, 210, 77, 91],
    [1262, 210, 77, 91],
    [1179, 310, 77, 91],
    [1262, 310, 77, 91],
    [1179, 410, 77, 91],
    [1262, 410, 77, 91],
    [1179, 510, 77, 91],
    [1262, 510, 77, 91],
    [1179, 610, 77, 91],
    [1262, 610, 77, 91], #30 buy slot 11
    [24, 294, 162, 39],  # buy upgrade 1
    [24, 384, 162, 39],  # buy upgrade 2
    [128, 627, 45, 35],   # sell button
    [1261, 693, 78, 69],   # next round button
    [1181, 695, 78, 69],    # speedup butotn
    [0, 0, 500, 500]      # win screen button
]

WAYPOINTS_DATA = [
    [
        [-30, 265],
        [640, 265],
        [640, 480],
        [420, 480],
        [420, 80],
        [170, 80],
        [170, 650],
        [800, 650],
        [800, 265],
        [1225, 265],
    ],
    [
        [-20, 400],
        [85, 470],
        [112, 525],
        [287, 616],
        [570, 700],
        [864, 738],
        [980, 720],
        [1050, 666],
        [1030, 445],
        [1100, 320],
        [1050, 245],
        [1010, 224],
        [1000, 180],
        [870, 125],
        [525, 95],
        [230, 100],
        [140, 145],
        [88, 230],
        [-20, 310]
    ],
    [
        [-30, 353],
        [174, 345],
        [300, 345],
        [277, 439],
        [354, 492],
        [451, 484],
        [502, 403],
        [487, 315],
        [420, 286],
        [317, 282],
        [283, 397],
        [323, 520],
        [391, 631],
        [489, 711],
        [456, 706],
        [631, 626],
        [635, 531],
        [568, 483],
        [478, 472],
        [450, 553],
        [433, 627],
        [466, 702],
        [575, 713],
        [672, 685],
        [776, 665],
        [882, 653],
        [931, 556],
        [932, 467],
        [851, 430],
        [778, 448],
        [745, 558],
        [747, 644],
        [876, 666],
        [944, 562],
        [945, 471],
        [832, 414],
        [836, 317],
        [902, 225],
        [985, 234],
        [1044, 282],
        [1019, 390],
        [981, 461],
        [1071, 493],
        [1236, 488]
    ]
]

# 0 red bloon
# 1 blue bloon
# 2 green bloon
# 3 yellow bloon
# 4 pink bloon
# 5 black bloon
# 6 white bloon
# 7 lead bloon
# 8 zebra bloon
# 9 rainbow bloon
# 10 ceramic bloon
# 11 moab
# 12 bfb
# 13 zomg
# 14 ddt
# 15 bad


# default spacing
df = 25


ROUND_DATA = [

    [[0, 30]] * 20,
    [[0, df]] * 35,
    [[0, df]] * 25 + [[1, df]] * 5,
    [[0, df]] * 35 + [[1, df]] * 18,
    # 5
    [[0, 30]] * 5 + [[1, df]] * 27,
    [[0, 30]] * 15 + [[1, df]] * 15 + [[2, df]] * 4,
    [[0, 30]] * 20 + [[1, df]] * 20 + [[2, df]] * 5,
    [[0, 30]] * 10 + [[1, df]] * 20 + [[2, df]] * 14,
    [[2, df]] * 30,
    # 10
    [[1, df]] * 102,
    [[0, 15]] * 10 + [[1, df]] * 10 + [[2, df]] * 12 + [[3, df]] * 3,
    [[1, df]] * 15 + [[2, df]] * 10 + [[3, df]] * 5,
    [[1, df]] * 50 + [[2, df]] * 23,
    [[0, 15]] * 49 + [[1, df]] * 15 + [[2, df]] * 10 + [[3, df]] * 9,
    # 15
    [[0, 15]] * 20 + [[1, df]] * 15 + [[2, df]] * 12 + [[3, df]] * 10 + [[4, df]] * 5,
    [[1, df]] * 40 + [[2, df]] * 8,
    [[3, df]] * 15,
    [[2, df]] * 80,
    [[2, df]] * 10 + [[3, df]] * 4 + [[3, df]] * 10 + [[4, df]] * 5,
    # 20
    [[5, df]] * 6,
    [[3, df]] * 40 + [[4, df]] * 14,
    [[6, df]] * 16,
    [[5, df]] * 7 + [[6, df]] * 7,
    [[1, df]] * 20 + [[2, df, 1]],
    # 25
    [[3, df]] * 35 + [[5, df]] * 10,
    [[4, df]] * 23 + [[8, df]] * 4,
    [[0, 5]] * 100 + [[1, df]] * df + [[2, df]] * df + [[3, df]] * df,
    [[7, df]] * 6,
    [[3, df]] * 80,
    # 30
    [[7, df]] * 9,
    [[5, df]] * 8 + [[6, df]] * 8 + [[8, df]] * 12,
    [[5, df]] * 15 + [[6, df]] * 20 + [[9, df]] * 3,
    [[0, 15, 1]] * 20 + [[3, df, 1]] * 13,
    [[3, 30]] * 145 + [[8, df]] * 6,
    # 35
    [[4, df]] * 35 + [[5, df]] * 30 + [[6, df]] * 25 + [[9, df]] * 5,
    [[4, 30]] * 140 + [[2, df, 1]] * 35,
    [[5, df]] * 25 + [[6, df]] * 25 + [[6, df, 1]] * 7 + [[8, df]] * 10 + [[7, df]] * 15,
    [[4, df]] * 42 + [[6, df]] * 17 + [[8, df]] * 10 + [[7, df]] * 14 + [[10, df]] * 2,
    [[5, df]] * 10 + [[6, df]] * 10 + [[8, df]] * 20 + [[9, df]] * 25,
    # 40
    [[11, df]] * 1,
    [[5, df]] * df + [[8, df]] * df,
    [[9, df]] * 10 + [[9, df, 1]] * 5,
    [[9, df]] * 10 + [[10, df]] * 7,
    [[8, df]] * 50,
    # df
    [[1, 30]] * 180 + [[4, df, 1]] * 10 + [[7, df]] * 12 + [[9, df]] * 25,
    [[10, df]] * 12,
    [[4, df, 1]] * 70, [[10, df]] * 12,
    [[4, 30]] * df + [[4, df, 1]] * 30 + [[9, df]] * 40 + [[10, df]] * 6,
    [[2, 8]] * 343 + [[8, df]] * 20 + [[9, df]] * 35 + [[10, df]] * 18,
    # 50
    [[0, 5]] * 20 + [[7, df]] * 16 + [[10, df]] * 20 + [[11, df]] * 2,
    [[9, df]] * 20 + [[10, df, 1]] * 15,
    [[9, df]] * 25 + [[10, df]] * 10 + [[11, df]] * 2,
    [[4, 20, 1]] * 80 + [[11, df]] * 3,
    [[10, df]] * 35 + [[11, df]] * 2,
    # 55
    [[10, df]] * df + [[11, df]] * 1,
    [[9, df, 1]] * 20 + [[11, df]] * 1,
    [[9, df, 1]] * 40 + [[11, df]] * 4,
    [[10, df]] * df + [[11, df]] * 5,
    [[7, 30, 1]] * 50 + [[10, 30]] * df,
    # 60
    [[12, df]] * 1,
    [[8, 25]] * 175 + [[11, df]] * 5,
    [[4, 10]] * 250 + [[9, df, 1]] * 15 + [[11, df]] * 10,
    [[7, 10]] * 75 + [[10, 10]] * 122,
    [[11, df]] * 13,
    # 65
    [[8, df]] * 100 + [[9, df]] * 70 + [[10, df]] * 50 + [[11, df]] * 3 + [[12, df]] * 2,
    [[11, df]] * 13,
    [[10, 5]] * 20 + [[11, df]] * 8,
    [[11, df]] * 4 + [[12, df]] * 1,
    [[5, df]] * 40 + [[7, df]] * 80 + [[10, df]] * 50,
    # 70
    [[1, 10]] * 120 + [[9, 20]] * 200 + [[11, df]] * 4,
    [[10, df]] * 30 + [[11, df]] * 10,
    [[10, df]] * 50 + [[12, df]] * 2,
    [[11, df]] * 8 + [[12, df]] * 2,
    [[10, 30]] * 150 + [[12, df]] * 1,
    # 75
    [[7, df]] * 50 + [[11, df]] * 8 + [[12, df]] * 7,
    [[10, 30]] * 80,
    [[11, df]] * 11 + [[12, df]] * 5,
    [[4, 20]] * 80 + [[9, 30]] * 150 + [[10, df]] * 75 + [[10, df, 1]] * 72 + [[12, df]] * 1,
    [[9, 3]] * 500 + [[12, df]] * 10,
    # 80
    [[13, df]] * 1,
    [[12, df]] * 17,
    [[12, df]] * 30,
    [[10, 30]] * 200 + [[11, df]] * 30,
    [[11, df]] * 50 + [[12, df]] * 10,
    # 85
    [[13, df]] * 2,
    [[12, df]] * 10,
    [[13, df]] * 4,
    [[11, df]] * 18 + [[12, df]] * 8 + [[13, df]] * 2,
    [[11, df]] * 40 + [[12, df]] * 16,
    # 90
    [[7, df, 1]] * 100 + [[14, df]] * 3,
    [[100, df]] * 150 + [[12, df]] * 20,
    [[11, 30]] * 75 + [[13, df]] * 4,
    [[12, df]] * 20 + [[14, df]] * 6,
    [[12, df]] * 25 + [[13, df]] * 6,
    # 95
    [[5, 5]] * 500 + [[7, 5, 1]] * 350 + [[11, 30]] * 100 + [[14, df]] * 30,
    [[11, df]] * 80 + [[12, df]] * 30 + [[13, df]] * 6,
    [[13, df]] * 5,
    [[12, df]] * df + [[13, df]] * 8,
    [[11, df]] * df + [[14, 30]] * 18,
    # 100
    [[15, df]] * 1





]

BLOON_SPEED_DATA = [1, 1.4, 1.8, 3.2, 3.5, 1.8, 2.0, 1, 1.8, 1.8, 2.5, 1, 0.25, 0.18, 2.75, 0.18]
BLOON_SPEED_MULTIPLIER = 1.2
BLOON_MONEY_DATA = [1, 2, 3, 4, 5, 11, 11, 23, 23, 47, 95, 381, 1525, 6101, 381, 13346]
BLOON_RBE_DATA = [1, 2, 3, 4, 5, 11, 11, 23, 23, 47, 104, 616, 3164, 16656, 816, 55760]
BLOON_HP_DATA = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 10, 200, 700, 4000, 400, 20000]
BLOON_CHILDREN_DATA = [[],
                       [0],
                       [1],
                       [2],
                       [3],
                       [4, 4],
                       [4, 4],
                       [5, 5],
                       [5, 6],
                       [8, 8],
                       [9, 9],
                       [10,10,10,10],
                       [11,11,11,11],
                       [12,12,12,12],
                       [10,10,10,10],
                       [13, 13, 14, 14, 14]]


TOWER_PRICE_DATA = [200, 325, 350, 400, 1250, 2000, 0, 0, 0, 0, 0, 0]
TOWER_DAMAGE_DATA = [1, 1, 2, 1, 100, 1, 0, 0, 0, 0, 0, 0]
TOWER_PIERCE_DATA = [3, 2, 1, 3, 0, 1, 0, 0, 0, 0, 0, 0]
TOWER_RANGE_DATA = [150, 100, 50, 200, 0, 175, 0, 0, 0, 0, 0, 0]
TOWER_AS_DATA = [0.95, 0.75, 1.60, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
TOWER_SIZE_DATA = [55, 30, 30, 30, 100, 30, 30, 30, 30, 30, 30, 30]
TOWER_FIRSTPATH_PRICE = [[140, 220, 300, 1800, 15000],
                         [450, 300, 1400, 13000, 32000],
                         [350, 1500, 3000, 5000, 34000],
                         [150, 600, 1300, 10900, 32000],
                         [500, 600, 3000, 19000, 100000],
                         [250, 750, 1000, 2500, 20000],
                         [1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1],
                         [1, 1, 1, 1, 1]]

TOWER_SECONDPATH_PRICE = [[100, 190, 400, 8000, 45000],
                          [450, 1000, 1100, 3000, 25000],
                          [400, 400, 3500, 4250, 14000],
                          [300, 900, 3000, 4000, 54000],
                          [300, 800, 3500, 7500, 100000],
                          [500, 1500, 4500, 7500, 40000],
                          [1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1]]
TOWER_NAMES = ["Dubstep Shit", "Natural Salt", "Spood", "Balou", "Slav", "Glebu", "test", "test", "test", "test", "test", "test"]
TOWER_FIRSTPATH_NAMES = [
    ["Sharp shots", "Razor sharp shots", "Spike-o-pult", "Juggernaut", "Ultra Juggernaut"],
    ["Barbed darts", "heat tiped darts", "yo mamam", "deexz", "muts"],
    ["AP bullets", "Destruction", "Sniper rifle", "Enhanced sniper", "Ultimate sniper"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
]
TOWER_SECONDPATH_NAMES = [
    ["Quick shots", "Very quick shots", "Crossbow", "Sharp shooter", "Crossbow master"],
    ["Twin guns", "shooty", "Triple guns", "Armor piercing darts", "Sub commander"],
    ["Fast firing", "Even faster firing", "Semi-automatic rifle", "Full auto rifle", "Elite rifleman"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
]


WINDOW = pygame.display.set_mode((1366, 768))
CLOCK = pygame.time.Clock()
CLIENT = classes.Client()
MENU_SCREEN = pygame.image.load("assets/menus/menu.png").convert()
MAP_SELECT_SCREEN = pygame.image.load("assets/menus/map_selection.png").convert()
DIFFICULTY_SELECT_SCREEN = pygame.image.load("assets/menus/difficulty_select.png").convert()
SIDEBAR = pygame.image.load("assets/menus/sidebar.png").convert()

CAT = pygame.image.load("assets/towers/cat.png").convert_alpha()
SALT = pygame.image.load("assets/towers/salt.png").convert_alpha()
SPOOD = pygame.image.load("assets/towers/spood.png").convert_alpha()
BALOU = pygame.image.load("assets/towers/balou.png").convert_alpha()
SLAV = pygame.image.load("assets/towers/slav.png").convert_alpha()
GLEBU = pygame.image.load("assets/towers/glebu.png").convert_alpha()
AJEAJE = pygame.image.load("assets/towers/ajeaje.png").convert_alpha()
SPEED = pygame.image.load("assets/towers/speed.png").convert_alpha()
ABNORMAL = pygame.image.load("assets/towers/abnormal.png").convert_alpha()
VIDEOGAMES1000 = pygame.image.load("assets/towers/videogames1000.png").convert_alpha()
GOGA = pygame.image.load("assets/towers/goga.png").convert_alpha()
MINION = pygame.image.load("assets/towers/minion.png").convert_alpha()
TOWER_MENU = pygame.image.load("assets/menus/tower_menu.png").convert()

HEART = pygame.image.load("assets/misc/heart.png").convert_alpha()
GOLD = pygame.image.load("assets/misc/gold.png").convert_alpha()
LIMIT = pygame.image.load("assets/misc/limit.png").convert_alpha()
STAR_EMPTY = pygame.image.load("assets/misc/star0.png").convert_alpha()
STAR_FULL = pygame.image.load("assets/misc/star1.png").convert_alpha()

WIN_SCREEN = pygame.image.load("assets/misc/win_screen.png").convert()
NEBUNU = pygame.image.load("assets/misc/nebunu.png").convert_alpha()

pygame.font.init()

BLOON_IMAGES = []
for i in range(0, 16):
    BLOON_IMAGES.append((pygame.image.load("assets/bloons/bloon_"+str(i)+".png")).convert_alpha())

CAMO_BLOON_IMAGES = []
for i in range(0, 11):
    CAMO_BLOON_IMAGES.append((pygame.image.load("assets/bloons/bloon_"+str(i)+"_camo.png")).convert_alpha())

PROJECTILE_IMAGES = []
for i in range(0, 4):
    PROJECTILE_IMAGES.append(pygame.image.load("assets/projectiles/projectile_"+str(i)+".png"))


MAPS = []
MAPS_COLLISIONS = []
for i in range(0, 3):
    MAPS.append(pygame.image.load("assets/maps/map" + str(i) + ".png").convert())
    MAPS_COLLISIONS.append(pygame.image.load("assets/maps/map" + str(i) + "_collision.png"))

TOWER_IMAGES = [CAT, SALT, SPOOD, BALOU, SLAV, GLEBU, AJEAJE, SPEED, ABNORMAL, VIDEOGAMES1000, GOGA, MINION]
