from conexion import db
from datetime import datetime

entradas = db["Entradas"]
funciones = db["Funciones"]


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
                "total": total,
                "fecha_compra": datetime.now()
            }

            entradas.insert_one(entrada)  
            usuarios = db["usuarios"]

            usuarios.update_one(
                {"nombre": usuario},
                {
                    "$push": {
                        "historial_compras": {
                            "pelicula": pelicula,
                            "cantidad": cantidad,
                            "total": total,
                            "fecha": datetime.now()
                        }
                    }
                }
            )

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
======== RECIBO ========

Usuario: {usuario}
Pelicula: {pelicula}
Horario: {horario}
Cantidad entradas: {cantidad}
Total pagado: {total}

========================
""")
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
        
def total_ventas():

    total = 0

    for entrada in entradas.find():
        total += entrada["total"]

    print(f"Total vendido: {total}")