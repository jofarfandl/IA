"""
Problema 1 del documento Practica 2_SI. pdf utilizando la busqueda en amplitud.

Salcedo Arellano Alexa
Esparza Duran Kenia Jaqueline
Farfan de Leon Jose Osvaldo

------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
from collections import deque
import random
import time

#Clase que define un nodo en el 8-puzzle.
class Nodo:
    def __init__(self, estado, padre, movimiento, profundidad, piezas_correctas):        
        self.estado = estado                        #Posición atual de las piezas.
        self.padre = padre                          #Nodo desde el que se llega a este nodo.
        self.movimiento = movimiento                #Movimiento para encontrar este nodo desde el padre.
        self.profundidad = profundidad              #Posición del nodo en el árbol de búsqueda.
        self.piezas_correctas = piezas_correctas    #Total de piezas en su lugar para este estado.

    #Método para mover las piezas en direcciones posibles.
    def mover(self, direccion):
        estado = list(self.estado)
        ind = estado.index(0)

        if direccion == "arriba":            
            if ind not in [6, 7, 8]:                
                temp = estado[ind + 3]
                estado[ind + 3] = estado[ind]
                estado[ind] = temp
                return tuple(estado)
            else:                
                return None

        elif direccion == "abajo":            
            if ind not in [0, 1, 2]:                
                temp = estado[ind - 3]
                estado[ind - 3] = estado[ind]
                estado[ind] = temp
                return tuple(estado)
            else:                
                return None

        elif direccion == "derecha":            
            if ind not in [0, 3, 6]:                
                temp = estado[ind - 1]
                estado[ind - 1] = estado[ind]
                estado[ind] = temp
                return tuple(estado)
            else:                
                return None

        elif direccion == "izquierda":            
            if ind not in [2, 5, 8]:                
                temp = estado[ind + 1]
                estado[ind + 1] = estado[ind]
                estado[ind] = temp
                return tuple(estado)
            else:                
                return None        

    #Método que encuentra y regresa todos los nodos sucesores del nodo actual.
    def encontrar_sucesores(self):
        sucesores = []
        sucesorN = self.mover("arriba")
        sucesorS = self.mover("abajo")
        sucesorE = self.mover("derecha")
        sucesorO = self.mover("izquierda")
        
        sucesores.append(Nodo(sucesorN, self, "arriba", self.profundidad + 1, calcular_heurisitica(sucesorN)))
        sucesores.append(Nodo(sucesorS, self, "abajo", self.profundidad + 1, calcular_heurisitica(sucesorS)))
        sucesores.append(Nodo(sucesorE, self, "derecha", self.profundidad + 1, calcular_heurisitica(sucesorE)))
        sucesores.append(Nodo(sucesorO, self, "izquierda", self.profundidad + 1, calcular_heurisitica(sucesorO)))
        
        sucesores = [nodo for nodo in sucesores if nodo.estado != None]  
        return sucesores

    #Método que encuentra el camino desde el nodo inicial hasta el actual.
    def encontrar_camino(self, inicial):
        camino = []
        nodo_actual = self
        while nodo_actual.profundidad >= 1:
            camino.append(nodo_actual)
            nodo_actual = nodo_actual.padre
        camino.reverse()
        return camino

    #Método que imprime ordenadamente el estado (piezas) de un nodo.
    def imprimir_nodo(self):
        renglon = 0
        for pieza in self.estado:
            if pieza == 0:
                print(" ", end = " ")
            else:
                print (pieza, end = " ")
            renglon += 1
            if renglon == 3:
                print()
                renglon = 0       

#Función que calcula la cantidad de piezas que están en su lugar para un estado dado.
def calcular_heurisitica(estado):
    correcto = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    valor_correcto = 0
    piezas_correctas = 0
    if estado:
        for valor_pieza, valor_correcto in zip(estado, correcto):
            if valor_pieza == valor_correcto:
                piezas_correctas += 1
            valor_correcto += 1
    return piezas_correctas   

#Algoritmo Breadth First Search.
def bfs(inicial, meta):
    visitados = set()   #Conjunto de estados visitados para no visitar el mismo estado más de una vez.
    frontera = deque()  #Cola de nodos aún por explorar. Se agrega el nodo inicial.  
    frontera.append(Nodo(inicial, None, None, 0, calcular_heurisitica(inicial)))
    
    while frontera:                         #Mientras haya nodos por explorar:
        nodo = frontera.popleft()           #Se toma el primer nodo de la cola.

        if nodo.estado not in visitados:    #Si no se había visitado, 
            visitados.add(nodo.estado)      #se agrega al conjunto de visitados.
        else:                               #Si ya se había visitado
            continue                        #se ignora.
        
        if nodo.estado == meta:                         #Si es una meta, 
            print("\n¡Se encontró la meta!")            
            return nodo.encontrar_camino(inicial)       #se regresa el camino para llegar a él y termina el algoritmo.        
        else:                                           #Si no es una meta, 
            frontera.extend(nodo.encontrar_sucesores()) #se agregan sus sucesores a los nodos por explorar.

def generar_lista():#generamos una matriz inicial para el juego
    lista_inicial=[]
    for i in range(9):
        band = False
        while(band == False):
            num = random.randint(0, 8)
            if num in lista_inicial:
                band = False
            else:
                band = True
                lista_inicial.append(num)
    mytuple = tuple(lista_inicial)
    return mytuple
    
#Función main.
def main():
    estado_final = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    estado_inicial = generar_lista()

    #Menú principal
    print("Inicio: ")
    (Nodo(estado_inicial, None, None, 0, calcular_heurisitica(estado_inicial))).imprimir_nodo()

    print("Corriendo BFS. Por favor espere.")
    nodos_camino = bfs(estado_inicial, estado_final)
    
    #Se imprime el camino si existe y si el usuario lo desea.
    if nodos_camino:
        print ("El camino tiene", len(nodos_camino), "movimientos.")

        print("\nEstado inicial:")
        (Nodo(estado_inicial, None, None, 0, calcular_heurisitica(estado_inicial))).imprimir_nodo()
        print ("Piezas correctas:", calcular_heurisitica(estado_inicial), "\n")
        print("Iniciando el recorrido de la meta...")
        time.sleep(3)           
        for nodo in nodos_camino:
            print("\nSiguiente movimiento:", nodo.movimiento)
            print("Estado actual:")
            nodo.imprimir_nodo()
            print("Piezas correctas:", nodo.piezas_correctas, "\n")     
            time.sleep(1) # Sleep for 3 seconds
    else:
        print ("\nNo existe una solucion con el estado inicial definido.")

    return 0    

if __name__ == "__main__":
    main()