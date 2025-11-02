from typing import Dict
from game.units.unit_factory import UnitFactory
from game.units.base_units import Infantry
from game.field.position import Position

@UnitFactory.register
class Pikeman(Infantry):
    def __init__(self, unit_data: Dict, position: Position):
        super().__init__(unit_data, position)

