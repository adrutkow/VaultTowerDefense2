import pygame
import funcs
import data
import variables
#from classes.scenes import MainMenu, MapSelect, DifficultySelect, Game


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
            # Go to map select
            data.CLIENT.go_to_map_select()

        # Exit button
        if self.id == 4:
            variables.running = False

        # Map button
        if 4 < self.id < 15:
            # Go to Difficulty select
            data.CLIENT.go_to_difficulty_select(self.id-5)

        if 15 < self.id < 19:
            # Go to game
            data.CLIENT.start_game(_map_id = data.CLIENT.scene.map_id, _difficulty=self.id-16)
            #data.CLIENT.scene = Game(map_id=data.CLIENT.scene.map_id, difficulty=self.id-16)

        # Go back to menu button
        if self.id == 15:
            data.CLIENT.go_to_main_menu()
            #data.CLIENT.scene = MainMenu()

        if 19 <= self.id <= 30:
            select = self.id - 19
            data.CLIENT.scene.sidebar.select = select

        if 31 <= self.id <= 33:
            if data.CLIENT.scene.tower_menu.get_tower_select() is not None:
                select = data.CLIENT.scene.tower_menu.get_tower_select()
                if self.id == 33:
                    select.sell()
                    data.CLIENT.scene.tower_menu.set_tower_select(None)
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
            #if not scene.round_spawner.round_playing:
            scene.round_spawner.next_round_button()
        if self.id == 35:
            variables.speedup = not variables.speedup
        if self.id == 36:
            if scene.win:
                map_id = scene.map_id
                difficulty = scene.difficulty
                variables.completed_maps[map_id][difficulty] = 1
                funcs.update_savefile()
                data.CLIENT.go_to_main_menu()
        
        if self.id >= 37 and self.id <= 43:
            button_slot_clicked = self.id - 37

            # If there's an ability at that slot
            if len(data.CLIENT.scene.grouped_abilities) - 1 >= button_slot_clicked:
                data.CLIENT.scene.activate_ability(button_slot_clicked)



    def is_inside(self, x, y):
        return self.x < x < self.x + self.w and self.y < y < self.y + self.h

    def check_click(self, x, y):
        if self.active:
            if self.is_inside(x, y):
                self.tick()

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
            size = data.TOWER_SIZE_DATA[self.select]
            #funcs.draw_image(tower_image, int(mouse_pos[0]-tower_image.get_width()/2), int(mouse_pos[1]-tower_image.get_height()/2))
            funcs.draw_image(tower_image, mouse_pos[0], mouse_pos[1], center=True)
            pygame.draw.circle(data.WINDOW, (0, 0, 0), (mouse_pos[0], mouse_pos[1]), size, 1)
            pygame.draw.circle(data.WINDOW, (255, 0, 0), (mouse_pos[0], mouse_pos[1]), range, 1)





class TowerMenu:
    def __init__(self):
        self.tower_select = None
        self.image = None
        self.text_image = None
        self.draw()

    def tick(self):
        self.draw()
        self.desc_display()
        if data.DEBUG_MODE:
            self.stat_display()

    def stat_display(self):
        if self.tower_select is None:
            return
        funcs.draw_text("AS: "+ str(self.tower_select.current_attack_speed), 15, 680, 10, [255, 0, 0])
        funcs.draw_text("DMG: "+ str(self.tower_select.current_damage), 15, 700, 10, [255, 0, 0])

    def desc_display(self):
        """Show upgrade description for towers when hovering the buy button"""
        # [24, 294, 162, 39],  # buy upgrade 1
        # [24, 384, 162, 39],  # buy upgrade 2

        if self.tower_select is None:
            self.text_image = None
            return

        mouse_pos = pygame.mouse.get_pos()
        is_hovering = None

        if funcs.is_in_rect(mouse_pos[0], mouse_pos[1], 24, 294, 162, 39):
            is_hovering = 0

        if funcs.is_in_rect(mouse_pos[0], mouse_pos[1], 24, 384, 162, 39):
            is_hovering = 1

        if is_hovering is not None:
            if self.text_image is None:
                if is_hovering == 0:
                    upgrade_level = self.tower_select.upgrade[0]
                    if upgrade_level < 5:
                        desc_text = data.TOWER_FIRSTPATH_DESCRIPTIONS[self.tower_select.id][upgrade_level]
                    else:
                        desc_text = "Max upgrade achieved"
                if is_hovering == 1:
                    upgrade_level = self.tower_select.upgrade[1]
                    if upgrade_level < 5:
                        desc_text = data.TOWER_SECONDPATH_DESCRIPTIONS[self.tower_select.id][upgrade_level]
                    else:
                        desc_text = "Max upgrade achieved"
                self.text_image = funcs.generate_text_image(desc_text)
            funcs.display_image_on_mouse(self.text_image)

        if is_hovering is None:
            # Reset the text image so that if we hover different upgrades, the text updates
            self.text_image = None

        


    def set_tower_select(self, tower):
        self.tower_select = tower
        self.update_image()

    def get_tower_select(self):
        return self.tower_select

    def update_image(self):
        off = 91
        self.text_image = None
        image = data.TOWER_MENU.copy()
        if self.tower_select is None:
            return
        image.blit(data.TOWER_IMAGES[self.tower_select.id], (65, 150-off))
        funcs.draw_text(data.TOWER_NAMES[self.tower_select.id]+str(self.tower_select.pops), 32, 13, targetImage=image)

        if self.tower_select.upgrade[0] < 5:
            funcs.draw_text(data.TOWER_FIRSTPATH_NAMES[self.tower_select.id][self.tower_select.upgrade[0]], 35, 255-off, targetImage=image)
            funcs.draw_text(str(data.TOWER_FIRSTPATH_PRICE[self.tower_select.id][self.tower_select.upgrade[0]])+"$", 32, 300-off, targetImage=image)
        else:
            funcs.draw_text("MAX!", 35, 255-off, targetImage=image)


        if self.tower_select.upgrade[1] < 5:
            funcs.draw_text(data.TOWER_SECONDPATH_NAMES[self.tower_select.id][self.tower_select.upgrade[1]], 35, 346-off, targetImage=image)
            funcs.draw_text(str(data.TOWER_SECONDPATH_PRICE[self.tower_select.id][self.tower_select.upgrade[1]])+"$", 32, 392-off, targetImage=image)
        else:
            funcs.draw_text("MAX!", 35, 346-off, targetImage=image)
        funcs.draw_text(str(int(self.tower_select.money_spent / 100 * 75))+"$", 26, 632-off, targetImage=image)

        for i in range(0, self.tower_select.upgrade[1]):
            image.blit(data.GREEN_RECT,(25, 374 - i*7 - off, 6, 6))

        for i in range(0, self.tower_select.upgrade[0]):
            image.blit(data.GREEN_RECT, (25, 284 - i*7 - off, 6, 6))

        if self.tower_select.upgrade[1] > 2:
            image.blit(data.LIMIT, (25, 256 - off))

        if self.tower_select.upgrade[0] > 2:
            image.blit(data.LIMIT, (25, 346 - off))

        
        self.image = image

    def draw(self):
        if self.tower_select is not None:
            if self.image is None:
                self.update_image()
            funcs.draw_image(self.image, 0, 91)
            return
        
            #funcs.draw_image(data.TOWER_MENU, 0, 91)
            #funcs.draw_text(data.TOWER_NAMES[self.tower_select.id]+str(self.tower_select.pops), 32, 104)
            #funcs.draw_image(data.TOWER_IMAGES[self.tower_select.id], 65, 150, final_x=78, final_y=92)
            # if self.tower_select.upgrade[0] < 5:
            #     funcs.draw_text(data.TOWER_FIRSTPATH_NAMES[self.tower_select.id][self.tower_select.upgrade[0]], 35, 255)
            #     funcs.draw_text(str(data.TOWER_FIRSTPATH_PRICE[self.tower_select.id][self.tower_select.upgrade[0]])+"$", 32, 300)
            # else:
            #     funcs.draw_text("MAX!", 35, 255)
            # if self.tower_select.upgrade[1] < 5:
            #     funcs.draw_text(data.TOWER_SECONDPATH_NAMES[self.tower_select.id][self.tower_select.upgrade[1]], 35, 346)
            #     funcs.draw_text(str(data.TOWER_SECONDPATH_PRICE[self.tower_select.id][self.tower_select.upgrade[1]])+"$", 32, 392)
            # else:
            #     funcs.draw_text("MAX!", 35, 346)
            # funcs.draw_text(str(int(self.tower_select.money_spent / 100 * 75))+"$", 26, 632)

            # for i in range(0, self.tower_select.upgrade[1]):
            #     pygame.draw.rect(data.WINDOW, (0, 255, 0), (25, 374 - i*7, 6, 6))

            # for i in range(0, self.tower_select.upgrade[0]):
            #     pygame.draw.rect(data.WINDOW, (0, 255, 0), (25, 284 - i*7, 6, 6))

            # if self.tower_select.upgrade[1] > 2:
            #     funcs.draw_image(data.LIMIT, 25, 256)

            # if self.tower_select.upgrade[0] > 2:
            #     funcs.draw_image(data.LIMIT, 25, 346)

class FloatingText:
    def __init__(self, text, x, y, size=30, speed=1, lifetime=3, color=(255, 255, 255), shadow=True):
        self.text = text
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = color
        self.lifetime = lifetime * 60
        self.timer = 0
        self.shadow = shadow

    def tick(self):
        self.draw()

    def draw(self):
        funcs.draw_text(self.text, self.x, self.y, size=self.size, shadow=self.shadow, color=self.color)
        self.timer += 1
        self.y -= self.speed
        print(self.timer)
        if self.timer > self.lifetime:
            data.CLIENT.scene.particles.remove(self)

class FloatingImage:
    def __init__(self, image, x, y, size=1, speed=1, dir_x=0, dir_y=0, lifetime=3):
        self.image = image
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.lifetime = lifetime * 60
        self.timer = 0
        self.dir_x = 0
        self.dir_y = 0

    def tick(self):
        self.draw()

    def draw(self):
        print(str(self.timer) + " " + str(self.lifetime))
        funcs.draw_image(self.image, self.x, self.y, center=True)
        self.timer += 1
        print(self.timer)
        if self.timer > self.lifetime:
            data.CLIENT.scene.particles.remove(self)