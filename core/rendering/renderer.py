from typing import TYPE_CHECKING
from core.logging.logger import Logger


logger = Logger(__name__)

if TYPE_CHECKING:
    from game.field.battlefield import BattleField
    from game.units.base_units import Unit

class Renderer:
    """
    Класс консольного рендерера

    Умеет получать всякие данные от других объектов и выплевывает их интерпретацию в консоль
    """

    def __init__(self, battlefield: 'BattleField'):
        self.battlefield = battlefield
        logger.info(f"{self.__class__.__name__} initiated")


    def render_start_info(self, unit_left: 'Unit', unit_right: 'Unit'):
        """
        Выводит стартовую информацию о бое.

        Статы юнитов и их стартовую позицию на поле
        :return:
        """

        print('================== НАЧАЛО БИТВЫ ==================')
        print(f"В левом углу полоски: {unit_left.name}")
        print(f"В правом углу полоски: {unit_right.name}")
        self.render_battlefield()
        print("=" * 50)
        logger.info('Start message rendered')


    @staticmethod
    def render_end_info(winner: 'Unit'):
        """
        Выводит финальную информацию о результате боя
        :return:
        """

        print('================= БИТВА ОКОНЧЕНА =================')
        print(f"Победитель: {winner.name}")
        print("=" * 50)
        logger.info('End message rendered')


    @staticmethod
    def render_turn_number(turn_number):
        print(f"ХОД {turn_number}")


    def render_battlefield(self):
        """
        Выводит поле каждый ход (с указанием хода)

        Также выводит hp bar юнитов
        :return:
        """

        string_field = "|"
        for i in range(self.battlefield.size):
            unit = self.battlefield.cells[i]
            if unit is None:
                string_field += (self.battlefield.icon + "|")
            else:
                string_field += (unit.icon + "|")
        print(string_field)
        logger.info('Battlefield rendered')

    @staticmethod
    def render_unit_action(action: str, unit: 'Unit', target: 'Unit'=None, damage: int=None, distance: int=None):
        """
        Выводит действие юнита
        :return:
        """

        if action == 'move':
            print(f"Юнит {unit.name} двигается на {distance}")
            logger.info('Unit movement rendered')
        elif action == 'attack':
            print(f"Юнит {unit.name} атакует юнита {target.name} и наносит {damage} урона")
            logger.info('Unit attack rendered')


    @staticmethod
    def render_hp_bars(unit: 'Unit', length=10):
        """
        Выводит hp bar для юнитов
        :return:
        """

        current_health = unit.health
        max_health = unit.max_health

        ratio = current_health / max_health
        filled = int(length * ratio)
        emptied = int(length - filled)
        bar = '▮' * filled + '▯' * emptied

        print(str(f"{unit.name}: {bar} ({current_health}/{max_health})"))
        logger.info(f"HP bar rendered for unit {unit}")


    @staticmethod
    def render_turns_separator():
        """
        Выводит разделитель ходов
        :return:
        """

        print('-' * 50)
