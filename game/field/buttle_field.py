from typing import List, Optional, Dict
from game.units.base_units import Unit
from game.field.position import Position
from utils.data_functions import load_field_data


class BattleField:
    def __init__(self, size: int):
        self.icon = load_field_data("icon")
        self.size = size
        self.cells: List[Optional[Unit]] = [None] * size
        self._unit_positions: Dict[Unit, Position] = {}


    def _is_cell_free(self, position: Position):
        return self.cells[position.x] is None


    def _is_valid_position(self, position: Position):
        return 0 <= position.x < self.size


    def add_unit(self, unit: Unit) -> None:
        if unit in self._unit_positions:
            raise ValueError('Этот юнит уже есть на поле')
        if self._is_cell_free(unit.position):
            if self._is_valid_position(unit.position):
                self.cells[unit.position.x] = unit
                self._unit_positions[unit] = unit.position
            else:
                raise ValueError('Указанные координаты превышают размеры поля')
        else:
            raise ValueError('Клетка занята, туда нельзя поставить юнита')


    def remove_unit(self, unit: Unit):
        unit_position = self._unit_positions[unit]
        self.cells[unit_position.x] = None
        self._unit_positions.pop(unit)


    def get_unit_at(self, position: Position) -> Optional[Unit]:
        if self._is_valid_position(position):
            return self.cells[position.x]
        else:
            return None


    def move_unit(self, unit: Unit, new_position: Position):
        if self._is_valid_position(new_position) and self._is_cell_free(new_position):
            old_position: Position = self._unit_positions[unit]
            self.cells[old_position.x] = None
            self.cells[new_position.x] = unit
            self._unit_positions[unit] = new_position
            unit.position = new_position
        else:
            raise ValueError('невозможно переместить юнита на эту позицию')


    @staticmethod
    def get_distance(position1: Position, position2: Position):
        return abs(position1.x - position2.x)


    def __str__(self):
        string_field = "|"
        for i in range(self.size):
            unit = self.cells[i]
            if unit is None:
                string_field += (self.icon + "|")
            else:
                string_field += (unit.icon + "|")
        return string_field

