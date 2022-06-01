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

def evaluar_entrada_rec(expresion):
# evaluamos la entrada y vamos dividiendo en operadores y operandos de forma recursiva
    # Caso Base: si la expresión es un caracter diferente a la lista de operadores de Thompson
    if expresion not in lista_operadores and len(expresion) == 1:
        print(expresion)
        return expresion
    # dividimos la expresión en operandos y operador
    op1 = op2 = operador = ""
    band = False
    # para cada caracter recorremos en reversa porque las operaciones deben hacerse de izquierda a derecha
    for caracter in expresion[::-1]:
        print("entra aca: {}".format(caracter))
        if caracter in lista_operadores and not band:
            print("y aqui jeje")
            # si no tenemos primer operando y recibimos el operador entonces es un error
            # if op1 == "":
            #     print("ERROR: asegurese de que su expresión regular esté bien definida")
            operador = caracter
            band = True
            continue
        # mientras la bandera esté apagada estaremos cargando el primer operando
        if band: 
            op1 = op1 + caracter
        # caso contrario vamos cargando el segundo operando
        else:
            op2 = op2 + caracter
    # evaluamos y desarmamos cada expresion
    if op2 != "":
        print("op1: {} operador: {} op2: {}".format(evaluar_entrada_rec(op1[::-1]),operador,evaluar_entrada_rec(op2)))
    # el 2do operando podría ser vacío (Ej: a*)
    else:
        print("op1: {} operador: {} ".format(evaluar_entrada_rec(op1[::-1]),operador))
    return expresion
    


def main():
    print("Bienvenido al analizador léxico")
    
    # 1. Definir el lenguaje de entrada. Ingresar definición regular
    print("Por favor ingrese una expresión regular (FIN para terminar)")
    entrada = input()
     # se ingresaran expresiones mientras el terminal sea diferente a FIN
    while entrada!= "FIN":
        print("La expresión ingresada es "+entrada)
        # dividimos en lado derecho e izquierdo con split
        expresion = entrada.split("->")
        # agregamos a la lista el no terminal
        noTerminales.append(expresion[0])
        print("No terminal: {}".format(noTerminales[0]))
        terminales.append(expresion[1])
        print("ingrese la siguiente expresión:")
        entrada = input()

    # 2. Crear el AFN con Thompson
    # primero debemos dividir la entrada en operandos
    for terminal in terminales:
        print(terminal)
        evaluar_entrada_rec(terminal)

main()