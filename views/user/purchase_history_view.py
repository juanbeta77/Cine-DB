import tkinter as tk
from tkinter import ttk
from Entradas import obtener_historial_usuario 

class PurchaseHistoryPage(tk.Frame):
    def __init__(self, master, user_data):
        super().__init__(master)
        self.master = master
        self.user_data = user_data 
        
        self.user_id = user_data.get('_id') if isinstance(user_data, dict) else user_data

        self.master.title("Mi Historial de Compras - Cine-DB")

        tk.Label(self, text="Historial de Compras", font=("Arial", 14, "bold")).pack(pady=10)

        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=15, pady=5)

        self.tree = ttk.Treeview(table_frame, columns=("ID Compra", "Película", "Fecha Compra", "Boletos", "Total Paid"), show="headings")
        
        self.tree.heading("ID Compra", text="ID Compra")
        self.tree.heading("Película", text="Película")
        self.tree.heading("Fecha Compra", text="Fecha Compra")
        self.tree.heading("Boletos", text="Boletos")
        self.tree.heading("Total Paid", text="Total Pagado")

        self.tree.column("ID Compra", width=90, anchor="center")
        self.tree.column("Película", width=150, anchor="w")
        self.tree.column("Fecha Compra", width=120, anchor="center")
        self.tree.column("Boletos", width=60, anchor="center")
        self.tree.column("Total Paid", width=90, anchor="e")

        self.tree.pack(fill="both", expand=True)

        self.load_history()

        ttk.Button(self, text="< Volver al Panel", command=self.volver_al_dashboard).pack(pady=15)

    def load_history(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        compras_list = obtener_historial_usuario(self.user_id)
        
        if not compras_list:
            self.tree.insert("", "end", values=("N/A", "No has realizado compras aún", "-", "-", "-"))
            return

        for compra in compras_list:
            id_corto = compra.get('id_compra')[-8:] if compra.get('id_compra') else "N/A"
            
            try:
                total_formateado = f"${float(compra.get('total', 0)):,.2f}"
            except (ValueError, TypeError):
                total_formateado = f"${compra.get('total')}"

            self.tree.insert("", "end", values=(
                id_corto,
                compra.get('pelicula'),
                compra.get('fecha_compra'),
                compra.get('cantidad'),
                total_formateado
            ))

    def volver_al_dashboard(self):
        from .user_dashboard_view import UserDashboard
        self.master.switch_frame(lambda m: UserDashboard(m, self.user_data))