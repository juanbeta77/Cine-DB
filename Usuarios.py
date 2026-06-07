from bson.objectid import ObjectId
from conexion import db

usuarios = db["usuarios"] 


def crear_usuario(documento, nombre, correo, telefono, password):
    if usuarios.find_one({"documento": str(documento)}):
        return "Error: Ya existe un usuario con ese documento de identidad"
        
    if usuarios.find_one({"correo": {"$regex": f"^{correo}$", "$options": "i"}}):
        return "El usuario ya existe con ese correo"

    usuario = {
        "documento": str(documento), 
        "nombre": nombre,
        "correo": correo,
        "telefono": telefono,
        "password": password,
        "preferencias": [],
        "historial_compras": []
    }
    usuarios.insert_one(usuario)
    return "Usuario creado con éxito"


def mostrar_usuarios(return_list=False):
    print("\nLISTA DE USUARIOS\n")
    
    users = list(usuarios.find({}, {"password": 0}))

    if return_list:
        return users

    for usuario in users:
        print(f"""
            ID: {usuario.get('_id')}
            Nombre: {usuario.get('nombre')}
            Correo: {usuario.get('correo')}
            Telefono: {usuario.get('telefono')}
            """)


def actualizar_usuario_por_documento(documento, nuevo_telefono, nuevo_correo):
    try:
        campos_a_actualizar = {}
        
        if nuevo_telefono: 
            campos_a_actualizar["telefono"] = nuevo_telefono
            
        if nuevo_correo: 
            campos_a_actualizar["correo"] = nuevo_correo

        resultado = db["usuarios"].update_one(
            {"documento": documento}, 
            {"$set": campos_a_actualizar}
        )
        
        if resultado.modified_count > 0:
            return "Usuario actualizado correctamente."
        return "El usuario existe pero no se realizaron cambios (los datos eran iguales)."
        
    except Exception as e:
        return f"Error en la base de datos: {e}"  

def eliminar_usuario_por_documento(documento):
    result = usuarios.delete_one({"documento": str(documento)})
    if result.deleted_count > 0:
        return "Usuario eliminado con éxito"
    else:
        return "Usuario no encontrado"

def obtener_historial_usuario(user_id):

    try:
        obj_id = ObjectId(str(user_id))
        usuario = usuarios.find_one({"_id": obj_id})
        
        if usuario:
            return usuario.get("historial_compras", [])
        return []
    except Exception as e:
        print(f"Error al obtener historial: {e}")
        return []


def login_usuario(correo, password):

    usuario = usuarios.find_one({
        "correo": correo,
        "password": password
    })

    if usuario:
        print(f"\nBienvenido {usuario['nombre']} (Desde Interfaz Gráfica)")
        
        usuario['id'] = usuario['_id'] 
        
        return usuario
    else:
        print("Credenciales incorrectas")
        return None