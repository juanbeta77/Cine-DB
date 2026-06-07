from bson.objectid import ObjectId
from conexion import db

peliculas = db["Peliculas"]

def agregar_pelicula(titulo, genero, duracion, clasificacion):
    existe = peliculas.find_one({"titulo": {"$regex": f"^{titulo}$", "$options": "i"}})

    if existe:
        return "La película ya existe"

    try:
        duracion_int = int(duracion)
    except ValueError:
        return "La duración debe ser un número entero."

    pelicula = {
        "titulo": titulo,
        "genero": genero,
        "duracion": duracion_int,
        "clasificacion": clasificacion,
        "disponible": True
    }

    peliculas.insert_one(pelicula)
    return "Pelicula agregada con éxito"


def mostrar_peliculas(return_list=False):
    print("\nLISTA DE PELICULAS\n")
    
    movies = list(peliculas.find({}))

    if return_list:
        return movies

    for pelicula in movies:
        print(f"""
            ID: {pelicula.get('_id')}
            Titulo: {pelicula.get('titulo')}
            Genero: {pelicula.get('genero')}
            Duracion: {pelicula.get('duracion')}
            Clasificacion: {pelicula.get('clasificacion')}
            Disponible: {pelicula.get('disponible')}
            """)


def actualizar_pelicula_por_id(id_o_titulo, nuevo_genero, nuevo_titulo=None):

    if len(str(id_o_titulo)) == 24 and not " " in str(id_o_titulo):
        try:
            obj_id = ObjectId(str(id_o_titulo))
            criterio = {"_id": obj_id}
        except Exception:
            criterio = {"titulo": id_o_titulo}
    else:
        criterio = {"titulo": id_o_titulo}

    campos_a_actualizar = {"genero": nuevo_genero}
    if nuevo_titulo:
        campos_a_actualizar["titulo"] = nuevo_titulo

    result = peliculas.update_one(criterio, {"$set": campos_a_actualizar})
    
    if result.modified_count > 0:
        return "Pelicula actualizada con éxito"
    else:
        return "Pelicula no encontrada o datos no modificados"


def eliminar_pelicula_por_id(id_o_titulo):

    if len(str(id_o_titulo)) == 24 and not " " in str(id_o_titulo):
        try:
            obj_id = ObjectId(str(id_o_titulo))
            criterio = {"_id": obj_id}
        except Exception:
            criterio = {"titulo": id_o_titulo}
    else:
        criterio = {"titulo": id_o_titulo}

    result = peliculas.delete_one(criterio)

    if result.deleted_count > 0:
        return "Pelicula eliminada con éxito"
    else:
        return "Pelicula no encontrada"

def get_pelicula_by_id(pelicula_id):
    
    try:
        return peliculas.find_one({"_id": ObjectId(str(pelicula_id))})
    except Exception as e:
        print(f"Error al obtener película por ID: {e}")
        return None