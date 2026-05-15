"""
Juego de conecta 4

El estado se va a representar como una lista de 42 elementos, tal que


0  1  2  3  4  5  6
7  8  9 10 11 12 13
14 15 16 17 18 19 20
21 22 23 24 25 26 27
28 29 30 31 32 33 34
35 36 37 38 39 40 41

y cada elemento puede ser 0, 1 o -1, donde 0 es vacío, 1 es una ficha del
jugador 1 y -1 es una ficha del jugador 2.

Las acciones son poner una ficha en una columna, que se representa como un
número de 0 a 6.

Un estado terminal es aquel en el que un jugador ha conectado 4 fichas
horizontales, verticales o diagonales, o ya no hay espacios para colocar
fichas.

La ganancia es 1 si gana el jugador 1, -1 si gana el jugador 2 y 0 si es un
empate.

"""

import math
import juegos_simplificado as js
import minimax

class Conecta4(js.JuegoZT2):
    def inicializa(self):
        return tuple([0 for _ in range(6 * 7)])
        
    def jugadas_legales(self, s, j):
        return (columna for columna in range(7) if s[columna] == 0)
    
    def sucesor(self, s, a, j):
        s = list(s[:])
        for i in range(5, -1, -1):
            if s[a + 7 * i] == 0:
                s[a + 7 * i] = j
                break
        return tuple(s)
    
    def ganancia(self, s):
        #Verticales
        for i in range(7):
            for j in range(3):
                if (s[i + 7 * j] == s[i + 7 * (j + 1)] == s[i + 7 * (j + 2)] == s[i + 7 * (j + 3)] != 0):
                    return s[i + 7 * j]
        #Horizontales
        for i in range(6):
            for j in range(4):
                if (s[7 * i + j] == s[7 * i + j + 1] == s[7 * i + j + 2] == s[7 * i + j + 3] != 0):
                    return s[7 * i + j]
        #Diagonales
        for i in range(4):
            for j in range(3):
                if (s[i + 7 * j] == s[i + 7 * j + 8] == s[i + 7 * j + 16] == s[i + 7 * j + 24] != 0):
                    return s[i + 7 * j]
                if (s[i + 7 * j + 3] == s[i + 7 * j + 9] == s[i + 7 * j + 15] == s[i + 7 * j + 21] != 0):
                    return s[i + 7 * j + 3]
        return 0
    
    def terminal(self, s):
        if 0 not in s:
            return True
        return self.ganancia(s) != 0
    
class InterfaceConecta4(js.JuegoInterface):
    def muestra_estado(self, s):
        """
        Muestra el estado del juego, se puede usar la función pprint_conecta4
        para mostrar el estado de forma más amigable

        """
        a = [' X ' if x == 1 else ' O ' if x == -1 else '   ' for x in s]
        print('\n 0 | 1 | 2 | 3 | 4 | 5 | 6')
        for i in range(6):
            print('|'.join(a[7 * i:7 * (i + 1)]))
            print('---+---+---+---+---+---+---\n')
    
    def muestra_ganador(self, g):
        """
        Muestra el ganador del juego, se puede usar " XO"[g] para mostrar el
        ganador de forma más amigable

        """
        if g != 0:
            print("Gana el jugador " + " XO"[g])
        else:
            print("Un asqueroso empate")

    def jugador_humano(self, s, j):
        print("Jugador", " XO"[j])
        jugadas = list(self.juego.jugadas_legales(s, j))
        print("Jugadas legales:", jugadas)
        jugada = None
        while jugada not in jugadas:
            jugada = int(input("Jugada: "))
        return jugada

def ordena_centro(jugadas, jugador):
    """
    Ordena las jugadas de acuerdo a la distancia al centro
    """
    return sorted(jugadas, key=lambda x: abs(x - 4))

def evalua_3con(s):
    """
    Evalua el estado s para el jugador 1
    """
    conect3 = sum(
        1 for i in range(7) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * (j + 1)] 
            == s[i + 7 * (j + 2)] == 1)
    ) - sum(
        1 for i in range(7) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * (j + 1)] 
            == s[i + 7 * (j + 2)] == -1)
    ) + sum(
        1 for i in range(6) for j in range(5) 
        if (s[7 * i + j] == s[7 * i + j + 1] 
            == s[7 * i + j + 2] == 1)
    ) - sum(
        1 for i in range(6) for j in range(5) 
        if (s[7 * i + j] == s[7 * i + j + 1] 
            == s[7 * i + j + 2] == -1)
    ) + sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * j + 8] 
            == s[i + 7 * j + 16] == 1)
    ) - sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * j + 8] 
            == s[i + 7 * j + 16] == -1)
    ) + sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j + 3] == s[i + 7 * j + 9] 
            == s[i + 7 * j + 15] == 1)
    ) - sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j + 3] == s[i + 7 * j + 9] 
            == s[i + 7 * j + 15] == -1)
    )
    promedio = conect3 / (7 * 4 + 6 * 5 + 5 * 4 + 5 * 4)
    if abs(promedio) >= 1:
        raise ValueError("Evaluación fuera de rango --> ", promedio)
    return promedio

# ---------------------------------------------------------------------------
# Funciones mejoradas de ordenamiento y evaluación
# ---------------------------------------------------------------------------

# Tabla de pesos posicionales: cada celda indica cuántas líneas ganadoras
# posibles la atraviesan. Las celdas centrales participan en más líneas,
# por lo que tienen mayor valor estratégico.
_TABLA_POSICION = [
    3, 4, 5, 7, 5, 4, 3,
    4, 6, 8,10, 8, 6, 4,
    5, 8,11,13,11, 8, 5,
    5, 8,11,13,11, 8, 5,
    4, 6, 8,10, 8, 6, 4,
    3, 4, 5, 7, 5, 4, 3,
]

# Pre-generación de todas las ventanas de 4 celdas (horizontal, vertical,
# diagonal \ y diagonal /). Se hace una sola vez al cargar el módulo para
# no repetir el cálculo en cada llamada a evalua_mejorada.
_VENTANAS_4 = (
    [[f*7+c+k for k in range(4)] for f in range(6) for c in range(4)] +
    [[(f+k)*7+c for k in range(4)] for c in range(7) for f in range(3)] +
    [[(f+k)*7+c+k for k in range(4)] for f in range(3) for c in range(4)] +
    [[(f+k)*7+c-k for k in range(4)] for f in range(3) for c in range(3,7)]
)

def ordena_mejor(jugadas, jugador):
    """
    Ordena las jugadas por cercanía al centro real del tablero (columna 3).

    La versión original usaba abs(x-4), lo que priorizaba la columna 4 en
    lugar del centro real. En un tablero de 7 columnas (0-6) el centro es
    la columna 3.

    Al explorar primero las columnas más prometedoras, alfa-beta encuentra
    cotas más ajustadas y poda más ramas, permitiendo llegar a mayor
    profundidad en el mismo tiempo.
    """
    ORDEN = {3: 0, 4: 1, 2: 2, 5: 3, 1: 4, 6: 5, 0: 6}
    return sorted(jugadas, key=lambda c: ORDEN.get(c, 6))

def evalua_mejorada(s):
    """
    Evalúa el estado s para el jugador 1. Devuelve un valor en (-1, 1).

    Combina dos criterios:
    - Ventanas de 4 celdas: puntúa cada ventana según su contenido.
        3 propias + 1 vacía  → +50  (amenaza inmediata de ganar)
        2 propias + 2 vacías → +10  (control de espacio)
        1 propia  + 3 vacías →  +2  (presencia mínima)
      Lo mismo en negativo para el rival.
    - Control posicional: suma los pesos de _TABLA_POSICION para las
      fichas propias y resta los del rival. Las celdas centrales valen
      más porque participan en más líneas ganadoras posibles.

    La combinación se normaliza con tanh para garantizar el rango (-1, 1)
    sin confundirse con los valores terminales exactos ±1.
    """
    puntaje_ventanas = 0
    for ventana in _VENTANAS_4:
        propias = sum(1 for i in ventana if s[i] ==  1)
        rival   = sum(1 for i in ventana if s[i] == -1)
        vacias  = 4 - propias - rival
        if propias > 0 and rival == 0:
            if   propias == 3 and vacias == 1: puntaje_ventanas += 50
            elif propias == 2 and vacias == 2: puntaje_ventanas += 10
            elif propias == 1 and vacias == 3: puntaje_ventanas +=  2
        elif rival > 0 and propias == 0:
            if   rival == 3 and vacias == 1: puntaje_ventanas -= 50
            elif rival == 2 and vacias == 2: puntaje_ventanas -= 10
            elif rival == 1 and vacias == 3: puntaje_ventanas -=  2

    puntaje_pos = sum(_TABLA_POSICION[i] * s[i] for i in range(42))

    score = (0.70 * puntaje_ventanas / 3450.0
           + 0.30 * puntaje_pos / 378.0)

    return max(-0.9999, min(0.9999, math.tanh(score * 3)))


if __name__ == '__main__':

    cfg = {
        "Jugador 1": "Humano",          #Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo", "NegamaxMejorado", "TiempoMejorado"
        "Jugador 2": "NegamaxMejorado", #Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo", "NegamaxMejorado", "TiempoMejorado"
        "profundidad máxima": 5,
        "tiempo": 10,
    }

    def jugador_cfg(cadena):
        if cadena == "Humano":
            return "Humano"
        elif cadena == "Aleatorio":
            return js.JugadorAleatorio()
        elif cadena == "Negamax":
            # Negamax con las funciones originales
            return minimax.JugadorNegamax(
                ordena=ordena_centro, d=cfg["profundidad máxima"], evalua=evalua_3con
            )
        elif cadena == "Tiempo":
            # Negamax iterativo con las funciones originales
            return minimax.JugadorNegamaxIterativo(
                tiempo=cfg["tiempo"], ordena=ordena_centro, evalua=evalua_3con
            )
        elif cadena == "NegamaxMejorado":
            # Negamax con las funciones mejoradas
            return minimax.JugadorNegamax(
                ordena=ordena_mejor, d=cfg["profundidad máxima"], evalua=evalua_mejorada
            )
        elif cadena == "TiempoMejorado":
            # Negamax iterativo con las funciones mejoradas
            return minimax.JugadorNegamaxIterativo(
                tiempo=cfg["tiempo"], ordena=ordena_mejor, evalua=evalua_mejorada
            )
        else:
            raise ValueError("Jugador no reconocido")

    interfaz = InterfaceConecta4(
        Conecta4(),
        jugador1=jugador_cfg(cfg["Jugador 1"]),
        jugador2=jugador_cfg(cfg["Jugador 2"])
    )

    print("El Juego del Conecta 4 ")
    print("Jugador 1:", cfg["Jugador 1"])
    print("Jugador 2:", cfg["Jugador 2"])
    print()

    interfaz.juega()