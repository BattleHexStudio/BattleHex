from abc import ABC
from typing import Dict
from game.field.position import Position


class Unit(ABC):
    def __init__(self, unit_data: dict, position: Position):
        self.name = unit_data["name"]
        self.type = unit_data["type"]
        self.health = unit_data["health"]
        self.max_health = unit_data["health"]  # для полоски здоровья
        self.attack = unit_data["attack"]
        self.defense = unit_data["defense"]
        self.damage_min = unit_data["damage_min"]
        self.damage_max = unit_data["damage_max"]
        self.speed = unit_data["speed"]
        self.icon = unit_data["icon"]
        self.position = position


class Flyer(Unit):
    def __init__(self, unit_data: Dict, position: Position):
        super().__init__(unit_data, position)
        self.can_fly_over_obstacles = True


class Infantry(Unit):
    def __init__(self, unit_data: Dict, position: Position):
        super().__init__(unit_data, position)


class Archer(Unit):
    def __init__(self, unit_data: Dict, position: Position):
        super().__init__(unit_data, position)
        self.ammo = unit_data.get("ammo", 5)
        self.range = unit_data.get("range", 10)

