from conexion import db

usuarios = db["usuarios"]


def crear_usuario():

    nombre = input("Nombre: ")
    correo = input("Correo: ")
    telefono = input("Telefono: ")
    password = input("Contraseña: ")
    existe = usuarios.find_one({"correo": correo})

    if existe:
        print("El usuario ya existe")
        return


    usuario = {
        "nombre": nombre,
        "correo": correo,
        "telefono": telefono,
        "password": password,
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


def ver_historial_compras():

    nombre = input("Nombre usuario: ")

    usuario = usuarios.find_one({"nombre": nombre})

    if usuario:

        historial = usuario.get("historial_compras", [])

        print("\n===== HISTORIAL COMPRAS =====\n")

        if historial:

            for compra in historial:

                print(f"""
Pelicula: {compra['pelicula']}
Cantidad: {compra['cantidad']}
Total: {compra['total']}
Fecha: {compra['fecha']}
""")

        else:
            print("No hay compras registradas")

    else:
        print("Usuario no encontrado")    



def login_usuario():

    correo = input("Correo: ")
    password = input("Contraseña: ")

    usuario = usuarios.find_one({
        "correo": correo,
        "password": password
    })

    if usuario:

        print(f"\nBienvenido {usuario['nombre']}")

        return usuario

    else:
        print("Credenciales incorrectas")
        return None