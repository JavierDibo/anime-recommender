import json
from datetime import datetime

### Este script filtra las entradas de anime_db.json y genera un archivo filtrado
### eliminando todas las entradas con rating menor a 5.00 y fecha anterior a 2010


def filtrar_animes(archivo_entrada, archivo_salida, anio_limite, rating_minimo):
    # Cargar los datos del archivo JSON
    with open(archivo_entrada, 'r', encoding='utf-8') as archivo:
        animes = json.load(archivo)

    # Filtrar animes que cumplen con los criterios de fecha y rating
    animes_filtrados = []
    for anime in animes:
        fecha_str = anime['Aired']
        rating_str = anime['Rating'].split(' ')[0]  # Obtener solo el número del rating

        try:
            # Convertir el rating a un número flotante
            rating = float(rating_str)
        except ValueError:
            # Si el rating no se puede convertir a flotante, ignorar la entrada
            continue

        try:
            # Intentar convertir la fecha a un objeto datetime
            fecha = datetime.strptime(fecha_str, '%d.%m.%Y')
            if fecha.year >= anio_limite and rating >= rating_minimo:
                animes_filtrados.append(anime)
        except ValueError:
            # Si la fecha no tiene el formato esperado, ignorar la entrada
            continue

    # Guardar los datos filtrados en un nuevo archivo JSON
    with open(archivo_salida, 'w', encoding='utf-8') as archivo:
        json.dump(animes_filtrados, archivo, ensure_ascii=False, indent=4)

# Usar la función para filtrar los animes
filtrar_animes('anime_db.json', 'anime_db_filtrado.json', 2010, 5.00)
