import sys
from views.main_window import App

def main():

    try:
        print("Iniciando aplicación Cine-DB...")
        app = App()
        app.mainloop()
    except Exception as e:
        print(f"Error crítico al iniciar la aplicación: {e}")
        input("Presione Enter para salir...")
        sys.exit(1)

if __name__ == "__main__":
    main()
