import random
from collections import Counter

def distancia(texto1, texto2):
    """Calcula la distancia de Hamming entre dos textos."""
    return sum(c1 != c2 for c1, c2 in zip(texto1, texto2))

def construir_solucion_greedy_random(textos, m):
    """Construye una solución inicial de manera greedy con algo de aleatoriedad."""
    solucion = []
    for i in range(m):
        # Contar la frecuencia de cada caracter en la posición i
        contador = Counter(texto[i] for texto in textos)
        # Crear una lista de candidatos (caracteres más comunes)
        max_frecuencia = max(contador.values())
        candidatos = [caracter for caracter, frecuencia in contador.items() if frecuencia == max_frecuencia]
        # Seleccionar aleatoriamente un caracter de los candidatos
        solucion.append(random.choice(candidatos))
    return ''.join(solucion)

def mejora_local(solucion, textos, m):
    """Mejora la solución utilizando búsqueda local."""
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
    """Procedimiento principal de GRASP."""
    mejor_solucion_global = None
    mejor_distancia_global = float('inf')
    
    for _ in range(max_iteraciones):
        # Fase constructiva (Greedy + Random)
        solucion_inicial = construir_solucion_greedy_random(textos, m)
        # Fase de mejora local
        solucion_mejorada = mejora_local(solucion_inicial, textos, m)
        # Evaluar la solución mejorada
        distancia_solucion = sum(distancia(solucion_mejorada, texto) for texto in textos)
        if distancia_solucion < mejor_distancia_global:
            mejor_distancia_global = distancia_solucion
            mejor_solucion_global = solucion_mejorada
    
    return mejor_solucion_global

def leer_textos_de_archivo(ruta_archivo):
    """Lee los textos desde un archivo y devuelve una lista de textos."""
    with open(ruta_archivo, 'r') as archivo:
        textos = [linea.strip() for linea in archivo.readlines()]
    return textos

def calcular_distancias(texto, textos):
    """Calcula las distancias entre el texto y una lista de textos."""
    distancias = [(distancia(texto, t), t) for t in textos]
    distancia_maxima, texto_maxima = max(distancias, key=lambda x: x[0])
    distancia_minima, texto_minima = min(distancias, key=lambda x: x[0])
    return distancia_maxima, texto_maxima, distancia_minima, texto_minima

# Ejemplo de uso
ruta_archivo = 'textos_32_100.txt'  # Cambia esto por la ruta a tu archivo de textos
textos = leer_textos_de_archivo(ruta_archivo)
m = len(textos[0])  # Asumimos que todos los textos tienen la misma longitud
max_iteraciones = 150

mejor_texto = grasp(textos, m, max_iteraciones)
distancia_maxima, texto_maxima, distancia_minima, texto_minima = calcular_distancias(mejor_texto, textos)

print(f"El mejor texto encontrado es: {mejor_texto}")
print(f"La mayor distancia encontrada es: {distancia_maxima}")
print(f"El texto con mayor distancia es: {texto_maxima}")
print(f"La menor distancia encontrada es: {distancia_minima}")
print(f"El texto con menor distancia es: {texto_minima}")

# Pausar la consola
input("Presiona Enter para salir...")