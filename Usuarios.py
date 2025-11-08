import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from Login import Usuario

class VentanaUsuario:
    def __init__(self, principal):
        self.principal = principal
        self.ventana = tk.Toplevel(principal)
        self.ventana.title("Usuarios")
        self.ventana.geometry("1200x700")
        self.ventana.configure(bg="#0D1B2A")

        self.id_seleccionado = None
        self.modo_edicion = False

        tk.Label(self.ventana, text="Gestión de Usuarios", bg="#0D1B2A", fg="white", font=("Arial", 16, "bold")).pack(pady=8)

        botones_principales = tk.Frame(self.ventana, bg="#0D1B2A")
        botones_principales.pack(fill="both", expand=True, padx=10, pady=8)

        form = tk.Frame(botones_principales, bg="#0D1B2A")
        form.pack(side="left", fill="y", padx=(4, 14))

        tk.Label(form, text="ID :", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=0, column=0, padx=4, pady=10, sticky="w")
        self.caja_id = tk.Entry(form, font=("Arial", 11), width=30, state="disabled")
        self.caja_id.grid(row=0, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="Usuario :", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=1, column=0, padx=4, pady=10, sticky="w")
        self.caja_usuario = tk.Entry(form, font=("Arial", 11), width=30)
        self.caja_usuario.grid(row=1, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="Contraseña :", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=2, column=0, padx=4, pady=10, sticky="w")
        self.caja_contra = tk.Entry(form, show="*", font=("Arial", 11), width=30)
        self.caja_contra.grid(row=2, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="Confirmar :", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=3, column=0, padx=4, pady=10, sticky="w")
        self.caja_contra2 = tk.Entry(form, show="*", font=("Arial", 11), width=30)
        self.caja_contra2.grid(row=3, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="Rol :", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=4, column=0, padx=4, pady=10, sticky="w")
        self.combo_rol = ttk.Combobox(form, state="readonly", width=28, values=["Administrador", "Vendedor"])
        self.combo_rol.set("Vendedor")
        self.combo_rol.grid(row=4, column=1, padx=4, pady=10, sticky="w")

