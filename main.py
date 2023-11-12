from Maze import Maze
from Player import Player
from MazeApp import MazeApp
from Solve import Solver
from Files import File
import sys
import random

sys.setrecursionlimit(10000)

def main():
    """
    Основная функция для создания и запуска игры в лабиринте.

    Считывает аргументы командной строки, проверяет их корректность и инициализирует игру.
    """
    type_game = ["multi", "solo"]

    if len(sys.argv) != 4:
        print("Прочитайте инструкцию по вводу и попробуйте еще раз")
        exit(0)

    width_ = int(sys.argv[1])
    height_ = int(sys.argv[2])

    if (not sys.argv[3] in type_game) or width_ > 200 or width_ < 2 or height_ > 200 or height_ < 2:
        print("Прочитайте инструкцию по вводу и попробуйте еще разzzz")
        exit(0)

    start_x = random.randint(0, width_ - 1)
    start_y = random.randint(0, height_ - 1)

    finish_x = random.randint(0, width_ - 1)
    finish_y = random.randint(0, height_ - 1)

    while finish_y == start_y and finish_x == start_x:
        finish_x = random.randint(0, width_ - 1)
        finish_y = random.randint(0, height_ - 1)

    CELL_SIZE = min(800 // height_, 1100 // width_)

    maze = Maze(width_, height_)
    maze.generate_dfs(start_x, start_y)  # Передаем экземпляр в качестве аргумента
    player = Player(start_x, start_y)
    solver = Solver(maze)
    solver.solve(start_x, start_y, finish_x, finish_y)
    file = File(maze)
    app = MazeApp(maze, CELL_SIZE, start_x, start_y, finish_x, finish_y, solver.path, solver, file, sys.argv[3])
    app.mainloop()

if __name__ == "__main__":
    main()
