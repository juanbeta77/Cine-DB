from conexion import db
from datetime import datetime
from bson.objectid import ObjectId

entradas = db["Entradas"]
funciones = db["Funciones"]
usuarios = db["usuarios"]
peliculas = db["Peliculas"]

def comprar_entrada(user_id, funcion_id, cantidad, precio_total):
 
    try:
        obj_funcion_id = ObjectId(str(funcion_id))
        obj_user_id = ObjectId(str(user_id))
    except Exception:
        return "Error: Formato de ID inválido para la función o el usuario."

    funcion = funciones.find_one({"_id": obj_funcion_id})
    if not funcion:
        return "Error: La función seleccionada ya no existe."

    asientos_disponibles = funcion.get("asientos_disponibles", 0)
    if asientos_disponibles < cantidad:
        return f"Error: No hay suficientes asientos disponibles. Quedan {asientos_disponibles}."

    pelicula = peliculas.find_one({"_id": ObjectId(funcion["pelicula_id"])})
    titulo_pelicula = pelicula["titulo"] if pelicula else "Película Desconocida"

    usuario_doc = usuarios.find_one({"_id": obj_user_id})
    nombre_usuario = usuario_doc["nombre"] if usuario_doc else "Usuario Desconocido"

    entrada = {
        "usuario_id": str(obj_user_id),
        "usuario_nombre": nombre_usuario,
        "funcion_id": str(obj_funcion_id),
        "pelicula_titulo": titulo_pelicula,
        "horario": funcion.get("horario"),
        "sala": funcion.get("sala"),
        "cantidad": cantidad,
        "total": precio_total,
        "fecha_compra": datetime.now()
    }

    entradas.insert_one(entrada)  

    usuarios.update_one(
        {"_id": obj_user_id},
        {
            "$push": {
                "historial_compras": {
                    "entrada_id": str(entrada["_id"]),
                    "pelicula": titulo_pelicula,
                    "cantidad": cantidad,
                    "total": precio_total,
                    "fecha": datetime.now()
                }
            }
        }
    )

    nuevos_asientos = asientos_disponibles - cantidad
    funciones.update_one(
        {"_id": obj_funcion_id},
        {"$set": {"asientos_disponibles": nuevos_asientos}}
    )

    return "exito"


def mostrar_entradas(return_list=False):
    print("\nLISTA DE ENTRADAS\n")
    
    entradas_list = list(entradas.find({}))

    if return_list:
        return entradas_list

    for entrada in entradas_list:
        print(f"""
            Usuario: {entrada.get('usuario_nombre')}
            Pelicula: {entrada.get('pelicula_titulo')}
            Horario: {entrada.get('horario')}
            Sala: {entrada.get('sala')}
            Cantidad: {entrada.get('cantidad')}
            Total: {entrada.get('total')}
            """)
        

def obtener_historial_usuario(user_id):

    try:
        obj_user_id = ObjectId(str(user_id))
    except Exception:
        print("Error: El ID del usuario no tiene un formato válido.")
        return []

    try:
        usuario_doc = usuarios.find_one({"_id": obj_user_id}, {"historial_compras": 1})
        
        if usuario_doc and "historial_compras" in usuario_doc:
            historial = usuario_doc["historial_compras"]
            
            historial_limpio = []
            for item in historial:
                fecha_str = item.get("fecha")
                if isinstance(fecha_str, datetime):
                    fecha_str = fecha_str.strftime("%d/%m/%Y %H:%M")
                elif not fecha_str:
                    fecha_str = "N/A"

                historial_limpio.append({
                    "id_compra": item.get("entrada_id", "N/A"),
                    "pelicula": item.get("pelicula", "Sin Título"),
                    "sala": "-",  
                    "horario": "-", 
                    "cantidad": item.get("cantidad", 0),
                    "total": item.get("total", 0.0),
                    "fecha_compra": fecha_str
                })
            
            return list(reversed(historial_limpio))
            
        return []
    except Exception as e:
        print(f"Error al extraer historial del usuario: {e}")
        return []