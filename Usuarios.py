from conexion import db

usuarios = db["usuarios"]


def crear_usuario():

    nombre = input("Nombre: ")
    correo = input("Correo: ")
    telefono = input("Telefono: ")

    usuario = {
        "nombre": nombre,
        "correo": correo,
        "telefono": telefono,
        "preferencias": [],
        "historial_compras": []
    }

    usuarios.insert_one(usuario)

    print("Usuario creado")


def mostrar_usuarios():

    print("\nLISTA DE USUARIOS\n")

    for usuario in usuarios.find():

        print(f"""
Nombre: {usuario['nombre']}
Correo: {usuario['correo']}
Telefono: {usuario['telefono']}
""")


def actualizar_usuario():

    correo = input("Correo del usuario: ")

    nuevo_telefono = input("Nuevo telefono: ")

    usuarios.update_one(
        {"correo": correo},
        {"$set": {"telefono": nuevo_telefono}}
    )

    print("Usuario actualizado")


def eliminar_usuario():

    correo = input("Correo del usuario: ")

    usuarios.delete_one({"correo": correo})

    print("Usuario eliminado")