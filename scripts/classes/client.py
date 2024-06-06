import data
from classes.scenes import MainMenu, DifficultySelect, Game, MapSelect
import variables

class Client:
    def __init__(self):
        self.scene = MainMenu()
        self.scene_list = [MainMenu, DifficultySelect, MapSelect, Game]

    def tick(self):
        self.scene.tick()
        update_speed = 120 if variables.speedup else 60
        data.CLOCK.tick(update_speed)

    def start_game(self, _map_id=0, _difficulty=1):
        self.scene = Game(map_id=_map_id, difficulty=_difficulty)

    def go_to_difficulty_select(self, _map_id):
        self.scene = DifficultySelect(map_id=_map_id)

    def go_to_map_select(self):
        self.scene = MapSelect()

    def go_to_main_menu(self):
        self.scene = MainMenu()