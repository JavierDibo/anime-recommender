import webbrowser
import json
from datetime import datetime
import random

def calcular_puntuacion(anime, anio_actual, max_rating):
    # Calcular la contribución de la recencia
    fecha_str = anime['Aired']
    try:
        fecha = datetime.strptime(fecha_str, '%d.%m.%Y')
        anios_diferencia = anio_actual - fecha.year
    except ValueError:
        anios_diferencia = float('inf')  # Si no hay fecha válida, se considera muy antiguo

    peso_recencia = 1 / (1 + anios_diferencia)  # Valor más alto para animes más recientes

    # Calcular la contribución del rating
    rating_str = anime['Rating'].split(' ')[0]
    try:
        rating = float(rating_str)
    except ValueError:
        rating = 0  # Si no hay rating válido, se considera como el más bajo

    peso_rating = rating / max_rating

    # Calcular la puntuación total
    puntuacion = 0.6 * peso_recencia + 0.4 * peso_rating
    return puntuacion

def recomendar_anime(archivo_json, anio_actual, max_rating):
    # Cargar los datos del archivo JSON
    with open(archivo_json, 'r', encoding='utf-8') as archivo:
        animes = json.load(archivo)

    # Calcular puntuaciones para cada anime
    puntuaciones = [(anime, calcular_puntuacion(anime, anio_actual, max_rating)) for anime in animes]

    # Ordenar animes por puntuación
    puntuaciones.sort(key=lambda x: x[1], reverse=True)

    # Elegir un anime al azar, con mayor probabilidad para puntuaciones más altas
    total_puntuaciones = sum(p[1] for p in puntuaciones)
    aleatorio = random.uniform(0, total_puntuaciones)
    acumulado = 0
    for anime, puntuacion in puntuaciones:
        acumulado += puntuacion
        if acumulado >= aleatorio:
            # Open a web browser tab with the anime name in Google Images
            anime_name = anime['Title']
            url = f"https://www.google.com/search?tbm=isch&q={anime_name.replace(' ', '+')}"
            webbrowser.open(url)
            return anime

    return None

# Usar la función para recomendar un anime
recomendado = recomendar_anime('anime_db_filtrado.json', 2023, 10)
print(recomendado)
