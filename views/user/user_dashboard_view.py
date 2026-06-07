import tkinter as tk
from tkinter import ttk
from .view_movies_view import ViewMoviesPage
from .buy_tickets_view import BuyTicketsView

class UserDashboard(tk.Frame):
    def __init__(self, master, user_data):
        super().__init__(master)
        from views.login_view import LoginPage 
        
        self.user_data = user_data
        self.master.title(f"Panel de Usuario: {self.user_data.get('nombre')} - Cine-DB")

        main_frame = tk.Frame(self)
        main_frame.pack(expand=True)

        ttk.Label(main_frame, text=f"¡Bienvenido, {self.user_data.get('nombre')}!", font=("Arial", 24)).pack(pady=10)


        self.pref_text = tk.StringVar()
        self.lbl_pref = ttk.Label(main_frame, textvariable=self.pref_text, font=("Arial", 10, "italic"), foreground="gray")
        self.lbl_pref.pack(pady=(0, 20))
        self.recargar_datos_perfil() 

        ttk.Button(main_frame, text="Ver Películas y Funciones", command=lambda: self.master.switch_frame(lambda m: ViewMoviesPage(m, self.user_data))).pack(pady=10, ipadx=20, ipady=5)
        ttk.Button(main_frame, text="Comprar Entrada", command=self.open_buy_tickets).pack(pady=10, ipadx=20, ipady=5)
        ttk.Button(main_frame, text="Ver Historial de Compras", command=self.open_purchase_history).pack(pady=10, ipadx=20, ipady=5)
        
        ttk.Button(main_frame, text="Configurar Mis Preferencias", command=self.open_preferences).pack(pady=10, ipadx=20, ipady=5)

        ttk.Button(self, text="< Cerrar Sesión", command=lambda: self.master.switch_frame(LoginPage)).pack(pady=20)

    def recargar_datos_perfil(self):
        lista_gustos = self.user_data.get("preferencias", [])
        if lista_gustos:
            texto = f"Tus géneros favoritos: {', '.join(lista_gustos)}"
        else:
            texto = "Aún no has configurado tus géneros favoritos."
        self.pref_text.set(texto)

    def open_buy_tickets(self):
        BuyTicketsView(self.master, self.user_data['_id'])

    def open_purchase_history(self):
        from .purchase_history_view import PurchaseHistoryPage
        self.master.switch_frame(lambda m: PurchaseHistoryPage(m, self.user_data))

    def open_preferences(self):
        from .preferences_view import PreferencesWindow
        PreferencesWindow(self, self.user_data)