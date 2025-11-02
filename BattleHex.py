from game.units.unit_factory import UnitFactory
from game.field.position import Position
from game.field.buttle_field import BattleField

pikeman = UnitFactory.create('pikeman', Position(1)) #TODO хардкод мерзость имени, хочется исправить

print(UnitFactory.get_registered_units())

print(f"имя: {pikeman.name}\n"
      f"скорость: {pikeman.speed}\n"
      f"здоровье: {pikeman.health}\n"
      f"{str(pikeman.position)}")

battlefield = BattleField(8)
battlefield.add_unit(pikeman)
battlefield.move_unit(pikeman, Position(3))
pikeman2 = UnitFactory.create('pikeman', Position(1))
battlefield.add_unit(pikeman2)
print(battlefield)
battlefield.move_unit(pikeman, Position(7))
print(battlefield)
battlefield.remove_unit(pikeman2)
print(battlefield)