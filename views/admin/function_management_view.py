import tkinter as tk
from tkinter import ttk, messagebox
from Funciones import agregar_funcion, mostrar_funciones 
from Peliculas import mostrar_peliculas

class FunctionManagementPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Gestión de Funciones - Cine-DB")

        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(top_frame, text="Agregar Función", command=self.open_create_function_window).pack(side="left", padx=5)
        ttk.Button(top_frame, text="Refrescar", command=self.load_functions).pack(side="right", padx=5)

        self.tree = ttk.Treeview(self, columns=("Película", "Sala", "Horario", "Asientos", "Precio"), show="headings")
        self.tree.heading("Película", text="Película")
        self.tree.heading("Sala", text="Sala")
        self.tree.heading("Horario", text="Horario")
        self.tree.heading("Asientos", text="Asientos Disp.")
        self.tree.heading("Precio", text="Precio")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_functions()

        ttk.Button(self, text="< Volver al Panel", command=self.volver_al_dashboard).pack(pady=10)

    def load_functions(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        functions_list = mostrar_funciones(return_list=True)
        if functions_list:
            for func in functions_list:
            
                nombre_pelicula = func.get('pelicula_titulo') or func.get('pelicula') or "Desconocida"
                
                try:
                    precio_formateado = f"${float(func.get('precio', 0)):.2f}"
                except (ValueError, TypeError):
                    precio_formateado = f"${func.get('precio')}"

                self.tree.insert("", "end", values=(
                    nombre_pelicula,
                    func.get('sala'),
                    func.get('horario'),
                    func.get('asientos_disponibles'),
                    precio_formateado
                ))

    def open_create_function_window(self):
        CreateFunctionWindow(self)

    def volver_al_dashboard(self):
        from .admin_dashboard_view import AdminDashboard
        self.master.switch_frame(AdminDashboard)


class CreateFunctionWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Agregar Función")
        self.geometry("300x320")
        self.transient(master)
        self.grab_set()

        ttk.Label(self, text="Película:").pack(pady=(10,0))
        
        peliculas_db = mostrar_peliculas(return_list=True)
        movie_titles = [p['titulo'] for p in peliculas_db] if peliculas_db else []
        
        self.pelicula_combo = ttk.Combobox(self, values=movie_titles, state="readonly")
        self.pelicula_combo.pack()
        if movie_titles:
            self.pelicula_combo.current(0) 

        ttk.Label(self, text="Sala:").pack(pady=(10,0))
        self.sala_entry = ttk.Entry(self)
        self.sala_entry.pack()

        ttk.Label(self, text="Horario (HH:MM):").pack(pady=(10,0))
        self.horario_entry = ttk.Entry(self)
        self.horario_entry.pack()

        ttk.Label(self, text="Cantidad de Asientos:").pack(pady=(10,0))
        self.asientos_entry = ttk.Entry(self)
        self.asientos_entry.pack()

        ttk.Label(self, text="Precio:").pack(pady=(10,0))
        self.precio_entry = ttk.Entry(self)
        self.precio_entry.pack()

        ttk.Button(self, text="Agregar", command=self.create_function_action).pack(pady=20)

    def create_function_action(self):
        pelicula = self.pelicula_combo.get()
        sala = self.sala_entry.get().strip()
        horario = self.horario_entry.get().strip()
        asientos = self.asientos_entry.get().strip()
        precio = self.precio_entry.get().strip()

        if not all([pelicula, sala, horario, asientos, precio]):
            messagebox.showerror("Error", "Todos los campos son requeridos", parent=self)
            return

        result = agregar_funcion(pelicula, sala, horario, asientos, precio)
        
        if "correctamente" in result.lower() or "éxito" in result.lower():
            messagebox.showinfo("Éxito", result, parent=self)
            self.master.load_functions()
            self.destroy()
        else:
            messagebox.showerror("Error", result, parent=self)