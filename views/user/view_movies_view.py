import tkinter as tk
from tkinter import ttk
from Peliculas import mostrar_peliculas
from Funciones import mostrar_funciones

class ViewMoviesPage(tk.Frame):
    def __init__(self, master, user_data):
        super().__init__(master)
        from .user_dashboard_view import UserDashboard 
        self.user_data = user_data
        self.master.title("Cartelera - Cine-DB")

        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1) 

        ttk.Label(main_frame, text="Cartelera", font=("Arial", 24)).grid(row=0, column=0, columnspan=2, pady=10)

        # --- Movies List ---
        movies_frame = ttk.LabelFrame(main_frame, text="Películas Disponibles")
        movies_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        movies_frame.grid_rowconfigure(0, weight=1)
        movies_frame.grid_columnconfigure(0, weight=1)

        self.movies_tree = ttk.Treeview(movies_frame, columns=("Título", "Género", "Duración", "Clasificación"), show="headings")
        self.movies_tree.heading("Título", text="Título")
        self.movies_tree.heading("Género", text="Género")
        self.movies_tree.heading("Duración", text="Duración (min)")
        self.movies_tree.heading("Clasificación", text="Clasificación")
        
        # Ajustes estéticos de ancho
        self.movies_tree.column("Título", width=130, anchor="w")
        self.movies_tree.column("Género", width=90, anchor="center")
        self.movies_tree.column("Duración", width=90, anchor="center")
        self.movies_tree.column("Clasificación", width=90, anchor="center")
        
        self.movies_tree.grid(row=0, column=0, sticky="nsew")
        
        movies_scrollbar = ttk.Scrollbar(movies_frame, orient="vertical", command=self.movies_tree.yview)
        self.movies_tree.configure(yscroll=movies_scrollbar.set)
        movies_scrollbar.grid(row=0, column=1, sticky="ns")

       
        functions_frame = ttk.LabelFrame(main_frame, text="Funciones Programadas")
        functions_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 0))
        functions_frame.grid_rowconfigure(0, weight=1)
        functions_frame.grid_columnconfigure(0, weight=1)

       
        self.functions_tree = ttk.Treeview(functions_frame, columns=("Película", "Sala", "Horario", "Disponibilidad", "Precio"), show="headings")
        self.functions_tree.heading("Película", text="Película")
        self.functions_tree.heading("Sala", text="Sala")
        self.functions_tree.heading("Horario", text="Horario")
        self.functions_tree.heading("Disponibilidad", text="Asientos Libres") 
        self.functions_tree.heading("Precio", text="Precio")
        
        
        self.functions_tree.column("Película", width=120, anchor="w")
        self.functions_tree.column("Sala", width=50, anchor="center")
        self.functions_tree.column("Horario", width=70, anchor="center")
        self.functions_tree.column("Disponibilidad", width=90, anchor="center")
        self.functions_tree.column("Precio", width=80, anchor="e")
        
        self.functions_tree.grid(row=0, column=0, sticky="nsew")

        functions_scrollbar = ttk.Scrollbar(functions_frame, orient="vertical", command=self.functions_tree.yview)
        self.functions_tree.configure(yscroll=functions_scrollbar.set)
        functions_scrollbar.grid(row=0, column=1, sticky="ns")

        ttk.Button(main_frame, text="< Volver al Panel", command=lambda: self.master.switch_frame(lambda m: UserDashboard(m, self.user_data))).grid(row=2, column=0, columnspan=2, pady=20)

        self.load_data()

    def load_data(self):
        for i in self.movies_tree.get_children():
            self.movies_tree.delete(i)
        movies_list = mostrar_peliculas(return_list=True)
        if movies_list:
            for movie in movies_list:
                self.movies_tree.insert("", "end", values=(
                    movie.get('titulo'), 
                    movie.get('genero'), 
                    movie.get('duracion'), 
                    movie.get('clasificacion', 'N/A')
                ))

        for i in self.functions_tree.get_children():
            self.functions_tree.delete(i)
        functions_list = mostrar_funciones(return_list=True)
        if functions_list:
            for func in functions_list:
                asientos = func.get('asientos_disponibles', 0)
                try:
                    precio_formateado = f"${float(func.get('precio', 0)):,.2f}"
                except (ValueError, TypeError):
                    precio_formateado = f"${func.get('precio')}"

                self.functions_tree.insert("", "end", values=(
                    func.get('pelicula'),
                    func.get('sala'),
                    func.get('horario'),
                    f"{asientos} und",
                    precio_formateado
                ))