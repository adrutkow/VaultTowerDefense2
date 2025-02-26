import pygame
from classes.client import Client
import os

DEBUG_MODE = True

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
    [0, 0, 500, 500], # win screen button
    [100, 700, 75, 75], # Ability 1 #37
    [200, 700, 75, 75], # Ability 2
    [300, 700, 75, 75], # Ability 3
    [400, 700, 75, 75], # Ability 4
    [500, 700, 75, 75], # Ability 5
    [600, 700, 75, 75], # Ability 6
    [700, 700, 75, 75], # Ability 7 #43
    

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
    ],
    [
        [261, 760],
        [272, 668],
        [251, 600],
        [299, 507],
        [302, 451],
        [286, 369],
        [359, 275],
        [346, 161],
        [349, 109],
        [377, 101],
        [459, 174],
        [467, 199],
        [708, 201],
        [819, 92],
        [877, 90],
        [892, 155],
        [848, 266],
        [877, 323],
        [881, 412],
        [864, 480],
        [906, 512],
        [909, 562],
        [942, 607],
        [927, 654],
        [941, 691],
        [940, 731],
        [959, 754],
        [959, 780],
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
df = 18
wat = 20

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
    [[0, 5]] * 100 + [[1, 5]] * 20 + [[2, 5]] * 20 + [[3, 5]] * 20,
    [[7, df]] * 6,
    [[3, df]] * 80,
    # 30
]


df /= 2


ROUND_DATA += [
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
    [[5, df]] * wat + [[8, df]] * wat,
    [[9, df]] * 10 + [[9, df, 1]] * 5,
    [[9, df]] * 10 + [[10, df]] * 7,
    [[8, df]] * 50,
    # df
    [[1, 30]] * 180 + [[4, df, 1]] * 10 + [[7, df]] * 12 + [[9, df]] * 25,
    [[10, df]] * 12,
    [[4, df, 1]] * 70, [[10, df]] * 12,
    [[4, 30]] * wat + [[4, df, 1]] * 30 + [[9, df]] * 40 + [[10, df]] * 6,
    [[2, 8]] * 343 + [[8, df]] * 20 + [[9, df]] * 35 + [[10, df]] * 18,
    # 50
    [[0, 5]] * 20 + [[7, df]] * 16 + [[10, df]] * 20 + [[11, df]] * 2,
    [[9, df]] * 20 + [[10, df, 1]] * 15,
    [[9, df]] * 25 + [[10, df]] * 10 + [[11, df]] * 2,
    [[4, 20, 1]] * 80 + [[11, df]] * 3,
    [[10, 5]] * 35 + [[11, df]] * 2,
    # 55
    [[10, df]] * wat + [[11, df]] * 1,
    [[9, df, 1]] * 20 + [[11, df]] * 1,
    [[9, df, 1]] * 40 + [[11, df]] * 4,
    [[10, df]] * wat + [[11, df]] * 5,
    [[7, 30, 1]] * 50 + [[10, 30]] * wat,
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
    [[12, df]] * wat + [[13, df]] * 8,
    [[11, df]] * wat + [[14, 30]] * 18,
    # 100
    [[15, df]] * 1





]

BLOON_SPEED_DATA = [1, 1.4, 1.8, 3.2, 3.5, 1.8, 2.0, 1, 1.8, 1.8, 2.5, 1, 0.25, 0.18, 2.75, 0.18]
BLOON_SPEED_MULTIPLIER = 1.8
BLOON_MONEY_DATA = [1, 2, 3, 4, 5, 11, 11, 23, 23, 47, 95, 381, 1525, 6101, 381, 13346]
BLOON_RBE_DATA = [1, 2, 3, 4, 5, 11, 11, 23, 23, 47, 104, 616, 3164, 16656, 816, 55760]
BLOON_HP_DATA =   [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 10, 200, 700, 4000, 400, 20000]
BLOON_SIZE_DATA = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 45, 50, 55, 50, 75]
BLOON_CHILDREN_DATA = [[], # RED 0
                       [0], # BLUE
                       [1], # GREEN
                       [2], # YELLOW
                       [3], # PINK
                       [4, 4], # BLACK 5
                       [4, 4], # WHITE
                       [5, 5], # LEAD
                       [5, 6], # ZEBRA
                       [8, 8], # RAINBOW
                       [9, 9], # CERAMIC 10
                       [10,10,10,10],
                       [11,11,11,11],
                       [12,12,12,12],
                       [10,10,10,10],
                       [13, 13, 14, 14, 14]]


TOWER_PRICE_DATA = [525, 325, 350, 400, 1250, 2000, 0, 0, 0, 0, 0, 200]
TOWER_DAMAGE_DATA = [1, 1, 2, 1, 100, 1, 0, 0, 0, 0, 0, 1]
TOWER_PIERCE_DATA = [14, 2, 1, 3, 0, 1, 0, 0, 0, 0, 0, 3]
TOWER_RANGE_DATA = [150, 100, 50, 200, 0, 175, 0, 0, 0, 0, 0, 150]
TOWER_AS_DATA = [1.5, 0.75, 1.60, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.95]
TOWER_SIZE_DATA = [25, 40, 30, 30, 50, 30, 30, 30, 30, 30, 30, 20]
TOWER_FIRSTPATH_PRICE = [[350, 650, 1100, 3200, 55000],
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
                         [140, 220, 300, 1800, 15000]]

TOWER_SECONDPATH_PRICE = [[250, 400, 1100, 3100, 25500],
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
                          [85, 190, 625, 2000, 21500]]
TOWER_NAMES = ["Dubstep Shit", "Natural Salt", "Spood", "Balou", "Slav", "Anonymous", "test", "test", "test", "test", "test", "test"]
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
    ["Sharp shots", "Razor sharp shots", "Spike-o-pult", "Juggernaut", "Ultra Juggernaut"],
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
    ["Quick shots", "Very quick shots", "Crossbow", "Sharp shooter", "Crossbow master"],
]

TOWER_FIRSTPATH_DESCRIPTIONS = [
    ["Sharp shots", "Razor sharp shots", "Spike-o-pult", "Juggernaut", "Ultra Juggernaut"],
    ["Barbed darts", "heat tiped darts", "yo mamam", "deexz", "muts"],
    ["Bullets now do 4 damage", "Bullets now do 7 damage", "20 damage per shot, with a bonus against ceramics. Can pop lead.", "30 damage, ceramic bonus, and bullets now stun MOAB class bloons", "280 damage per shot, shots cripple MOAB class bloons, stunning them and making them take +5 damage"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["Sharp shots", "Razor sharp shots", "Spike-o-pult", "Juggernaut", "Ultra Juggernaut"],
]

TOWER_SECONDPATH_DESCRIPTIONS = [
    ["Faster shots", "Even faster shots", "Gain a crossbow, +damage, +pierce, +range, +camo vision", "Sharp shooter", "Crossbow master"],
    ["Twin guns", "shooty", "Triple guns", "Armor piercing darts", "Sub commander"],
    ["Faster shooting", "Even faster firing", "Attack x3 as fast", "Fully automatic rifle, with +2 damage against MOAB-class bloons", "Ultimate attack speed, +4 damage against MOAB-class bloons"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["test", "test", "test", "test", "test"],
    ["Quick shots", "Very quick shots", "Crossbow", "Sharp shooter", "Crossbow master"],
]




WINDOW = pygame.display.set_mode((1366, 768))
IS_FULLSCREEN = False
CLOCK = pygame.time.Clock()
CLIENT = Client()
MENU_SCREEN = pygame.image.load("assets/menus/menu.png").convert()
MAP_SELECT_SCREEN = pygame.image.load("assets/menus/map_selection.png").convert()
DIFFICULTY_SELECT_SCREEN = pygame.image.load("assets/menus/difficulty_select.png").convert()
SIDEBAR = pygame.image.load("assets/menus/sidebar.png").convert()

CAT = pygame.image.load("assets/towers/cat.png").convert_alpha()
SALT = pygame.image.load("assets/towers/salt.png").convert_alpha()
SPOOD = pygame.image.load("assets/towers/spood.png").convert_alpha()
BALOU = pygame.image.load("assets/towers/balou.png").convert_alpha()
SLAV = pygame.image.load("assets/towers/slav.png").convert_alpha()
ANONYMOUS = pygame.image.load("assets/towers/anonymous.png").convert_alpha()
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
GREEN_RECT = pygame.image.load("assets/misc/green_rect.png").convert()

WIN_SCREEN = pygame.image.load("assets/misc/win_screen.png").convert()
NEBUNU = pygame.image.load("assets/misc/nebunu.png").convert_alpha()



ABILITY_NAME = ["Moab assassin", "Moab eliminator"]
# in seconds
ABILITY_COOLDOWN = [30, 10]
ABILITY_IMAGES = []

for i in range(0, 20):
    filename_prefix = "ability"
    suffix = str(i)
    file_path = 'assets/abilities/' + filename_prefix + suffix + '.png'
    path_exists = os.path.exists(file_path)

    if path_exists:
        ABILITY_IMAGES.append(pygame.image.load(file_path).convert_alpha())



TOWER_UPGRADE_IMAGES = [
    [[],[]],
    [[],[]],
    [[],[]],
    [[],[]],
    [[],[]],
    [[],[]],
    [[],[]],
    [[],[]],
    [[],[]],
    [[],[]],
    [[],[]],
    [[],[]],
    ]
upgrade_images_file_prefixes = ["cat", "salt", "spood", "balou", "slav", "anonymous", "ajeaje", "speed", "abnormal", "vg1000", "goga", "minion"]


iterable_array = zip(TOWER_UPGRADE_IMAGES, upgrade_images_file_prefixes)

for working_array, filename_prefix in iterable_array:
    for path in range(0, 2):
        for i in range(1, 6):
            suffix = ""
            if path == 0:
                suffix = str(i) + "0"
            if path == 1:
                suffix = "0" + str(i)

            file_path = 'assets/towers/upgrades/' + filename_prefix + '/' + filename_prefix + suffix + '.png'
            path_exists = os.path.exists(file_path)

            if path_exists:
                image = pygame.image.load(file_path).convert_alpha()
                working_array[path].append(image)
            else:
                working_array[path].append(None)
                print("filepath doesnt exist: "+file_path)



print(TOWER_UPGRADE_IMAGES)

pygame.font.init()
pygame.mixer.init()

sounds = []

SOUND_HITMARK = pygame.mixer.Sound("assets/sounds/hitmark.mp3")
SOUND_METAL_HIT1 = pygame.mixer.Sound("assets/sounds/HitMetal01.ogg")
SOUND_METAL_HIT2 = pygame.mixer.Sound("assets/sounds/HitMetal02.ogg")
SOUND_BLOON_POP1 = pygame.mixer.Sound("assets/sounds/bloonpop1.mp3")
SOUND_BLOON_POP2 = pygame.mixer.Sound("assets/sounds/bloonpop2.mp3")
SOUND_BLOON_POP3 = pygame.mixer.Sound("assets/sounds/bloonpop3.mp3")


sounds.append(SOUND_HITMARK)
sounds.append(SOUND_METAL_HIT1)
sounds.append(SOUND_METAL_HIT2)
sounds.append(SOUND_BLOON_POP1)
sounds.append(SOUND_BLOON_POP2)
sounds.append(SOUND_BLOON_POP3)

for i in sounds:
    i.set_volume(0.1)

SOUND_BLOON_POP1.set_volume(0.015)
SOUND_BLOON_POP2.set_volume(0.015)
SOUND_BLOON_POP3.set_volume(0.015)
SOUND_METAL_HIT1.set_volume(0.02)
SOUND_METAL_HIT2.set_volume(0.02)


BLOON_IMAGES = []
for i in range(0, 16):
    BLOON_IMAGES.append((pygame.image.load("assets/bloons/bloon_"+str(i)+".png")).convert_alpha())

for i in range(0, 16):
    BLOON_IMAGES[i] = pygame.transform.scale(BLOON_IMAGES[i], (BLOON_IMAGES[i].get_width() * 0.75, BLOON_IMAGES[i].get_height() * 0.75))

CAMO_BLOON_IMAGES = []
for i in range(0, 11):
    CAMO_BLOON_IMAGES.append((pygame.image.load("assets/bloons/bloon_"+str(i)+"_camo.png")).convert_alpha())

for i in range(0, 11):
    CAMO_BLOON_IMAGES[i] = pygame.transform.scale(CAMO_BLOON_IMAGES[i], (CAMO_BLOON_IMAGES[i].get_width() * 0.75, CAMO_BLOON_IMAGES[i].get_height() * 0.75))

PROJECTILE_IMAGES = []
for i in range(0, 20):
    file_path = "assets/projectiles/projectile_"+str(i)+".png"
    if os.path.exists(file_path):
        PROJECTILE_IMAGES.append(pygame.image.load("assets/projectiles/projectile_"+str(i)+".png").convert_alpha())


MAPS = []
MAPS_COLLISIONS = []
MAP_COUNT = 4
for i in range(0, MAP_COUNT):
    MAPS.append(pygame.image.load("assets/maps/map" + str(i) + ".png").convert())
    MAPS_COLLISIONS.append(pygame.image.load("assets/maps/map" + str(i) + "_collision.png").convert())

TOWER_IMAGES = [CAT, SALT, SPOOD, BALOU, SLAV, ANONYMOUS, AJEAJE, SPEED, ABNORMAL, VIDEOGAMES1000, GOGA, MINION]
