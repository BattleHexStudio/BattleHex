from typing import TYPE_CHECKING, List, Optional


if TYPE_CHECKING:
    from game.field.buttle_field import BattleField
    from game.units.base_units import Unit


class BattleManager:
    def __init__(self, battlefield: 'BattleField'):
        self.battlefield = battlefield
        self.units_in_game: List['Unit'] = []
        self.current_turn = 0
        self.game_over = False
        self.winner:  Optional[str] = None


    def run(self, *units):
        for unit in units:
            self._add_unit(unit)
        print('-' * 50 + '\n')
        while not self.game_over:
            self._process_full_turn()
            self.current_turn += 1
            print(f"Ход {self.current_turn} завершён")
            print(self.battlefield, '\n')
            print('-' * 50 + '\n')

        print(f"🎉 Победитель: {self.winner}!")


    def get_game_state(self):
        pass


    def _add_unit(self, unit: 'Unit'):
        self.battlefield.add_unit(unit)
        self.units_in_game.append(unit)


    def _process_full_turn(self):
        alive_units = self._get_alive_units()
        sorted_units = sorted(alive_units, key=lambda unit: unit.speed, reverse=True)
        for unit_turned in sorted_units:
            self._process_unit_turn(unit_turned)
            if self._check_victory():
                break


    def _process_unit_turn(self, unit: 'Unit'):

        # TODO юнит не подходит вплотную, а останавливается в другом месте, надо подумать над логикой

        enemies = [enemy for enemy in self.units_in_game if enemy.alive and enemy != unit]
        if not enemies:
            return

        nearest_enemy = min(enemies, key=lambda e: self.battlefield.get_distance(unit.position, e.position))

        if unit.can_attack(nearest_enemy, self.battlefield):
            unit.attack(nearest_enemy, self.battlefield)
            return

        direction = unit.position.direction_to(nearest_enemy.position)

        new_position = unit.position + (direction * unit.speed)

        if not (self.battlefield.is_position_available(new_position)):
            for steps in range(unit.speed, 0, -1):
                new_position = unit.position + (direction * steps)
                if self.battlefield.is_position_available(new_position):
                    break
            else:
                return

        self.battlefield.move_unit(unit, new_position)


    def _check_victory(self):
        alive_units = self._get_alive_units()
        alive_unit_quantity = len(alive_units)
        if alive_unit_quantity == 1:
            self.game_over = True
            self.winner = alive_units[0].name
            return True
        else:
            return False


    def _get_alive_units(self):
        return [unit for unit in self.units_in_game if unit.alive]