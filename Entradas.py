from conexion import db

entradas = db["entradas"]
funciones = db["funciones"]


def comprar_entrada():

    pelicula = input("Pelicula: ")
    horario = input("Horario: ")
    cantidad = int(input("Cantidad entradas: "))
    usuario = input("Nombre usuario: ")

    funcion = funciones.find_one({
        "pelicula": pelicula,
        "horario": horario
    })

    if funcion:

        if funcion["asientos_disponibles"] >= cantidad:

            total = cantidad * funcion["precio"]

            entrada = {
                "usuario": usuario,
                "pelicula": pelicula,
                "horario": horario,
                "cantidad": cantidad,
                "total": total
            }

            entradas.insert_one(entrada)

            nuevos_asientos = funcion["asientos_disponibles"] - cantidad

            funciones.update_one(
                {
                    "pelicula": pelicula,
                    "horario": horario
                },
                {
                    "$set": {
                        "asientos_disponibles": nuevos_asientos
                    }
                }
            )

            print(f"""
Compra realizada correctamente
Total pagado: {total}
""")

        else:
            print("No hay suficientes asientos")

    else:
        print("Funcion no encontrada")


def mostrar_entradas():

    print("\nLISTA DE ENTRADAS\n")

    for entrada in entradas.find():

        print(f"""
Usuario: {entrada['usuario']}
Pelicula: {entrada['pelicula']}
Horario: {entrada['horario']}
Cantidad: {entrada['cantidad']}
Total: {entrada['total']}
""")