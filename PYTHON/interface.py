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
