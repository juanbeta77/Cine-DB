from Usuarios import *
from Peliculas import *
from Funciones import *
from Entradas import *


print("""
========= LOGIN =========

1. Administrador
2. Usuario
""")

tipo = input("Seleccione acceso: ")


# ======================================
# ADMINISTRADOR
# ======================================

if tipo == "1":

    admin_user = input("Usuario admin: ")
    admin_pass = input("Contraseña: ")

    if admin_user == "admin" and admin_pass == "1234":

        print("\nAcceso administrador correcto")

        while True:

            print("""
========= ADMINISTRADOR =========

========= USUARIOS =========
1. Crear usuario
2. Mostrar usuarios
3. Actualizar usuario
4. Eliminar usuario

========= PELICULAS =========
5. Agregar pelicula
6. Mostrar peliculas
7. Actualizar pelicula
8. Eliminar pelicula

========= FUNCIONES =========
9. Agregar funcion
10. Mostrar funciones

========= ENTRADAS =========
11. Mostrar entradas

========= REPORTES =========
12. Total ventas

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
                actualizar_pelicula()

            elif opcion == "8":
                eliminar_pelicula()

            elif opcion == "9":
                agregar_funcion()

            elif opcion == "10":
                mostrar_funciones()

            elif opcion == "11":
                mostrar_entradas()

            elif opcion == "12":
                total_ventas()

            elif opcion == "0":
                print("Saliendo...")
                break

            else:
                print("Opcion invalida")

    else:
        print("Credenciales admin incorrectas")



# ======================================
# USUARIO
# ======================================

elif tipo == "2":

    usuario_logueado = login_usuario()

    if usuario_logueado:

        while True:

            print("""
========= USUARIO =========

1. Ver peliculas
2. Ver funciones
3. Comprar entrada
4. Ver historial compras

0. Salir
""")

            opcion = input("Seleccione una opcion: ")

            if opcion == "1":
                mostrar_peliculas()

            elif opcion == "2":
                mostrar_funciones()

            elif opcion == "3":
                comprar_entrada()

            elif opcion == "4":
                ver_historial_compras()

            elif opcion == "0":
                print("Saliendo...")
                break

            else:
                print("Opcion invalida")

    else:
        print("No fue posible iniciar sesion")


else:
    print("Opcion invalida")