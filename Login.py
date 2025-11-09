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
                rol TEXT NOT NULL CHECK(rol IN ('Administrador','Vendedor'))
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
            rol = input(f"Nuevo rol (Administrador/Vendedor) [{fila['rol']}]: ") or fila['rol']
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
                VALUES ('darwinchoma','12345','Administrador')
            """)
            conn.commit()

class VentanaLogin:
    def __init__(self, master):
        self.ventana = master
        self.ventana.title("Login Autoventas")
        self.ventana.resizable(False, False)
        self.ventana.geometry("375x475")
        self.ventana.configure(bg="#0D1B2A")

        self.centrar_ventana(375,475)

        self.logo = tk.PhotoImage(file="icono_usuario.png")

        frame = tk.Frame(self.ventana, bg="#1B263B")
        frame.place(relx=0.5, rely=0.51, anchor="center")

        label_logo = tk.Label(frame, image=self.logo, bg="#1B263B")
        label_logo.image = self.logo
        label_logo.pack(pady=20)

        tk.Label(self.ventana, text="USUARIO", bg="#0D1B2A", fg="white",font=("Arial", 12, "bold")).pack(pady=30)
        self.texto_usuario = tk.Entry(self.ventana, font=("Arial", 14))
        self.texto_usuario.pack()

        tk.Label(self.ventana, text="CONTRASEÑA", bg="#0D1B2A", fg="white",font=("Arial", 12, "bold")).pack(pady=30)
        self.texto_contrasenia = tk.Entry(self.ventana, show="*", font=("Arial", 14))
        self.texto_contrasenia.pack()

        self.mostrar=False
        def mostrar_contrasenia():
            if self.mostrar:
                self.texto_contrasenia.config(show="*")
                boton_ver.config(text="👁️")
                self.mostrar=False
            else:
                self.texto_contrasenia.config(show="")
                boton_ver.config(text="👁️")
                self.mostrar=True

        boton_ver=tk.Button(self.ventana, text=" 👁️", command=mostrar_contrasenia,bg="#0D1B2A", fg="white", font=("Arial", 14))
        boton_ver.pack(pady=30)
        tk.Button(self.ventana, text="Iniciar sesión", command=self.verificar_login,bg="#1B263B", fg="white", font=("Arial", 14, "bold"), width=16).pack(pady=30)

    def verificar_login(self):
        usuario = self.texto_usuario.get()
        contrasenia = self.texto_contrasenia.get()

        if not usuario or not contrasenia:
            messagebox.showwarning("Advertencia", "Ingrese su usuario y contraseña.")
            return

        fila = Usuario.autenticar(usuario, contrasenia)
        if fila:
            nombre_usuario = fila["usuario"]
            rol = fila["rol"]

            messagebox.showinfo("Acceso", f"Bienvenido {nombre_usuario} ({rol})")
            self.abrir_menu(nombre_usuario, rol)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos, o no existen.")

    def abrir_menu(self, nombre_usuario, rol):
        self.ventana.destroy()
        from menuprincipal import VentanaPrincipal
        root = tk.Tk()
        VentanaPrincipal(root, nombre_usuario, rol)
        root.mainloop()

    def centrar_ventana(self, ancho, alto):
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)
        self.ventana.geometry(f'{ancho}x{alto}+{x}+{y}')

def main():
    Usuario.admin_principal()
    win = tk.Tk()
    VentanaLogin(win)
    win.mainloop()
if __name__ == "__main__":
    main()
