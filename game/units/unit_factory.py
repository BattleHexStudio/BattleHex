from typing import Dict, Type
from re import sub

from game.field.position import Position
from game.units.base_units import Unit
from utils.data_functions import load_unit_data
from core.logging.logger import Logger


logger = Logger(__name__)


class UnitFactory:
    """
    Класс для создания юнитов

    Каждый класс юнита сохраняется в классе фабрики при помощи декоратора @UnitFactory.register

    При этом фабрика автоматически определяет ключ юнита в JSON

    Необходимо сохранять связь название класса <-> ключ в JSON

    Преобразование происходит в формате SpecialUnitClass --> special_unit_class
    """

    # Словарь, в котором хранятся все существующие классы по ключам из JSON
    _unit_list: Dict[str, Type[Unit]] = {}

    # Данные обо всех юнитах загружаются один раз при инициализации
    _unit_data_cache: Dict[str, dict] = {}
    _data_loaded = False


    @classmethod
    def preload_data(cls):
        """
        Подгружает все данные юнитов и хранит их внутри класса, чтобы не вызывать load по 1000 раз
        :return:
        """

        if not cls._data_loaded:
            for unit_name in cls._unit_list:
                cls._unit_data_cache[unit_name] = load_unit_data(unit_name)
            cls._data_loaded = True
        logger.info(f"Units data preloaded")


    @classmethod
    def register(cls, unit_class: Type[Unit]) -> Type[Unit]:
        """
        Декоратор регистрирует класс юнита в реестре фабрики, автоматически определяя его ключ в JSON
        :param unit_class:
        :return: unit_class
        """

        unit_name = cls._class_name_to_key(unit_class.__name__)

        cls._unit_list[unit_name] = unit_class

        logger.info(f"Unit class {unit_class.__name__} registered in UnitFactory")

        return unit_class


    @classmethod
    def create(cls, unit_name: str, position: Position) -> Unit:
        """
        Основной метод класса.

        Создает нового юнита по имени СТРОГО такому же, как ключ в JSON. TODO надо как-то автоматизировать

        1. Загружает данные из JSON TODO поправить, не прикольно при создании каждого нового юнита загружать все данные
        2. Находит в реестре зарегистрированных юнитов соответствующий класс
        3. Кастует новый экземпляр класса

        ValueError: если юнит не зарегистрирован, вылетает ошибка о том, что юнит не зарегистрирован

        :param unit_name:
        :param position:
        :return: unit_class
        """

        if not cls._data_loaded:
            cls.preload_data()

        unit_data = cls._unit_data_cache[unit_name]

        if unit_name not in cls._unit_list:
            available_units = list(cls._unit_list)
            logger.warning(f"Unsuccessful attempt to register a unit")
            raise ValueError(
                f'Юнит {unit_name} не зарегистрирован в фабрике.\n'
                f'Убедитесь, что юнит зарегистрирован при помощи декоратора @UnitFactory.register\n'
                f'Доступные юниты: {available_units}'
            )
        unit_class: Type['Unit'] = cls._unit_list[unit_name]

        created_unit = unit_class(unit_data=unit_data, position=position)

        logger.info(f"{unit_class.__name__} class unit has been created")

        return created_unit


    @classmethod
    def get_registered_units(cls) -> Dict[str, str]:
        """
        Возвращает словарь всех зарегистрированных юнитов вида {"json_key": "UnitClassName"}
        :return:
        """

        registered_units = {unit_name: unit_class.__name__ for unit_name, unit_class in cls._unit_list.items()}
        return registered_units


    @staticmethod
    def _class_name_to_key(class_name: str):
        """
        Преобразует имя класса в ключ для использования при загрузке данных из JSON

        Формат преобразований SpecialUnitClass --> special_unit_class
        :param class_name:
        :return: key_name:
        """

        key_name = sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower()
        return key_name
