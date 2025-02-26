import pygame
import data
from classes.tower_classes import class_list
#from classes.scenes import MainMenu
import variables
import pickle
import math
from classes.ui import FloatingText


def draw_image(image, x, y, final_x=None, final_y=None, rect=None, center=False):
    if rect is not None:
        data.WINDOW.blit(image, rect)
        return

    if final_x is not None:
        trans_image = pygame.transform.scale(image, (final_x, final_y))
        if center:
            pos = (x + final_x / 2, y + final_y / 2)
        else:
            pos = (x, y)
        data.WINDOW.blit(trans_image, pos)
        
    else:
        if center:
            pos = (x - image.get_width() / 2, y - image.get_height() / 2)
        else:
            pos = (x, y)
        data.WINDOW.blit(image, pos)
        #pygame.display.update([x, y, image.get_width(), image.get_height()])
    


def draw_text(text, x, y, size=20, color=(255, 255, 255), shadow=False, targetImage=None):
    font = pygame.font.Font("assets/OETZTYP_.TTF", size)
    if shadow:
        temp = font.render(str(text), False, (0, 0, 0))
        data.WINDOW.blit(temp, (x+5, y+5))
    temp = font.render(str(text), False, color)

    if targetImage is not None:
        targetImage.blit(temp, (x, y))
        return
    data.WINDOW.blit(temp, (x, y))


def rotate_image(image, angle_degrees):
    """returns a rotated version of the image"""
    new_image = pygame.transform.rotate(image, angle_degrees)
    return new_image


def left_click(x, y):
    # Check buttons
    for i in data.CLIENT.scene.buttons:
        i.check_click(x, y)

    # If in game and has tower selected, attempt to place tower
    if data.CLIENT.scene.id == 3:
        select = data.CLIENT.scene.sidebar.select
        scene = data.CLIENT.scene
        collision_map = data.MAPS_COLLISIONS[scene.map_id]

        # if tower is selected and mouse in game
        if select is not None and pygame.mouse.get_pos()[0] < 1170:
            size = data.TOWER_SIZE_DATA[select]
            #tower_w = data.TOWER_IMAGES[select].get_width()
            #tower_h = data.TOWER_IMAGES[select].get_height()
            #tower_x = int(x - tower_w / 2)
            #tower_y = int(y - tower_h / 2)
            # if enough gold
            if data.CLIENT.scene.gold >= data.TOWER_PRICE_DATA[select]:
                # check if tower is colliding with another tower
                collision = False
                for i in scene.towers:
                    #x1 = i.x + i.w / 2 - i.size / 2
                    #y1 = i.y + i.h / 2 - i.size / 2
                    #w1 = i.size
                    #h1 = i.size

                    #x2 = x - size / 2
                    #y2 = y - size / 2
                    #w2 = size
                    #h2 = size

                    #if rect_collision(x1, y1, w1, h1, x2, y2, w2, h2):
                    #    collision = True
                    #    break

                    # Selected tower circle
                    c1 = (x, y, data.TOWER_SIZE_DATA[select])

                    # Iterated tower circle
                    c2 = (i.x, i.y, data.TOWER_SIZE_DATA[i.id])

                    if circle_collision(c1, c2):
                        collision = True
                        break


                if not collision:
                    out_of_bounds = False
                    # if collision box doesnt collide with map
                    #values_x = [int(x - size / 2), int(x + size / 2)]
                    #values_y = [int(y - size / 2), int(y + size / 2)]
                    #for i in values_x:
                    #    if i > 1366 or i < 0:
                    #        out_of_bounds = True
                    #for i in values_y:
                    #    if i > 768 or i < 0:
                    #       out_of_bounds = True
                    if x > 1366 or y > 768:
                        out_of_bounds = True
                    if not out_of_bounds:
                        # if collision_map.get_at((int(x - size / 2), int(y - size / 2)))[0] != 255:
                        #     if collision_map.get_at((int(x + size / 2), int(y - size / 2)))[0] != 255:
                        #         if collision_map.get_at((int(x - size / 2), int(y + size / 2)))[0] != 255:
                        #             if collision_map.get_at((int(x + size / 2), int(y + size / 2)))[0] != 255:
                        #                 b = [classes.DubstepCat, classes.Salt, classes.Spood, classes.Balou,
                        #                      classes.Slav, classes.Anonymous, classes.Ajeaje, classes.Speed,
                        #                      classes.Abnormal, classes.Videogames1000, classes.Goga,
                        #                      classes.Minion]
                        #                 scene.towers.append(b[select](tower_x, tower_y))
                        #                 scene.gold -= data.TOWER_PRICE_DATA[select]
                        #                 scene.sidebar.select = None
                        tower_size = data.TOWER_SIZE_DATA[select]
                        collided = False
                        for i in range(0, 9):
                            target_pos = (int((x + math.cos(i * math.pi/4) * tower_size)), int((y + math.sin(i * math.pi/4) * tower_size)))
                            if target_pos[0] > 1366 or target_pos[1] > 768 or target_pos[0] < 0 or target_pos[1] < 0:
                                collided = True
                                break
                            if collision_map.get_at(target_pos)[0] == 255:
                                collided = True
                                break

                        #if collision_map.get_at((x, y))[0] != 255:
                        if collided == False:
                            b = class_list
                            scene.towers.append(b[select](x, y))
                            scene.gold -= data.TOWER_PRICE_DATA[select]
                            scene.sidebar.select = None


        if select is None:
            for i in scene.towers:
                if i.is_clicked(x, y):
                    scene.tower_menu.set_tower_select(i)
                    break

                if not is_in_rect(x, y, 0, 91, 196, 583):
                    scene.tower_menu.set_tower_select(None)


def right_click(x, y):
    print(f"[{x}, {y}]")

    if data.CLIENT.scene.id == 3:
        data.CLIENT.scene.sidebar.select = None


def rect_collision(x1, y1, w1, h1, x2, y2, w2, h2):
    return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and h1 + y1 > y2

def circle_collision(circle1, circle2):
    x1 = circle1[0]
    y1 = circle1[1]
    r1 = circle1[2]
    x2 = circle2[0]
    y2 = circle2[1]
    r2 = circle2[2]
    return math.dist((x1, y1), (x2, y2)) < r1 + r2

def is_in_circle(pos, circle):
    return math.dist(pos, (circle[0], circle[1])) <= circle[2]

def is_in_rect(x, y, x1, y1, w1, h1):
    return x1 <= x <= x1 + w1 and y1 <= y <= y1 + h1


def handle_events(e):
    if e.type == pygame.QUIT:
        variables.running = False
    if e.type == pygame.MOUSEBUTTONDOWN:
        if e.button == pygame.BUTTON_LEFT:
            left_click(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        if e.button == pygame.BUTTON_RIGHT:
            right_click(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])


        

    keys = pygame.key.get_pressed()



    if e.type == pygame.KEYDOWN:
        if keys[pygame.K_1]:
            data.CLIENT.scene.spawn_bloon(1)
        if keys[pygame.K_2]:
            data.CLIENT.scene.spawn_bloon(2)
        if keys[pygame.K_3]:
            data.CLIENT.scene.spawn_bloon(3)
        if keys[pygame.K_4]:
            data.CLIENT.scene.spawn_bloon(4)
        if keys[pygame.K_5]:
            data.CLIENT.scene.spawn_bloon(5)
        if keys[pygame.K_6]:
            data.CLIENT.scene.spawn_bloon(9)
        if keys[pygame.K_7]:
            data.CLIENT.scene.spawn_bloon(10)
        if keys[pygame.K_8]:
            data.CLIENT.scene.spawn_bloon(11)
        if keys[pygame.K_9]:
            data.CLIENT.scene.spawn_bloon(14)
        if keys[pygame.K_0]:
            data.CLIENT.scene.spawn_bloon(15)
        if keys[pygame.K_b]:
            data.CLIENT.scene.gold += 999999
            data.CLIENT.scene.particles.append(FloatingText("test", 600, 600, color=(255, 255, 0)))
        if keys[pygame.K_s]:
            data.CLIENT.scene.round_spawner.round += 1
        if keys[pygame.K_f]:
            print(data.CLOCK.get_fps())
        if keys[pygame.K_ESCAPE]:
            if data.CLIENT.scene.id == 3:
                data.CLIENT.go_to_main_menu()
        if keys[pygame.K_SPACE]:
            if data.CLIENT.scene.id == 3:
                data.CLIENT.scene.round_spawner.next_round_button()
        if keys[pygame.K_f]:
            data.IS_FULLSCREEN = not data.IS_FULLSCREEN


            if data.IS_FULLSCREEN:
                data.WINDOW = pygame.display.set_mode((1366, 768), pygame.FULLSCREEN)
            if not data.IS_FULLSCREEN:
                data.WINDOW = pygame.display.set_mode((1366, 768))

            if data.CLIENT.scene.id == 3:
                data.CLIENT.scene.draw_sidebar()
            pygame.display.update()
        

def generate_text_image(text, shadow=False, size=20, color=(255, 255, 255)):
    font = pygame.font.Font("assets/OETZTYP_.TTF", size)
    #if shadow:
    #    temp_shadow = font.render(str(text), False, (0, 0, 0))
    temp = font.render(str(text), False, color)
    #temp_shadow.blit(temp, (-5, -5))
    return temp

    # if targetImage is not None:
    #     targetImage.blit(temp, (x, y))
    #     return
    #data.WINDOW.blit(temp, (x, y))

def display_image_on_mouse(image):
    draw_image(image, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])


def update_savefile():
    data = [variables.completed_maps, variables.points, variables.skins_owned, variables.other]
    pickle.dump(data, open("assets/savefile/savefile.p", "wb"))

def get_opposite_path(path):
    """Returns opposite path as an int, 0 being top path, 1 being bottom path"""
    new_path = path + 1
    if new_path > 1:
        new_path = 0
    return new_path
