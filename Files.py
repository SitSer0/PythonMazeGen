class File:
    def __init__(self, maze):
        self.maze = maze

    def saving(self):  # /Users/serafim/Desktop/Testaa
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
