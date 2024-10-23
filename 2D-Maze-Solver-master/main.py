import search
from graph import Graph


if __name__ == "__main__":
    # Setting graph we initiated to search class...
    graph = Graph()
    search.graph = graph

    #search.depth_first_search()#profundidad
    #search.breath_first_search()
    #search.iterative_deepening_search()#profundidad iterativa
    #search.greedy_best_first_search()
    search.a_star_search()
