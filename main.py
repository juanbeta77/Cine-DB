from Usuarios import *
from Peliculas import *
from Funciones import *
from Entradas import *


while True:

    print("""
========= SISTEMA CINE =========

USUARIOS
1. Crear usuario
2. Mostrar usuarios
3. Actualizar usuario
4. Eliminar usuario

PELICULAS
5. Agregar pelicula
6. Mostrar peliculas

FUNCIONES
7. Agregar funcion
8. Mostrar funciones

ENTRADAS
9. Comprar entrada
10. Mostrar entradas

0. Salir
""")

    opcion = input("Seleccione una opcion: ")


    if opcion == "1":
        crear_usuario()

    elif opcion == "2":
        mostrar_usuarios()

    elif opcion == "3":
        actualizar_usuario()

    elif opcion == "4":
        eliminar_usuario()

    elif opcion == "5":
        agregar_pelicula()

    elif opcion == "6":
        mostrar_peliculas()

    elif opcion == "7":
        agregar_funcion()

    elif opcion == "8":
        mostrar_funciones()

    elif opcion == "9":
        comprar_entrada()

    elif opcion == "10":
        mostrar_entradas()

    elif opcion == "0":
        print("Saliendo...")
        break

    else:
        print("Opcion invalida")