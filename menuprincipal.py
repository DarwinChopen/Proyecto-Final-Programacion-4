import tkinter as tk
from tkinter import messagebox, ttk

class VentanaPrincipal:
    def __init__(self, principal,nombre_usuario  ,rol):
        self.ventana = principal
        self.ventana.title("Menu Autoventas Los Altos")
        self.ventana.geometry("950x500")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#1B263B")
        self.rol = rol
        self.nombre_usuario=nombre_usuario

        principal = tk.Frame(self.ventana, bg="#1B263B")
        principal.pack(fill="both", expand=True, padx=10, pady=10)

        lado_izquerdo = tk.Frame(principal, bg="#1B263B")
        lado_izquerdo.pack(side="left", fill="y", padx=(10, 30))

        self.usuario = nombre_usuario
        self.rol = rol

        tk.Label(lado_izquerdo, text=f"Bienvenido al Sistema", bg="#1B263B", fg="dim gray",font=("Arial", 14, "bold"), anchor="w").pack(pady=18, anchor="w")
        tk.Button(lado_izquerdo, text="Registrar Auto", width=24,bg="#1B263B", fg="white", font=("Arial", 12),command=self.abrir_autos).pack(pady=8, anchor="w")
        tk.Button(lado_izquerdo, text="Registrar Proveedor", width=24,bg="#1B263B", fg="white", font=("Arial", 12),command=self.abrir_proveedor).pack(pady=8, anchor="w")
        tk.Button(lado_izquerdo, text="Taller", width=24,bg="#1B263B", fg="white", font=("Arial", 12),command=self.abrir_taller).pack(pady=8, anchor="w")
        tk.Button(lado_izquerdo, text="Registrar Cliente", width=24,bg="#1B263B", fg="white", font=("Arial", 12), command=self.abrir_cliente).pack(pady=8, anchor="w")
        tk.Button(lado_izquerdo, text="Registrar Venta", width=24,bg="#1B263B", fg="white", font=("Arial", 12),command=self.abrir_venta).pack(pady=8, anchor="w")
        if rol == "Administrador": tk.Button(lado_izquerdo, text="Usuario", width=24,bg="#1B263B", fg="white", font=("Arial", 12),command=self.abrir_usuario).pack(pady=8, anchor="w")
        tk.Button(lado_izquerdo, text="Salir", width=24,bg="#1B263B", fg="red", font=("Arial", 12),command=self.ventana.destroy).pack(pady=8, anchor="w")
        tk.Label(lado_izquerdo, text=f"{nombre_usuario} ({rol}) ", bg="#1B263B", fg="dim gray",font=("Arial", 14, "bold"), anchor="w").pack(pady=8, anchor="w")
        lado_derecho = tk.Frame(principal, width=300, height=400)
        lado_derecho.pack(side="right", fill="both", expand=True)
        lado_derecho.pack_propagate(False)

        self.canvas = tk.Canvas(lado_derecho, width=300, height=400)
        self.canvas.pack(fill="both", expand=True)

        self.fondo_img = tk.PhotoImage(file="logo_autoventas.png")
        self.canvas.create_image(0, 0, anchor="nw", image=self.fondo_img)

        self.canvas.create_text(350, 250, text="Autoventas Los Altos", fill="white", font=("Arial", 30, "bold"))

    def abrir_autos(self):
        self.ventana.withdraw()
        from RegisrtoVehiculo import VentanaAutos
        VentanaAutos(self.ventana)

    def abrir_proveedor(self):
        self.ventana.withdraw()
        from Proveedores import VentanaProveedores
        VentanaProveedores(self.ventana)

    def abrir_taller(self):
        self.ventana.withdraw()
        from Taller import VentanaTaller
        VentanaTaller(self.ventana)

    def abrir_cliente(self):
        self.ventana.withdraw()
        from Clientes import VentanaClientes
        VentanaClientes(self.ventana)

    def abrir_venta(self):
        pass

    def abrir_usuario(self):
        if self.rol != "Administrador":
            messagebox.showwarning("Permisos", "Solo el Administrador puede acceder.")
            return
        try:
            self.ventana.withdraw()
        except Exception:
            pass
        from Usuarios import VentanaUsuario
        VentanaUsuario(self.ventana)





