"""
==================================================
Nombre del Proyecto: Proyecto No.1 Inteligencia Artificial 
~ Algoritmos de busqueda y heuristicas

Archivo: Proyecto No.1

Descripción: Breve descripción de lo que hace este archivo.

Autor: Pablo Sebastian Herrera

Correo: pablos.herrera@outlook.com

Fecha de creación: 16-03-2025

Última modificación: 2025-03-17
==================================================
"""

from heapq import heappush, heappop
import pandas as pd
from collections import defaultdict
from math import sqrt 
import time
from random import randint,seed

class Nodo:
    def __init__(self, estado: str, padre=None, accion=None, costo_camino=0, heuristica=0):
        self.estado = estado  # Renombrado para mayor claridad
        self.padre = padre
        self.accion = accion
        self.costo_camino = costo_camino
        self.heuristica = heuristica

    def __lt__(self, otro):
        return (self.costo_camino + self.heuristica) < (otro.costo_camino + otro.heuristica)
    

class ColaFIFO:
    def __init__(self):
        self.cola = []
        
    def Empty(self):
        #verdadero si esta vacia
        #falso si no esta vacia
        return not self.cola
        
    def Top(self):
        """
        En una cola FIFO, el primer elemento
        es el que se inserta de primero.
        Lanza una excepción si la cola está vacía.
        """
        if self.cola: #si no esta vacia
            return self.cola[0]
        else:
            #si esta vacia se maneja el error
            raise IndexError("La cola está vacía")
    
    def Pop(self):
        """
        Devuelve el primer elemento y lo remueve.
        Lanza una excepción si la cola está vacía.
        """
        if self.cola: #cola no vacia
            return self.cola.pop(0)
        else:
            raise IndexError("La cola está vacía")
    
    def Add(self, elemento):
        """
        Agrega elementos al final de la cola.
        """
        self.cola.append(elemento)
#------------------------------------------------------------------------------
class ColaLIFO:
    def __init__(self):
        self.cola = []
        
    def Empty(self):
        return not self.cola  # Verifica si la cola está vacía
        
    def Top(self):
        """
        Devuelve el último elemento de la cola LIFO sin eliminarlo.
        Lanza una excepción si la cola está vacía.
        """
        if self.cola:
            return self.cola[-1]
        else:
            raise IndexError("La cola está vacía")
    
    def Pop(self):
        """
        Devuelve y remueve el último elemento de la cola LIFO.
        Lanza una excepción si la cola está vacía.
        """
        if self.cola:
            return self.cola.pop(-1)
        else:
            raise IndexError("La cola está vacía")
    
    def Add(self, elemento):
        """
        Agrega elementos al final de la cola.
        """
        self.cola.append(elemento)
#------------------------------------------------------------------------------
class ColaPrioridad:
    def __init__(self):
        self.cola = []
    
    def Empty(self):
        return not self.cola  # Verifica si la cola está vacía (True si está vacía)
    
    def AddUCS(self, elemento):
       heappush(self.cola, (elemento.costo_camino, elemento))
       
    def AddGBFS(self, elemento):
        heappush(self.cola, (elemento.heuristica, elemento))
        
    def AddAstar(self, elemento):
        heappush(self.cola, (elemento.costo_camino + elemento.heuristica, elemento))

    
    def Top(self):
        if not self.cola:  # Asegúrate de que no esté vacía antes de acceder
            raise IndexError("No hay elementos en la cola")
        return self.cola[0][1]  
    
    def Pop(self):
        if not self.cola:  # Si la cola está vacía
            raise IndexError("No hay elementos en la cola")
        else:
            return heappop(self.cola)[1]     
#------------------------------------------------------------------------------
def ReconstruirCamino(nodo):
    camino = []
    while nodo is not None:
        camino.append(nodo.estado)
        nodo = nodo.padre
    return list(reversed(camino))
#-----------------------------------------------------------------------------
#Implementacion de los algoritmos
def BFS(grafo, nodo_inicial, nodo_final):
    frontera = ColaFIFO()
    frontera.Add(Nodo(estado=nodo_inicial, costo_camino=0))
    explorado = set()
    nodos_explorados = []  # Lista para almacenar los nodos explorados

    while not frontera.Empty():
        actual = frontera.Pop()

        if actual.estado in explorado:
            continue  # Evita contar nodos ya explorados

        nodos_explorados.append(actual.estado)  # Guardar el nodo explorado
        explorado.add(actual.estado)

        if actual.estado == nodo_final:
            return ReconstruirCamino(actual), actual.costo_camino, len(nodos_explorados)  # Contar la cantidad de nodos explorados
        
        for vecino in grafo.get(actual.estado, []):
            if vecino not in explorado and not any(n.estado == vecino for n in frontera.cola):
                hijo = Nodo(estado=vecino, padre=actual, costo_camino=actual.costo_camino + 1)
                frontera.Add(hijo)

    return None, None, len(nodos_explorados)  # Retornar solo la cantidad de nodos explorados



def DFS(grafo, nodo_inicial, nodo_final):
    frontera = ColaLIFO()
    frontera.Add(Nodo(estado=nodo_inicial, costo_camino=0))
    explorado = set()
    nodos_explorados = 0  # Contador de nodos explorados
    max_profundidad = 0  # Profundidad máxima

    while not frontera.Empty():
        actual = frontera.Pop()

        nodos_explorados += 1  # Contar cada nodo explorado
        
        if actual.estado == nodo_final:
            return nodos_explorados, max_profundidad  # Devolver el número de nodos explorados y la profundidad máxima
        
        explorado.add(actual.estado)
        
        # Actualizamos la profundidad máxima
        max_profundidad = max(max_profundidad, actual.costo_camino)
        
        # Recorre los vecinos del nodo actual
        for vecino in grafo.get(actual.estado, []):
            if vecino not in explorado and not any(n.estado == vecino for n in frontera.cola):
                hijo = Nodo(estado=vecino, padre=actual, accion=f"ir_{actual.estado}_a_{vecino}", costo_camino=actual.costo_camino + 1)
                frontera.Add(hijo)

    return nodos_explorados, max_profundidad  # Si no se encuentra el camino, devolvemos el número de nodos explorados




def GBFS(grafo, nodo_inicial, nodo_final, heuristicas):
    frontera = ColaPrioridad()
    nodo_inicio = Nodo(estado=nodo_inicial, heuristica=heuristicas.get(nodo_inicial, 0))
    frontera.AddGBFS(nodo_inicio)
    explorado = set()
    nodos_explorados = 0  # Contador de nodos explorados

    while not frontera.Empty():
        actual = frontera.Pop()

        if actual.estado == nodo_final:
            return ReconstruirCamino(actual), actual.costo_camino, nodos_explorados  # Devolver cantidad de nodos explorados
        
        # Incrementar contador de nodos explorados
        nodos_explorados += 1
        explorado.add(actual.estado)

        for vecino in grafo.get(actual.estado, []):
            if vecino not in explorado and not any(n.estado == vecino for _, n in frontera.cola):
                hijo = Nodo(
                    estado=vecino,
                    padre=actual,
                    accion=f"ir_{actual.estado}_a_{vecino}",
                    costo_camino=actual.costo_camino + 1,  # CORREGIDO
                    heuristica=heuristicas.get(vecino, 0)
                )
                frontera.AddGBFS(hijo)

    return None, None, nodos_explorados  # Devolver cantidad de nodos explorados si no se encuentra


def Astar(grafo, nodo_inicial, nodo_final, costos_reales, heuristicas):
    frontera = ColaPrioridad()
    nodo_inicio = Nodo(estado=nodo_inicial, costo_camino=0, heuristica=heuristicas.get(nodo_inicial, 0))
    frontera.AddAstar(nodo_inicio)
    nodos_explorados = {}  # Cambié esto a un diccionario en lugar de una lista

    while not frontera.Empty():
        actual = frontera.Pop()

        if actual.estado == nodo_final:
            return ReconstruirCamino(actual), actual.costo_camino, len(nodos_explorados)  # Devuelvo la cantidad de nodos explorados

        # Verificamos si ya fue explorado con menor costo
        if actual.estado in nodos_explorados and nodos_explorados[actual.estado] <= actual.costo_camino:
            continue

        nodos_explorados[actual.estado] = actual.costo_camino  # Ahora usamos el diccionario para almacenar el costo

        for vecino in grafo.get(actual.estado, []):
            costo_real = costos_reales.get((actual.estado, vecino), 1)  # Asumiendo costo por defecto 1
            hijo = Nodo(
                estado=vecino,
                padre=actual,
                accion=f"ir_{actual.estado}_a_{vecino}",
                costo_camino=actual.costo_camino + costo_real,
                heuristica=heuristicas.get(vecino, 0)
            )
            frontera.AddAstar(hijo)

    return None, None, len(nodos_explorados)  # Devolver cantidad de nodos explorados si no se encuentra


#------------------------------------------------------------------------------
#Implementacion de las heuristicas
def ConstruirHeuristica(grafo,nodo_final,heuristica_a_utilizar=0):
    heuristica_a_utilizar = heuristica_a_utilizar.lower()
    heuristica = {}
    for nodo in grafo.keys():
        if heuristica_a_utilizar == "manhattan":
            heuristica[nodo] = abs(nodo[0]-nodo_final[0]) + abs(nodo[1] - nodo_final[1])
        elif heuristica_a_utilizar == "euclideana":
            heuristica[nodo] = sqrt((nodo[0]-nodo_final[0])**2 + (nodo[1]-nodo_final[1])**2)
            
    return heuristica
#------------------------------------------------------------------------------
#Funcion para crear al grafo
def CrearGrafo(laberinto):
    grafo = defaultdict(list)
    costos_reales = {}  # Nuevo diccionario para almacenar costos reales
    filas, columnas = laberinto.shape
    
    # Definir las direcciones posibles: arriba, derecha, abajo, izquierda
    direcciones = [(0, 1), (1,0), (0, -1), (-1, 0)]  # (fila, columna)

    for i in range(filas):
        for j in range(columnas):
            if laberinto.iloc[i, j] != 1:  # Si no es pared
                for d in direcciones:
                    fila_vecino = i + d[0]
                    col_vecino = j + d[1]
                    
                    # Verificar si la celda vecina está dentro del laberinto
                    if 0 <= fila_vecino < filas and 0 <= col_vecino < columnas:
                        if laberinto.iloc[fila_vecino, col_vecino] != 1:  # No es pared
                            grafo[(i, j)].append((fila_vecino, col_vecino))
                            costos_reales[((i, j), (fila_vecino, col_vecino))] = 1  # Costo real de 1

    return grafo, costos_reales


def Estados(laberinto):
    estados_iniciales = []
    estados_finales = []
    filas, columnas = laberinto.shape
    
    for i in range(filas):
        for j in range(columnas):
            if laberinto.iloc[i, j] == 2:
                estados_iniciales.append((i, j))
            elif laberinto.iloc[i, j] == 3:
                estados_finales.append((i, j))
    
    return estados_iniciales, estados_finales

def EstadosAleatorios(laberinto1, laberinto2, laberinto3):
    seed(123)
    estados = set()  
    
    while len(estados) < 3:
        fila = randint(0, 127)
        columna = randint(0, 127)
        
        # Verifica que las tres matrices no contengan una pared en la posición aleatoria
        if laberinto1.iloc[fila, columna] != 1 and laberinto2.iloc[fila, columna] != 1 and laberinto3.iloc[fila, columna] != 1:
            estados.add((fila, columna))
    
    return list(estados)


def MostrarResultados(algoritmo, nodos_explorados, largo_camino, tiempo):
    resultados = {
        "Algoritmo": algoritmo,
        "Nodos explorados": nodos_explorados,  # Solo la cantidad de nodos
        "Largo del camino": largo_camino if largo_camino else "No encontrado",
        "Tiempo de ejecución (s)": round(tiempo, 5)
    }
    return resultados


    
#------------------------------------------------------------------------------
laberinto1 = pd.read_csv("Laberinto1.txt",sep=",",header=None)
laberinto2 = pd.read_csv("Laberinto2.txt",sep=",",header=None)
laberinto3 = pd.read_csv("Laberinto3.txt",sep=",",header=None)

inicial1,final1 = Estados(laberinto1)
inicial2,final2 = Estados(laberinto2)
inicial3,final3 = Estados(laberinto3)

estados_aleatorios = EstadosAleatorios(laberinto1,laberinto2,laberinto3)
estado_aleatorio_inicial1 = estados_aleatorios[0]
estado_aleatorio_inicial2 = estados_aleatorios[1]
estado_aleatorio_inicial3 = estados_aleatorios[2]

grafo1,costos_reales1 = CrearGrafo(laberinto1)
grafo2,costos_reales2 = CrearGrafo(laberinto2)
grafo3,costos_reales3 = CrearGrafo(laberinto3)

laberintos = [grafo1, grafo2, grafo3]
costos_reales = [costos_reales1,costos_reales2,costos_reales3]
estados_iniciales_no_aleatorios = [inicial1[0], inicial2[0], inicial3[0]]
estados_iniciales_aleatorios = [estado_aleatorio_inicial1, estado_aleatorio_inicial2, estado_aleatorio_inicial3]
finales = [final1[0], final2[0], final3[0]]
#------------------------------------------------------------------------------
pd.set_option('display.max_columns', None)
#ALGORITMO BFS
resultadosBFS = []
for i in range(len(laberintos)):
    # BFS con estado inicial no aleatorio
    inicio = time.time()
    camino, costo_camino, nodos_explorados = BFS(laberintos[i], estados_iniciales_no_aleatorios[i], finales[i])
    tiempo = time.time() - inicio
    resultadosBFS.append(MostrarResultados(f"BFS Laberinto {i+1}", nodos_explorados, costo_camino, tiempo))

    # BFS con estado inicial aleatorio
    inicio = time.time()
    camino, costo_camino, nodos_explorados = BFS(laberintos[i], estados_iniciales_aleatorios[i], finales[i])
    tiempo = time.time() - inicio
    resultadosBFS.append(MostrarResultados(f"BFS (Estado Aleatorio) Laberinto {i+1}", nodos_explorados, costo_camino, tiempo))

resultadosBFS = pd.DataFrame(resultadosBFS)
#------------------------------------------------------------------------------
#ALGORITMO DFS
resultadosDFS = []
for i in range(len(laberintos)):
    # DFS con estado inicial no aleatorio
    inicio = time.time()
    nodos_explorados, nivel_profundidad = DFS(laberintos[i], estados_iniciales_no_aleatorios[i], finales[i])
    tiempo = time.time() - inicio
    resultadosDFS.append(MostrarResultados(f"DFS Laberinto {i+1}", nodos_explorados, nivel_profundidad, tiempo))
    
    # DFS con estado inicial aleatorio
    inicio = time.time()
    nodos_explorados, nivel_profundidad = DFS(laberintos[i], estados_iniciales_aleatorios[i], finales[i])
    tiempo = time.time() - inicio
    resultadosDFS.append(MostrarResultados(f"DFS Laberinto {i+1}", nodos_explorados, nivel_profundidad, tiempo))


resultadosDFS = pd.DataFrame(resultadosDFS)
#------------------------------------------------------------------------------
# ALGORITMO GBFS
resultadosGBFS = []
for i in range(len(laberintos)):
    # GBFS con estado inicial no aleatorio
    inicio = time.time()
    camino, costo_camino, nodos_explorados = GBFS(laberintos[i], estados_iniciales_no_aleatorios[i], finales[i], heuristicas=ConstruirHeuristica(laberintos[i],finales[i],heuristica_a_utilizar="euclideana"))
    tiempo = time.time() - inicio
    resultadosGBFS.append(MostrarResultados(f"GBFS Laberinto {i+1} - Heurística Euclideana", nodos_explorados, costo_camino, tiempo))

    # GBFS con estado inicial no aleatorio
    inicio = time.time()
    camino, costo_camino, nodos_explorados = GBFS(laberintos[i], estados_iniciales_no_aleatorios[i], finales[i], heuristicas=ConstruirHeuristica(laberintos[i],finales[i],heuristica_a_utilizar="manhattan"))
    tiempo = time.time() - inicio
    resultadosGBFS.append(MostrarResultados(f"GBFS Laberinto {i+1} - Heurística Manhattan", nodos_explorados, costo_camino, tiempo))
    
    # GBFS con estado inicial aleatorio
    inicio = time.time()
    camino, costo_camino, nodos_explorados = GBFS(laberintos[i], estados_iniciales_aleatorios[i], finales[i], heuristicas=ConstruirHeuristica(laberintos[i],finales[i],heuristica_a_utilizar="euclideana"))
    tiempo = time.time() - inicio
    resultadosGBFS.append(MostrarResultados(f"GBFS Laberinto {i+1} Aleatorio- Heurística Euclideana", nodos_explorados, costo_camino, tiempo))

    # GBFS con estado inicial aleatorio
    inicio = time.time()
    camino, costo_camino, nodos_explorados = GBFS(laberintos[i], estados_iniciales_aleatorios[i], finales[i], heuristicas=ConstruirHeuristica(laberintos[i],finales[i],heuristica_a_utilizar="manhattan"))
    tiempo = time.time() - inicio
    resultadosGBFS.append(MostrarResultados(f"GBFS Laberinto {i+1} Aleatorio- Heurística Manhattan", nodos_explorados, costo_camino, tiempo))

resultadosGBFS = pd.DataFrame(resultadosGBFS)
#------------------------------------------------------------------------------
resultadosAstar = []
for i in range(len(laberintos)):
    # A* con estado inicial no aleatorio
    inicio = time.time()
    camino, costo_camino, nodos_explorados = Astar(laberintos[i], estados_iniciales_no_aleatorios[i], finales[i],costos_reales = costos_reales[i], heuristicas=ConstruirHeuristica(laberintos[i],finales[i],heuristica_a_utilizar="euclideana"))
    tiempo = time.time() - inicio
    resultadosAstar.append(MostrarResultados(f"A* Laberinto {i+1} - Heurística Euclideana", nodos_explorados, costo_camino, tiempo))

    # A* con estado inicial no aleatorio
    inicio = time.time()
    camino, costo_camino, nodos_explorados = Astar(laberintos[i], estados_iniciales_no_aleatorios[i], finales[i],costos_reales[i], heuristicas=ConstruirHeuristica(laberintos[i],finales[i],heuristica_a_utilizar="manhattan"))
    tiempo = time.time() - inicio
    resultadosAstar.append(MostrarResultados(f"A* Laberinto {i+1} - Heurística Manhattan", nodos_explorados, costo_camino, tiempo))
    
    # A* con estado inicial aleatorio
    inicio = time.time()
    camino, costo_camino, nodos_explorados = Astar(laberintos[i], estados_iniciales_aleatorios[i], finales[i],costos_reales[i], heuristicas=ConstruirHeuristica(laberintos[i],finales[i],heuristica_a_utilizar="euclideana"))
    tiempo = time.time() - inicio
    resultadosAstar.append(MostrarResultados(f"A* Laberinto {i+1} Aleatorio- Heurística Euclideana", nodos_explorados, costo_camino, tiempo))

    # A* con estado inicial aleatorio
    inicio = time.time()
    camino, costo_camino, nodos_explorados = Astar(laberintos[i], estados_iniciales_aleatorios[i], finales[i],costos_reales[i], heuristicas=ConstruirHeuristica(laberintos[i],finales[i],heuristica_a_utilizar="manhattan"))
    tiempo = time.time() - inicio
    resultadosAstar.append(MostrarResultados(f"A* Laberinto {i+1} Aleatorio- Heurística Manhattan", nodos_explorados, costo_camino, tiempo))

resultadosAstar = pd.DataFrame(resultadosAstar)

resultados_totales = pd.concat([resultadosBFS, resultadosDFS,resultadosGBFS,resultadosAstar], ignore_index=True)
print(resultados_totales)
