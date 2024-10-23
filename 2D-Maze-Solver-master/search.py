from collections import OrderedDict


# ############################################## GLOBAL VARIABLES
graph = None
frontier = []
visited = OrderedDict()  # To prevent duplicates, we use OrderedDict


def depth_first_search():
    graph.clear_parents()
    dfs_bfs_ids_ucs("Depth First Search(DFS):")


def breath_first_search():
    graph.clear_parents()
    dfs_bfs_ids_ucs("Breath First Search(BFS):")


def iterative_deepening_search():
    graph.clear_parents()
    dfs_bfs_ids_ucs("Iterative Deepening Search(IDS):")


def uniform_cost_search():
    graph.clear_parents()
    dfs_bfs_ids_ucs("Uniform Cost Search(UCS):")


def greedy_best_first_search():
    graph.clear_parents()
    heuristic_search("Greedy Best First Search(GBFS):", return_heuristic)


def a_star_search():
    graph.clear_parents()
    heuristic_search("A Star Search(A*):", return_cost_and_heuristic)


def heuristic_search(algorithm, sort_by):

    # Variables
    goal_state = None
    solution_cost = 0
    solution = []

    # Limpiamos frontier y visited, y agregamos root a frontier.
    frontier.clear()
    visited.clear()
    frontier.append(graph.root)

    while len(frontier) > 0:

        # Ordemos frontier de acuerdo a la heuristica
        sort_frontier(sort_by)

        # removemos el nodo coorecto de frontier y lo agregamos a los visitados.
        current_node = frontier.pop(0)
        visited[current_node] = None

        # Para GBFS, si estamos en la meta
        if is_goal(current_node):
            goal_state = current_node
            break

        # print(current_node, current_node.parent)

        # Agregamos a la frontera como BFS.
        add_to_frontier(current_node, "BFS")

    #Revisa si GBFS fue exitoso
    if goal_state is not None:

        # Calculamos el costo de la solucion y la solucion
        current = goal_state
        while current is not None:
            solution_cost += current.cost
            solution.insert(0, current)
            # Get the parent node and continue...
            #optenemos el nodo padre y continuamos
            current = current.parent

        # Print the results...
        print_results(algorithm, solution_cost, solution, visited)
    else:
        print("No goal state found.")


def dfs_bfs_ids_ucs(algorithm):

    # Variables
    pop_index = 0
    goal_state = None
    solution_cost = 0
    solution = []
    expanded_nodes = []
    iteration = -1

    # DFS_BFS_IDS
    while goal_state is None and iteration <= graph.maximum_depth:

        # Para cada iteración, aumentaremos la iteración en uno y borraremos la frontera y lo visitado. También agregue el nodo raíz.
        iteration += 1
        frontier.clear()
        visited.clear()
        frontier.append(graph.root)

        #si el algoritmo es iterativo (IDS) agregamos numero de iteraciones
        if "IDS" in algorithm:
            expanded_nodes.append("Iteration " + str(iteration) + ":")

        while len(frontier) > 0:

            # Si DFS o IDS, remueve el ultimo nodo de frontier.
            # Si BFS, remueve el primer nodo de frontier
            if "DFS" in algorithm or "IDS" in algorithm:
                pop_index = len(frontier) - 1

            # Si UCS, ordenamos frontier de acuerdo al costo
            if "UCS" in algorithm:
                sort_frontier(return_cost)

            # Necesitamos eliminar el nodo correcto de la frontera según el algoritmo y agregarlo al visitado.
            current_node = frontier.pop(pop_index)
            visited[current_node] = None

            # Para DFS_BFS_IDS, si estamos en una meta
            if is_goal(current_node):
                goal_state = current_node
                break

            # agrega todos los nodos hijos al elemento actual al final de la lista.
            # Si IDS, agrega los nodos hijos de acuerdo al numero de iteraciones.
            if "IDS" in algorithm:
                parent = current_node
                for i in range(iteration):
                    # si el padre no es none, iteramos al padre superior.
                    parent = parent if parent is None else parent.parent

                if parent is None:
                    add_to_frontier(current_node, "DFS")
            # Else, agregamos todos los nodos hijos
            else:
                add_to_frontier(current_node, algorithm)

        # Agrega todos los nodos visitados a expanded_nodes, antes de limpiarlos.
        for node in visited:
            expanded_nodes.append(node)

        # Continuamos solo si es IDS
        if "IDS" not in algorithm:
            break

    # Revisa si DFS_BFS_IDS logro la meta
    if goal_state is None:
        print("No goal state found.")
        return

    # Calculamos el costo de la solucion y obtenemos la solucion
    current = goal_state
    while current is not None:
        solution_cost += current.cost
        solution.insert(0, current)
        # obtenemos el nodo padre y continuamos
        current = current.parent

    # Print the results...
    print_results(algorithm, solution_cost, solution, expanded_nodes)


def add_to_frontier(current_node, algorithm):
    # Si los nodos secundarios no son NONE Y si no están visitados, los agregaremos a la frontera.
    nodes_to_add = []
    if current_node.east is not None and not is_in_visited(current_node.east):
        nodes_to_add.append(set_parent(current_node, current_node.east, algorithm))
    if current_node.south is not None and not is_in_visited(current_node.south):
        nodes_to_add.append(set_parent(current_node, current_node.south, algorithm))
    if current_node.west is not None and not is_in_visited(current_node.west):
        nodes_to_add.append(set_parent(current_node, current_node.west, algorithm))
    if current_node.north is not None and not is_in_visited(current_node.north):
        nodes_to_add.append(set_parent(current_node, current_node.north, algorithm))

    # Para DFS lo hacemos en reversa por que agregamos cada nodo al final y EAST debe ser el ultimo nodo.
    # Para BFS se hace en orden normal.
    if "DFS" in algorithm:
        nodes_to_add.reverse()

    # agregamos cada nodo al frontier.
    for node in nodes_to_add:
        frontier.append(node)


def set_parent(parent_node, child_node, algorithm):
    # set el nodo padre como NONE si el algoritmo es DFS
    if "DFS" in algorithm or child_node.parent is None:
        child_node.parent = parent_node
    return child_node


def is_in_visited(node):
    if node in visited:
        return True
    return False


def is_goal(node):
    for goal in graph.maze.goals:
        if goal[0] == node.x and goal[1] == node.y:
            return True
    return False


def print_results(algorithm, solution_cost, solution, expanded_nodes):
    print(algorithm)
    print("Cost of the solution:", solution_cost)
    print("The solution path (" + str(len(solution)) + " nodes):", end=" ")
    for node in solution:
        print(node, end=" ")
    print("\nExpanded nodes (" + str(len(expanded_nodes)) + " nodes):", end=" ")
    if "IDS" in algorithm:
        print()
        for i in range(len(expanded_nodes) - 1):
            if type(expanded_nodes[i+1]) == str:
                print(expanded_nodes[i])
            else:
                print(expanded_nodes[i], end=" ")
    else:
        for node in expanded_nodes:
            print(node, end=" ")
    print("\n")


def return_cost(node):
    return node.cost


def return_heuristic(node):
    return node.heuristic


def return_cost_and_heuristic(node):
    return node.heuristic + node.cost


def sort_frontier(sort_by):
    frontier.sort(key=sort_by)
