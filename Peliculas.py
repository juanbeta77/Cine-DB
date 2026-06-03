from conexion import db

peliculas = db["Peliculas"]


def agregar_pelicula():

    titulo = input("Titulo: ")
    genero = input("Genero: ")
    duracion = int(input("Duracion: "))
    clasificacion = input("Clasificacion: ")

    existe = peliculas.find_one({"titulo": titulo})

    if existe:
        print("La pelicula ya existe")
        return


    pelicula = {
        "titulo": titulo,
        "genero": genero,
        "duracion": duracion,
        "clasificacion": clasificacion,
        "disponible": True
    }

    peliculas.insert_one(pelicula)

    print("Pelicula agregada")


def mostrar_peliculas():

    print("\nLISTA DE PELICULAS\n")

    for pelicula in peliculas.find():

        print(f"""
Titulo: {pelicula['titulo']}
Genero: {pelicula['genero']}
Duracion: {pelicula['duracion']}
Clasificacion: {pelicula['clasificacion']}
""")



def actualizar_pelicula():

    titulo = input("Titulo pelicula: ")

    nuevo_genero = input("Nuevo genero: ")

    peliculas.update_one(
        {"titulo": titulo},
        {
            "$set": {
                "genero": nuevo_genero
            }
        }
    )

    print("Pelicula actualizada")


def eliminar_pelicula():

    titulo = input("Titulo pelicula: ")

    peliculas.delete_one({"titulo": titulo})

    print("Pelicula eliminada")