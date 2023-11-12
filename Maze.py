import random


class Maze:
    """
    Класс Maze представляет генератор лабиринта и методы для его генерации с использованием различных алгоритмов.

    Attributes:
    - width (int): Ширина лабиринта.
    - height (int): Высота лабиринта.
    - matrix (list): Двумерный массив, представляющий лабиринт. Каждая ячейка содержит битовую маску, представляющую стены.
    - visited (list): Двумерный массив, отслеживающий посещенные ячейки в процессе генерации лабиринта.
    - sets (list): Двумерный массив, представляющий наборы ячеек для алгоритма Крускала.

    Methods:
    - find_set(self, x, y): Находит набор (set) для указанной ячейки в алгоритме Крускала.
    - union_sets(self, x1, y1, x2, y2): Объединяет два набора в алгоритме Крускала.
    - delete_wall(self, x1, y1, x2, y2): Удаляет стену между двумя ячейками.
    - _add_walls(self, cell, walls): Добавляет стены для ячейки в список стен.
    - generate_prims(self): Генерирует лабиринт методом Прима.
    - generate_kruskal(self): Генерирует лабиринт методом Крускала.
    - generate_dfs(self, x, y): Генерирует лабиринт методом Depth-First Search (DFS).
    - regenerate_dfs(self): Перегенерирует лабиринт методом DFS.
    - regenerate_kruskal(self): Перегенерирует лабиринт методом Крускала.
    - regenerate_prim(self): Перегенерирует лабиринт методом Прима.
    """
    def __init__(self, width, height):
        """
        Инициализирует экземпляр класса Maze.

        Parameters:
        - width (int): Ширина лабиринта.
        - height (int): Высота лабиринта.
        """
        self.width = width
        self.height = height
        self.matrix = [[15 for _ in range(width)] for _ in range(height)]
        self.visited = [[False for _ in range(width)] for _ in range(height)]
        self.sets = [[y * width + x for x in range(width)] for y in range(height)]

    def find_set(self, x, y):
        """
        Находит набор (set) для указанной ячейки в алгоритме Крускала.

        Parameters:
        - x (int): Координата x ячейки.
        - y (int): Координата y ячейки.

        Returns:
        - int: Номер набора, к которому принадлежит указанная ячейка.
        """
        if self.sets[y][x] == y * self.width + x:
            return self.sets[y][x]
        else:
            self.sets[y][x] = self.find_set(self.sets[y][x] % self.width, self.sets[y][x] // self.width)
            return self.sets[y][x]

    def union_sets(self, x1, y1, x2, y2):
        """
        Объединяет два набора в алгоритме Крускала.

        Parameters:
        - x1 (int): Координата x первой ячейки.
        - y1 (int): Координата y первой ячейки.
        - x2 (int): Координата x второй ячейки.
        - y2 (int): Координата y второй ячейки.
        """
        set1 = self.find_set(x1, y1)
        set2 = self.find_set(x2, y2)
        if set1 != set2:
            self.sets[set2 // self.width][set2 % self.width] = set1

    def delete_wall(self, x1, y1, x2, y2):
        """
        Удаляет стену между двумя ячейками.

        Parameters:
        - x1 (int): Координата x первой ячейки.
        - y1 (int): Координата y первой ячейки.
        - x2 (int): Координата x второй ячейки.
        - y2 (int): Координата y второй ячейки.
        """
        if x1 == x2:
            if y1 > y2:
                self.matrix[y1][x1] &= ~4  # удалить верхнюю стену
                self.matrix[y2][x2] &= ~1  # удалить нижнюю стену
            else:
                self.matrix[y1][x1] &= ~1  # удалить нижнюю стену
                self.matrix[y2][x2] &= ~4  # удалить верхнюю стену
        else:
            if x1 > x2:
                self.matrix[y1][x1] &= ~2  # удалить левую стену
                self.matrix[y2][x2] &= ~8  # удалить правую стену
            else:
                self.matrix[y1][x1] &= ~8  # удалить правую стену
                self.matrix[y2][x2] &= ~2  # удалить левую стену

    def _add_walls(self, cell, walls):
        """
        Добавляет стены для ячейки в список стен.

        Parameters:
        - cell (tuple): Кортеж с координатами x и y ячейки.
        - walls (list): Список стен для добавления.
        """
        x, y = cell
        if y > 0 and self.visited[y - 1][x] == False:
            walls.append((x, y, x, y - 1))  # верхняя стена
        if y < self.height - 1 and self.visited[y + 1][x] == False:
            walls.append((x, y, x, y + 1))  # нижняя стена
        if x > 0 and self.visited[y][x - 1] == False:
            walls.append((x, y, x - 1, y))  # левая стена
        if x < self.width - 1 and self.visited[y][x + 1] == False:
            walls.append((x, y, x + 1, y))  # правая стена

    def generate_prims(self):
        """
        Генерирует лабиринт методом Прима.
        """
        walls = []
        # Выбираем начальную ячейку случайным образом и добавляем её стены в список
        start_cell = (random.randint(0, self.height - 1), random.randint(0, self.width - 1))
        self.visited[start_cell[0]][start_cell[1]] = True
        self._add_walls((start_cell[1], start_cell[0]), walls)

        while len(walls) != 0:
            wall = random.choice(walls)
            x1, y1, x2, y2 = wall

            # Если одна из двух ячеек посещена, а другая нет, разрушаем стену между ними
            if self.visited[y1][x1] != self.visited[y2][x2]:
                self.delete_wall(x1, y1, x2, y2)

                new_cell = (x2, y2) if self.visited[y1][x1] else (x1, y1)

                self.visited[new_cell[1]][new_cell[0]] = True

                self._add_walls(new_cell, walls)

            walls.remove(wall)

    def generate_kruskal(self):
        """
        Генерирует лабиринт методом Крускала.
        """
        edges = []
        for y in range(self.height):
            for x in range(self.width):
                if x > 0:
                    edges.append((x, y, x - 1, y))  # левая стена
                if y > 0:
                    edges.append((x, y, x, y - 1))  # верхняя стена

        random.shuffle(edges)  # Перемешиваем стены для случайного выбора

        # объединяем наборы, если стена разделяет два разных набора
        for edge in edges:
            x1, y1, x2, y2 = edge
            if self.find_set(x1, y1) != self.find_set(x2, y2):
                self.union_sets(x1, y1, x2, y2)
                self.delete_wall(x1, y1, x2, y2)

    def generate_dfs(self, x, y):
        """
        Генерирует лабиринт методом Depth-First Search (DFS).

        Parameters:
        - x (int): Координата x начальной ячейки.
        - y (int): Координата y начальной ячейки.
        """
        self.visited[y][x] = True
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.width and 0 <= new_y < self.height and not self.visited[new_y][new_x]:
                self.delete_wall(x, y, new_x, new_y)
                self.generate_dfs(new_x, new_y)

    def regenerate_dfs(self):
        """
        Перегенерирует лабиринт методом DFS.
        """
        self.matrix = [[15 for _ in range(self.width)] for _ in range(self.height)]
        self.visited = [[False for _ in range(self.width)] for _ in range(self.height)]

        self.generate_dfs(random.randint(0, self.width - 1), random.randint(0, self.height - 1))

    def regenerate_kruskal(self):
        """
        Перегенерирует лабиринт методом Крускала.
        """
        self.matrix = [[15 for _ in range(self.width)] for _ in range(self.height)]
        self.sets = [[y * self.width + x for x in range(self.width)] for y in range(self.height)]
        self.generate_kruskal()

    def regenerate_prim(self):
        """
        Перегенерирует лабиринт методом Прима.
        """
        self.matrix = [[15 for _ in range(self.width)] for _ in range(self.height)]
        self.visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.generate_prims()