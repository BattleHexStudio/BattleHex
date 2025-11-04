from typing import TYPE_CHECKING, List, Optional
from core.logging.logger import Logger
from core.rendering.renderer import Renderer


logger = Logger(__name__)


if TYPE_CHECKING:
    from game.field.battlefield import BattleField
    from game.units.base_units import Unit


class BattleManager:
    """
    Класс менеджера битвы

    Умеет запускать и полностью обрабатывать автоматический бой 1 на 1 на одномерной карте.
    Примитивный ИИ умеет просто бить, когда бьется
    """

    def __init__(self, battlefield: 'BattleField'):
        self.battlefield = battlefield
        self.renderer = Renderer(self.battlefield)
        self.units_in_game: List['Unit'] = []
        self.current_turn = 0
        self.game_over = False
        self.winner:  Optional[str] = None
        logger.info(f"{self.__class__.__name__} initiated")


    def run(self, *units):
        """
        Основной геймлуп.
            - Добавляет поданных юнитов на поле
            - Ходит за каждого юнита
            - Атакует за каждого юнита
            - Отсылает данные в рендер
        :param units:
        :return:
        """

        logger.info(f"Game started")

        for unit in units:
            self._add_unit(unit)

        # TODO
        # надо каким-то образом исправить это дело, потому что на данный момент я никак не проверяю,
        # какой юнит слева, а какой справа, у меня даже нет понятия команд
        self.renderer.render_start_info(self.units_in_game[0], self.units_in_game[-1])

        while not self.game_over:
            self.current_turn += 1
            self.renderer.render_turn_number(self.current_turn)
            self._process_full_turn()
            self.renderer.render_battlefield()
            for unit in self.units_in_game:
                self.renderer.render_hp_bars(unit)
            self.renderer.render_turns_separator()

        self.renderer.render_end_info(self.winner)

        logger.info(f"Game is over with winner {self.winner}")


    def get_game_state(self):
        """
        Концептуально должна мочь послать все данные о бое в рендер, но пока просто молча существует
        :return:
        """
        pass


    def _add_unit(self, unit: 'Unit'):
        """
        Добавляет юнита на поле (простит поле битвы добавить юнита через self.battlefield.add_unit())
        :param unit:
        :return:
        """

        self.battlefield.add_unit(unit)
        self.units_in_game.append(unit)


    def _process_full_turn(self):
        """
        Обрабатывает один полный ход (ход за каждого юнита)
        :return:
        """

        alive_units = self._get_alive_units()
        sorted_units = sorted(alive_units, key=lambda unit: unit.speed, reverse=True)
        for unit_turned in sorted_units:
            self._process_unit_turn(unit_turned)
            if self._check_victory():
                break

        logger.info(f"Turn number {self.current_turn} processed")


    def _process_unit_turn(self, unit: 'Unit'):
        """
        С позволения сказать ИИ, который решает, что делать юниту в зависимости от ситуации на поле.

        Теоретически умеет обрабатывать бои не только 1 на 1, но тестов не проходила и скорее всего сдохнет.
        Хотя по идее оно будет работать, как просто "каждый сам за себя"
        :param unit:
        :return:
        """

        # находим всех врагов
        enemies = [enemy for enemy in self.units_in_game if enemy.alive and enemy != unit]
        if not enemies:
            return

        # находим ближайшего врага
        nearest_enemy = min(enemies, key=lambda e: self.battlefield.get_distance(unit.position, e.position))


        # атакуем врага, если можем с текущей позиции
        if unit.can_attack(nearest_enemy, self.battlefield):
            damage = unit.attack(nearest_enemy, self.battlefield)
            self.renderer.render_unit_action('attack', unit=unit, target=nearest_enemy, damage=damage)
            return


        # пытаемся найти позицию, с которой можно атаковать
        attack_position = unit.find_attack_position(nearest_enemy, self.battlefield)


        # если атакующая позиция найдена, двигаемся на нее
        if attack_position:
            # Двигаемся к атакующей позиции
            self.battlefield.move_unit(unit, attack_position)
            return


        # Если не смогли найти атакующую позицию, просто двигаемся в сторону врага
        direction = unit.position.direction_to(nearest_enemy.position)

        new_position = unit.position + (direction * unit.speed)

        if not (self.battlefield.is_position_available(new_position)):
            for steps in range(unit.speed, -1, -1):
                new_position = unit.position + (direction * steps)
                if self.battlefield.is_position_available(new_position):
                    break
            else:
                return

        distance = self.battlefield.move_unit(unit, new_position)
        self.renderer.render_unit_action('move', unit=unit, distance=distance)


    def _check_victory(self):
        """
        Проверяет, не случилась ли победы и, как следствие - конец игры
        :return:
        """

        alive_units = self._get_alive_units()
        alive_unit_quantity = len(alive_units)
        if alive_unit_quantity == 1:
            self.game_over = True
            self.winner = alive_units[0]
            return True
        else:
            return False


    def _get_alive_units(self):
        """
        Добывает список всех живых юнитов на поле
        :return:
        """

        return [unit for unit in self.units_in_game if unit.alive]