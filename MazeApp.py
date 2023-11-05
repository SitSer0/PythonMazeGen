import tkinter as tk
import tkinter.messagebox as messagebox
from Player import Player
from tkinter import Button
import random
from Solve import Solver

class MazeApp(tk.Tk):

    def __init__(self, maze, cell_size, start_x, start_y, finish_x, finish_y, path, solver, file, type_game):
        super().__init__()
        self.type_game = type_game
        self.player = Player(start_x, start_y)

        self.finish_x = finish_x
        self.finish_y = finish_y
        self.maze = maze
        self.cell_size = cell_size
        self.start_x = start_x
        self.start_y = start_y
        self.title('Maze Generator')
        self.canvas = tk.Canvas(self, width=self.maze.width * self.cell_size, height=self.maze.height * self.cell_size, bg='white')
        self.canvas.pack(padx=10, pady=10)
        self.canvas.focus_set()  # Added this line to ensure canvas has focus
        self.path = path
        self.solver = solver
        self.file = file
        self.player2 = Player(random.randint(0, self.maze.width - 1), random.randint(0, self.maze.height - 1))

        self.bind("w", self.move_up)
        self.bind("s", self.move_down)
        self.bind("a", self.move_left)
        self.bind("d", self.move_right)

        if type_game == "multi":
            self.bind("<Up>", self.move_up_player2)
            self.bind("<Down>", self.move_down_player2)
            self.bind("<Left>", self.move_left_player2)
            self.bind("<Right>", self.move_right_player2)

        self.focus_set()
        self.draw_maze()

        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=10)

        self.restart_button = Button(buttons_frame, text="Генерация Prim", command=self.restart_game_prim)
        self.restart_button.pack(side=tk.LEFT,
                                 padx=5)

        self.restart_button = Button(buttons_frame, text="Генерация Краскала", command=self.restart_game_kruskal)
        self.restart_button.pack(side=tk.LEFT,
                                 padx=5)

        self.restart_button = Button(buttons_frame, text="Генерация DFS", command=self.restart_game_dfs)
        self.restart_button.pack(side=tk.LEFT,
                                 padx=5)
        if type_game != "multi":
            self.solve_button = Button(buttons_frame, text="Решить", command=self.solve_mazee)
            self.solve_button.pack(side=tk.LEFT,
                                   padx=5)

        self.save_button = Button(buttons_frame, text="Сохранить", command=self.saving)
        self.save_button.pack(side=tk.LEFT,
                              padx=5)

        self.save_button = Button(buttons_frame, text="Загрузить", command=self.loading)
        self.save_button.pack(side=tk.LEFT,
                              padx=5)

    def draw_maze(self):
        self.canvas.delete(tk.ALL)
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                cell_value = self.maze.matrix[y][x]
                if cell_value & 1:  # Южная стена
                    self.canvas.create_line(x * self.cell_size, (y + 1) * self.cell_size, (x + 1) * self.cell_size,
                                            (y + 1) * self.cell_size, fill="black", width=1)
                if cell_value & 2:  # Западная стена
                    self.canvas.create_line(x * self.cell_size, y * self.cell_size, x * self.cell_size,
                                            (y + 1) * self.cell_size,
                                            fill="black")
                if cell_value & 4:  # Северная стена
                    self.canvas.create_line(x * self.cell_size, y * self.cell_size, (x + 1) * self.cell_size,
                                            y * self.cell_size,
                                            fill="black")
                if cell_value & 8:  # Восточная стена
                    self.canvas.create_line((x + 1) * self.cell_size, y * self.cell_size, (x + 1) * self.cell_size,
                                            (y + 1) * self.cell_size, fill="black", width=1)
        #self.draw_green_cell(self.start_x, self.start_y, self.cell_size)
        self.draw_red_cell(self.finish_x, self.finish_y, self.cell_size)

        self.draw_player(self.player)
        if self.type_game == "multi":
            self.draw_player(self.player2, "purple")

    def draw_player(self, player, color=None):
        size = self.cell_size
        radius = size * 0.4
        circle_x = player.x * size + size / 2
        circle_y = player.y * size + size / 2
        self.canvas.create_oval(circle_x - radius, circle_y - radius,
                                circle_x + radius, circle_y + radius,
                                fill=color or player.color, tag="player")

    def draw_green_cell(self, x, y, cell_size):
        self.canvas.create_rectangle(
            x * cell_size + 1, y * cell_size + 1, (x + 1) * cell_size - 1, (y + 1) * cell_size - 1,
            fill="green"
        )

    def draw_red_cell(self, x, y, cell_size):
        self.canvas.create_rectangle(
            x * cell_size + 1, y * cell_size + 1, (x + 1) * cell_size - 1, (y + 1) * cell_size - 1,
            fill="red"
        )

    def draw_yellow_line_up(self, x, y, cell_size):
        start_x = (x + 0.5) * cell_size
        start_y = (y + 0.5) * cell_size
        end_x = start_x
        end_y = y * cell_size
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill="orange", width=2)

    def draw_yellow_line_right(self, x, y, cell_size):
        start_x = (x + 0.5) * cell_size
        start_y = (y + 0.5) * cell_size
        end_x = (x + 1) * cell_size
        end_y = start_y
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill="orange", width=2)

    def draw_yellow_line_down(self, x, y, cell_size):
        start_x = (x + 0.5) * cell_size
        start_y = (y + 0.5) * cell_size
        end_x = start_x
        end_y = (y + 1) * cell_size
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill="orange", width=2)

    def draw_yellow_line_left(self, x, y, cell_size):
        start_x = (x + 0.5) * cell_size
        start_y = (y + 0.5) * cell_size
        end_x = x * cell_size
        end_y = start_y
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill="orange", width=2)

    def move_up(self, event):
        self.player.move_up(self.maze)
        self.redraw_player()
        self.check_finish()

    def move_down(self, event):
        self.player.move_down(self.maze)
        self.redraw_player()
        self.check_finish()

    def move_left(self, event):
        self.player.move_left(self.maze)
        self.redraw_player()
        self.check_finish()

    def move_right(self, event):
        self.player.move_right(self.maze)
        self.redraw_player()
        self.check_finish()

    def move_up_player2(self, event):
        self.player2.move_up(self.maze)
        self.redraw_player()
        self.check_finish()

    def move_down_player2(self, event):
        self.player2.move_down(self.maze)
        self.redraw_player()
        self.check_finish()

    def move_left_player2(self, event):
        self.player2.move_left(self.maze)
        self.redraw_player()
        self.check_finish()

    def move_right_player2(self, event):
        self.player2.move_right(self.maze)
        self.redraw_player()
        self.check_finish()

    def redraw_player(self):
        self.canvas.delete("player")
        self.draw_player(self.player)
        if self.type_game == "multi":
            self.draw_player(self.player2, "purple")

    def game_over(self, message):
        messagebox.showinfo("Игра окончена", message)
        self.restart_game_dfs()

    def check_finish(self):
        if self.player.x == self.finish_x and self.player.y == self.finish_y:
            self.game_over("Вы прошли лабиринт!")
        if self.player2.x == self.finish_x and self.player2.y == self.finish_y:
            self.game_over("Player2 прошел лабиринт!")


    def restart_game_dfs(self):
        self.maze.regenerate_dfs()
        self.start_x = random.randint(0, self.maze.width - 1)
        self.start_y = random.randint(0, self.maze.height - 1)
        self.finish_x = random.randint(0, self.maze.width - 1)
        self.finish_y = random.randint(0, self.maze.height - 1)

        # Пересоздаем solver для нового лабиринта
        self.solver = Solver(self.maze)
        self.solver.solve(self.player.x, self.player.y, self.finish_x, self.finish_y)

        # Обновляем path на основе нового решения
        self.path = self.solver.path

        self.player.x = self.start_x
        self.player.y = self.start_y

        self.start_x = random.randint(0, self.maze.width - 1)
        self.start_y = random.randint(0, self.maze.height - 1)

        if self.type_game == "multi":
            self.start_x2 = random.randint(0, self.maze.width - 1)
            self.start_y2 = random.randint(0, self.maze.height - 1)
            self.player2.x = self.start_x2
            self.player2.y = self.start_y2

        self.draw_maze()
        self.draw_player(self.player)
        if self.type_game == "multi":
            self.draw_player(self.player2, "purple")

    def restart_game_prim(self):
        self.maze.regenerate_prim()
        self.start_x = random.randint(0, self.maze.width - 1)
        self.start_y = random.randint(0, self.maze.height - 1)
        self.finish_x = random.randint(0, self.maze.width - 1)
        self.finish_y = random.randint(0, self.maze.height - 1)

        # Пересоздаем solver для нового лабиринта
        self.solver = Solver(self.maze)
        self.solver.solve(self.player.x, self.player.y, self.finish_x, self.finish_y)

        # Обновляем path на основе нового решения
        self.path = self.solver.path

        self.player.x = self.start_x
        self.player.y = self.start_y

        if self.type_game == "multi":
            self.start_x2 = random.randint(0, self.maze.width - 1)
            self.start_y2 = random.randint(0, self.maze.height - 1)
            self.player2.x = self.start_x2
            self.player2.y = self.start_y2

        self.draw_maze()
        self.draw_player(self.player)
        if self.type_game == "multi":
            self.draw_player(self.player2, "purple")

    def restart_game_kruskal(self):
        self.maze.regenerate_kruskal()
        self.start_x = random.randint(0, self.maze.width - 1)
        self.start_y = random.randint(0, self.maze.height - 1)
        self.finish_x = random.randint(0, self.maze.width - 1)
        self.finish_y = random.randint(0, self.maze.height - 1)

        self.solver = Solver(self.maze)
        self.solver.solve(self.player.x, self.player.y, self.finish_x, self.finish_y)

        self.path = self.solver.path

        self.player.x = self.start_x
        self.player.y = self.start_y

        self.start_x = random.randint(0, self.maze.width - 1)
        self.start_y = random.randint(0, self.maze.height - 1)
        if self.type_game == "multi":
            self.start_x2 = random.randint(0, self.maze.width - 1)
            self.start_y2 = random.randint(0, self.maze.height - 1)
            self.player2.x = self.start_x2
            self.player2.y = self.start_y2

        self.draw_maze()
        self.draw_player(self.player)
        if self.type_game == "multi":
            self.draw_player(self.player2, "purple")

    def draw_path(self):
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.path[y][x] == -2:
                    continue
                if y + 1 < self.maze.height and abs(self.path[y + 1][x] - self.path[y][x]) == 1:
                    self.draw_yellow_line_down(x, y, self.cell_size)
                if y > 0 and abs(self.path[y - 1][x] - self.path[y][x]) == 1:
                    self.draw_yellow_line_up(x, y, self.cell_size)
                if x + 1 < self.maze.width and abs(self.path[y][x + 1] - self.path[y][x]) == 1:
                    self.draw_yellow_line_right(x, y, self.cell_size)
                if x > 0 and abs(self.path[y][x - 1] - self.path[y][x]) == 1:
                    self.draw_yellow_line_left(x, y, self.cell_size)

    def solve_mazee(self):
        self.solver.solve(self.player.x, self.player.y, self.finish_x, self.finish_y)
        self.path = self.solver.path
        self.draw_maze()
        self.draw_path()

    def saving(self):
        messagebox.showinfo("Сохранение файла", "Посмотрите консоль")
        self.file.saving()
        messagebox.showinfo("Файл сохранен", "Ок")

    def loading(self):
        messagebox.showinfo("Загрузка файла", "Посмотрите консоль")
        self.file.loading()

        self.start_x = random.randint(0, self.maze.width - 1)
        self.start_y = random.randint(0, self.maze.height - 1)
        self.finish_x = random.randint(0, self.maze.width - 1)
        self.finish_y = random.randint(0, self.maze.height - 1)

        # Пересоздаем solver для нового лабиринта
        self.solver = Solver(self.maze)
        self.solver.solve(self.player.x, self.player.y, self.finish_x, self.finish_y)

        # Обновляем path на основе нового решения
        self.path = self.solver.path

        self.player.x = self.start_x
        self.player.y = self.start_y

        self.start_x = random.randint(0, self.maze.width - 1)
        self.start_y = random.randint(0, self.maze.height - 1)
        if self.type_game == "multi":
            self.player2.x = self.start_x
            self.player2.y = self.start_y

        self.draw_maze()
        self.draw_player(self.player)
        if self.type_game == "multi":
            self.draw_player(self.player2, "purple")