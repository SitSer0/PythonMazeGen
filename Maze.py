import random


class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = [[15 for _ in range(width)] for _ in range(height)]
        self.visited = [[False for _ in range(width)] for _ in range(height)]
        self.sets = [[y * width + x for x in range(width)] for y in range(height)]

    def find_set(self, x, y):
        if self.sets[y][x] == y * self.width + x:
            return self.sets[y][x]
        else:
            self.sets[y][x] = self.find_set(self.sets[y][x] % self.width, self.sets[y][x] // self.width)
            return self.sets[y][x]

    def union_sets(self, x1, y1, x2, y2):
        set1 = self.find_set(x1, y1)
        set2 = self.find_set(x2, y2)
        if set1 != set2:
            self.sets[set2 // self.width][set2 % self.width] = set1

    def delete_wall(self, x1, y1, x2, y2):
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
        self.visited[y][x] = True
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.width and 0 <= new_y < self.height and not self.visited[new_y][new_x]:
                self.delete_wall(x, y, new_x, new_y)
                self.generate_dfs(new_x, new_y)

    def regenerate_dfs(self):
        self.matrix = [[15 for _ in range(self.width)] for _ in range(self.height)]
        self.visited = [[False for _ in range(self.width)] for _ in range(self.height)]

        self.generate_dfs(random.randint(0, self.width - 1), random.randint(0, self.height - 1))

    def regenerate_kruskal(self):
        self.matrix = [[15 for _ in range(self.width)] for _ in range(self.height)]
        self.sets = [[y * self.width + x for x in range(self.width)] for y in range(self.height)]
        self.generate_kruskal()

    def regenerate_prim(self):
        self.matrix = [[15 for _ in range(self.width)] for _ in range(self.height)]
        self.visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        self.generate_prims()
