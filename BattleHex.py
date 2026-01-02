def main():
    from game.units.unit_factory import UnitFactory
    from game.field.position import Position
    from game.field.battlefield import BattleField
    from game.manager.battle_manager import BattleManager

    pikeman = UnitFactory.create('pikeman', Position(0)) #TODO хардкод-мерзость имени, хочется исправить
    archer = UnitFactory.create('archer', Position(22))

    battlefield = BattleField(23)


    battle = BattleManager(battlefield)

    battle.run(pikeman, archer)


if __name__ == "__main__":
    main()
