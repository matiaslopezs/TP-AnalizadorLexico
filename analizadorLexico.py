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
tokens = [] # lista de no terminales o tokens
expresiones_regulares = [] # lista de lados izquierdos
lista_operadores = ["|","*","."] # lista de operadores de Thompson
estado = 0 #inicializamos el contador de estados en 0
dic_estados_finales = {} # diccionario que contendra todos los AFN


def simulador_afd(afd_min,entrada):
# función que simula la ejecución del afd mínimo para procesar y validar una entrada
    # el primer estado que visitaremos será el estado inicial
    estado_actual = afd_min['origen']
    # para cada caracter en la entrada
    for caracter in entrada:
        # el proximo estado será igual a invalido si no se encuentra ningun símbolo igual al caracter de entrada
        proximo_estado = "invalido"
        # si el estado actual es invalido entonces salimos del loop for y estaremos en un estado no final
        if estado_actual == "invalido":
            print('caracter no definido')
            break
        # para el estado actual miramos a que estado lleva ese caracter
        for transicion in afd_min[estado_actual]:
            # si encontramos la transicion con el caracter actual
            if transicion[0] == caracter:
                # cargamos el estado al que lleva esa transicion
                proximo_estado = str(transicion[1])
        # actualizamos el estado actual
        estado_actual = proximo_estado
    # si el último estado visitado es final entonces la entrada es valida
    if estado_actual in afd_min['final']:
        print('entrada válida')
    else:
        print('entrada inválida')

def imprimir_lista_en_linea(fila_afd):
# funcion para dar forma a la impresión de una linea del afd
    for elemento in fila_afd:
        print(elemento[1],end='\t')
    print()

def eliminar_estados_inalcanzables(afd_min,cant_simbolos):
# función que se encarga de eliminar los estados redudantes del afd para que sea minimo
    # realizamos una copia del afd para ir verificando si existen modificaciones
    afd_min_new = afd_min.copy()
    band = True
    while afd_min != afd_min_new or band:
        # if al que entramos solo una vez para apagar la bandera
        if band:
            band = False
        else:
            afd_min = afd_min_new.copy()
        # verificaremos cada clave..
        for clave in afd_min.keys():
            alcanzable = False
            # el estado de origen es un estado inalcanzable pero es la excepción a la regla
            if clave != afd_min['origen'] and clave != 'origen' and clave != 'final':
                # ..con todos los demás elementos
                for elemento in afd_min.items():
                    # no nos interesa si el elemento se apunta a si mismo, tampoco los datos de origen y final en el diccionario
                    if elemento[0] != clave and elemento[0] != 'origen' and elemento[0] != 'final':
                        for i in range(cant_simbolos):
                            # si algún elemento llega a la clave, entonces es alcanzable
                            if str(elemento[1][i][1]) == clave:
                                alcanzable = True
                # si el elemento es inalcanzable lo removemos del afd minimo
                if not alcanzable:
                    afd_min_new.pop(clave)
    #retornamos el afd minimo sin estados inalcanzables
    return afd_min_new

def get_grupo(elemento, lista_grupos):
# retorna el grupo en una lista de grupos al que pertenece un elemento
    for grupo in lista_grupos:
        if elemento in grupo:
            return grupo

def comparar(estado,estado_comp,pi,dtran_afd,simbolos):
# función que compara si dos estados en un AFD van a los mismos grupos con todos sus símbolos
    # valor de retorno
    iguales = True
    # cargamos los valores en el diccionario de ambos estados
    valor_estado = dtran_afd[estado]
    valor_comp = dtran_afd[estado_comp]
    # para cada símbolo de entrada
    for i in range(len(simbolos)):
        # si los estados no apuntan a estados del mismo grupo entonces retornaremos falso
        if get_grupo(valor_estado[i][1],pi) != get_grupo(valor_comp[i][1],pi):
            iguales = False
    return iguales

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
    # cargamos todos los estados de pi en una sola lista sin importar los grupos
    lista_estados_pi = f + s_f
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
            # para cada estado en el grupo
            for estado in grupo:
                # cargamos el primer estado en la lista
                lista = [estado]
                # comparamos con los demas elementos del grupo
                for estado_comp in grupo:
                    if estado_comp != estado:
                        # si van a los mismos grupos por cada simbolo de entrada
                        if comparar(estado,estado_comp,pi,dtran_afd,simbolos):
                            # añadimos al estado a comparar a la lista junto al estado actual
                            lista.append(estado_comp)
                # ordenamos la lista
                lista.sort()
                # luego añadimos la lista a pi nueva si es que el grupo de la lista aún no se encuentra
                if lista not in pi_nueva:
                    pi_nueva.append(lista)
    # declaramos un dic donde guardaremos el AFD mínimo
    afd_minimo = {}
    # ya tenemos los estados, ahora veremos las relaciones entre ellos
    for elemento in pi:
        # veremos el primer elemento de cada grupo a que estado va por cada símbolo de entrada
        elem_afd = dtran_afd[elemento[0]]
        for i in range(len(simbolos)):
            # guardamos en el nuevo dic los valores
            if str(elemento) not in afd_minimo.keys():
                afd_minimo[str(elemento)] = []
            afd_minimo[str(elemento)].append([simbolos[i],get_grupo(elem_afd[i][1],pi)])
    # señalamos al diccionario el estado inicial y los finales
    # tenemos el inicial del afd no minimizado, entonces buscamos en que grupo está del afd minimo
    afd_minimo['origen'] = str(get_grupo(dtran_afd['origen'][0],pi))
    # mismo proceso con la lista de estados finales
    for estado_final in dtran_afd['final']:
        if 'final' not in afd_minimo.keys():
            afd_minimo['final'] = []
        afd_minimo['final'].append(str(get_grupo(estado_final,pi)))
    # descartamos los elementos repetidos en el item de key 'final'
    afd_minimo['final'] = list(set(afd_minimo["final"]))
    return afd_minimo

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
        if transicion[0] == estado and transicion[1] == '&':
            resultado += cerradura_epsilon(afn,transicion[2])
    # retornamos el resultado
    return resultado

def get_AFD(afn,lista_simbolos):
# función que transforma un AFN en un AFD. Recibe como parámetros al AFN y a los terminales del AFN
    # dtran es la matriz del AFD, en este caso será un diccionario de listas
    dtran = {}
    # primero inicializamos destados con el estado inicial
    destados = []
    destados.append(cerradura_epsilon(afn,afn[0][0]))
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
            u = []
            # para cada estado devuelto por mover, agregamos a u
            for estado_mov in estados_mover:
                u += cerradura_epsilon(afn,estado_mov)
            u.sort()
            # quitamos los estados repetidos
            u = list(set(u))
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
    # por último guardamos en el diccionario cuales son el estado origen y los estados finales del AFD
    dtran["origen"] = get_key_valor_afd(dic_AFD,afn[0][0])
    # guardamos en el afd todos los estados finales que guardamos en el diccionario global de estados
    for estado_final in dic_estados_finales.values():
        if "final" not in dtran.keys():
            # hacemos un set para no tener elementos repetidos
            dtran["final"] = []
        dtran["final"] += get_key_valor_afd(dic_AFD,estado_final)
    # transformamos el item con key 'final' en una lista
    dtran["final"] = list(set(dtran["final"]))
    return dtran

def get_lista_simbolos(afn):
# función que retorna un set (lista ordenada sin repetidos) de todos los símbolos de entrada de un afn
    # creamos un set para que no hayan elementos repetidos
    set_simbolos = set()
    for transicion in afn:
        # no debemos guardar el vacío ya que no forma parte del alfabeto de entrada
        if transicion[1] != "&":
            set_simbolos.add(transicion[1])
    return set_simbolos
        

def get_nuevo_estado(ultimo_estado = estado):
# retorna un número aún no utilizado para denominar un estado (enviara a partir de 1, dejando a 0=origen sin asignar)
# el parametro ultimo estado es el ultimo estado conocido, de no mandarlo es la variable global estado
    # referenciamos a la variable global estado
    global estado
    estado += 1
    # si estado es menor al último estaado conocido entonces lo modificamos
    if estado <= ultimo_estado:
        estado = ultimo_estado+1
    return estado

def thompson(op1, operador, op2, afn1, afn2):
# Convertimos las producciones en AFN con Thompson
# función que transforma cada parte de la expresión regular en un AFN
    nuevo_afn = []
    # si el operador es igual a base significa que la entrada es solo un caracter
    if operador == "base":
        nuevo_estado_i = get_nuevo_estado()
        nuevo_estado_f = get_nuevo_estado()
        nuevo_afn.append([nuevo_estado_i,op1,nuevo_estado_f])
    # si es una concatenacion (.) entonces estado_i_op2 = estado_f_op1   
    elif operador == ".":
        # cargamos cada elemento del primer afn exactamente como está
        for elemento1 in afn1:
            nuevo_afn.append(elemento1)
        # a cada estado del afn2 le vamos sumando +1 (empezando desde el último estado del afn1)
        valor = afn1[-1][2]
        for elemento2 in afn2:
            elemento2[0] = valor
            valor += 1
            elemento2[2] = valor
            valor += 1
            nuevo_afn.append(elemento2)
    elif operador == "|":
        # agregamos dos transiciones vacías al inicio al primer estado de ambos afn
        nuevo_afn.append([afn1[0][0],"&",afn1[0][0]+1])
        nuevo_afn.append([afn1[0][0],"&",afn2[0][0]+1])
        # sumamos +1 a todos los estados de ambos afn y los añadimos al nuevo afn
        for elemento1 in afn1:
            elemento1[0] += 1
            elemento1[2] += 1
            nuevo_afn.append(elemento1)
        for elemento2 in afn2:
            elemento2[0] += 1
            elemento2[2] += 1
            nuevo_afn.append(elemento2)
        # agregamos transiciones vacías del ultimo estado de ambos afn a un nuevo estado final
        nuevo_estado_f = get_nuevo_estado(afn2[-1][2])
        nuevo_afn.append([afn1[-1][2],"&",nuevo_estado_f])
        nuevo_afn.append([afn2[-1][2],"&",nuevo_estado_f])
    elif operador == "*":
        # agregamos una transicion vacía al inicio al primer estado del afn
        nuevo_afn.append([afn1[0][0],"&",afn1[0][0]+1])
        # sumamos +1 a todos los estados del afn y los añadimos al nuevo afn
        for elemento in afn1:
            elemento[0] += 1
            elemento[2] += 1
            nuevo_afn.append(elemento)
        # agregamos una transicion vacia del ultimo al primer estado del viejo afn
        nuevo_afn.append([afn1[-1][2],"&",afn1[0][0]])
        # agregamos un nuevo estado final y una transicion vacía del nuevo primer estado al nuevo estado final
        nuevo_estado_f = get_nuevo_estado(afn1[-1][2])
        nuevo_afn.append([afn1[0][0]-1,"&",nuevo_estado_f])
        # agregamos una transicion vacia del ultimo estado del viejo afn al ultimo estado del nuevo afn
        nuevo_afn.append([afn1[-1][2],"&",nuevo_estado_f])
    return nuevo_afn

def buscar_parentesis(expresion):
# función que retorna true si encuentra un parentesis en la expresión (la gramatica de entrada)
    if "(" in expresion or ")" in expresion:
        return True
    return False

def evaluar_entrada_rec(expresion):
# evaluamos la gramática de entrada y vamos dividiendo en operadores y operandos de forma recursiva
    # print("nueva recursion: {}".format(expresion))
    # quitamos los parentesis de la expresion
    if expresion[0] == "(" and expresion[-1]==")": # and not buscar_parentesis(expresion[1:-1]):
        expresion = expresion[1:-1]
        # print("quitamos los parentesis => {}".format(expresion))

    # Caso Base: si la expresión es un caracter diferente a la lista de operadores de Thompson
    if expresion not in lista_operadores and len(expresion) == 1:
        # print(expresion)
        # transformamos la expresión en un AFN
        nuevo_afn = thompson(expresion,"base",None,None,None)
        return expresion,nuevo_afn
    # dividimos la expresión en operandos y operador
    op1 = op2 = operador = ""
    band = band_asterisco = False
    parentesis_cerrado = parentesis_abierto = 0
    # para cada caracter recorremos en reversa porque las operaciones deben hacerse de izquierda a derecha
    for caracter in expresion[::-1]:
        # Debemos tener en cuentra procesar los paréntesis primero
        # como está recorriendo al revés buscamos primero el ")"
        if caracter == ")":
            parentesis_cerrado += 1
        # luego vamos contando los parentesis abiertos
        elif caracter == "(":
            parentesis_abierto += 1    
        # caso en el que venga un operador, lo guardamos y empezamos a cargar el siguiente operando
        elif caracter in lista_operadores and not band:
            # solamente si se cerraron todos los paréntesis pasamos al siguiente operando
            if parentesis_abierto == parentesis_cerrado:
                # * es un caso especial
                if caracter != '*':
                    operador = caracter
                    band = True
                    continue
                else:
                    band_asterisco = True
        # mientras la bandera esté apagada estaremos cargando el segundo operando (ya que va en reversa)
        if not band: 
            op2 += caracter
        # caso contrario vamos cargando el primer operando
        else:
            op1 += caracter
    # volvemos a dar la vuelta a los operandos
    op1 = op1[::-1]
    op2 = op2[::-1]
    # verificamos si existe * en la expresion
    if band_asterisco:
        # verificamos que no exista otro operador
        if operador == "":
            # quitamos el * de la operacion
            op2 = op2[:-1]
            # el operador será *
            operador = '*'

    # print("al salir op1: {} oper: {} op2: {}".format(op1,operador,op2))
    # evaluamos y desarmamos cada expresion
    if op1 != "":
        exp1,afn1 = evaluar_entrada_rec(op1) 
        exp2,afn2 = evaluar_entrada_rec(op2)
        # print("op1: {} operador: {} op2: {}".format(exp1,operador,exp2))
        # transformamos a un AFN la expresión
        nuevo_afn = thompson(op1,operador,op2,afn1,afn2)
    # el 2do operando podría ser vacío (Ej: a*)
    else: 
        exp2,afn2 = evaluar_entrada_rec(op2)
        # print("op1: {} operador: {} ".format(exp2,operador))
        # transformamos a un AFN la expresión
        nuevo_afn = thompson(op2,operador,None,afn2,None)
    return expresion,nuevo_afn
    

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
        tokens.append(expresion[0])
        print("No terminal: {}".format(tokens[i]))
        i+=1
        expresiones_regulares.append(expresion[1])
        print("ingrese la siguiente expresión:")
        entrada = input()

    # 2. Crear el AFN con Thompson
    # uniremos todos los afn en uno solo con un origen o' en común
    afn_completo = []
    # iremos guardando también los simbolos de entrada en las expresiones regulares
    lista_simbolos = set()
    # primero debemos dividir la gramática de entrada en operandos
    for j in range(len(expresiones_regulares)):
        # para cada expresion hallamos su afn (utilizando las construcciones de thompson)
        expres,afn = evaluar_entrada_rec(expresiones_regulares[j])
        # cargamos los símbolos de transiciones en la lista de simbolos
        for sim in get_lista_simbolos(afn):
            lista_simbolos.add(sim)
        # guardamos en el diccionario a cada token con su estado final (obtenido de su afn)
        dic_estados_finales[tokens[j]] = afn[-1][2]
        # luego creamos la transicion vacía de o' al primer estado del afn
        afn_completo.append([0,"&",afn[0][0]])
        # y agregamos al afn unico que representara a la definicion regular completa
        afn_completo += afn
    
    # 3. Una vez que tenemos el afn que representa a la definicion regular completa, Hallamos el AFD
    # obtenemos la matriz del afd
    dtran_afd = get_AFD(afn_completo,list(lista_simbolos))
    # 4. Optimizamos nuestro AFD obteniendo el AFD mínimo
    afd_min = get_AFD_minimo(dtran_afd, list(lista_simbolos))
    # 4.1 eliminamos los estados inalcanzables
    afd_minimo = eliminar_estados_inalcanzables(afd_min,len(lista_simbolos))
    # 4.2 imprimimos en consola la tabla del AFD mínimo
    print("\nTabla del AFD Mínimo\n")
    print("Estado", end='\t')
    for simb in lista_simbolos:
        print(simb, end='\t')
    print()
    for elemento in afd_minimo.items():
        if(elemento[0] == 'origen'):
            print('---------'*len(lista_simbolos))
        print(elemento[0], end='\t')
        if(elemento[0]!= 'origen'):
            imprimir_lista_en_linea(elemento[1])
        else:
            print(elemento[1])
    # 5. ahora simulamos la ejecución del analizador léxico 
    # entrada_test='ababb abb ababa baabb'
    # for palabra in entrada_test.split():
    #     print(palabra)
    #     simulador_afd(afd_min,palabra)
    #     print('___')
    print('fin')
    

main()
# afn_test = [[0,"$",1],[1,"$",2],[1,"$",4],[2,"a",3],[4,"b",5],[3,"$",6],[5,"$",6],[6,"$",7],[6,"$",1],[0,"$",7],[7,"a",8],[8,"b",9],[9,"b",10]]
# # afd_min_test = {
# #     'A': [['a','B'],['b','B']],
# #     'B': [['a','B'],['b','C']],
# #     'C': [['a','B'],['b','C']],
# #     'D': [['a','B'],['b','C']],
# #     'E': [['a','B'],['b','E']],
# #     'F': [['a','B'],['b','E']],
# #     'origen': 'A',
# #     'final':['D']
# # }
# entrada_test='ababb abb ababa baabb'