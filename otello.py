"""
Juego de Otello (Reversi)

El tablero es de 8x8 y se representa como una tupla de 64 elementos,
donde cada elemento puede ser:
    0  → casilla vacía
    1  → ficha del jugador 1 (negras)
   -1  → ficha del jugador 2 (blancas)

Los índices del tablero son:
     0  1  2  3  4  5  6  7
     8  9 10 11 12 13 14 15
    16 17 18 19 20 21 22 23
    24 25 26 27 28 29 30 31
    32 33 34 35 36 37 38 39
    40 41 42 43 44 45 46 47
    48 49 50 51 52 53 54 55
    56 57 58 59 60 61 62 63

Una jugada es un entero de 0 a 63 que indica la casilla donde se coloca
la ficha. Si un jugador no tiene jugadas legales, pasa su turno con la
jugada especial -1.

La ganancia es:
     1  si gana el jugador 1 (más fichas negras al final)
    -1  si gana el jugador 2 (más fichas blancas al final)
     0  si hay empate
"""

import math
import juegos_simplificado as js
import minimax

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

# Las 8 direcciones posibles en el tablero (fila, columna)
_DIRS = [(-1,-1), (-1, 0), (-1, 1),
         ( 0,-1),          ( 0, 1),
         ( 1,-1), ( 1, 0), ( 1, 1)]

# Tabla de pesos posicionales para Otello.
# Las esquinas valen muchísimo (no se pueden voltear nunca).
# Las casillas adyacentes a las esquinas valen negativo porque
# darle al rival acceso a la esquina es muy perjudicial.
_TABLA_POSICION = [
    120, -20,  20,  5,  5,  20, -20, 120,
    -20, -40,  -5, -5, -5,  -5, -40, -20,
     20,  -5,  15,  3,  3,  15,  -5,  20,
      5,  -5,   3,  3,  3,   3,  -5,   5,
      5,  -5,   3,  3,  3,   3,  -5,   5,
     20,  -5,  15,  3,  3,  15,  -5,  20,
    -20, -40,  -5, -5, -5,  -5, -40, -20,
    120, -20,  20,  5,  5,  20, -20, 120,
]

# Índices de las 4 esquinas
_ESQUINAS = {0, 7, 56, 63}


# ---------------------------------------------------------------------------
# Funciones auxiliares del tablero
# ---------------------------------------------------------------------------

def _fila(idx): return idx // 8
def _col(idx):  return idx % 8

def _fichas_volteadas(s, casilla, jugador):
    """
    Devuelve la lista de índices de fichas del rival que se voltean
    al colocar una ficha del jugador en `casilla`.
    """
    if s[casilla] != 0:
        return []
    rival = -jugador
    volteadas = []
    for df, dc in _DIRS:
        f, c = _fila(casilla) + df, _col(casilla) + dc
        linea = []
        while 0 <= f < 8 and 0 <= c < 8:
            idx = f * 8 + c
            if s[idx] == rival:
                linea.append(idx)
                f += df
                c += dc
            elif s[idx] == jugador:
                volteadas.extend(linea)
                break
            else:
                break
    return volteadas


# ---------------------------------------------------------------------------
# Clase principal del juego
# ---------------------------------------------------------------------------

class Otello(js.JuegoZT2):
    """
    Implementación de Otello (Reversi) basada en JuegoZT2.
    """

    def inicializa(self):
        """
        Estado inicial: 4 fichas en el centro.
        Jugador 1 (negras) inicia.

            . . . . . . . .
            . . . . . . . .
            . . . . . . . .
            . . . O X . . .
            . . . X O . . .
            . . . . . . . .
            . . . . . . . .
            . . . . . . . .
        """
        s = [0] * 64
        s[27] = -1   # fila 3, col 3 → blanca
        s[28] =  1   # fila 3, col 4 → negra
        s[35] =  1   # fila 4, col 3 → negra
        s[36] = -1   # fila 4, col 4 → blanca
        return tuple(s)

    def jugadas_legales(self, s, j):
        """
        Devuelve un generador con las jugadas legales para el jugador j.
        Si no hay jugadas, devuelve [-1] (pasar turno).
        """
        legales = [
            i for i in range(64)
            if s[i] == 0 and _fichas_volteadas(s, i, j)
        ]
        return legales if legales else [-1]

    def sucesor(self, s, a, j):
        """
        Devuelve el estado resultante de colocar la ficha de j en la casilla a.
        Si a == -1, el jugador pasa (no hay jugadas legales).
        """
        if a == -1:
            return s  # turno pasado, el estado no cambia
        # Calcular fichas a voltear ANTES de modificar el tablero
        voltear = _fichas_volteadas(s, a, j)
        s = list(s)
        s[a] = j
        for idx in voltear:
            s[idx] = j
        return tuple(s)

    def terminal(self, s):
        """
        El juego termina cuando ninguno de los dos jugadores tiene jugadas.
        """
        if list(self.jugadas_legales(s, 1))  == [-1] and \
           list(self.jugadas_legales(s, -1)) == [-1]:
            return True
        return False

    def ganancia(self, s):
        """
        Ganancia para el jugador 1:
            +1 si tiene más fichas,  -1 si tiene menos, 0 si empate.
        """
        n1 = s.count(1)
        n2 = s.count(-1)
        if n1 > n2: return  1
        if n2 > n1: return -1
        return 0


# ---------------------------------------------------------------------------
# Interfaz de texto (CLI)
# ---------------------------------------------------------------------------

class InterfaceOtello(js.JuegoInterface):

    def muestra_estado(self, s):
        simbolo = {0: ' . ', 1: ' X ', -1: ' O '}
        print('\n   ' + '  '.join(str(c) for c in range(8)))
        print('  +' + '---+' * 8)
        for f in range(8):
            fila = '|'.join(simbolo[s[f*8 + c]] for c in range(8))
            print(f'{f} |{fila}|')
            print('  +' + '---+' * 8)
        n1 = s.count(1)
        n2 = s.count(-1)
        print(f'  Negras (X): {n1}   Blancas (O): {n2}\n')

    def muestra_ganador(self, g):
        if g == 1:
            print('¡Ganan las negras (X)!')
        elif g == -1:
            print('¡Ganan las blancas (O)!')
        else:
            print('¡Empate!')

    def jugador_humano(self, s, j):
        nombre = 'Negras (X)' if j == 1 else 'Blancas (O)'
        jugadas = list(self.juego.jugadas_legales(s, j))
        if jugadas == [-1]:
            print(f'{nombre} no tiene jugadas legales. Pasa el turno.')
            return -1
        print(f'Turno de {nombre}')
        print('Jugadas legales (fila*8 + col):')
        for idx in jugadas:
            print(f'  {idx:2d} → fila {_fila(idx)}, col {_col(idx)}')
        jugada = None
        while jugada not in jugadas:
            try:
                jugada = int(input('Ingresa el índice de tu jugada: '))
            except ValueError:
                pass
        return jugada


# ---------------------------------------------------------------------------
# Función de ordenamiento
# ---------------------------------------------------------------------------

def ordena_otello(jugadas, jugador):
    """
    Ordena las jugadas usando la tabla de pesos posicionales _TABLA_POSICION.

    Las esquinas se exploran primero (valor 120), luego las aristas y
    casillas centrales, y al final las casillas adyacentes a las esquinas
    (valores negativos) que son perjudiciales.

    Explorar primero las jugadas de mayor valor permite a alfa-beta encontrar
    cotas más ajustadas y podar más ramas, alcanzando mayor profundidad.

    El turno de pasar (-1) se mueve al final para no gastar el presupuesto
    de búsqueda en él antes de explorar jugadas reales.
    """
    def peso(jugada):
        if jugada == -1:
            return -9999   # pasar turno siempre al final
        return _TABLA_POSICION[jugada]

    return sorted(jugadas, key=peso, reverse=True)


# ---------------------------------------------------------------------------
# Función de evaluación
# ---------------------------------------------------------------------------

def evalua_otello(s):
    """
    Evaluación heurística del estado s para el jugador 1. Devuelve (-1, 1).

    Combina dos criterios con pesos fijos:

    1. Control posicional (70%):
       Suma ponderada de _TABLA_POSICION para las fichas de cada jugador.
       Las esquinas valen 120 pts porque no se pueden voltear nunca,
       las casillas adyacentes a ellas valen negativo porque le dan
       acceso al rival a la esquina.

    2. Movilidad (30%):
       Diferencia normalizada de jugadas legales entre ambos jugadores.
       Tener más opciones disponibles es una ventaja táctica.

    Se normaliza con tanh para mantener el resultado en (-1, 1) sin
    confundirse con los valores terminales exactos ±1.
    """
    # --- 1. Control posicional ---
    pos = sum(_TABLA_POSICION[i] * s[i] for i in range(64))
    max_pos = sum(abs(v) for v in _TABLA_POSICION)  # 1420
    posicion = pos / max_pos

    # --- 2. Movilidad ---
    juego = Otello()
    mov1 = len([m for m in juego.jugadas_legales(s,  1) if m != -1])
    mov2 = len([m for m in juego.jugadas_legales(s, -1) if m != -1])
    if mov1 + mov2 > 0:
        movilidad = (mov1 - mov2) / (mov1 + mov2)
    else:
        movilidad = 0

    score = 0.70 * posicion + 0.30 * movilidad
    return max(-0.9999, min(0.9999, math.tanh(score * 3)))


# ---------------------------------------------------------------------------
# Script principal
# ---------------------------------------------------------------------------

if __name__ == '__main__':

    cfg = {
        "Jugador 1": "Humano",      # "Humano", "Aleatorio", "Negamax", "Tiempo"
        "Jugador 2": "Negamax",     # "Humano", "Aleatorio", "Negamax", "Tiempo"
        "profundidad máxima": 5,
        "tiempo": 10,
    }

    def jugador_cfg(cadena):
        if cadena == "Humano":
            return "Humano"
        elif cadena == "Aleatorio":
            return js.JugadorAleatorio()
        elif cadena == "Negamax":
            return minimax.JugadorNegamax(
                ordena=ordena_otello,
                d=cfg["profundidad máxima"],
                evalua=evalua_otello
            )
        elif cadena == "Tiempo":
            return minimax.JugadorMinimaxIterativo(
                tiempo=cfg["tiempo"],
                ordena=ordena_otello,
                evalua=evalua_otello
            )
        else:
            raise ValueError("Jugador no reconocido")

    interfaz = InterfaceOtello(
        Otello(),
        jugador1=jugador_cfg(cfg["Jugador 1"]),
        jugador2=jugador_cfg(cfg["Jugador 2"])
    )

    print("=" * 40)
    print("        EL JUEGO DE OTELLO")
    print("=" * 40)
    print(f"Jugador 1 (X - Negras): {cfg['Jugador 1']}")
    print(f"Jugador 2 (O - Blancas): {cfg['Jugador 2']}")
    print()

    interfaz.juega()