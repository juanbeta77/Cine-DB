import tkinter as tk
from tkinter import ttk, messagebox
from conexion import db
from bson.objectid import ObjectId

class PreferencesWindow(tk.Toplevel):
    def __init__(self, parent, user_data):
        super().__init__(parent)
        self.title("Mis Preferencias de Cine")
        self.geometry("300x250")
        self.user_data = user_data
        self.user_id = user_data.get('_id')
        self.parent = parent 

        self.transient(parent)
        self.grab_set()

        tk.Label(self, text="Selecciona tus géneros favoritos", font=("Arial", 11, "bold")).pack(pady=10)

        self.generos = ["Acción", "Comedia", "Drama", "Terror", "Ciencia Ficción", "Animación"]
        self.variables = {}

        preferencias_actuales = user_data.get("preferencias", [])

        for genero in self.generos:
            var = tk.BooleanVar(value=(genero in preferencias_actuales))
            self.variables[genero] = var
            chk = ttk.Checkbutton(self, text=genero, variable=var)
            chk.pack(anchor="w", padx=40, pady=2)

        ttk.Button(self, text="Guardar Preferencias", command=self.guardar_preferencias).pack(pady=15)

    def guardar_preferencias(self):
        generos_seleccionados = [genero for genero, var in self.variables.items() if var.get()]

        try:
            db["usuarios"].update_one(
                {"_id": ObjectId(str(self.user_id))},
                {"$set": {"preferencias": generos_seleccionados}}
            )

            self.user_data["preferencias"] = generos_seleccionados
            
            messagebox.showinfo("Éxito", "Preferencias actualizadas correctamente.", parent=self)
            
            if hasattr(self.parent, "recargar_datos_perfil"):
                self.parent.recargar_datos_perfil()

            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar las preferencias: {e}", parent=self)