import random
from collections import Counter

def distancia(texto1, texto2):
    diferencia = 0

    for i in range(len(texto1)):
        if texto1[i] != texto2[i]:
            diferencia += 1

    return diferencia

def construir_solucion_greedy_random(textos, m):
    solucion = [] 

    for i in range(m):
        # Contar la frecuencia de cada caracter en la posición i
        contador = Counter()
        for texto in textos:
            caracter = texto[i]
            if caracter in contador:
                contador[caracter] += 1
            else:
                contador[caracter] = 1

        # Encontrar la frecuencia máxima
        max_frecuencia = max(contador.values())

        # Crear una lista de candidatos (caracteres más comunes)
        candidatos = []
        for caracter, frecuencia in contador.items():
            if frecuencia == max_frecuencia:
                candidatos.append(caracter)

        # Seleccionar aleatoriamente un caracter de los candidatos
        elegido = random.choice(candidatos)
        solucion.append(elegido)

    return ''.join(solucion)

def mejora_local(solucion, textos, m):
    mejor_solucion = solucion
    mejor_distancia = sum(distancia(solucion, texto) for texto in textos)
    
    for i in range(m):
        # Probar cambiar el caracter en la posición i por cada caracter posible
        for caracter in set(caracter for texto in textos for caracter in texto):
            if caracter != mejor_solucion[i]:
                nueva_solucion = mejor_solucion[:i] + caracter + mejor_solucion[i+1:]
                nueva_distancia = sum(distancia(nueva_solucion, texto) for texto in textos)
                if nueva_distancia < mejor_distancia:
                    mejor_distancia = nueva_distancia
                    mejor_solucion = nueva_solucion
    return mejor_solucion

def grasp(textos, m, max_iteraciones):
    
    mejor_solucion_global = None
    mejor_maxima_distancia_global = float('inf')
    mejor_minima_distancia_global = float('inf')
    texto_maxima_distancia_global = ""
    texto_minima_distancia_global = ""

    for iteracion in range(max_iteraciones):
        
        solucion_inicial = construir_solucion_greedy_random(textos, m)
        
        solucion_mejorada = mejora_local(solucion_inicial, textos, m)
        
        # Calcular distancias para la solución mejorada
        distancias = [distancia(solucion_mejorada, texto) for texto in textos]
        max_distancia = max(distancias)
        min_distancia = min(distancias)
        
        if max_distancia < mejor_maxima_distancia_global:
            mejor_maxima_distancia_global = max_distancia
            texto_maxima_distancia_global = textos[distancias.index(max_distancia)]
        
        if min_distancia < mejor_minima_distancia_global:
            mejor_minima_distancia_global = min_distancia
            texto_minima_distancia_global = textos[distancias.index(min_distancia)]
            mejor_solucion_global = solucion_mejorada

        print(f"Iteración {iteracion + 1}: Menor distancia encontrada: {mejor_minima_distancia_global}")

    print(f"Mejor solución encontrada: {mejor_solucion_global}")
    print(f"Mayor distancia encontrada: {mejor_maxima_distancia_global}")
    print(f"Texto a mayor distancia: {texto_maxima_distancia_global}")
    print(f"Menor distancia encontrada: {mejor_minima_distancia_global}")
    print(f"Texto a menor distancia: {texto_minima_distancia_global}")

    return mejor_solucion_global

def leer_textos_de_archivo(ruta_archivo):
    """Lee los textos desde un archivo y devuelve una lista de textos."""
    with open(ruta_archivo, 'r') as archivo:
        textos = [linea.strip() for linea in archivo.readlines()]
    return textos

# Uso de instancia
ruta_archivo = 'texto_mas_parecido_10_300_1.txt'
textos = leer_textos_de_archivo(ruta_archivo)
m = len(textos[0]) 
max_iteraciones = 100

mejor_texto = grasp(textos, m, max_iteraciones)