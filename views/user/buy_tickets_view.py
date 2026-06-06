import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from Funciones import get_funciones_disponibles, get_funcion_by_id
from Peliculas import get_pelicula_by_id
from Entradas import comprar_entrada

class BuyTicketsView(tk.Toplevel):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.title("Comprar Entradas")
        self.geometry("450x320")
        self.user_id = user_id

        self.funciones = get_funciones_disponibles()
        self.selected_funcion_id = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Seleccione una función:", font=("Arial", 10, "bold")).pack(pady=5)

        if not self.funciones:
            tk.Label(self, text="No hay funciones disponibles.").pack(pady=10)
            return

        funcion_options = []
        self.mapa_funciones = {}

        for funcion in self.funciones:
            id_pelicula = funcion.get('pelicula_id')
            pelicula = None
            
            if id_pelicula:
                pelicula = get_pelicula_by_id(id_pelicula)
            
            titulo_peli = pelicula['titulo'] if pelicula else funcion.get('pelicula_titulo', 'Película Desconocida')
            
            id_str = str(funcion['_id'])
            texto_opcion = f"{titulo_peli} - Sala {funcion.get('sala', 'N/A')} ({funcion.get('horario', 'S/H')})"
            
            funcion_options.append(texto_opcion)
            self.mapa_funciones[texto_opcion] = id_str

        self.funcion_menu = ttk.Combobox(self, textvariable=self.selected_funcion_id, values=funcion_options, state="readonly", width=40)
        self.funcion_menu.pack(pady=5)
        self.funcion_menu.bind("<<ComboboxSelected>>", self.show_funcion_details)

        self.details_frame = tk.Frame(self)
        self.details_frame.pack(pady=10)

        tk.Label(self.details_frame, text="Cantidad:").grid(row=0, column=0, padx=5, pady=5)
        self.cantidad_spinbox = tk.Spinbox(self.details_frame, from_=1, to=10, width=5)
        self.cantidad_spinbox.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(self, text="Comprar", command=self.comprar, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(pady=20)

    def show_funcion_details(self, event):
        selected_option = self.selected_funcion_id.get()
        if not selected_option or selected_option not in self.mapa_funciones:
            return

        funcion_id = self.mapa_funciones[selected_option]
        funcion = get_funcion_by_id(funcion_id)
        
        if funcion:
            self.cantidad_spinbox.config(to=funcion.get('asientos_disponibles', 10))

    def comprar(self):
        selected_option = self.selected_funcion_id.get()
        if not selected_option or selected_option not in self.mapa_funciones:
            messagebox.showerror("Error", "Por favor seleccione una función válida.")
            return

        try:
            funcion_id = self.mapa_funciones[selected_option]
            cantidad = int(self.cantidad_spinbox.get())

            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a cero.")
                return

            funcion = get_funcion_by_id(funcion_id)
            if not funcion:
                messagebox.showerror("Error", "La función seleccionada no existe.")
                return

            if cantidad > funcion.get('asientos_disponibles', 0):
                messagebox.showerror("Error", "No hay suficientes asientos disponibles.")
                return

            precio_total = funcion['precio'] * cantidad
            pelicula = get_pelicula_by_id(funcion['pelicula_id'])
            titulo_pelicula = pelicula['titulo'] if pelicula else funcion.get('pelicula_titulo', 'Película Desconocida')
            
            precio_formateado = f"${precio_total:,.2f}"

            confirm = messagebox.askyesno(
                "Confirmar Compra", 
                f"Película: {titulo_pelicula}\nHorario: {funcion.get('horario', 'S/H')}\nCantidad: {cantidad}\nPrecio Total: {precio_formateado}\n\n¿Desea proceder al pago?"
            )

            if confirm:
                tarjeta = simpledialog.askstring(
                    "Pasarela de Pago", 
                    f"Monto a pagar: {precio_formateado}\n\nIngrese su número de tarjeta (16 dígitos):",
                    parent=self
                )
                
                if not tarjeta:
                    messagebox.showwarning("Pago Cancelado", "La compra fue cancelada porque no se completó el pago.")
                    return
                
                if len(tarjeta.strip()) < 4 or not tarjeta.isdigit():
                    messagebox.showerror("Pago Rechazado", "Transacción rechazada: El método de pago no es válido.")
                    return
                
                messagebox.showinfo("Pago Exitoso", "Conectando con la entidad financiera...\n\n¡Transacción Aprobada!")

                resultado = comprar_entrada(self.user_id, funcion_id, cantidad, precio_total)
                if "exito" in str(resultado).lower() or "correcto" in str(resultado).lower():
                    
                    try:
                        from datetime import datetime
                        id_corto = funcion_id[-6:]
                        timestamp = int(datetime.now().timestamp())
                        nombre_archivo = f"recibo_{id_corto}_{timestamp}.txt"
                        
                        with open(nombre_archivo, "w", encoding="utf-8") as file:
                            file.write("========================================\n")
                            file.write("           CINE-DB - RECIBO DE COMPRA   \n")
                            file.write("========================================\n")
                            file.write(f"Fecha/Hora:   {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                            file.write(f"ID Función:   {funcion_id}\n")
                            file.write(f"Película:     {titulo_pelicula}\n")
                            file.write(f"Cantidad:     {cantidad} boletos\n")
                            file.write(f"Total Pagado: {precio_formateado}\n")
                            file.write("========================================\n")
                            file.write("   ¡Gracias por su compra! Disfrute.    \n")
                            file.write("========================================\n")
                        
                        messagebox.showinfo("Éxito", f"¡Compra registrada!\n\nSe ha generado su recibo en el archivo:\n{nombre_archivo}")
                    
                    except Exception as error_archivo:
                        messagebox.showinfo("Éxito", f"¡Compra realizada con éxito!\n(Nota: No se pudo escribir el archivo del recibo: {error_archivo})")

                    self.destroy()
                else:
                    messagebox.showerror("Error", resultado)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")