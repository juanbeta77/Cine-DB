import tkinter as tk
from tkinter import ttk, messagebox
from Usuarios import crear_usuario, mostrar_usuarios, actualizar_usuario_por_documento, eliminar_usuario_por_documento

class UserManagementPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        from .admin_dashboard_view import AdminDashboard
        self.master.title("Gestión de Usuarios - Cine-DB")

        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(top_frame, text="Crear Usuario", command=self.open_create_user_window).pack(side="left", padx=5)
        ttk.Button(top_frame, text="Actualizar Usuario", command=self.open_update_user_window).pack(side="left", padx=5)
        ttk.Button(top_frame, text="Eliminar Usuario", command=self.open_delete_user_window).pack(side="left", padx=5)
        ttk.Button(top_frame, text="Refrescar", command=self.load_users).pack(side="right", padx=5)

        self.tree = ttk.Treeview(self, columns=("Documento", "Nombre", "Correo", "Teléfono"), show="headings")
        self.tree.heading("Documento", text="Documento")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Correo", text="Correo")
        self.tree.heading("Teléfono", text="Teléfono")
        
        self.tree.column("Documento", width=100, anchor="center")
        self.tree.column("Nombre", width=120)
        self.tree.column("Correo", width=150)
        self.tree.column("Teléfono", width=100, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_users()

        ttk.Button(self, text="< Volver al Panel", command=lambda: self.master.switch_frame(AdminDashboard)).pack(pady=10)

    def load_users(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        users_list = mostrar_usuarios(return_list=True)
        if users_list:
            for user in users_list:
                self.tree.insert("", "end", values=(
                    user.get('documento', 'S/D'),
                    user.get('nombre'), 
                    user.get('correo'), 
                    user.get('telefono')
                ))

    def open_create_user_window(self):
        CreateUserWindow(self)

    def open_update_user_window(self):
        UpdateUserWindow(self)

    def open_delete_user_window(self):
        DeleteUserWindow(self)


class CreateUserWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Crear Usuario")
        self.geometry("300x300") 

        self.transient(master)
        self.grab_set()

        ttk.Label(self, text="Documento de Identidad:").pack(pady=(10,0))
        self.documento_entry = ttk.Entry(self)
        self.documento_entry.pack()

        ttk.Label(self, text="Nombre:").pack(pady=(10,0))
        self.nombre_entry = ttk.Entry(self)
        self.nombre_entry.pack()

        ttk.Label(self, text="Correo:").pack(pady=(10,0))
        self.correo_entry = ttk.Entry(self)
        self.correo_entry.pack()

        ttk.Label(self, text="Teléfono:").pack(pady=(10,0))
        self.telefono_entry = ttk.Entry(self)
        self.telefono_entry.pack()

        ttk.Label(self, text="Contraseña:").pack(pady=(10,0))
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack()

        ttk.Button(self, text="Crear", command=self.create_user_action).pack(pady=20)

    def create_user_action(self):
        documento = self.documento_entry.get().strip()
        nombre = self.nombre_entry.get().strip()
        correo = self.correo_entry.get().strip()
        telefono = self.telefono_entry.get().strip()
        password = self.password_entry.get().strip()

        if not all([documento, nombre, correo, telefono, password]):
            messagebox.showerror("Error", "Todos los campos son requeridos", parent=self)
            return

        result = crear_usuario(documento, nombre, correo, telefono, password)

        if "éxito" in result.lower() or "creado" in result.lower():
            messagebox.showinfo("Éxito", result, parent=self)
            self.master.load_users()
            self.destroy()
        else:
            messagebox.showerror("Error", result, parent=self)

class UpdateUserWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Actualizar Usuario")
        self.geometry("320x280")
        self.resizable(False, False)

        self.transient(master)
        self.grab_set()

        padding_frame = tk.Frame(self)
        padding_frame.pack(fill="both", expand=True, padx=20, pady=10)

        ttk.Label(padding_frame, text="Documento del usuario a actualizar:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5, 2))
        self.documento_entry = ttk.Entry(padding_frame, width=30)
        self.documento_entry.pack(fill="x", pady=(0, 10))

        ttk.Separator(padding_frame, orient="horizontal").pack(fill="x", pady=5)
        ttk.Label(padding_frame, text="Campos a modificar (llene al menos uno):", font=("Arial", 9, "italic"), foreground="gray").pack(anchor="w", pady=(0, 5))

        ttk.Label(padding_frame, text="Nuevo Teléfono:").pack(anchor="w", pady=(5, 2))
        self.telefono_entry = ttk.Entry(padding_frame, width=30)
        self.telefono_entry.pack(fill="x", pady=(0, 10))

        ttk.Label(padding_frame, text="Nuevo Correo:").pack(anchor="w", pady=(5, 2))
        self.correo_entry = ttk.Entry(padding_frame, width=30)
        self.correo_entry.pack(fill="x", pady=(0, 15))

        self.btn_actualizar = ttk.Button(
            padding_frame, 
            text="✔ Confirmar Actualización", 
            command=self.update_user_action
        )
        self.btn_actualizar.pack(fill="x", ipady=3)

    def update_user_action(self):
        documento = self.documento_entry.get().strip()
        telefono = self.telefono_entry.get().strip()
        correo = self.correo_entry.get().strip()

        if not documento:
            messagebox.showerror("Error", "El documento del usuario es obligatorio para realizar la búsqueda.", parent=self)
            return

        if not telefono and not correo:
            messagebox.showwarning("Atención", "Debe ingresar al menos un dato nuevo para actualizar (Teléfono o Correo).", parent=self)
            return

        from Usuarios import actualizar_usuario_por_documento
        result = actualizar_usuario_por_documento(documento, telefono, correo)
        
        messagebox.showinfo("Resultado", result, parent=self)
        
        if hasattr(self.master, "load_users"):
            self.master.load_users()
            
        self.destroy()

class DeleteUserWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Eliminar Usuario")
        self.geometry("300x120")

        self.transient(master)
        self.grab_set()

        ttk.Label(self, text="Documento del usuario a eliminar:").pack(pady=(10,0))
        self.documento_entry = ttk.Entry(self)
        self.documento_entry.pack()

        ttk.Button(self, text="Eliminar", command=self.delete_user_action).pack(pady=20)

    def delete_user_action(self):
        documento = self.documento_entry.get().strip()
        if not documento:
            messagebox.showerror("Error", "El documento es requerido", parent=self)
            return

        if messagebox.askyesno("Confirmar", f"¿Seguro que quieres eliminar al usuario con documento {documento}?", parent=self):
            result = eliminar_usuario_por_documento(documento)
            messagebox.showinfo("Info", result, parent=self)
            self.master.load_users()
            self.destroy()