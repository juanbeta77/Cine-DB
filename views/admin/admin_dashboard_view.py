import tkinter as tk
from tkinter import ttk
from .user_management_view import UserManagementPage
from .movie_management_view import MovieManagementPage
from .function_management_view import FunctionManagementPage

class AdminDashboard(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        from ..login_view import LoginPage
        self.master.title("Panel de Administrador - Cine-DB")

        main_frame = tk.Frame(self)
        main_frame.pack(expand=True)

        ttk.Label(main_frame, text="Panel de Administrador", font=("Arial", 24)).pack(pady=20)

        ttk.Button(main_frame, text="Gestionar Usuarios", command=lambda: self.master.switch_frame(UserManagementPage)).pack(pady=10, ipadx=20, ipady=5)
        ttk.Button(main_frame, text="Gestionar Películas", command=lambda: self.master.switch_frame(MovieManagementPage)).pack(pady=10, ipadx=20, ipady=5)
        ttk.Button(main_frame, text="Gestionar Funciones", command=lambda: self.master.switch_frame(FunctionManagementPage)).pack(pady=10, ipadx=20, ipady=5)

        ttk.Button(self, text="< Cerrar Sesión", command=lambda: self.master.switch_frame(LoginPage)).pack(pady=20)
