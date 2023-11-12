class Solver:
    """
    Класс Solver представляет собой объект для поиска пути в лабиринте.

    Attributes:
    - maze (Maze): Экземпляр класса Maze, представляющий лабиринт.
    - path (list): Двумерный список, представляющий длины пути от каждой ячейки до конечной точки.

    Methods:
    - solve(self, x1, y1, x2, y2): Использует глубинный поиск для нахождения кратчайшего пути от (x1, y1) до (x2, y2).
    """

    def __init__(self, maze):
        """
        Инициализирует экземпляр класса Solver.

        Parameters:
        - maze (Maze): Экземпляр класса Maze, представляющий лабиринт.
        """
        self.maze = maze
        self.path = [[-2 for x in range(self.maze.width)] for y in range(self.maze.height)]

    def solve(self, x1, y1, x2, y2):
        """
        Использует глубинный поиск для нахождения кратчайшего пути от (x1, y1) до (x2, y2) в лабиринте.

        Parameters:
        - x1 (int): Координата x начальной точки.
        - y1 (int): Координата y начальной точки.
        - x2 (int): Координата x конечной точки.
        - y2 (int): Координата y конечной точки.
        """
        self.path = [[-2 for x in range(self.maze.width)] for y in range(self.maze.height)]
        visited_solve = [[False for x in range(self.maze.width)] for y in range(self.maze.height)]

        def dfs(x, y, length):
            """
            Рекурсивная функция для выполнения глубинного поиска.

            Parameters:
            - x (int): Текущая координата x.
            - y (int): Текущая координата y.
            - length (int): Длина текущего пути.

            Returns:
            - bool: True, если путь найден, иначе False.
            """
            if x == x2 and y == y2:  # Если мы достигли конечной точки
                self.path[y][x] = length
                return True
            visited_solve[y][x] = True

            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height and not visited_solve[ny][nx]:
                    if dx == 1:
                        wall = 8
                    elif dx == -1:
                        wall = 2
                    elif dy == 1:
                        wall = 1
                    else:
                        wall = 4

                    if not (self.maze.matrix[y][x] & wall) and dfs(nx, ny, length + 1):
                        self.path[y][x] = length
                        return True

            return False

        dfs(x1, y1, 0)