class File:
    """
    Класс File предоставляет методы для сохранения и загрузки лабиринта в файл.

    Attributes:
    - maze (Maze): Экземпляр класса Maze, который будет сохранен или загружен.

    Methods:
    - __init__(self, maze): Инициализирует экземпляр класса File с переданным лабиринтом.
    - saving(self): Сохраняет текущий лабиринт в файл.
    - loading(self): Загружает лабиринт из файла и обновляет текущий лабиринт.
    """
    def __init__(self, maze):
        """
        Инициализирует экземпляр класса File.

        Parameters:
        - maze (Maze): Экземпляр класса Maze, который будет сохранен или загружен.
        """
        self.maze = maze

    def saving(self):  # /Users/serafim/Desktop/Testaa
        """
        Сохраняет текущий лабиринт в файл.

        Пользователь вводит путь и имя файла для сохранения лабиринта в текстовый файл (.txt).
        """
        output_path = str(input("Путь до файла в формате /Users/serafim/Desktop/Testaa (файл сохранится в папку "
                                "Testaa): "))
        file_name = str(input("Введите желаемое имя (без формата файла .txt): "))
        try:
            maze_file = open(output_path + "/" + file_name + ".txt", 'w')
            for i in self.maze.matrix:
                for j in i:
                    maze_file.write(str(j) + " ")
                maze_file.write("\n")
            maze_file.close()
        except:
            print("Вы ввели некорректный путь")

    def loading(self):
        """
        Загружает лабиринт из файла и обновляет текущий лабиринт.

        Пользователь вводит путь и имя файла для загрузки лабиринта из текстового файла (.txt).
        """
        input_path = str(
            input("Путь до файла в формате /Users/serafim/Desktop/Testaa (файл должен быть в папке Testaa): "))
        file_name = str(input("Введите имя (без формата файла .txt): "))
        try:
            maze_file = open(input_path + "/" + file_name + ".txt", 'r')
            print(self.maze.matrix)
            self.maze.matrix = []
            for line in maze_file:
                self.maze.matrix.append(list(map(int, line.split())))
            print(self.maze.matrix)
            self.maze.width = len(self.maze.matrix[0])
            self.maze.height = len(self.maze.matrix)
            maze_file.close()
        except:
            print("Вы ввели некорректный путь")
