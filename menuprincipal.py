import tkinter as tk
from tkinter import messagebox, ttk

class VentanaPrincipal:
    def __init__(self, principal, rol):
        self.ventana = principal
        self.ventana.title("Menu Autoventas Los Altos")
        self.ventana.geometry("750x450")
        self.ventana.configure(bg="#1B263B")
        self.ventana.resizable(False, False)
        self.rol = rol

        principal = tk.Frame(self.ventana, bg="#1B263B")
        principal.pack(fill="both", expand=True, padx=10, pady=10)

        lado_izquerdo = tk.Frame(principal, bg="#1B263B")
        lado_izquerdo.pack(side="left", fill="y", padx=(10, 30))

        tk.Label(lado_izquerdo, text=f"Bienvenido al Sistema", bg="#1B263B", fg="white",font=("Arial", 14, "bold"), anchor="w").pack(pady=18, anchor="w")
        tk.Button(lado_izquerdo, text="Registrar Auto", width=24,bg="#1B263B", fg="white", font=("Arial", 12),command=self.abrir_autos).pack(pady=8, anchor="w")
        tk.Button(lado_izquerdo, text="Registrar Proveedor", width=24,bg="#1B263B", fg="white", font=("Arial", 12),command=self.abrir_proveedor).pack(pady=8, anchor="w")
        tk.Button(lado_izquerdo, text="Taller", width=24,bg="#1B263B", fg="white", font=("Arial", 12),command=self.abrir_taller).pack(pady=8, anchor="w")
        tk.Button(lado_izquerdo, text="Registrar Cliente", width=24,bg="#1B263B", fg="white", font=("Arial", 12), command=self.abrir_cliente).pack(pady=8, anchor="w")
        tk.Button(lado_izquerdo, text="Registrar Venta", width=24,bg="#1B263B", fg="white", font=("Arial", 12),command=self.abrir_venta).pack(pady=8, anchor="w")
        if rol == "Administrador": tk.Button(lado_izquerdo, text="Usuario", width=24,bg="#1B263B", fg="white", font=("Arial", 12),command=self.abrir_usuario).pack(pady=8, anchor="w")
        tk.Button(lado_izquerdo, text="Salir", width=24,bg="#1B263B", fg="white", font=("Arial", 12),command=self.ventana.destroy).pack(pady=8, anchor="w")

        lado_derecho = tk.Frame(principal, bg="#1B263B", width=280)
        lado_derecho.pack(side="right", fill="both", expand=True)
        tk.Label(lado_derecho, text="AUTOVENTAS LOS ALTOS", bg="#1B263B", fg="#A0AEC0",font=("Arial", 22, "bold")).pack(expand=True)

    def abrir_autos(self):
        from RegisrtoVehiculo import VentanaAutos
        VentanaAutos(self.ventana)

    def abrir_proveedor(self):
        print("Proveedores")
    def abrir_taller(self):
         print("Taller")
    def abrir_cliente(self):
        print("Clientes")
    def abrir_venta(self):
        print("Ventas")
    def abrir_usuario(self):
        if self.rol != "Administrador":
            messagebox.showwarning("Permisos", "Solo el Administrador puede acceder.")
            return



