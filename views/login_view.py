import tkinter as tk
from tkinter import ttk, messagebox
from .admin.admin_dashboard_view import AdminDashboard
from .user.user_login_view import UserLoginPage

class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        self.master.title("Bienvenido a Cine-DB")

        main_frame = tk.Frame(self)
        main_frame.pack(expand=True)

        ttk.Label(main_frame, text="Sistema de Cine-DB", font=("Arial", 28, "bold")).pack(pady=30)
        ttk.Label(main_frame, text="Seleccione su tipo de acceso", font=("Arial", 14)).pack(pady=10)

        ttk.Button(main_frame, text="Módulo Administrador", command=self.open_admin_login).pack(pady=10, ipadx=30, ipady=10)
        ttk.Button(main_frame, text="Módulo Usuario", command=self.open_user_login).pack(pady=10, ipadx=45, ipady=10)

    def open_admin_login(self):
        self.master.switch_frame(AdminLoginPage)

    def open_user_login(self):
        self.master.switch_frame(UserLoginPage)

class AdminLoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master.title("Login Administrador - Cine-DB")

        main_frame = tk.Frame(self)
        main_frame.pack(expand=True)

        ttk.Label(main_frame, text="Acceso Administrador", font=("Arial", 20)).pack(pady=20)

        ttk.Label(main_frame, text="Usuario:").pack(pady=(10,0))
        self.admin_user_entry = ttk.Entry(main_frame)
        self.admin_user_entry.pack(pady=(0,10))
        self.admin_user_entry.insert(0, "admin")

        ttk.Label(main_frame, text="Contraseña:").pack(pady=(10,0))
        self.admin_pass_entry = ttk.Entry(main_frame, show="*")
        self.admin_pass_entry.pack(pady=(0,10))
        self.admin_pass_entry.insert(0, "1234")

        ttk.Button(main_frame, text="Ingresar", command=self.login).pack(pady=20, ipadx=10, ipady=3)
        
        ttk.Button(main_frame, text="< Volver", command=lambda: self.master.switch_frame(LoginPage)).pack(pady=10)

    def login(self):
        user = self.admin_user_entry.get()
        password = self.admin_pass_entry.get()

        if user == "admin" and password == "1234":
            self.master.switch_frame(AdminDashboard)
        else:
            messagebox.showerror("Error", "Credenciales de administrador incorrectas")
