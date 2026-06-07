import tkinter as tk
from tkinter import ttk, messagebox
from Peliculas import agregar_pelicula, mostrar_peliculas, actualizar_pelicula_por_id, eliminar_pelicula_por_id

class MovieManagementPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master.title("Gestión de Películas - Cine-DB")

        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(top_frame, text="Agregar Película", command=self.open_create_movie_window).pack(side="left", padx=5)
        ttk.Button(top_frame, text="Actualizar Película", command=self.open_update_movie_window).pack(side="left", padx=5)
        ttk.Button(top_frame, text="Eliminar Película", command=self.open_delete_movie_window).pack(side="left", padx=5)
        ttk.Button(top_frame, text="Refrescar", command=self.load_movies).pack(side="right", padx=5)

        self.tree = ttk.Treeview(self, columns=("Título", "Género", "Duración", "Clasificación"), show="headings")
        self.tree.heading("Título", text="Título")
        self.tree.heading("Género", text="Género")
        self.tree.heading("Duración", text="Duración (min)")
        self.tree.heading("Clasificación", text="Clasificación")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_movies()

        ttk.Button(self, text="< Volver al Panel", command=self.volver_al_dashboard).pack(pady=10)

    def load_movies(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        movies_list = mostrar_peliculas(return_list=True)
        if movies_list:
            for movie in movies_list:
                self.tree.insert("", "end", values=(movie.get('titulo'), movie.get('genero'), movie.get('duracion'), movie.get('clasificacion')))

    def volver_al_dashboard(self):
        from .admin_dashboard_view import AdminDashboard
        self.master.switch_frame(AdminDashboard)

    def open_create_movie_window(self):
        CreateMovieWindow(self)

    def open_update_movie_window(self):
        UpdateMovieWindow(self)

    def open_delete_movie_window(self):
        DeleteMovieWindow(self)


class CreateMovieWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Agregar Película")
        self.geometry("300x250")
        self.transient(master)
        self.grab_set()

        ttk.Label(self, text="Título:").pack(pady=(10,0))
        self.titulo_entry = ttk.Entry(self)
        self.titulo_entry.pack()

        ttk.Label(self, text="Género:").pack(pady=(10,0))
        self.genero_entry = ttk.Entry(self)
        self.genero_entry.pack()

        ttk.Label(self, text="Duración (min):").pack(pady=(10,0))
        self.duracion_entry = ttk.Entry(self)
        self.duracion_entry.pack()

        ttk.Label(self, text="Clasificación:").pack(pady=(10,0))
        self.clasificacion_entry = ttk.Entry(self)
        self.clasificacion_entry.pack()

        ttk.Button(self, text="Agregar", command=self.create_movie_action).pack(pady=20)

    def create_movie_action(self):
        titulo = self.titulo_entry.get()
        genero = self.genero_entry.get()
        duracion = self.duracion_entry.get()
        clasificacion = self.clasificacion_entry.get()

        if not all([titulo, genero, duracion, clasificacion]):
            messagebox.showerror("Error", "Todos los campos son requeridos", parent=self)
            return

        result = agregar_pelicula(titulo, genero, duracion, clasificacion)
        if "agregada" in result:
            messagebox.showinfo("Éxito", result, parent=self)
            self.master.load_movies()
            self.destroy()
        else:
            messagebox.showerror("Error", result, parent=self)


class UpdateMovieWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Actualizar Película")
        self.geometry("300x150")
        self.transient(master)
        self.grab_set()

        ttk.Label(self, text="Título de la película a actualizar:").pack(pady=(10,0))
        self.titulo_entry = ttk.Entry(self)
        self.titulo_entry.pack()

        ttk.Label(self, text="Nuevo Género:").pack(pady=(10,0))
        self.genero_entry = ttk.Entry(self)
        self.genero_entry.pack()

        ttk.Button(self, text="Actualizar", command=self.update_movie_action).pack(pady=20)

    def update_movie_action(self):
        titulo = self.titulo_entry.get()
        genero = self.genero_entry.get()

        if not all([titulo, genero]):
            messagebox.showerror("Error", "Todos los campos son requeridos", parent=self)
            return

        result = actualizar_pelicula_por_id(titulo, genero)
        messagebox.showinfo("Info", result, parent=self)
        self.master.load_movies()
        self.destroy()


class DeleteMovieWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Eliminar Película")
        self.geometry("300x100")
        self.transient(master)
        self.grab_set()

        ttk.Label(self, text="Título de la película a eliminar:").pack(pady=(10,0))
        self.titulo_entry = ttk.Entry(self)
        self.titulo_entry.pack()

        ttk.Button(self, text="Eliminar", command=self.delete_movie_action).pack(pady=20)

    def delete_movie_action(self):
        titulo = self.titulo_entry.get()
        if not titulo:
            messagebox.showerror("Error", "El título es requerido", parent=self)
            return

        if messagebox.askyesno("Confirmar", f"¿Seguro que quieres eliminar la película '{titulo}'?", parent=self):
            result = eliminar_pelicula_por_id(titulo)
            messagebox.showinfo("Info", result, parent=self)
            self.master.load_movies()
            self.destroy()