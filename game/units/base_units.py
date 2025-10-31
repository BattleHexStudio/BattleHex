from abc import ABC
from utils.data_functions import load_unit_data


class Unit(ABC):
    def __init__(self, unit_name: str, position):
        self.unit_data = load_unit_data(unit_name)
        self.name = self.unit_data["name"]
        self.type = self.unit_data["type"]
        self.health = self.unit_data["health"]
        self.max_health = self.unit_data["health"]  # для полоски здоровья
        self.attack = self.unit_data["attack"]
        self.defense = self.unit_data["defense"]
        self.damage_min = self.unit_data["damage_min"]
        self.damage_max = self.unit_data["damage_max"]
        self.speed = self.unit_data["speed"]
        self.position = position


    def move(self):
        pass


    def attack(self):
        pass


class Flyer(Unit):
    def __init__(self, unit_name: str, position):
        super().__init__(unit_name, position)
        self.can_fly_over_obstacles = True


class Infantry(Unit):
    def __init__(self, unit_name: str, position):
        super().__init__(unit_name, position)
        self.can_retaliate = True


class Archer(Unit):
    def __init__(self, unit_name: str, position):
        super().__init__(unit_name, position)
        self.ammo = self.unit_data.get("ammo", 5)
        self.range = self.unit_data.get("range", 10)

