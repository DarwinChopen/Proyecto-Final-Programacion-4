import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

DB_NAME = "autoventas.db"

class Usuario:
    def __init__(self, usuario, contrasenia, rol="Vendedor"):
        self.usuario = usuario
        self.contrasenia = contrasenia
        self.rol = rol

    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                contrasenia TEXT NOT NULL,
                rol TEXT NOT NULL CHECK(rol IN ('Administrador','Vendedor','Supervisor'))
            );
        """)
        conn.commit()
        return conn

    def guardar(self):
        with Usuario._conn() as conn:
            conn.execute(
                "INSERT INTO usuarios (usuario, contrasenia, rol) VALUES (?, ?, ?)",
                (self.usuario.strip().lower(), self.contrasenia, self.rol)
            )
        print(f"Usuario '{self.usuario}' guardado con éxito.")

    @staticmethod
    def listar():
        with Usuario._conn() as conn:
            cur = conn.execute("SELECT * FROM usuarios ORDER BY id_usuario")
            filas = cur.fetchall()
            if not filas:
                print("No hay usuarios registrados.")
                return
            print("\nLISTADO DE USUARIOS ")
            for f in filas:
                print(f"ID: {f['id_usuario']} | Usuario: {f['usuario']} | Rol: {f['rol']}")

    @staticmethod
    def modificar():
        ide = input("ID de usuario a modificar: ")
        with Usuario._conn() as conn:
            cur = conn.execute("SELECT * FROM usuarios WHERE id_usuario = ?", (ide,))
            fila = cur.fetchone()
            if not fila:
                print("No se encontró el usuario.")
                return
            usuario = input(f"Nuevo usuario [{fila['usuario']}]: ") or fila['usuario']
            contrasenia = input(f"Nueva contraseña [****]: ") or fila['contrasenia']
            rol = input(f"Nuevo rol (Administrador/Vendedor/Supervisor) [{fila['rol']}]: ") or fila['rol']
            conn.execute("UPDATE usuarios SET usuario=?, contrasenia=?, rol=? WHERE id_usuario=?",
                (usuario.strip().lower(), contrasenia, rol, ide)
            )
        print("Usuario actualizado con éxito.")

    @staticmethod
    def eliminar():
        ide = input("ID de usuario a eliminar: ")
        with Usuario._conn() as conn:
            cur = conn.execute("DELETE FROM usuarios WHERE id_usuario = ?", (ide,))
            if cur.rowcount == 0:
                print("No se encontró el usuario.")
            else:
                print("Usuario eliminado con éxito.")

    @staticmethod
    def autenticar(usuario, contrasenia):
        with Usuario._conn() as conn:
            cur = conn.execute(
                "SELECT * FROM usuarios WHERE lower(trim(usuario)) = ? AND contrasenia = ?",
                (usuario.strip().lower(), contrasenia)
            )
            return cur.fetchone()

    @staticmethod
    def admin_principal():
        with Usuario._conn() as conn:
            conn.execute("""
                INSERT OR IGNORE INTO usuarios (usuario, contrasenia, rol)
                VALUES ('darwin','7733','Administrador')
            """)
            conn.commit()

class Vehiculo:
    def __init__(self, vin, marca, modelo, color, anio, caja, kilometraje, estado, procedencia, impuesto, placa, precio_costo):
        self.vin = vin
        self.marca = marca
        self.modelo = modelo
        self.color = color
        self.anio = anio
        self.caja = caja
        self.kilometraje = kilometraje
        self.estado = estado
        self.procedencia = procedencia
        self.impuesto = impuesto
        self.placa = placa
        self.precio_costo = precio_costo

    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        conn.execute("""
            CREATE TABLE IF NOT EXISTS vehiculos (
                vin TEXT PRIMARY KEY,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                color TEXT NOT NULL,
                anio INTEGER NOT NULL,
                caja TEXT NOT NULL,
                kilometraje INTEGER,
                estado TEXT NOT NULL,
                procedencia TEXT NOT NULL,
                impuesto REAL,
                placa TEXT NOT NULL,
                precio_costo REAL
            );
        """)
        conn.commit()
        return conn

    def guardar(self):
        with Vehiculo._conn() as conn:
            conn.execute(
                """INSERT INTO vehiculos (vin, marca, modelo, color, anio, caja, kilometraje,estado, procedencia, impuesto, placa, precio_costo)VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (self.vin, self.marca, self.modelo, self.color, self.anio, self.caja,self.kilometraje, self.estado, self.procedencia, self.impuesto,self.placa, self.precio_costo))
        print(f"Vehículo '{self.vin}' guardado con éxito.")

    @staticmethod
    def listar():
        with Vehiculo._conn() as conn:
            cur = conn.execute("SELECT * FROM vehiculos ORDER BY marca, modelo, anio DESC")
            return cur.fetchall()

    @staticmethod
    def modificar(vin_original, vehiculo_nuevo: "Vehiculo"):
        with Vehiculo._conn() as conn:
            conn.execute(
                """
                UPDATE vehiculos
                SET vin=?, marca=?, modelo=?, color=?, anio=?, caja=?, kilometraje=?,estado=?, procedencia=?, impuesto=?, placa=?, precio_costo=?WHERE vin=?
            """, (vehiculo_nuevo.vin, vehiculo_nuevo.marca, vehiculo_nuevo.modelo,
                  vehiculo_nuevo.color, vehiculo_nuevo.anio, vehiculo_nuevo.caja,
                  vehiculo_nuevo.kilometraje, vehiculo_nuevo.estado,
                  vehiculo_nuevo.procedencia, vehiculo_nuevo.impuesto,
                  vehiculo_nuevo.placa, vehiculo_nuevo.precio_costo, vin_original))
        print(f"Vehículo '{vin_original}' actualizado con éxito.")

    @staticmethod
    def eliminar(vin):
        with Vehiculo._conn() as conn:
            conn.execute("DELETE FROM vehiculos WHERE vin = ?", (vin,))
        print(f"Vehículo '{vin}' eliminado con éxito.")

class VentanaLogin:
    def __init__(self, master):
        self.ventana = master
        self.ventana.title("Login Autoventas Los Altos")
        self.ventana.geometry("400x500")
        self.ventana.configure(bg="#0D1B2A")

        tk.Label(self.ventana, text="USUARIO", bg="#0D1B2A", fg="white",font=("Arial", 12, "bold")).pack(pady=30)
        self.texto_usuario = tk.Entry(self.ventana, font=("Arial", 14))
        self.texto_usuario.pack()

        tk.Label(self.ventana, text="CONTRASEÑA", bg="#0D1B2A", fg="white",font=("Arial", 12, "bold")).pack(pady=30)
        self.texto_contrasenia = tk.Entry(self.ventana, show="*", font=("Arial", 14))
        self.texto_contrasenia.pack()

        tk.Button(self.ventana, text="Iniciar sesión", command=self.verificar_login, bg="#1B263B", fg="white", font=("Arial", 14, "bold"),width=16).pack(pady=30)

    def verificar_login(self):
        usuario = self.texto_usuario.get()
        contrasenia = self.texto_contrasenia.get()

        if not usuario or not contrasenia:
            messagebox.showwarning("Advertencia", "Llenar usuario y contraseña .")
            return
        fila = Usuario.autenticar(usuario, contrasenia)
        if fila:
            messagebox.showinfo("Acceso", f"Bienvenido {fila['usuario']} ({fila['rol']})")
            self.abrir_menu(fila['rol'])
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos, o no existen jaja.")

    def abrir_menu(self, rol):
        self.ventana.destroy()
        root = tk.Tk()
        VentanaPrincipal(root, rol)
        root.mainloop()

class VentanaPrincipal:
    def __init__(self, principal, rol):
        self.ventana = principal
        self.ventana.title("Menu Autoventas Los Altos")
        self.ventana.geometry("750x450")
        self.ventana.configure(bg="#1B263B")
        self.rol = rol

        principal = tk.Frame(self.ventana, bg="#1B263B")
        principal.pack(fill="both", expand=True, padx=10, pady=10)

        izquerda = tk.Frame(principal, bg="#1B263B")
        izquerda.pack(side="left", fill="y", padx=(10, 30))

        tk.Label(izquerda, text=f"Bienvenido al Sistema ", bg="#1B263B", fg="white",font=("Arial", 14, "bold"), anchor="w").pack(pady=18, anchor="w")

        tk.Button(izquerda, text="Registrar Auto", width=24, bg="#1B263B", fg="white",font=("Arial", 12),command=self.abrir_autos).pack(pady=8, anchor="w")
        tk.Button(izquerda, text="Registrar Proveedor", width=24, font=("Arial", 12),command=self.abrir_proveedor).pack(pady=8, anchor="w")
        tk.Button(izquerda, text="Taller", width=24, font=("Arial", 12),command=self.abrir_taller).pack(pady=8, anchor="w")
        tk.Button(izquerda, text="Registrar Cliente", width=24, font=("Arial", 12), command=self.abrir_cliente).pack(pady=8, anchor="w")
        tk.Button(izquerda, text="Registrar Venta", width=24, font=("Arial", 12),command=self.abrir_venta).pack(pady=8, anchor="w")

        if rol == "Administrador":
            tk.Button(izquerda, text="Usuario", width=24, font=("Arial", 12),command=self.abrir_usuario).pack(pady=8, anchor="w")
        tk.Button(izquerda, text="Salir", width=24, font=("Arial", 12),command=self.ventana.destroy).pack(pady=8, anchor="w")


        derecha = tk.Frame(principal, bg="#1B263B", width=280)
        derecha.pack(side="right", fill="both", expand=True)
        tk.Label(derecha, text="AUTOVENTAS LOS ALTOS", bg="#1B263B", fg="#A0AEC0",font=("Arial", 22, "bold")).pack(expand=True)

    def abrir_autos(self):
        VentanaAutos(self.ventana)

    def abrir_proveedor(self):
        VentanaProveedor(self.ventana)

    def abrir_taller(self):
        VentanaTaller(self.ventana)

    def abrir_cliente(self):
        VentanaCliente(self.ventana)

    def abrir_venta(self):
        VentanaVenta(self.ventana)

    def abrir_usuario(self):
        if self.rol != "Administrador":
            messagebox.showwarning("Permisos", "Solo el Administrador puede acceder jaja.")
            return
        VentanaUsuario(self.ventana)
class VentanaAutos:
    def __init__(self, principal):
        self.ventana = tk.Toplevel(principal)
        self.ventana.title("Registrar Vehículo")
        self.ventana.geometry("1000x560")
        self.ventana.configure(bg="#0D1B2A")

class VentanaProveedor:
    def __init__(self, principal):
        top = tk.Toplevel(principal)
        top.title("Registrar Proveedor")
        top.geometry("750x450")
        top.configure(bg="#0D1B2A")


class VentanaTaller:
    def __init__(self, principal):
        top = tk.Toplevel(principal)
        top.title("Taller")
        top.geometry("750x450")
        top.configure(bg="#0D1B2A")

class VentanaCliente:
    def __init__(self, principal):
        top = tk.Toplevel(principal)
        top.title("Registrar Cliente")
        top.geometry("750x450")
        top.configure(bg="#0D1B2A")


class VentanaVenta:
    def __init__(self, principal):
        top = tk.Toplevel(principal)
        top.title("Registrar Venta")
        top.geometry("750x450")
        top.configure(bg="#0D1B2A")


class VentanaUsuario:
    def __init__(self, principal):
        top = tk.Toplevel(principal)
        top.title("Usuarios (Administrador)")
        top.geometry("750x450")
        top.configure(bg="#0D1B2A")


def main():
    Usuario.admin_principal()
    win = tk.Tk()
    VentanaLogin(win)
    win.mainloop()

if __name__ == "__main__":
    main()