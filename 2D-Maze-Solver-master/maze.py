import re


class Maze:

    # Variables
    size = []
    wall_vertical = [[]]
    walls_horizontal = [[]]
    traps = [[]]
    start = []
    goals = []

    def __init__(self):
        self.read_maze()

    def read_maze(self):
        file = open("maze.txt", "r")
        #Lee la primera linea y remueve el salto de linea del final
        line = file.readline().rstrip("\n\r")
        empty_line = 0

        while empty_line < 2:
            # To be able to construct more beautiful input file, we let a blank line to be readable.
            if not line:
                empty_line += 1
            else:
                empty_line = 0

            # Revisamos encabezados
            if line == "Size":
                # Lee las siguientes dos lineas del txt
                first_size = file.readline().rstrip("\n\r")
                second_size = file.readline().rstrip("\n\r")
                self.set_size(first_size, second_size)
            elif line == "Walls":
                walls = []
                line = file.readline().rstrip("\n\r")
                #Leemos cada linea hasta la linea negra
                while line:
                    walls.append(line)
                    line = file.readline().rstrip("\n\r")
                self.set_walls(walls)
            elif line == "Traps":
                traps = []
                line = file.readline().rstrip("\n\r")
                #Leemos cada linea hasta la linea negra
                while line:
                    traps.append(line)
                    line = file.readline().rstrip("\n\r")
                self.set_traps(traps)
            elif line == "Start":
                start = file.readline().rstrip("\n\r")
                self.set_start(start)
            elif line == "Goals":
                goals = []
                line = file.readline().rstrip("\n\r")
                #Leemos cada linea hasta la linea negra
                while line:
                    goals.append(line)
                    line = file.readline().rstrip("\n\r")
                self.set_goals(goals)

            line = file.readline().rstrip("\n\r")

        file.close()

    # noinspection PyUnusedLocal
    def set_size(self, x, y):
        # Determinamos el numero de filas
        if "rows" in x:
            # Está escrito en maze.txt como "8 filas", por ej. Ahora, solo necesitamos el número 8 y eliminar otros caracteres.
            # Entonces usamos expresiones regulares para eliminar caracteres no numéricos y convertirlos en un número entero.
            self.size.append(int(re.sub("[^0-9]", "", x)))
        elif "rows" in y:
            self.size.append(int(re.sub("[^0-9]", "", y)))

        # Determinamos el numero de columnas
        if "columns" in x:
            self.size.append(int(re.sub("[^0-9]", "", x)))
        elif "columns" in y:
            self.size.append(int(re.sub("[^0-9]", "", y)))

        # Por último, llenaremos las matrices de paredes y trampas con cero.
        self.wall_vertical = [[0 for i in range(self.size[1] - 1)] for i in range(self.size[0])]
        self.walls_horizontal = [[0 for i in range(self.size[1])] for i in range(self.size[0] - 1)]
        self.traps = [[0 for i in range(self.size[1])] for i in range(self.size[0])]

    def set_walls(self, walls):
        walls_length = len(walls)

        for i in range(walls_length):
            # case fila
            if "row" in walls[i]:
                row_index = int(re.sub("[^0-9]", "", walls[i]))
                column_indexes = walls[i+1].split()
                for index in column_indexes:
                    self.wall_vertical[row_index - 1][int(index) - 1] = 1
            # case columna
            elif "column" in walls[i]:
                column_index = int(re.sub("[^0-9]", "", walls[i]))
                row_indexes = walls[i + 1].split()
                for index in row_indexes:
                    self.walls_horizontal[int(index) - 1][column_index - 1] = 1

    def set_traps(self, traps):
        for trap in traps:
            # Al usar una función de mapa, dividimos una cadena por espacios en blanco y convertimos cada uno de ellos en un número entero.
            indexes = list(map(int, trap.split()))
            self.traps[indexes[0] - 1][indexes[1] - 1] = 1

    def set_start(self, start):
        indexes = list(map(int, start.split()))
        self.start.append(indexes[0] - 1)
        self.start.append(indexes[1] - 1)

    def set_goals(self, goals):
        for goal in goals:
            indexes = list(map(int, goal.split()))
            indexes = list(map(lambda x: x - 1, indexes))
            self.goals.append(indexes)

    def can_pass(self, row, column, direction):
        #Revisa si el jugador puede pasar
        if direction == "east":
            if column == (self.size[1] - 1):
                return False
            # Devuelva True si no hay un muro de bloqueo en el lado este. De lo contrario, devuelve Falso.
            return self.wall_vertical[row][column] == 0
        elif direction == "south":
            if row == (self.size[0] - 1):
                return False
            return self.walls_horizontal[row][column] == 0
        elif direction == "west":
            if column == 0:
                return False
            return self.wall_vertical[row][column - 1] == 0
        elif direction == "north":
            if row == 0:
                return False
            return self.walls_horizontal[row - 1][column] == 0
