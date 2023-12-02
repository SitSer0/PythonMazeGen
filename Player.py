class Player:
    """
    Класс Player представляет игрового персонажа, который может перемещаться в лабиринте.

    Attributes:
    - x (int): Координата x текущего положения игрока.
    - y (int): Координата y текущего положения игрока.
    - color (str): Цвет игрока.

    Methods:
    - move_up(self, maze=None): Перемещает игрока вверх, если возможно.
    - move_down(self, maze=None): Перемещает игрока вниз, если возможно.
    - move_left(self, maze=None): Перемещает игрока влево, если возможно.
    - move_right(self, maze=None): Перемещает игрока вправо, если возможно.
    """
    def __init__(self, x, y):
        """
        Инициализирует экземпляр класса Player.

        Parameters:
        - x (int): Координата x начального положения игрока.
        - y (int): Координата y начального положения игрока.
        """
        self.x = x
        self.y = y
        self.color = "blue"

    def move_up(self, maze=None):
        """
        Перемещает игрока вверх, если возможно.

        Parameters:
        - maze (Maze): Экземпляр класса Maze, представляющий лабиринт.
        """
        if self.y > 0 and not maze.matrix[self.y][self.x] & 4:
            self.y -= 1

    def move_down(self, maze=None):
        """
        Перемещает игрока вниз, если возможно.

        Parameters:
        - maze (Maze): Экземпляр класса Maze, представляющий лабиринт.
        """
        if self.y < maze.height - 1 and not maze.matrix[self.y][self.x] & 1:
            self.y += 1

    def move_left(self, maze=None):
        """
        Перемещает игрока влево, если возможно.

        Parameters:
        - maze (Maze): Экземпляр класса Maze, представляющий лабиринт.
        """
        if self.x > 0 and not maze.matrix[self.y][self.x] & 2:
            self.x -= 1

    def move_right(self, maze=None):
        """
        Перемещает игрока вправо, если возможно.

        Parameters:
        - maze (Maze): Экземпляр класса Maze, представляющий лабиринт.
        """
        if self.x < maze.width - 1 and not maze.matrix[self.y][self.x] & 8:
            self.x += 1