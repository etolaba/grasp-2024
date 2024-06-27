import random
from collections import Counter
import time
import math

def distancia(texto1, texto2):
    return sum(1 for a, b in zip(texto1, texto2) if a != b)

def construir_solucion_greedy_random(textos, m, alfabeto):
    solucion = []
    n = math.ceil(len(alfabeto) * 0.3)  # Calculamos el 30% del tamaño del alfabeto, redondeado hacia arriba
    
    for i in range(m):
        contador = Counter(texto[i] for texto in textos)
        # Ordenar los caracteres por frecuencia en orden descendente
        caracteres_ordenados = sorted(contador.items(), key=lambda x: x[1], reverse=True)
        # Seleccionar los n caracteres más frecuentes
        candidatos = [caracter for caracter, _ in caracteres_ordenados[:n]]
        # Seleccionar aleatoriamente un caracter de los candidatos
        solucion.append(random.choice(candidatos))
    
    return ''.join(solucion)

def mejora_local(solucion, textos, m, alfabeto):
    mejor_solucion = solucion
    mejor_distancia = sum(distancia(solucion, texto) for texto in textos)
    
    for i in range(m):
        for caracter in alfabeto:
            if caracter != mejor_solucion[i]:
                nueva_solucion = mejor_solucion[:i] + caracter + mejor_solucion[i+1:]
                nueva_distancia = sum(distancia(nueva_solucion, texto) for texto in textos)
                if nueva_distancia < mejor_distancia:
                    mejor_distancia = nueva_distancia
                    mejor_solucion = nueva_solucion
    return mejor_solucion

def grasp(textos, m, max_iteraciones, alfabeto, archivo_salida):
    mejor_solucion_global = None
    mejor_maxima_distancia_global = float('inf')
    
    tiempo_inicio = time.time()
    
    with open(archivo_salida, 'w') as archivo:
        for i in range(max_iteraciones):
            solucion_inicial = construir_solucion_greedy_random(textos, m, alfabeto)
            solucion_mejorada = mejora_local(solucion_inicial, textos, m, alfabeto)
            
            distancias = [distancia(solucion_mejorada, texto) for texto in textos]
            maxima_distancia = max(distancias)
            
            if maxima_distancia < mejor_maxima_distancia_global:
                mejor_maxima_distancia_global = maxima_distancia
                mejor_solucion_global = solucion_mejorada
            
            archivo.write(f"{mejor_maxima_distancia_global}\n")
            print(f"Mejor maxima distancia en iteracion numero {i+1}: {mejor_maxima_distancia_global}")
    
    tiempo_final = time.time()
    tiempo_ejecucion = tiempo_final - tiempo_inicio
    print(f"Tiempo de ejecucion: {tiempo_ejecucion:.2f} segundos")
    
    return mejor_solucion_global

def leer_textos_de_archivo(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        textos = [linea.strip() for linea in archivo.readlines()]
    return textos

def calcular_distancias(texto, textos):
    distancias = [(distancia(texto, t), t) for t in textos]
    distancia_maxima, texto_maxima = max(distancias, key=lambda x: x[0])
    distancia_minima, texto_minima = min(distancias, key=lambda x: x[0])
    return distancia_maxima, texto_maxima, distancia_minima, texto_minima

def obtener_alfabeto(textos):
    return set(caracter for texto in textos for caracter in texto)

# Ejemplo de uso
ruta_archivo = 'texto_mas_parecido_15_500_1.txt'  # Cambia esto por la ruta a tu archivo de textos
textos = leer_textos_de_archivo(ruta_archivo)
m = len(textos[0])
max_iteraciones = 500
alfabeto = obtener_alfabeto(textos)
archivo_salida = 'distancias_por_iteracion.txt'

mejor_texto = grasp(textos, m, max_iteraciones, alfabeto, archivo_salida)
distancia_maxima, texto_maxima, distancia_minima, texto_minima = calcular_distancias(mejor_texto, textos)

print(f"El mejor texto encontrado es: {mejor_texto}")
print(f"La mayor distancia encontrada es: {distancia_maxima}")
print(f"El texto con mayor distancia es: {texto_maxima}")
print(f"La menor distancia encontrada es: {distancia_minima}")
print(f"El texto con menor distancia es: {texto_minima}")

# Considerar poner un punto de corte de acuerdo a la proporción de la mejora respecto a la mejor solución encontrada
# O bien un límite a la cantidad de iteraciones sobre la búsqueda local
# Documentar todo esto en el documento del algortimo y la entrega
# Considerar eliminar de la iteración en búsqueda local que tenga en cuenta una letra del alfabeto que no aparece en esa posición
# Volver a consultar dónde se generan los vecinos explicitamente en la mejora local
# Reconsiderar la forma en la que se mide la distancia para comparar una solución con la otra
# Considerar no mirar TOOODO el texto para medir nueva distancia en mejora local, del modo que lo estoy haciendo es batante costoso
# De igual a distinto, de distinto a distinto, o distinto a igual (?)

# NOTAS CLASE
# La solución es un string la m longitud de los textos dados