from conexion import db
from bson.objectid import ObjectId

funciones = db["Funciones"]
peliculas = db["Peliculas"] 

def agregar_funcion(titulo_pelicula, sala, horario, asientos, precio):
   
    peli_encontrada = peliculas.find_one({"titulo": {"$regex": f"^{titulo_pelicula}$", "$options": "i"}})
    
    if not peli_encontrada:
        return f"Error: La película '{titulo_pelicula}' no existe en la base de datos."
    
    obj_id_pelicula = peli_encontrada["_id"]

    try:
        sala_int = int(sala)
        asientos_int = int(asientos)
        precio_float = float(precio)
    except ValueError:
        return "Error: Sala, asientos y precio deben ser números válidos."

    if funciones.find_one({"pelicula_id": str(obj_id_pelicula), "sala": sala_int, "horario": horario}):
        return "Error: Ya existe una función para esa película, en esa sala y a ese horario."

    funcion = {
        "pelicula_id": str(obj_id_pelicula), 
        "sala": sala_int,
        "horario": horario,
        "asientos_disponibles": asientos_int,
        "precio": precio_float
    }

    funciones.insert_one(funcion)
    return "Funcion agregada correctamente"

def mostrar_funciones(return_list=False):
    functions_list = list(funciones.find({}))

    for funcion in functions_list:
        p_id = funcion.get('pelicula_id')
        pelicula = None
        
        if p_id:
            try:
                pelicula = peliculas.find_one({"_id": ObjectId(str(p_id))})
            except Exception:
                pass
            
            if not pelicula:
                pelicula = peliculas.find_one({"_id": str(p_id)})

        titulo_pelicula = pelicula['titulo'] if pelicula else "Desconocida"
        
        funcion['pelicula_titulo'] = titulo_pelicula
        funcion['pelicula'] = titulo_pelicula 

    if return_list:
        return functions_list

    print("\nLISTA DE FUNCIONES\n")
    for funcion in functions_list:
        print(f"""
                ID Función: {funcion.get('_id')}
                Pelicula: {funcion.get('pelicula_titulo')} (ID: {funcion.get('pelicula_id')})
                Sala: {funcion.get('sala')}
                Horario: {funcion.get('horario')}
                Asientos disponibles: {funcion.get('asientos_disponibles')}
                Precio: {funcion.get('precio')}
                """)


def get_funciones_disponibles():
    
    try:
        return list(funciones.find({"asientos_disponibles": {"$gt": 0}}))
    except Exception as e:
        print(f"Error al obtener funciones disponibles: {e}")
        return []


def get_funcion_by_id(funcion_id):
    
    try:
        return funciones.find_one({"_id": ObjectId(str(funcion_id))})
    except Exception as e:
        print(f"Error al obtener función por ID: {e}")
        return None