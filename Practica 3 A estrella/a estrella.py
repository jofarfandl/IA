# A* puzzle8

from copy import deepcopy
from colorama import Fore, Back, Style

DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}     # estas son las instrucciones para mover el espacio vacio
END = [[0, 1, 2],       # este es el resultado esperado
       [3, 4, 5],
       [6, 7, 8]]

# unicode para dibujar la cajita
left_down_angle = '\u2514'
right_down_angle = '\u2518'
right_up_angle = '\u2510'
left_up_angle = '\u250C'

middle_junction = '\u253C'
top_junction = '\u252C'
bottom_junction = '\u2534'
right_junction = '\u2524'
left_junction = '\u251C'

bar = Style.BRIGHT + Fore.CYAN + '\u2502' + Fore.RESET + Style.RESET_ALL
dash = '\u2500'

first_line = Style.BRIGHT + Fore.CYAN + left_up_angle + dash + dash + dash + top_junction + dash + dash + dash + top_junction + dash + dash + dash + right_up_angle + Fore.RESET + Style.RESET_ALL
middle_line = Style.BRIGHT + Fore.CYAN + left_junction + dash + dash + dash + middle_junction + dash + dash + dash + middle_junction + dash + dash + dash + right_junction + Fore.RESET + Style.RESET_ALL
last_line = Style.BRIGHT + Fore.CYAN + left_down_angle + dash + dash + dash + bottom_junction + dash + dash + dash + bottom_junction + dash + dash + dash + right_down_angle + Fore.RESET + Style.RESET_ALL


# funcion que imprime el puzzle
def print_puzzle(array):
    print(first_line)
    for a in range(len(array)):
        for i in array[a]:
            if i == 0:
                print(bar, Back.RED + ' ' + Back.RESET, end=' ')
            else:
                print(bar, i, end=' ')
        print(bar)
        if a == 2:
            print(last_line)
        else:
            print(middle_line)

#crea el nodo para el puzzle

class Node:
    def __init__(self, current_node, previous_node, g, h, dir):
        self.current_node = current_node
        self.previous_node = previous_node
        self.g = g
        self.h = h
        self.dir = dir

    def f(self):
        return self.g + self.h

#esta funcion obtiene la posicion actual del elemento revisado y regresa la fila

def get_pos(current_state, element):
    for row in range(len(current_state)):
        if element in current_state[row]:
            return row, current_state[row].index(element)

#obtiene el costo total que se mueve desde el nodo raiz hasta el nodo meta

def total_cost(current_state):
    cost = 0
    for row in range(len(current_state)):
        for col in range(len(current_state[0])):
            pos = get_pos(END, current_state[row][col])
            cost += abs(row - pos[0]) + abs(col - pos[1])
    return cost
#la funcion que mueve el espacio vacio dentro del puzzle y comienza a hacer los movimientos con las direcciones declaradas
#y agrega un estado completamente nuevo en la lista de los estados cambiantes
# deepcopy lo hace recursivo, crea un nuevo contenedor para que todo pueda reorganizarse con el espacio vacío moviéndose
def expand(node):
    listNode = []
    emptyPos = get_pos(node.current_node, 0)

    for dir in DIRECTIONS.keys():
        newPos = (emptyPos[0] + DIRECTIONS[dir][0], emptyPos[1] + DIRECTIONS[dir][1])
        if 0 <= newPos[0] < len(node.current_node) and 0 <= newPos[1] < len(node.current_node[0]):
            newState = deepcopy(node.current_node)
            newState[emptyPos[0]][emptyPos[1]] = node.current_node[newPos[0]][newPos[1]]
            newState[newPos[0]][newPos[1]] = 0
            # listNode += [Node(newState, node.current_node, node.g + 1, total_cost(newState), dir)]
            listNode.append(Node(newState, node.current_node, node.g + 1, total_cost(newState), dir))

    return listNode

#esto considera cual es el mejor nodo para mover el espacio vacio y hacer las iteraciones

def getBestNode(openSet):
    #global mejor F
    firstIter = True

    for node in openSet.values():
        if firstIter or node.f() < bestF:
            firstIter = False
            bestNode = node
            bestF = bestNode.f()
    return bestNode

#esto crea nuevas maneras de llegar al nodo meta regresando nuevas listas

def buildPath(closedSet):
    node = closedSet[str(END)]
    branch = list()

    while node.dir:
        branch.append({
            'dir': node.dir,
            'node': node.current_node
        })
        node = closedSet[str(node.previous_node)]
    branch.append({
        'dir': '',
        'node': node.current_node
    })
    branch.reverse()

    return branch

#llama a las funciones, pasa los parametros y setea la nueva lista en un array de valores
#compara la nueva lista que ha sido creada con los movimientos del espacio vacio y el final es el nodo meta
#compara en cual hay menos movimientos para obtener la mejor opcion

def main(puzzle):
    open_set = {str(puzzle): Node(puzzle, puzzle, 0, total_cost(puzzle), "")}
    closed_set = {}

    while True:
        test_node = getBestNode(open_set)
        closed_set[str(test_node.current_node)] = test_node

        if test_node.current_node == END:
            return buildPath(closed_set)

        adj_node = expand(test_node)
        for node in adj_node:
            if str(node.current_node) in closed_set.keys() or str(node.current_node) in open_set.keys() and open_set[
                str(node.current_node)].f() < node.f():
                continue
            open_set[str(node.current_node)] = node

        del open_set[str(test_node.current_node)]


if __name__ == '__main__':      #obtiene el input para el puzzle
    inp = main([[0, 8, 3],
                [1, 2, 4],
                [7, 6, 5]])

    print('total steps : ', len(inp) -   1)    #imprime el total de pasos que hizo el algoritmo para completar el puzzle
    print()
    print(dash + dash + right_junction, "INPUT", left_junction + dash + dash)
    for i in inp:
        if i['dir'] != '':
            letter = ''
            if i['dir'] == 'U':
                letter = 'UP'
            elif i['dir'] == 'R':
                letter = "RIGHT"
            elif i['dir'] == 'L':
                letter = 'LEFT'
            elif i['dir'] == 'D':
                letter = 'DOWN'
            print(dash + dash + right_junction, letter, left_junction + dash + dash)
        print_puzzle(i['node'])
        print()

    print(dash + dash + right_junction, 'ABOVE IS THE OUTPUT', left_junction + dash + dash)