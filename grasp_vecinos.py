import random
from collections import Counter

def distancia(texto1, texto2):
    # Función para calcular la distancia entre dos textos
    return sum(1 for a, b in zip(texto1, texto2) if a != b)

def leer_textos_de_archivo(ruta_archivo):
    # Lee los textos desde un archivo y devuelve una lista de textos
    with open(ruta_archivo, 'r') as archivo:
        textos = [linea.strip() for linea in archivo.readlines()]
    return textos

def construir_solucion_greedy_random(textos, m):
    # Función para construir una solución inicial de manera greedy con algo de aleatoriedad
    solucion = []
    for i in range(m):
        contador = Counter(texto[i] for texto in textos)
        max_frecuencia = max(contador.values())
        candidatos = [caracter for caracter, frecuencia in contador.items() if frecuencia == max_frecuencia]
        solucion.append(random.choice(candidatos))
    return ''.join(solucion)

def generar_vecindad_cambio_caracter(solucion_actual, textos):
    # Genera todas las soluciones vecinas cambiando un solo carácter en la solución actual
    vecindad = []
    m = len(solucion_actual)
    for i in range(m):
        for caracter in set(caracter for texto in textos for caracter in texto):
            if caracter != solucion_actual[i]:
                vecino = solucion_actual[:i] + caracter + solucion_actual[i+1:]
                vecindad.append(vecino)
    return vecindad

def generar_vecindad_permutar_caracteres(solucion_actual):
    # Genera todas las soluciones vecinas permutando dos caracteres adyacentes en la solución actual
    vecindad = []
    m = len(solucion_actual)
    for i in range(m - 1):
        vecino = solucion_actual[:i] + solucion_actual[i+1] + solucion_actual[i] + solucion_actual[i+2:]
        vecindad.append(vecino)
    return vecindad

def mejora_local_con_vecindades(solucion, textos, m, max_iter_vecindad):
    # Mejora la solución utilizando búsqueda local con dos vecindades diferentes
    mejor_solucion = solucion
    mejor_distancia = sum(distancia(solucion, texto) for texto in textos)
    iteraciones_vecindad_actual = 0
    cambiar_a_vecindad_permutacion = False
    
    while iteraciones_vecindad_actual < max_iter_vecindad:
        if cambiar_a_vecindad_permutacion:
            vecindad = generar_vecindad_permutar_caracteres(mejor_solucion)
        else:
            vecindad = generar_vecindad_cambio_caracter(mejor_solucion, textos)
        
        for vecino in vecindad:
            nueva_distancia = sum(distancia(vecino, texto) for texto in textos)
            if nueva_distancia < mejor_distancia:
                mejor_distancia = nueva_distancia
                mejor_solucion = vecino
        
        iteraciones_vecindad_actual += 1
        if iteraciones_vecindad_actual == max_iter_vecindad // 2:
            cambiar_a_vecindad_permutacion = True
    
    return mejor_solucion, mejor_distancia

def grasp_con_vecindades(textos, m, max_iteraciones, max_iter_vecindad):
    # Implementación de GRASP con exploración de vecindades en la mejora local
    mejor_solucion_global = None
    mejor_distancia_global = float('inf')
    solucion_con_mayor_distancia = None
    mayor_distancia_encontrada = 0
    
    for i in range(max_iteraciones):
        solucion_inicial = construir_solucion_greedy_random(textos, m)
        solucion_mejorada, distancia_mejorada = mejora_local_con_vecindades(solucion_inicial, textos, m, max_iter_vecindad)
        
        if distancia_mejorada < mejor_distancia_global:
            mejor_distancia_global = distancia_mejorada
            mejor_solucion_global = solucion_mejorada
        
        if distancia_mejorada > mayor_distancia_encontrada:
            mayor_distancia_encontrada = distancia_mejorada
            solucion_con_mayor_distancia = solucion_mejorada
        
        print(f"Iteración {i+1}: Mejor distancia encontrada = {mejor_distancia_global}")
    
    return mejor_solucion_global, mejor_distancia_global, solucion_con_mayor_distancia, mayor_distancia_encontrada

# Ejemplo de uso
if __name__ == "__main__":
    # Definir parámetros del ejemplo
    ruta_archivo = 'texto_mas_parecido_10_300_1.txt'  # Cambia esto por la ruta a tu archivo de textos
    textos = leer_textos_de_archivo(ruta_archivo)
    m = len(textos[0])
    max_iteraciones = 100
    max_iter_vecindad = 25
    
    # Ejecutar el algoritmo GRASP con vecindades
    mejor_solucion, mejor_distancia, solucion_con_mayor_distancia, mayor_distancia_encontrada = grasp_con_vecindades(textos, m, max_iteraciones, max_iter_vecindad)
    
    print(f"\nMejor solución encontrada: {mejor_solucion}")
    print(f"Mejor distancia encontrada: {mejor_distancia}")
    print(f"Solución con mayor distancia encontrada ({mayor_distancia_encontrada}): {solucion_con_mayor_distancia}")