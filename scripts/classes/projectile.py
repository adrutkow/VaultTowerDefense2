import pygame
import math
import funcs
import data
import random

class Projectile:
    def __init__(self, x, y, id, angle, damage, pierce, lifetime, speed, camo, lead, owner=None, bomb=False, size=10):
        self.x = x
        self.y = y
        self.size = size
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
        self.bomb = bomb
        #self.w = data.PROJECTILE_IMAGES[self.id].get_width()
        #self.h = data.PROJECTILE_IMAGES[self.id].get_height()
        self.owner = owner
        #image = data.PROJECTILE_IMAGES[self.id]
        #self.image = pygame.transform.rotate(image, -math.degrees(self.angle))
        #self.image_rect = self.image.get_rect(center = (self.x, self.y))
        #self.image = data.PROJECTILE_IMAGES[self.id]
        image = data.PROJECTILE_IMAGES[self.id]
        self.image = funcs.rotate_image(image, -math.degrees(self.angle))
        

    def tick(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.lifetime += 1

        if self.lifetime > self.maxlifetime:
            self.die()
            return

        for i in data.CLIENT.scene.bloons:
            if self.pierce <= 0:
                break
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
            #if funcs.circle_collision(self.x, self.y, self.w, self.h, i.x, i.y, i.w, i.h):
            if funcs.circle_collision((self.x, self.y, self.size), (i.x, i.y, i.size)):

                # if self.bomb:
                #     self.owner.summon_projectile(_x = self.x, _y = self.y, _projectile_id = 2, _speed = 0,
                #                                   _damage = self.damage, _pierce = self.pierce, _lifetime = 15, _size = 30)
                #     #data.CLIENT.scene.projectiles.append(Projectile(self.x, self.y, 2, 0, self.current_damage, self.pierce, 8*60, 0, False, True, self.owner))
                #     self.pierce = 0

                if i.lead and not self.lead:
                    metal_sounds = [data.SOUND_METAL_HIT1, data.SOUND_METAL_HIT2]
                    random.choice(metal_sounds).play()
                    self.die()
                    break

                if self.owner is not None:
                    self.owner.on_target_hit(self, i)
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


                # Get all bonus damage towards bloon
                self.damage += i.get_bonus_damage()

                # if the bloon's RBE value is lower or equal to damage, pop it
                if data.BLOON_RBE_DATA[i.id] <= self.damage:
                    i.pop()
                    scene.gold += data.BLOON_RBE_DATA[i.id] * multiplier
                    self.owner.add_pops(data.BLOON_RBE_DATA[i.id])
                else:
                    # ALGORITHM FOR BLOONS
                    if i.id < 11:
                        children = []
                        # if the bloon has more hp than projectile has damage, just remove some hp from bloon
                        if i.health > self.damage:
                            i.health -= self.damage
                            self.owner.add_pops(self.damage)
                            self.already_hit.append(i)
                        # if the hp and damage is exactly the same, simply spawn bloon's children
                        elif i.health == self.damage:
                            print("SPAWNED CHILDREN")
                            i.spawn_children(self)
                            i.pop()
                            scene.gold += 1 * multiplier
                            self.owner.add_pops(self.damage)
                        # if the hp is lower than proj damage:
                        elif i.health < self.damage:
                            # Damage the current health left
                            remaining_damage = self.damage - i.health
                            self.owner.add_pops(i.health)
                            scene.gold += 1 * multiplier

                            # Go down a layer for each extra damage
                            children = data.BLOON_CHILDREN_DATA[i.id].copy()
                            for _ in range(0, remaining_damage):

                                # Give rewards simulating popping the current children
                                for child in children:
                                    self.owner.add_pops(1)
                                    scene.gold += 1 * multiplier
                                
                                # Get the children's children
                                temp_children = []
                                for child in children:
                                    child_children = data.BLOON_CHILDREN_DATA[child]

                                    for child_child in child_children:
                                        temp_children.append(child_child)

                                # Replace current children by the children's children
                                children = temp_children.copy()

                            i.spawn_children(self, children)
                            i.pop()








                            # layer_down = 0
                            # current_damage = self.damage
                            # children = []
                            # self.owner.add_pops(self.damage)

                            # while current_damage > 0:

                            #     i.health -= 1
                            #     current_damage -= 1

                            #     if i.health <= 0:
                            #         scene.gold += 1 * multiplier
                            #         print("ADDED GOLD")
                            #         i.health = data.BLOON_HP_DATA[i.id-layer_down]

                            #         if i.id - layer_down == 0:
                            #             if len(children) > 0:
                            #                 children.remove(children[-1])
                            #         else:
                            #             if children == []:
                            #                 children = data.BLOON_CHILDREN_DATA[i.id]
                            #             else:
                            #                 new_children = []
                            #                 for j in children:
                            #                     for k in data.BLOON_CHILDREN_DATA[j]:
                            #                         new_children.append(k)
                            #                 children = new_children
                            #         layer_down += 1

                            # i.spawn_children(self, children)
                            # i.pop()

                    # ALGORITHM FOR MOABS
                    else:
                        # if the moab has more hp than projectile has damage, just remove some hp from bloon
                        if i.health > self.damage:
                            i.health -= self.damage
                            self.already_hit.append(i)
                            self.owner.add_pops(self.damage)
                        # if the hp and damage is exactly the same, simply spawn moab's children
                        elif i.health == self.damage:
                            i.spawn_children(self)
                            i.pop()
                            scene.gold += 1 * multiplier
                            self.owner.add_pops(self.damage)
                        # if the hp is lower than projectile damage, spawn children anyway
                        elif i.health < self.damage:
                            i.spawn_children(self)
                            i.pop()
                            scene.gold += 1 * multiplier
                            self.owner.add_pops(i.health)


                self.pierce -= 1
                if self.pierce <= 0:
                    # temporary fix: if projectile is salt's explosion, don't kill it yet
                    if self.id == 2:    
                        break
                    self.die()
                    return


        self.draw()

    def die(self):
        data.CLIENT.scene.projectiles.remove(self)
        del self

    def draw(self):
        #pygame.draw.rect(data.WINDOW, (255, 255, 255), (self.x, self.y, 15, 15), 3)
        #funcs.draw_image(self.image, self.x, self.y, center=True, rect=self.image_rect)
        #new_rect = self.image_rect.move(self.x, self.y)
        #data.WINDOW.blit(self.image, self.image_rect)
        funcs.draw_image(self.image, self.x, self.y, center=True)
        pygame.draw.circle(data.WINDOW, (255, 0, 0), (self.x, self.y), self.size, 1)