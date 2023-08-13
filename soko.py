JUGADOR="@"
OBJETIVO="."
PARED="#"
JUGADOR_SOBRE_OBJETIVO="+"
CAJA="$"
CAJA_SOBRE_OBJETIVO="*"
CELDA_VACIA=" "

def crear_grilla(desc):
    '''
    Crea una grilla a partir de la descripción del estado inicial
    '''
    grilla=[]
    for i in range(len(desc)):
        lista_aux=[]
        for elemento in desc[i]:
            lista_aux.append(elemento)
        grilla.append(lista_aux)
    return grilla
    
    
def dimensiones(grilla):
    '''
    Devuelve una tupla con la cantidad de columnas y filas de la grilla.
    '''
    filas=len(grilla)
    columnas=len(grilla[0])
    return columnas,filas

    
def hay_pared(grilla, c, f):
    '''
    Devuelve True si hay una pared en la columna y fila (c, f).
    '''
    return grilla[f][c]==PARED


def hay_objetivo(grilla, c, f):
    '''
    Devuelve True si hay un objetivo en la columna y fila (c, f).
    '''
    return grilla[f][c]==OBJETIVO or grilla[f][c]==JUGADOR_SOBRE_OBJETIVO or grilla[f][c]==CAJA_SOBRE_OBJETIVO

def hay_caja(grilla, c, f):
    '''
    Devuelve True si hay una caja en la columna y fila (c, f).
    '''
    return grilla[f][c]==CAJA or grilla[f][c]==CAJA_SOBRE_OBJETIVO


def hay_jugador(grilla, c, f):
    '''
    Devuelve True si el jugador está en la columna y fila (c, f).
    '''
    return grilla[f][c]==JUGADOR or grilla[f][c]==JUGADOR_SOBRE_OBJETIVO
       

def juego_ganado(grilla):
    '''
    Devuelve True si el juego está ganado.
    '''
    for fila in range(len(grilla)):
        for col in range(len(grilla[0])):
            if hay_objetivo(grilla,col,fila) and not hay_objetivo_mas_caja(grilla,col,fila):
                return False
    return True


def posicion_jugador(grilla):
    '''
    Busca la posicion del jugador en la grilla, devolviendo una tupla (c,f) 
    '''
    for fila in range(len(grilla)):
        for col in range(len(grilla[0])):
            if hay_jugador(grilla,col,fila):
                return col,fila  


def suma_vectores(vector1,vector2):
    '''
    Recibe dos tuplas como vectores y las suma componente a componente
    '''
    suma=[]
    for i in range(len(vector1)):
        suma.append(vector1[i]+vector2[i])
    return tuple(suma)


def movimiento_valido(grilla,direccion):
    '''
    Verifica si el movimiento en la direccion indicada es valida
    si en el siguiente movimiento hay una pared, devuelve False, en caso contrario devuelve True
    '''
    nueva_posicion_jugador=suma_vectores(posicion_jugador(grilla),direccion)
    columna_sig,fila_sig=nueva_posicion_jugador
    columna_caja,fila_caja=suma_vectores(nueva_posicion_jugador,direccion)
    if hay_caja(grilla,columna_sig,fila_sig):
        return not hay_pared(grilla,columna_caja,fila_caja) and not hay_caja(grilla,columna_caja,fila_caja)
    return not hay_pared(grilla,columna_sig,fila_sig)


def hay_solo_objetivo(grilla,c,f):
    '''
    Devuelve True si hay solamente un objetivo en la columna y fila (c, f).
    '''
    return grilla[f][c]==OBJETIVO


def hay_objetivo_mas_caja(grilla,c,f):
    '''
    Devuelve True si hay un objetivo mas caja en la columna y fila (c, f).
    '''
    return grilla[f][c]==CAJA_SOBRE_OBJETIVO


def hay_objetivo_mas_jugador(grilla,c,f):
    '''
    Devuelve True si hay solamente un objetivo mas jugador en la columna y fila (c, f).
    '''
    return grilla[f][c]==JUGADOR_SOBRE_OBJETIVO


def posicion_vacia(grilla,c,f):
    '''
    Devuelve True si hay una posicion vacia en la columna y fila (c, f).
    '''
    return grilla[f][c]==CELDA_VACIA


def jugador_solo(grilla,c,f):
    '''
    Devuelve True si el jugador esta solo en la columna y fila (c, f).
    '''
    return grilla[f][c]==JUGADOR


def jugador_mas_objetivo(grilla,c,f):
    '''
    Devuelve True si hay jugador mas objetivo en la columna y fila (c, f).
    '''
    return grilla[f][c]==JUGADOR_SOBRE_OBJETIVO 


def hay_solo_caja(grilla,c,f):
    '''
    Devuelve True si hay solamente un objetivo mas jugador en la columna y fila (c, f).
    '''
    return grilla[f][c]==CAJA
    

def mover(grilla, direccion):
    '''
    Mueve el jugador en la dirección indicada
    '''
    nueva_grilla=crear_grilla(grilla)

    # verifico si el movimiento en la direccion direccion es valida

    if not movimiento_valido(grilla,direccion):
        return nueva_grilla
    
    columna_jug,fila_jug=posicion_jugador(grilla)
    nueva_posicion_jugador=suma_vectores(posicion_jugador(grilla),direccion)
    columna_sig,fila_sig=nueva_posicion_jugador
    posicion_next_sig=suma_vectores(nueva_posicion_jugador,direccion)
    columna_next_sig,fila_next_sig=posicion_next_sig

    # verifico si el jugador estaba sobre un objetivo

    nueva_grilla[fila_jug][columna_jug] = OBJETIVO if jugador_mas_objetivo(grilla, columna_jug, fila_jug) else CELDA_VACIA

    # verifico si hay un objetivo en esa posicion

    nueva_grilla[fila_sig][columna_sig]= JUGADOR_SOBRE_OBJETIVO if hay_objetivo(grilla,columna_sig,fila_sig) else JUGADOR

    # verifico si hay un objetivo + caja en esa posicion
        
    if hay_objetivo_mas_caja(grilla,columna_sig,fila_sig):

        nueva_grilla[fila_next_sig][columna_next_sig]=CAJA_SOBRE_OBJETIVO if hay_solo_objetivo(grilla,columna_next_sig,fila_next_sig) else CAJA

    # verifico si hay una caja sola en esa posicion
        
    elif hay_solo_caja(grilla,columna_sig,fila_sig):
        
        nueva_grilla[fila_next_sig][columna_next_sig]= CAJA_SOBRE_OBJETIVO if hay_solo_objetivo(grilla,columna_next_sig,fila_next_sig) else CAJA

    return nueva_grilla






     










        
    
    
    
    

