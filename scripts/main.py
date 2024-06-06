import pygame
import variables
import data
import funcs
import os
import pickle


# data = [completed_maps, points, skins_owned, other]
print("Checking if savefile exists")

pygame.mixer.init()

print("skipping savefile")
savefile_exists = os.path.exists('assets/savefile/savefile.p')
if savefile_exists:
    savefile_data = pickle.load(open("assets/savefile/savefile.p", "rb"))
    variables.completed_maps = savefile_data[0]
    variables.points = savefile_data[1]
    variables.skins_owned = savefile_data[2]
    variables.other = savefile_data[3]


# else:
#     completed_maps = [0, 0, 0] * 10
#     points = 0
#     skins_owned = []
#     other = []
#     data = [completed_maps, points, skins_owned, other]
#     print(completed_maps)
#     pickle.dump(data, open("assets/savefile/savefile.p", "wb"))


while variables.running:
    for e in pygame.event.get():
        funcs.handle_events(e)
    data.CLIENT.tick()

