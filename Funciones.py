from conexion import db

funciones = db["funciones"]


def agregar_funcion():

    pelicula = input("Nombre pelicula: ")
    sala = int(input("Sala: "))
    horario = input("Horario: ")
    asientos = int(input("Cantidad asientos: "))
    precio = float(input("Precio entrada: "))

    funcion = {
        "pelicula": pelicula,
        "sala": sala,
        "horario": horario,
        "asientos_disponibles": asientos,
        "precio": precio
    }

    funciones.insert_one(funcion)

    print("Funcion agregada correctamente")


def mostrar_funciones():

    print("\nLISTA DE FUNCIONES\n")

    for funcion in funciones.find():

        print(f"""
Pelicula: {funcion['pelicula']}
Sala: {funcion['sala']}
Horario: {funcion['horario']}
Asientos disponibles: {funcion['asientos_disponibles']}
Precio: {funcion['precio']}
""")