# Trabajo Práctico
# Compiladores
# Alumno Matías López San Martín.
""""
 Consideraciones:
    valores prohibidos: ->, |, *, ., (, ), & (que simboliza a vacío)
"""

# http://micaminomaster.com.co/grafo-algoritmo/todo-trabajar-grafos-python/

noTerminales = [] # lista de no terminales
terminales = [] # lista de terminales
lista_operadores = ["|","*","."] # lista de operadores de Thompson
    
def thompson(entrada):
    nro_estado = 1
    matriz = []
# función que transforma cada parte de la expresión regular en un AFN
    # cadena vacía
    if entrada == "&":
        pass

def buscar_parentesis(expresion):
# función que retorna true si encuentra un parentesis en la expresión
    if "(" in expresion or ")" in expresion:
        return True
    return False

def evaluar_entrada_rec(expresion):
# evaluamos la entrada y vamos dividiendo en operadores y operandos de forma recursiva

    print("nueva recursion: {}".format(expresion))
    
    # quitamos los parentesis de la expresion
    if expresion[0] == "(" and expresion[-1]==")" and not buscar_parentesis(expresion[1:-1]):
        expresion = expresion[1:-1]
        print("quitamos los parentesis => {}".format(expresion))

    # Caso Base: si la expresión es un caracter diferente a la lista de operadores de Thompson
    if expresion not in lista_operadores and len(expresion) == 1:
        print(expresion)
        return expresion
    # dividimos la expresión en operandos y operador
    op1 = op2 = operador = ""
    band = False
    parentesis_cerrado = parentesis_abierto = 0
    # para cada caracter recorremos en reversa porque las operaciones deben hacerse de izquierda a derecha
    for caracter in expresion[::-1]:
        print("entra aca: {}".format(caracter))
        # Debemos tener en cuentra procesar los paréntesis primero
        # como está recorriendo al revés buscamos primero el ")"
        if caracter == ")":
            parentesis_cerrado += 1
            
        # luego vamos contando los parentesis abiertos
        elif caracter == "(":
            parentesis_abierto += 1
            
        # caso en el que venga un operador, lo guardamos y empezamos a cargar el siguiente operando
        elif caracter in lista_operadores and not band:
            print(parentesis_abierto)
            print(parentesis_cerrado)    
            print("se encuentra operador")
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
    # el 2do operando podría ser vacío (Ej: a*)
    # else:
    else:
        print("op1: {} operador: {} ".format(evaluar_entrada_rec(op2[::-1]),operador))
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
    # primero debemos dividir la entrada en operandos
    for terminal in terminales:
        print(terminal)
        evaluar_entrada_rec(terminal)

main()