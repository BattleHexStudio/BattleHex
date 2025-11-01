from game.units.unit_factory import UnitFactory
from game.field.buttle_field import Position

pikeman = UnitFactory.create('pikeman', Position(1)) #TODO хардкод мерзость имени, хочется исправить

print(UnitFactory.get_registered_units())

print(f"имя: {pikeman.name}\n"
      f"скорость: {pikeman.speed}\n"
      f"здоровье: {pikeman.health}\n"
      f"{str(pikeman.position)}")
