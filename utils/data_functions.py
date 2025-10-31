from json import load

def load_unit_data(unit_name: str) -> dict:
    with open('data/game_data/units.json') as file:
        return load(file)[unit_name]

