class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = "blue"

    def move_up(self, maze=None):
        if self.y > 0 and not maze.matrix[self.y][self.x] & 4:  # Проверяем северную стену
            self.y -= 1

    def move_down(self, maze=None):
        if self.y < maze.height - 1 and not maze.matrix[self.y][self.x] & 1:  # Проверяем южную стену
            self.y += 1

    def move_left(self, maze=None):
        if self.x > 0 and not maze.matrix[self.y][self.x] & 2:  # Проверяем западную стену
            self.x -= 1

    def move_right(self, maze=None):
        if self.x < maze.width - 1 and not maze.matrix[self.y][self.x] & 8:  # Проверяем восточную стену
            self.x += 1
