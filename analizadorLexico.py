# Trabajo Práctico
# Compiladores
# Alumno Matías López San Martín.
""""
 Consideraciones:
    valores prohibidos para los lexemas: ->, |, *, ., (, ), & (que simboliza a vacío)
"""

# http://micaminomaster.com.co/grafo-algoritmo/todo-trabajar-grafos-python/

import math

# variables globales:
noTerminales = [] # lista de no terminales
terminales = [] # lista de terminales
lista_operadores = ["|","*","."] # lista de operadores de Thompson
estado = 0 #inicializamos el contador de estados en 0
dic_regexp = {} # diccionario donde guardaremos el estado de entrada y salida de cada expresion y subexpresion
dic_AFN = {} # diccionario que contendra todos los AFN
afn = [] # lista que contiene al AFN actual

def get_AFD_minimo(dtran_afd,simbolos):
# función que minimiza el AFD. Recibe la matríz del AFD como parámetro
    # empezamos dividiendo los estados en dos grupos
    # estados finales
    f = dtran_afd["final"]
    # los demás estados (cargamos todos los estados en la tabla menos los finales y los valores origen y final)
    s_f = [estado for estado in dtran_afd.keys() if estado not in f and estado != 'origen' and estado != 'final']
    # guardamos todos los grupos en pi
    pi = []
    pi.append(f)
    pi.append(s_f)
    pi_nueva = []
    # bandera para que no copie la primera pi_nueva vacía en pi
    band = False
    # mientras pi y pi_nueva sean diferentes (mientras haya cambios en pi)
    while pi != pi_nueva:
        # en este if solo no entrará la primera vez
        if band:
            # copiamos por referencia los valores de pi_nueva en pi
            pi = pi_nueva.copy()
            pi_nueva = []
        # activamos la bandera para el resto de las iteraciones
        band = True
        # para cada grupo en pi
        for grupo in pi:
            # definimos un set donde guardaremos los elementos que se queden fuera del grupo
            afuera = set()
            # para cada simbolo de entrada
            for simbolo in simbolos:
                # para cada elemento en el grupo
                for elemento in grupo:
                    for valor in dtran_afd[elemento]:
                        if valor[0] == simbolo:
                            # si el elemento apunta no a otro estado dentro de su grupo se queda afuera en otro grupo
                            if valor[1] not in grupo:
                                afuera.add(elemento)
            # valores que apuntan a estados dentro del grupo
            adentro = [x for x in grupo if x not in afuera]
            # agregamos los nuevos grupos a la nueva pi
            if afuera != []:
                pi_nueva.append(list(afuera))
            if adentro != []:
                pi_nueva.append(adentro)
    print("end")

def get_key_valor_afd(dic_AFD,valor):
# funcion que devuelve la clave del diccionario si el valor de parámetro está en la lista del dic.
    respuesta = []
    for key,lista_estados in dic_AFD.items():
        if valor in lista_estados:
            respuesta.append(key)
    return respuesta

def obtener_key(diccionario,valor):
#función para obtener el key de un diccionario, teniendo el valor como dato
    for key,value in diccionario.items():
        if value == valor:
            return key
    return -1

def mover(afn,estado,simbolo):
# función que implementa la función mover del AFD
    resultado = []
    for transicion in afn:
        # si va desde el estado actual con el simbolo entonces añadimos a resultado
        if transicion[0] == estado and transicion[1] == simbolo:
            resultado.append(transicion[2])
    return resultado

def cerradura_epsilon(afn,estado):
# función que implementa las cerraduras epsilon del AFD
    # por la identidad el primer estado que puede alcanzar es el mismo
    resultado = [estado]
    for transicion in afn:
        # si va desde el estado actual con el símbolo entonces es parte de la respuesta
        if transicion[0] == estado and transicion[1] == '$':
            resultado += cerradura_epsilon(afn,transicion[2])
    # retornamos el resultado
    return resultado

def get_AFD(afn,lista_simbolos):
# función que transforma un AFN en un AFD. Recibe como parámetros al AFN y a los terminales del AFN
    # dtran es la matriz del AFD, en este caso será un diccionario de listas
    dtran = {}
    menor_estado = afn[0][0]
    mayor_estado = -math.inf
    # primero inicializamos destados con el estado inicial
    destados = []
    destados.append(cerradura_epsilon(afn,menor_estado))
    # guardaremos los nuevos estados en un diccionario
    nuevo_estado = estado_origen = 0
    destados[0].sort()
    dic_AFD = {nuevo_estado: destados[0]}
    # mientras haya un estado sin procesar seguimos
    while len(destados)>0:
        estado_origen = obtener_key(dic_AFD,destados[0])
        lista_estados = destados.pop(0)
        # para cada simbolo de entrada
        for simbolo in lista_simbolos:
            # aplicamos la funcion mover a todos los estados de la lista
            estados_mover = []
            for estado in lista_estados:
                # para cada estado en la lista aplicamos la función mover
                estados_mover += mover(afn,estado,simbolo)
                # aprovechamos y calculamos el estado mayor del afn
                if mayor_estado < estado:
                    mayor_estado = estado
                    
            u = []
            # para cada estado devuelto por mover, agregamos a u
            for estado_mov in estados_mover:
                u += cerradura_epsilon(afn,estado_mov)
            u.sort()
            # si es un nuevo estado
            if u not in dic_AFD.values():
                nuevo_estado += 1
                estado_destino = nuevo_estado
                # lo guardamos en el diccionario
                dic_AFD[nuevo_estado]= u
                # lo metemos en destados para procesarlo
                destados.append(u)
            # si es un estado conocido
            else:
                # obtenemos el id
                estado_destino = obtener_key(dic_AFD,u)
            # cargamos al resultado el valor al que el estado origen lleva desde ese simbolo
            if estado_origen not in dtran.keys():
                dtran[estado_origen] = []
            dtran[estado_origen].append([simbolo,estado_destino])
    # por último guardamos en el diccionario cuales son el origen y el final del AFD
    dtran["origen"] = get_key_valor_afd(dic_AFD,menor_estado)
    dtran["final"] = get_key_valor_afd(dic_AFD,mayor_estado)
    # print(dtran)
    return dtran

def get_nuevo_estado():
    # retorna un número aún no utilizado para denominar un estado (enviara a partir de 1, dejando a 0=origen sin asignar)
    global estado
    estado += 1
    return estado

def thompson(op1, operador, op2, expresion):
# 3. Convertimos las producciones en AFN con Thompson
# función que transforma cada parte de la expresión regular en un AFN
    # solo en los estados de concatenacion el estado inicial y final no seran nuevos estados
    if operador != ".":
        nuevo_estado_i = get_nuevo_estado()
        nuevo_estado_f = get_nuevo_estado()
        # guardamos el estado inicial y final de cada expresion en el diccionario de regex
        dic_regexp[expresion] = [nuevo_estado_i,nuevo_estado_f]
    
    # si el operador es igual a base significa que la entrada es solo un caracter
    if operador == "base":
        dic_regexp[op1] = [nuevo_estado_i,nuevo_estado_f]
        afn.append([nuevo_estado_i,op1,nuevo_estado_f])
    # si es una concatenacion (.) entonces estado_f_op1 = estado_i_op2    
    elif operador == ".":
        # quitamos los antiguos valores del afn
        afn.remove([dic_regexp[op1][0],op1,dic_regexp[op1][1]])
        # actualizamos el diccionario
        dic_regexp[op1][1] = dic_regexp[op2][0]
        # agregamos los nuevos valores al afn
        afn.append([dic_regexp[op1][0],op1,dic_regexp[op1][1]])
        # guardamos los estados inicial y final en el diccionario de regex
        dic_regexp[expresion] = [dic_regexp[op1][0],dic_regexp[op2][1]]
    elif operador == "|":
        afn.append([nuevo_estado_i,"&",dic_regexp[op1][0]])
        afn.append([dic_regexp[op1][1],"&",nuevo_estado_f])
        afn.append([nuevo_estado_i,"&",dic_regexp[op2][0]])
        afn.append([dic_regexp[op2][1],"&",nuevo_estado_f])
    elif operador == "*":
        afn.append([nuevo_estado_i,"&",nuevo_estado_f])
        afn.append([nuevo_estado_i,"&",dic_regexp[op1][0]])
        afn.append([dic_regexp[op1][1],"&",nuevo_estado_f])
        afn.append([dic_regexp[op1][1],"&",dic_regexp[op1][0]])

def buscar_parentesis(expresion):
# función que retorna true si encuentra un parentesis en la expresión (la gramatica de entrada)
    if "(" in expresion or ")" in expresion:
        return True
    return False

def evaluar_entrada_rec(expresion):
# evaluamos la gramática de entrada y vamos dividiendo en operadores y operandos de forma recursiva

    print("nueva recursion: {}".format(expresion))
    
    # quitamos los parentesis de la expresion
    if expresion[0] == "(" and expresion[-1]==")" and not buscar_parentesis(expresion[1:-1]):
        expresion = expresion[1:-1]
        print("quitamos los parentesis => {}".format(expresion))

    # Caso Base: si la expresión es un caracter diferente a la lista de operadores de Thompson
    if expresion not in lista_operadores and len(expresion) == 1:
        print(expresion)
        # transformamos la expresión en un AFN
        thompson(expresion,"base","",expresion)
        return expresion
    # dividimos la expresión en operandos y operador
    op1 = op2 = operador = ""
    band = False
    parentesis_cerrado = parentesis_abierto = 0
    # para cada caracter recorremos en reversa porque las operaciones deben hacerse de izquierda a derecha
    for caracter in expresion[::-1]:
        # print("entra aca: {}".format(caracter))
        # Debemos tener en cuentra procesar los paréntesis primero
        # como está recorriendo al revés buscamos primero el ")"
        if caracter == ")":
            parentesis_cerrado += 1
        # luego vamos contando los parentesis abiertos
        elif caracter == "(":
            parentesis_abierto += 1    
        # caso en el que venga un operador, lo guardamos y empezamos a cargar el siguiente operando
        elif caracter in lista_operadores and not band:
            # print(parentesis_abierto)
            # print(parentesis_cerrado)    
            # print("se encuentra operador")
            # solamente si se cerraron todos los paréntesis pasamos al siguiente operando
            if parentesis_abierto == parentesis_cerrado:
                operador = caracter
                band = True
                continue
        # mientras la bandera esté apagada estaremos cargando el segundo operando (ya que va en reversa)
        if not band: 
            op2 += caracter
        # caso contrario vamos cargando el primer operando
        else:
            op1 += caracter
    # volvemos a dar la vuelta a los operandos
    op1 = op1[::-1]
    op2 = op2[::-1]
    print("al salir op1: {} oper: {} op2: {}".format(op1,operador,op2))
    # evaluamos y desarmamos cada expresion
    if op1 != "":
        print("op1: {} operador: {} op2: {}".format(evaluar_entrada_rec(op1),operador,evaluar_entrada_rec(op2)))
        # transformamos a un AFN la expresión
        thompson(op1,operador,op2,expresion)
    # el 2do operando podría ser vacío (Ej: a*)
    else:
        print("op1: {} operador: {} ".format(evaluar_entrada_rec(op2),operador))
        # transformamos a un AFN la expresión
        thompson(op1,operador,"",expresion)
    return expresion
    


def main():
    print("Bienvenido al analizador léxico")
    
    # 1. Definir el lenguaje de entrada. Ingresar definición regular
    print("Por favor ingrese una expresión regular (FIN para terminar)")
    entrada = input()
    i = 0
    # se ingresaran expresiones mientras el terminal sea diferente a FIN
    while entrada!= "FIN":
        print("La expresión ingresada es "+entrada)
        # dividimos en lado derecho e izquierdo con split
        expresion = entrada.split("->")
        # agregamos a la lista el no terminal
        noTerminales.append(expresion[0])
        print("No terminal: {}".format(noTerminales[i]))
        i+=1
        terminales.append(expresion[1])
        print("ingrese la siguiente expresión:")
        entrada = input()

    # 2. Crear el AFN con Thompson
    # primero debemos dividir la gramática de entrada en operandos
    for terminal in terminales:
        print(terminal)
        # para lado izquierdo reiniciamos los diccionarios
        dic_regexp = afn = {} 
        evaluar_entrada_rec(terminal)
        print("diccionario:")
        print(dic_regexp)
        print("AFN:")
        print(afn)

# main()
afn_test = [[0,"$",1],[1,"$",2],[1,"$",4],[2,"a",3],[4,"b",5],[3,"$",6],[5,"$",6],[6,"$",7],[6,"$",1],[0,"$",7],[7,"a",8],[8,"b",9],[9,"b",10]]
lista_simbolos = ["a","b"]
# obtenemos la matriz del afd
dtran_afd = get_AFD(afn_test,lista_simbolos)
# print(dtran_afd)
get_AFD_minimo(dtran_afd, lista_simbolos)
print("final")