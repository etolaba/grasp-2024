import random
from collections import Counter
import time
import math

def distancia(texto1, texto2):
    return sum(1 for a, b in zip(texto1, texto2) if a != b)

def construir_solucion_greedy_random(textos, m, alfabeto):
    solucion = []
    # Calculo el 30% del tamaño del alfabeto, redondeado hacia arriba, esto con el objetivo de no usar todas
    # las letras en caso de que el alfabeto sea muy extenso
    n = math.ceil(len(alfabeto) * 0.3)  
    
    for i in range(m):
        contador = Counter(texto[i] for texto in textos)
        # Ordeno los caracteres por frecuencia en orden descendente
        caracteres_ordenados = sorted(contador.items(), key=lambda x: x[1], reverse=True)
        # Selecciono los n caracteres más frecuentes
        candidatos = [caracter for caracter, _ in caracteres_ordenados[:n]]
        # Selecciono aleatoriamente un caracter de los candidatos
        solucion.append(random.choice(candidatos))
    
    return ''.join(solucion)

def mejora_local(solucion, textos, m, caracteres_por_posicion):
    mejor_solucion = solucion
    mejor_distancias = [distancia(solucion, texto) for texto in textos]
    mejor_distancia_maxima = max(mejor_distancias)
    
    iteraciones_sin_mejora = 0
    k = math.ceil(m * 0.3)
    
    for i in range(m):
        # Itero solo sobre los caracteres en esa posición
        for caracter in caracteres_por_posicion[i]:
            if caracter != mejor_solucion[i]:
                # Inserto el nuevo caracter distinto en la posición que estoy iterando
                nueva_solucion = mejor_solucion[:i] + caracter + mejor_solucion[i+1:]
                nueva_distancias = mejor_distancias[:]
                nueva_distancia_maxima = -1
                
                for idx, texto in enumerate(textos):
                    # Si la distancia cambia en la posición i, recalculamos la distancia total para ese texto
                    if mejor_solucion[i] != texto[i] and caracter == texto[i]:
                        nueva_distancias[idx] -= 1
                    elif mejor_solucion[i] == texto[i] and caracter != texto[i]:
                        nueva_distancias[idx] += 1
                    
                    # Actualizo la distancia máxima encontrada hasta el momento
                    dist_nueva = nueva_distancias[idx]
                    if dist_nueva > nueva_distancia_maxima:
                        nueva_distancia_maxima = dist_nueva
                
                # Verifico si la nueva solución mejora la mejor distancia máxima encontrada
                if nueva_distancia_maxima < mejor_distancia_maxima:
                    mejor_distancia_maxima = nueva_distancia_maxima
                    mejor_solucion = nueva_solucion
                    mejor_distancias = nueva_distancias
                    iteraciones_sin_mejora = 0
                else:
                    iteraciones_sin_mejora += 1
                
                # Termino si no se encuentra mejora después de k iteraciones
                if iteraciones_sin_mejora >= k:
                    return mejor_solucion
    
    return mejor_solucion

def grasp(textos, m, alfabeto, caracteres_por_posicion, archivo_salida):
    mejor_solucion_global = None
    mejor_maxima_distancia_global = float('inf')
    
    max_iteraciones_prima = calcular_max_iteraciones(len(textos), m)

    tiempo_inicio = time.time()
    
    for i in range(max_iteraciones_prima):
        solucion_inicial = construir_solucion_greedy_random(textos, m, alfabeto)
        solucion_mejorada = mejora_local(solucion_inicial, textos, m, caracteres_por_posicion)
        
        distancias = [distancia(solucion_mejorada, texto) for texto in textos]
        maxima_distancia = max(distancias)
        
        if maxima_distancia < mejor_maxima_distancia_global:
            mejor_maxima_distancia_global = maxima_distancia
            mejor_solucion_global = solucion_mejorada
            
    with open(archivo_salida, 'w') as archivo:
        archivo.write(f"{mejor_solucion_global}\n")       
        archivo.write(f"{mejor_maxima_distancia_global}\n")
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

def obtener_caracteres_por_posicion(textos, m):
    caracteres_por_posicion = []
    for i in range(m):
        caracteres_por_posicion.append(set(texto[i] for texto in textos))
    return caracteres_por_posicion

def calcular_max_iteraciones(n, m):
    k = 0.0035 # Este es un número que saqué en base a diversas pruebas para las instancias con longitud 
    # 300, 500 y 700, con n que varía de 10 a 20, considero que el resultado es un número de iteraciones
    # muy cercano al ideal para esos n y m variables
    max_iteraciones = int(k * n * m)
    if max_iteraciones < 1:
        return 15
    # Este número es solo por si las instancias de n y m son algo pequeñas, como para las instancias con
    # alfabeto más extenso
    else:
        return math.ceil(max_iteraciones)

# Uso
ruta_archivo = 'texto_mas_parecido_15_700_3.txt'
textos = leer_textos_de_archivo(ruta_archivo)
m = len(textos[0])
alfabeto = obtener_alfabeto(textos)
caracteres_por_posicion = obtener_caracteres_por_posicion(textos, m)
archivo_salida = 'mejor_solucion.txt'

mejor_texto = grasp(textos, m, alfabeto, caracteres_por_posicion, archivo_salida)
distancia_maxima, texto_maxima, distancia_minima, texto_minima = calcular_distancias(mejor_texto, textos)

print(f"El mejor texto encontrado es: {mejor_texto}")
print(f"La mayor distancia encontrada es: {distancia_maxima}")
print(f"El texto con mayor distancia es: {texto_maxima}")
print(f"La menor distancia encontrada es: {distancia_minima}")
print(f"El texto con menor distancia es: {texto_minima}")