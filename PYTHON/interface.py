import tkinter as tk
from tkinter import messagebox, ttk
from logic import Item, ShipmentsQueue, StorageArray, TruckStack

class App:
    def __init__(self, window):
        self.window = window
        self.window.title("Amazon Hub - Simulador de Logística")
        self.window.configure(bg="#f0f2f5") 
        
        self.incoming = ShipmentsQueue()
        self.warehouse = StorageArray()
        self.truck = TruckStack()

        self.setup_ui()

    def setup_ui(self):
        title_font = ("Segoe UI", 12, "bold")
        label_font = ("Segoe UI", 10)

        main_frame = tk.Frame(self.window, bg="#f0f2f5")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        col1 = tk.Frame(main_frame, bg="white", highlightbackground="#d1d9e6", highlightthickness=1)
        col1.pack(side="left", padx=10, fill="both", expand=True)
        
        tk.Label(col1, text=" RECEPCIÓN (Cola)", font=title_font, bg="#232f3e", fg="white").pack(fill="x")
        
        form = tk.Frame(col1, bg="white", pady=10)
        form.pack()

        tk.Label(form, text="ID Paquete:", bg="white", font=label_font).grid(row=0, column=0, sticky="w")
        self.id_in = tk.Entry(form, highlightthickness=1)
        self.id_in.grid(row=0, column=1, pady=2)

        tk.Label(form, text="Categoría:", bg="white", font=label_font).grid(row=1, column=0, sticky="w")
        self.cat_in = tk.Entry(form, highlightthickness=1)
        self.cat_in.grid(row=1, column=1, pady=2)

        tk.Label(form, text="Parada #:", bg="white", font=label_font).grid(row=2, column=0, sticky="w")
        self.stop_in = tk.Entry(form, highlightthickness=1)
        self.stop_in.grid(row=2, column=1, pady=2)

        tk.Button(col1, text="Registrar Ingreso", bg="#ff9900", fg="black", font=("Segoe UI", 10, "bold"), 
                  relief="flat", command=self.add_order).pack(pady=10, padx=20, fill="x")
        
        self.list_q = tk.Listbox(col1, borderwidth=0, font=label_font, height=10)
        self.list_q.pack(padx=10, pady=10, fill="both", expand=True)


        col2 = tk.Frame(main_frame, bg="white", highlightbackground="#d1d9e6", highlightthickness=1)
        col2.pack(side="left", padx=10, fill="both", expand=True)

        tk.Label(col2, text="ALMACÉN (Arreglo)", font=title_font, bg="#37475a", fg="white").pack(fill="x")
        
        tk.Label(col2, text="Posición Estante (0-5):", bg="white", font=label_font).pack(pady=(10,0))
        self.slot_in = tk.Entry(col2, width=10, highlightthickness=1)
        self.slot_in.pack(pady=5)

        tk.Button(col2, text="Ubicar en Estante", bg="#146eb4", fg="white", font=("Segoe UI", 10, "bold"),
                  relief="flat", command=self.to_warehouse).pack(pady=10, padx=20, fill="x")
        
        self.list_w = tk.Listbox(col2, borderwidth=0, font=label_font, height=10)
        self.list_w.pack(padx=10, pady=10, fill="both", expand=True)


        col3 = tk.Frame(main_frame, bg="white", highlightbackground="#d1d9e6", highlightthickness=1)
        col3.pack(side="left", padx=10, fill="both", expand=True)

        tk.Label(col3, text=" CAMIÓN (Pila LIFO)", font=title_font, bg="#000000", fg="white").pack(fill="x")

        tk.Button(col3, text="Optimizar y Cargar", bg="#ff9900", fg="black", font=("Segoe UI", 10, "bold"),
                  relief="flat", command=self.fill_truck).pack(pady=10, padx=20, fill="x")
        
        tk.Button(col3, text="Entregar Paquete", bg="#cc0000", fg="white", font=("Segoe UI", 10, "bold"),
                  relief="flat", command=self.deliver).pack(pady=5, padx=20, fill="x")
        
        self.list_t = tk.Listbox(col3, borderwidth=0, font=label_font, height=10)
        self.list_t.pack(padx=10, pady=10, fill="both", expand=True)

    def add_order(self):
        val_id = self.id_in.get()
        val_stop = self.stop_in.get()
        if val_id and val_stop.isdigit():
            obj = Item(val_id, self.cat_in.get(), val_stop)
            self.incoming.add(obj)
            self.refresh()
            self.id_in.delete(0, 'end')
            self.cat_in.delete(0, 'end')
            self.stop_in.delete(0, 'end')
        else:
            messagebox.showwarning("Atención", "Completa los campos correctamente.")

    def to_warehouse(self):
        idx = self.slot_in.get()
        if idx.isdigit():
            p = self.incoming.get_next()
            if p:
                if not self.warehouse.put_in_slot(p, int(idx)):
                    self.incoming.data.insert(0, p)
                    messagebox.showerror("Error", "Estante ocupado o inválido")
                self.refresh()
                self.slot_in.delete(0, 'end')
            else:
                messagebox.showinfo("Info", "No hay paquetes en espera.")

    def fill_truck(self):
        items = self.warehouse.clear_and_get_all()
        if not items:
            messagebox.showinfo("Info", "El almacén está vacío.")
            return
        items.sort(key=lambda x: x.stop_index, reverse=True)
        for i in items:
            self.truck.push(i)
        self.refresh()
        messagebox.showinfo("Logística", "Camión cargado: El último en entrar será el primero en salir (Parada más cercana)")

    def deliver(self):
        p = self.truck.pop()
        if p:
            messagebox.showinfo("Entregado", f"Paquete {p.item_id} entregado en parada {p.stop_index}")
        else:
            messagebox.showinfo("Info", "El camión está vacío.")
        self.refresh()

    def refresh(self):
        self.list_q.delete(0, 'end')
        for x in self.incoming.data:
            self.list_q.insert('end', f"ID: {x.item_id} | Parada: {x.stop_index}")

        self.list_w.delete(0, 'end')
        for i, x in enumerate(self.warehouse.slots):
            txt = f"[{i}] Paquete: {x.item_id}" if x else f"[{i}] --- Vacío ---"
            self.list_w.insert('end', txt)

        self.list_t.delete(0, 'end')
        for x in reversed(self.truck.stack):
            self.list_t.insert('end', f" ID: {x.item_id} (Parada {x.stop_index})")
