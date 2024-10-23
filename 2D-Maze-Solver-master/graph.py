import sys
from maze import Maze


class Node:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.cost = 0
        self.parent = None
        self.east = None
        self.south = None
        self.west = None
        self.north = None
        self.heuristic = 0

    def check_equality(self, x, y):
        return x == self.x and y == self.y

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"


class Graph:

    nodes = [] #Mantiene todos los nodos en una lista para prevenir nodos duplicados
    maze = None

    def __init__(self):
        #Creando el grafo
        self.maze = Maze()
        self.root = self.create_node(self.maze.start[0], self.maze.start[1])

        # Encontrar la profundidad máxima.
        self.maximum_depth = self.find_maximum_depth() - 1

        # Creando heurística
        self.create_heuristic()

        # Hacemos costo del nodo raíz 0, porque ahí es donde comenzamos.
        self.root.cost = 0

        self.imprimir()
         
    def imprimir(self):

        for node in self.nodes:
            print(self.get_node_cost(node.x,node.y))

    def create_node(self, x, y):
        node = Node()

        # inicializando las coordenadas del nodo.
        node.x = x
        node.y = y

        # Agrega el nodo en la lista de nodos
        self.nodes.append(node)

        # Fijando el coste 1 si no es una casilla trampa.
        if self.maze.traps[node.x][node.y] == 1:
            node.cost = 7
        else:
            node.cost = 1

        # Setting todos los nodos secundarios
        if self.maze.can_pass(node.x, node.y, "east"):
            # Antes de crear un nuevo nodo, debemos verificar si ese nodo existe. Si es así, no necesitamos crearlo.
            node.east = self.node_exists(node.x, node.y + 1)
            if node.east is None:
                node.east = self.create_node(node.x, node.y + 1)
                node.east.parent = node

        if self.maze.can_pass(node.x, node.y, "south"):
            node.south = self.node_exists(node.x + 1, node.y)
            if node.south is None:
                node.south = self.create_node(node.x + 1, node.y)
                node.south.parent = node

        if self.maze.can_pass(node.x, node.y, "west"):
            node.west = self.node_exists(node.x, node.y - 1)
            if node.west is None:
                node.west = self.create_node(node.x, node.y - 1)
                node.west.parent = node

        if self.maze.can_pass(node.x, node.y, "north"):
            node.north = self.node_exists(node.x - 1, node.y)
            if node.north is None:
                node.north = self.create_node(node.x - 1, node.y)
                node.north.parent = node

        return node

    def node_exists(self, x, y):
        for node in self.nodes:
            if node.check_equality(x, y):
                return node
        return None

    def find_maximum_depth(self):
        maximum_depth = 0

        for node in self.nodes:
            current_node = node
            local_depth = 0
            while current_node is not None:
                current_node = current_node.parent
                local_depth += 1

            # If local_depth is greater, we will set it as maximum_depth.
            maximum_depth = max(maximum_depth, local_depth)

        return maximum_depth

    def get_node_cost(self, x, y):
        for node in self.nodes:
            if node.check_equality(x, y):
                return node.cost
        return 0

    def clear_parents(self):
        for node in self.nodes:
            node.parent = None

    def create_heuristic(self):
        #Creando heurística por cada nodo
        for node in self.nodes:
            # Seleccione la distancia mínima a un objetivo más cercano
            total_cost = sys.maxsize
            for goal in self.maze.goals:
                cost = 0
                vertical_distance = goal[1] - node.y
                horizontal_distance = goal[0] - node.x

                # Luego agregaremos el costo de cada nodo hasta el estado objetivo
                x = 0
                y = 0
                while vertical_distance > 0:
                    y += 1
                    cost += self.get_node_cost(node.x, node.y + y)
                    vertical_distance -= 1
                while horizontal_distance > 0:
                    x += 1
                    cost += self.get_node_cost(node.x + x, node.y + y)
                    horizontal_distance -= 1
                while vertical_distance < 0:
                    y -= 1
                    cost += self.get_node_cost(node.x + x, node.y + y)
                    vertical_distance += 1
                while horizontal_distance < 0:
                    x -= 1
                    cost += self.get_node_cost(node.x + x, node.y + y)
                    horizontal_distance += 1

                #Selecciona la heuristica minima
                total_cost = min(total_cost, cost)

            # Después de calcular el costo total, lo asignamos a la heurística del nodo
            node.heuristic = total_cost
