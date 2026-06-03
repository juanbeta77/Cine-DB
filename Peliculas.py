from conexion import db

peliculas = db["peliculas"]


def agregar_pelicula():

    titulo = input("Titulo: ")
    genero = input("Genero: ")
    duracion = int(input("Duracion: "))

    pelicula = {
        "titulo": titulo,
        "genero": genero,
        "duracion": duracion,
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
""")