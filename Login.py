import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk



class Usuario:
    def __init__(self, usuario, contrasenia):
        self.usuario = usuario
        self.contrasenia = contrasenia

class Login(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login AutoVentas Los Altos")
        self.geometry("300x500")
        self.configure(bg="#0D1B2A")
        self.resizable(False, False)

        self.usuarios = {}
        self.cargar_usuarios()
        self.guardar_usuarios()

        self.logo = tk.PhotoImage(file="icono_usuario.png")
        tk.Label(self, image=self.logo, bg="white").pack(pady=10)

        tk.Label(self, text="Usuario:", bg="#0D1B2A", fg="white", font=("Arial", 12)).pack(pady=10)
        self.txt_usuario = tk.Entry(self)
        self.txt_usuario.pack(pady=10)
        self.txt_usuario.focus()

        tk.Label(self, text="Contraseña:", bg="#0D1B2A", fg="white", font=("Arial", 12)).pack(pady=10)
        self.txt_contra = tk.Entry(self, show="•")
        self.txt_contra.pack(pady=10)

        tk.Button(self, text="Ingresar", command=self.ingresar, bg="#1B263B", fg="white",font=("Arial", 14)).pack(pady=20)
        tk.Button(self, text="Salir", command=self.destroy, bg="#1B263B", fg="white",font=("Arial", 14)).pack()


    def cargar_usuarios(self):
        try:
            with open("Usuarios.txt", "r", encoding="utf-8") as f:
                for linea in f:
                    linea = linea.strip()
                    if linea:
                        usuario, contra = linea.split(",")
                        self.usuarios[usuario] = Usuario(usuario, contra)
            print("Usuarios importados desde Usuarios.txt")
        except FileNotFoundError:
            print("No existe el archivo Usuarios.txt")

    def guardar_usuarios(self):
        with open("Usuarios.txt", "w", encoding="utf-8") as archivo:
            for u in self.usuarios.values():
                archivo.write(f"{u.usuario},{u.contrasenia}\n")
        print("Usuarios guardados en Usuarios.txt")

    def ingresar(self):
        usuario = self.txt_usuario.get().strip()
        contra = self.txt_contra.get().strip()

        if usuario in self.usuarios and self.usuarios[usuario].contrasenia == contra:
            messagebox.showinfo("Acceso", f"Bienvenido, {usuario}")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
if __name__ == "__main__":
    app = Login()
    app.mainloop()