import json

### Este script elimina los parentesis en el apartado de rating


# Cargar el archivo JSON
with open('anime_db_filtrado.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Modificar la sección de calificaciones
for entry in data:
    rating = entry['Rating']
    score = rating.split(' ')[0]  # Separa la puntuación y el número de votos, y toma solo la puntuación
    entry['Rating'] = score

# Guardar los cambios en el archivo JSON
with open('anime_db_filtrado_modificado.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("Archivo modificado con éxito.")
