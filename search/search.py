# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):   
    pila = util.Stack()   #Encargada de almacenar tanto el nodo como el camino
    nodosVis = []       #Lista de los nodos visitados
    
    #Se inicia la pila con un nodo inicial y camino vacio 
    pila.push((problem.getStartState(), []))
    
    #Mientras la pila no esta vacia, pues el algoritmo sigue buscando
    while not (pila.isEmpty()):
        #Se extrae el nodo actual y el camino
        nodoAct, camino = pila.pop()

        #Si el nodo actual no ha sido visitado, procede a expandirlo
        if nodoAct not in nodosVis:
            nodosVis.append(nodoAct)   #Guarda a nodo en la lista de visitados

            #Hay que verificar si el nodo es el nodo que buscamos
            if (problem.isGoalState(nodoAct)):
                return camino
           
            hijos = problem.getSuccessors(nodoAct)     #sucesores del nodo actual
            for hijo, direccion,costo in hijos:
                nuevoCamino = camino + [direccion]
                pila.push((hijo, nuevoCamino))
    return camino

def breadthFirstSearch(problem):
    cola = util.Queue()     #Se maneja los nodos en orden FIFO
    nodosVis = []           #Guarda los nodos visitados

    #Se inicia la pila con un nodo inicial y camino vacio
    cola.push((problem.getStartState(), []))

    #Mientras la pila no esta vacia, pues el algoritmo sigue buscando
    while not (cola.isEmpty()):
        #Se extrae el nodo actual y el camino hasta este nodo.
        nodoAct, camino = cola.pop()

        #Si el nodo actual no ha sido visitado, procede a expandirlo.
        if nodoAct not in nodosVis:
                nodosVis.append(nodoAct)
                
                #Se verifica que sea el nodo buscado, de ser así, se regresa las "acciones" -> camino
                if (problem.isGoalState(nodoAct)):
                    return camino

                #vecinos o sucesores del nodo actual
                hijos = problem.getSuccessors(nodoAct)
                for hijo, direccion,costo in hijos:
                    nuevoCamino = camino + [direccion] #Se crea un nuevo camino agregando la una dirección al camino actual.
                    cola.push((hijo, nuevoCamino))      #Se añade el sucesor y el nuevo camino a la cola.

    return camino

def uniformCostSearch(problem):
    cola = util.PriorityQueue()     #Se maneja los nodos en orden FIFO
    nodosVis = []                           #Guarda los nodos visitados

    #Se inicia la pila con un nodo inicial y camino vacio y se le agrega un costo inicial de 0
    cola.push((problem.getStartState(), [], 0),0)

    #Mientras la pila no esta vacia, pues el algoritmo sigue buscando
    while not (cola.isEmpty()):
        nodoAct, camino, costo = cola.pop()     #Se extrae el nodo con el menor costo total acumulado

        #Si el nodo actual no ha sido visitado, procede a expandirlo.
        if nodoAct not in nodosVis:
                nodosVis.append(nodoAct)
                
                #Se verifica que sea el nodo buscado, de ser así, se regresa las "acciones" -> camino
                if (problem.isGoalState(nodoAct)):
                    return camino

                #vecinos o sucesores del nodo actual
                hijos = problem.getSuccessors(nodoAct)
                for hijo, direccion, costoAct in hijos:      
                    
                    #Se crea un nuevo camino agregando la una dirección al camino actual.
                    nuevoCamino = camino + [direccion] 

                    #Calcula el costo acumulado siendo que suma el costo actual y el costo para llegar al sucesor.
                    costoAcumu = problem.getCostOfActions(nuevoCamino) 
                    
                    #Se añade el sucesor, el nuevo camino a la cola de prioridad y junto al costo como prioridad.
                    cola.push((hijo, nuevoCamino, costoAcumu),costoAcumu)      

    return camino


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    cola = util.PriorityQueue()     #Se maneja los nodos en orden FIFO
    nodosVis = []                           #Guarda los nodos visitados

    #Se inicia la pila con un nodo inicial y camino vacio y se le agrega un costo inicial de 0
    cola.push((problem.getStartState(), [], 0), 0 + heuristic(problem.getStartState(), problem))

    #Mientras la pila no esta vacia, pues el algoritmo sigue buscando
    while not (cola.isEmpty()):
        nodoAct, camino, costo = cola.pop()     #Se extrae el nodo con el menor costo total acumulado

        #Si el nodo actual no ha sido visitado, procede a expandirlo.
        if nodoAct not in nodosVis:
                nodosVis.append(nodoAct)
                
                #Se verifica que sea el nodo buscado, de ser así, se regresa las "acciones" -> camino
                if (problem.isGoalState(nodoAct)):
                    return camino

                #vecinos o sucesores del nodo actual
                hijos = problem.getSuccessors(nodoAct)
                for hijo, direccion, costoAct in hijos:  

                    #Se calcula el costo acumulado sumando el costo actual y el costo para llegar al sucesor
                    costoAcumu = costo + costoAct    
                    
                    #Se crea un nuevo camino agregando la una dirección al camino actual.
                    nuevoCamino = camino + [direccion] 

                    #Calcula el costo acumulado 
                    costoTotal = costoAcumu + heuristic(hijo,problem)
                    
                    #Se añade el sucesor, el nuevo camino a la cola de prioridad y junto al costo como prioridad.
                    cola.push((hijo, nuevoCamino, costoAcumu),costoTotal)   

    return camino


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
