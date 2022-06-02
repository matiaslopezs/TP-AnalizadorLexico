# Trabajo Práctico
# Compiladores
# Alumno Matías López San Martín.
""""
 Consideraciones:
    valores prohibidos para los lexemas: ->, |, *, ., (, ), & (que simboliza a vacío)
"""

# http://micaminomaster.com.co/grafo-algoritmo/todo-trabajar-grafos-python/

# variables globales:
noTerminales = [] # lista de no terminales
terminales = [] # lista de terminales
lista_operadores = ["|","*","."] # lista de operadores de Thompson
estado = 0 #inicializamos el contador de estados en 0
dic_regexp = {} # diccionario donde guardaremos el estado de entrada y salida de cada expresion y subexpresion
dic_AFN = {} # diccionario que contendra todos los AFN
afn = {} # diccionario que contiene al AFN actual

def get_nuevo_estado():
    # retorna un número aún no utilizado para denominar un estado (enviara a partir de 1, dejando a 0=origen sin asignar)
    return estado+1

def thompson(op1, operador, op2, expresion):
# 3. Convertimos las producciones en AFN con Thompson
# función que transforma cada parte de la expresión regular en un AFN
    # solo en los estados de concatenacion el estado inicial y final no seran nuevos estados
    if operador != ".":
        nuevo_estado_i = get_nuevo_estado()
        nuevo_estado_f = get_nuevo_estado()
        # guardamos el estado inicial y final de cada expresion en el diccionario
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
        thompson(expresion,"base","")
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
        # mientras la bandera esté apagada estaremos cargando el primer operando
        if not band: 
            op1 += caracter
        # caso contrario vamos cargando el segundo operando
        else:
            op2 += caracter
    print("al salir op1: {} oper: {} op2: {}".format(op1,operador,op2))
    # evaluamos y desarmamos cada expresion
    if op1 != "":
        print("op1: {} operador: {} op2: {}".format(evaluar_entrada_rec(op1[::-1]),operador,evaluar_entrada_rec(op2[::-1])))
        # transformamos a un AFN la expresión
        thompson(op1,operador,op2,expresion)
    # el 2do operando podría ser vacío (Ej: a*)
    else:
        print("op1: {} operador: {} ".format(evaluar_entrada_rec(op2[::-1]),operador))
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
main()