from typing import List, Optional, Dict, TYPE_CHECKING
from game.field.position import Position
from utils.data_functions import load_field_data


if TYPE_CHECKING:
    from game.units.base_units import Unit


class BattleField:
    """
    Класс поля битвы, который создает поле и хранит информацию о нем.
    Может делать следующее:
        - Добавлять юнитов на поле
        - Убирать юнитов с поля
        - Передвигать юнитов по полю в рамках возможного
        - Рассчитывать дистанцию между двумя ячейками TODO (возможно, имеет смысл перенести это в класс Position)
    """

    # TODO УБРАТЬ принты в функциях, этим должен заниматься рендер

    def __init__(self, size: int):
        self.icon = load_field_data("icon")
        self.size = size
        self.cells: List[Optional['Unit']] = [None] * size
        self._unit_positions: Dict['Unit', Position] = {}


    def _is_cell_free(self, position: Position):
        """
        Проверяет свободна ли ячейка и можно ли поставить туда юнита.

        :param position:
        :return:
        """

        if self._is_valid_position(position):
            return self.cells[position.x] is None
        else:
            raise ValueError('позиция за пределами поля')


    def _is_valid_position(self, position: Position):
        """
        Проверяет размеры поля и возвращает возможность существования поданной позиции на данном поле

        :param position:
        :return:
        """

        return 0 <= position.x < self.size


    def _unit_on_field(self, unit: 'Unit'):
        """
        Проверяет, есть ли поданный юнит на поле

        :param unit:
        :return:
        """

        return unit in self.cells and unit in self._unit_positions


    def is_position_available(self, position: Position):
        """
        Публичный метод для проверки доступности ячейки для перемещения в нее юнита

        :param position:
        :return:
        """

        return self._is_valid_position(position) and self._is_cell_free(position)


    def add_unit(self, unit: 'Unit') -> None:
        """
        Добавляет поданного юнита на поле, если это возможно

        :param unit:
        :return:
        """

        if unit in self._unit_positions:
            raise ValueError('Этот юнит уже есть на поле')
        if self._is_cell_free(unit.position):
            if self._is_valid_position(unit.position):
                self.cells[unit.position.x] = unit
                self._unit_positions[unit] = unit.position
                print(f"Юнит {unit.name} добавлен на поле")
            else:
                raise ValueError('Указанные координаты превышают размеры поля')
        else:
            raise ValueError('Клетка занята, туда нельзя поставить юнита')


    def remove_unit(self, unit: 'Unit'):
        """
        Убирает юнита с поля, если это возможно

        :param unit:
        :return:
        """

        if self._unit_on_field(unit):
            unit_position = self._unit_positions[unit]
            self.cells[unit_position.x] = None
            self._unit_positions.pop(unit)
            print(f"Юнит {unit.name} убран с поля")


    def get_unit_at(self, position: Position) -> Optional['Unit']:
        """
        Возвращает юнита, который находится на поданной позиции

        :param position:
        :return:
        """

        if self._is_valid_position(position):
            return self.cells[position.x]
        else:
            return None


    def move_unit(self, unit: 'Unit', new_position: Position):
        """
        Передвигает юнита по полю в рамках допустимого
            - Проверяет, есть ли юнит на поле
            - Проверяет, возможна ли поданная позиция на данном поле
            - Проверяет, свободна ли поданная позиция
            - Двигает юнита
        :param unit:
        :param new_position:
        :return:
        """

        if self._unit_on_field(unit):
            if self._is_valid_position(new_position) and self._is_cell_free(new_position):
                old_position: Position = self._unit_positions[unit]
                self.cells[old_position.x] = None
                self.cells[new_position.x] = unit
                self._unit_positions[unit] = new_position
                unit.position = new_position
                print(f"Юнит {unit.name} передвинут на {self.get_distance(old_position, new_position)}")
            else:
                raise ValueError('невозможно переместить юнита на эту позицию')


    @staticmethod
    def get_distance(position1: Position, position2: Position):
        """
        Рассчитывает расстояние между двумя ячейками поля
        TODO возможно, тоже стоит переместить в класс Position

        :param position1:
        :param position2:
        :return:
        """

        return abs(position1.x - position2.x)


    def __str__(self):
        """
        Преобразует поле в строку для более удобного вывода в консоль
        :return:
        """

        string_field = "|"
        for i in range(self.size):
            unit = self.cells[i]
            if unit is None:
                string_field += (self.icon + "|")
            else:
                string_field += (unit.icon + "|")
        return string_field
