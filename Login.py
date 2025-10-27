import sqlite3
import tkinter as tk
from tkinter import messagebox

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
            print("\nLISTADO DE USUARIOS")
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
                VALUES ('admin','1234','Administrador')
            """)
            conn.commit()

class VentanaLogin:
    def __init__(self, master):
        self.ventana = master
        self.ventana.title("Login Autoventas")
        self.ventana.geometry("400x500")
        self.ventana.configure(bg="#0D1B2A")

        tk.Label(self.ventana, text="USUARIO", bg="#0D1B2A", fg="white",font=("Arial", 12, "bold")).pack(pady=30)
        self.texto_usuario = tk.Entry(self.ventana, font=("Arial", 14))
        self.texto_usuario.pack()

        tk.Label(self.ventana, text="CONTRASEÑA", bg="#0D1B2A", fg="white",font=("Arial", 12, "bold")).pack(pady=30)
        self.texto_contrasenia = tk.Entry(self.ventana, show="*", font=("Arial", 14))
        self.texto_contrasenia.pack()

        tk.Button(self.ventana, text="Iniciar sesión", command=self.verificar_login,bg="#1B263B", fg="white", font=("Arial", 14, "bold"), width=16).pack(pady=30)

    def verificar_login(self):
        usuario = self.texto_usuario.get()
        contrasenia = self.texto_contrasenia.get()

        if not usuario or not contrasenia:
            messagebox.showwarning("Advertencia", "Ingrese su usuario y contraseña.")
            return

        fila = Usuario.autenticar(usuario, contrasenia)
        if fila:
            messagebox.showinfo("Acceso", f"Bienvenido {fila['usuario']} ({fila['rol']})")
            self.abrir_menu(fila['rol'])
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos, o no existen.")

    def abrir_menu(self, rol):
        self.ventana.destroy()
        from menuprincipal import VentanaPrincipal
        root = tk.Tk()
        VentanaPrincipal(root, rol)
        root.mainloop()

def main():
    Usuario.admin_principal()
    win = tk.Tk()
    VentanaLogin(win)
    win.mainloop()

if __name__ == "__main__":
    main()
