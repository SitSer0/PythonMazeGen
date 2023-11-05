class Solver:

    def __init__(self, maze):
        self.maze = maze
        self.path = [[-2 for x in range(self.maze.width)] for y in range(self.maze.height)]

    def solve(self, x1, y1, x2, y2):
        self.path = [[-2 for x in range(self.maze.width)] for y in range(self.maze.height)]
        visited_solve = [[False for x in range(self.maze.width)] for y in range(self.maze.height)]

        def dfs(x, y, length):
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