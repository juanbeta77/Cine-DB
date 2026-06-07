import tkinter as tk
from tkinter import ttk, messagebox
from Usuarios import login_usuario
from .user_dashboard_view import UserDashboard

class UserLoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        from views.login_view import LoginPage 
        self.LoginPage = LoginPage

        self.master.title("Login Usuario - Cine-DB")

        main_frame = tk.Frame(self)
        main_frame.pack(expand=True)

        ttk.Label(main_frame, text="Acceso Usuario", font=("Arial", 20)).pack(pady=20)

        ttk.Label(main_frame, text="Correo:").pack(pady=(10,0))
        self.correo_entry = ttk.Entry(main_frame)
        self.correo_entry.pack(pady=(0,10))

        ttk.Label(main_frame, text="Contraseña:").pack(pady=(10,0))
        self.password_entry = ttk.Entry(main_frame, show="*")
        self.password_entry.pack(pady=(0,10))

        ttk.Button(main_frame, text="Ingresar", command=self.login).pack(pady=20, ipadx=10, ipady=3)
        
        ttk.Button(main_frame, text="< Volver", command=lambda: self.master.switch_frame(self.LoginPage)).pack(pady=10)

    def login(self):
        correo = self.correo_entry.get()
        password = self.password_entry.get()

        if not correo or not password:
            messagebox.showerror("Error", "Correo y contraseña son requeridos", parent=self)
            return

        usuario_logueado = login_usuario(correo, password)

        if usuario_logueado:
            self.master.switch_frame(lambda master: UserDashboard(master, usuario_logueado))
        else:
            messagebox.showerror("Error", "Credenciales incorrectas", parent=self)
