class Position:
    """
    Класс позиции (в будущем для более удобной работы с гексами)
    Хранит координаты ячейки поля, отсчет начинается с НУЛЯ, чтобы не ебаться с этим пока
    """

    def __init__(self, x: int, y: int = 0):
        self.x = x
        self.y = y


    def direction_to(self, target_position: 'Position'):
        return 1 if target_position.x > self.x else -1


    def __add__(self, other: int):
        return Position(self.x + other, self.y)


    def __sub__(self, other):
        return Position(self.x - other, self.y)


    def __lt__(self, other: 'Position'):
        return self.x < other.x


    def __str__(self):
        return f"({self.x}, {self.y})"
