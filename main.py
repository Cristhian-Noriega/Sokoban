import soko
import gamelib
from pila import Pila
from cola import Cola

OESTE = (-1, 0)
ESTE = (1, 0)
NORTE = (0, -1)
SUR = (0, 1)
ANCHO_VENTANA =372
ALTO_VENTANA =434
MEDIDA_CUADRADO = 62
MOVIMIENTOS=[ESTE, OESTE, SUR, NORTE]


class Juego:
    '''
    Representa el estado del juego, mediante el atributo nivel
    '''
    def __init__(self,niveles,teclas):
        '''
        Recibe un diccionario de niveles, en donde la clave es el nivel y el valor la descripcion 
        '''
        self.i=0
        self.niveles=niveles
        self.teclas=teclas
        self.nivel=list(niveles.items())[self.i][1]
        self.grilla=soko.crear_grilla(self.nivel)
        self.pila_undo=Pila()
        self.pila_redo=Pila()
        self.cola_pistas=Cola()
        self.pistas=None

    def next_level(self):
        '''
        Permite pasar al siguiente nivel
        '''
        if self.i+1<len(self.niveles):
            self.i+=1
            self.nivel=list(self.niveles.items())[self.i][1]

    def actualizar_pila_undo(self):
        ''''
        Actualiza la pila deshacer desapilando todos los elementos dejando el primer estado
        '''
        while not self.pila_undo.esta_vacia():
            self.pila_undo.desapilar()
        self.pila_undo.apilar(self.grilla)

    def actualizar_pila_redo(self):
        '''
        Actualiza la pila rehacer desapilando todos los elementos
        '''
        while not self.pila_redo.esta_vacia():
            self.pila_redo.desapilar()

    def actualizar_cola_pistas(self):
        '''
        Actualiza la cola de pistas 
        '''
        if self.pistas:
            for pista in self.pistas:
                self.cola_pistas.encolar(pista)

    def next_clue(self):
        '''
        Desencola la siguiente pista de la cola de pistas
        '''
        if not self.cola_pistas.esta_vacia():
            return self.cola_pistas.desencolar()    
    
    def juego_ganado(self):
        '''
        Si el juego esta ganado, pasa al siguiente nivel y actualiza el estado 
        '''
        self.next_level()
        self.grilla=soko.crear_grilla(self.nivel)
        self.actualizar_pila_undo()
        while not self.cola_pistas.esta_vacia():
            self.cola_pistas.desencolar()
        self.pistas=None



def crear_niveles(archivo):
    '''
    Recibe un archivo con niveles y devuelve un diccionario
    con los niveles como clave y la descripcion como valor
    '''
    with open(archivo) as f: 
        niveles={}
        contador=0
        for linea in f: 
            linea=linea.rstrip("\n")
            if "Level" in linea:
                niveles[linea]=[]
                contador+=1
                continue
            if "'" in linea:
                continue
            if linea!="" and "Level" not in linea :
                niveles["Level "+str(contador)].append(linea)

        for nivel in niveles:
            desc=crear_descripcion(niveles[nivel])
            niveles[nivel]=desc
    
    return niveles


def crear_descripcion(nivel):
    '''
    Modifica la descripcion de un nivel para que 
    tengan la misma longitud por igual
    '''
    maximo_len=len(max(nivel,key=len))
    res=[]
    for desc in nivel:
        if len(desc)<maximo_len:
            desc+=" "*(maximo_len-len(desc))
            res.append(desc)
        else:
            res.append(desc)
    return res


def dicc_teclas(archivo):
    '''
    Recibe un archivo de teclas y devuelve un diccionario
    con la tecla como clave y el movimiento como valor
    '''
    res={}
    with open(archivo) as f:
        for linea in f:
            linea=linea.rstrip()
            if linea=="":
                continue
            tecla,mov=linea.split(" = ")
            res[tecla]=mov
    
    return res


def grilla_inmutable(grilla):
    '''
    Recibe un estado y devuelve una representacion inmutable del mismo
    '''
    col,fila=soko.dimensiones(grilla)
    estado_inmutable=""
    for i in range(fila):
        for j in range(col):
            estado_inmutable+=grilla[i][j]
    return estado_inmutable
    

def buscar_solucion(grilla):
    '''
    Wrapper de la funcion recursiva backtrack
    '''
    visitados={}
    return backtrack(grilla,visitados)


def backtrack(grilla,visitados):
    '''
    Funcion recursiva que busca todas las pistas desde el estado actual
    '''
    visitados[grilla_inmutable(grilla)]=grilla_inmutable(grilla)
    if soko.juego_ganado(grilla):
        return True, []
    for mov in MOVIMIENTOS:
        nuevo_estado=soko.mover(grilla,mov)
        if grilla_inmutable(nuevo_estado) in visitados:
            continue
        solucion_encontrada,acciones=backtrack(nuevo_estado,visitados)
        if solucion_encontrada:
            return True, [mov]+acciones
    return False, None

    
def juego_actualizar(juego,tecla,keys):
    '''
    Actualiza el estado del juego
    '''
    if tecla in keys:
        mov=keys[tecla]
        if mov=="NORTE":
            juego=soko.mover(juego,NORTE)
        elif mov=="SUR":
            juego=soko.mover(juego,SUR)
        elif mov=="ESTE":
            juego=soko.mover(juego,ESTE)
        elif mov=="OESTE":
            juego=soko.mover(juego,OESTE)
        return juego,mov
    return False


def juego_mostrar(grilla):
    '''
    Acutaliza la ventana
    '''
    col,fila=soko.dimensiones(grilla)

    for i in range(fila):
        for j in range(col):
            y=i*MEDIDA_CUADRADO
            x=j*MEDIDA_CUADRADO
            if soko.hay_pared(grilla,j,i):
                gamelib.draw_image('img/wall.gif', x, y)
            else:
                gamelib.draw_image('img/ground.gif',x, y)

            if soko.hay_caja(grilla,j,i):
               gamelib.draw_image('img/box.gif', x, y)                

            if soko.hay_jugador(grilla,j,i):
               gamelib.draw_image('img/player.gif', x, y)       
            
            if soko.hay_objetivo(grilla,j,i):
               gamelib.draw_image('img/goal.gif', x, y)


def main():
    # Inicializar el estado del juego

    try:
        niveles=crear_niveles("niveles.txt")
        teclas=dicc_teclas("teclas.txt")
    except FileNotFoundError as e:
        print("Archivo/s no encontrado/s: ",e)
    except IOError as e:
        print("Error de entrada/salida: ",e)
    
    juego=Juego(niveles,teclas)
    juego.pila_undo.apilar(juego.grilla)
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)

    while gamelib.is_alive():
        gamelib.draw_begin()
        # Dibujar la pantalla
        juego_mostrar(juego.grilla)
        gamelib.draw_end()
        
        if soko.juego_ganado(juego.grilla):
            juego.juego_ganado()
            gamelib.resize(len(juego.grilla[0])*MEDIDA_CUADRADO,len(juego.grilla)*MEDIDA_CUADRADO)
            continue

        ev = gamelib.wait(gamelib.EventType.KeyPress)
        if not ev:
            break

        tecla = ev.key
        # Actualizar el estado del juego, según la `tecla` presionada

        if not juego_actualizar(juego.grilla,tecla,juego.teclas):
            continue

        if juego_actualizar(juego.grilla,tecla,juego.teclas)[1]=="SALIR":
            break

        elif juego_actualizar(juego.grilla,tecla,juego.teclas)[1]=="REINICIAR":
            juego.grilla=soko.crear_grilla(juego.nivel)
            juego.actualizar_pila_undo()
            juego.actualizar_pila_redo()
            juego.pistas=None
            continue
        
        elif juego_actualizar(juego.grilla,tecla,juego.teclas)[1]=="DESHACER":
            if juego.pila_undo.ver_tope()!=soko.crear_grilla(juego.nivel):
                juego.pila_redo.apilar(juego.pila_undo.desapilar())
                juego.grilla=juego.pila_undo.ver_tope()
            continue

        elif juego_actualizar(juego.grilla,tecla,juego.teclas)[1]=="REHACER":
            if not juego.pila_redo.esta_vacia():
                juego.pila_undo.apilar(juego.pila_redo.desapilar())
                juego.grilla=juego.pila_undo.ver_tope() 
            continue

        elif juego_actualizar(juego.grilla,tecla,juego.teclas)[1]=="PISTA":
            if not juego.pistas:
                _,juego.pistas=buscar_solucion(juego.grilla)
                juego.actualizar_cola_pistas()
                continue
            juego.grilla=soko.mover(juego.grilla,juego.next_clue())
            continue

        juego.grilla=juego_actualizar(juego.grilla,tecla,juego.teclas)[0]
        juego.pistas=None
        juego.pila_undo.apilar(juego.grilla)
        juego.actualizar_pila_redo()
            
gamelib.init(main)