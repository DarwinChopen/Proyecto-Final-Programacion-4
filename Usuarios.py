# usuarios.py
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


        self.mostrar = False
        def mostrar_contrasenia():
            if self.mostrar:
                self.caja_contra.config(show="*")
                self.caja_contra2.config(show="*")
                self.mostrar = False
            else:
                self.caja_contra.config(show="")
                self.caja_contra2.config(show="")
                self.mostrar = True
        tk.Button(form, text="👁️‍", command=mostrar_contrasenia, bg="#1B263B", fg="white", font=("Arial", 10)).grid(row=5, column=1, padx=6, pady=6, sticky="w")


        panel_listado = tk.Frame(botones_principales, bg="#0D1B2A")
        panel_listado.pack(side="right", fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#0D1B2A",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#0D1B2A",
                        font=("Arial", 10)
                        )
        style.configure("Treeview.Heading",
                        background="#1B263B",
                        foreground="white",
                        font=("Arial", 10, "bold")
                        )
        style.map("Treeview",
                  background=[("selected", "#1E6091")],
                  foreground=[("selected", "white")]
                  )

        columnas = ("id_usuario", "usuario", "rol")
        self.tabla = ttk.Treeview(panel_listado, columns=columnas, show="headings", height=18)

        encabezados = {"id_usuario": "ID", "usuario": "Usuario", "rol": "Rol"}
        for col, txt in encabezados.items():
            self.tabla.heading(col, text=txt)

        anchos = {"id_usuario": 80, "usuario": 500, "rol": 150}
        for col, w in anchos.items():
            self.tabla.column(col, width=w, anchor="w")


        scroll_y = ttk.Scrollbar(panel_listado, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll_y.set)
        scroll_x = ttk.Scrollbar(panel_listado, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(xscrollcommand=scroll_x.set)

        self.tabla.pack(side="top", fill="both", expand=True, padx=(4, 0), pady=(4, 0))
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

        pie = tk.Frame(self.ventana, bg="#0D1B2A")
        pie.pack(fill="x", padx=10, pady=8)

        self.btn_guardar = tk.Button(pie, text="Guardar 💾", command=self.boton_guardar, bg="dim grey", fg="white", font=("Arial", 13), width=12)
        self.btn_guardar.pack(side="left", padx=6)

        self.btn_editar = tk.Button(pie, text="Editar 📝", command=self.boton_editar, bg="DodgerBlue4", fg="white", font=("Arial", 13), width=12)
        self.btn_editar.pack(side="left", padx=6)

        self.btn_eliminar = tk.Button(pie, text="Eliminar 🗑️", command=self.boton_eliminar, bg="red4", fg="white", font=("Arial", 13), width=12)
        self.btn_eliminar.pack(side="left", padx=6)

        self.btn_limpiar = tk.Button(pie, text="Limpiar/Cancelar ❌", command=self.boton_limpiar_formulario, bg="dark slate gray", fg="white", font=("Arial", 13), width=18)
        self.btn_limpiar.pack(side="right", padx=6)

        self.btn_salir = tk.Button(pie, text="Salir ↩️", command=self.boton_salir, bg="green", fg="white", font=("Arial", 13), width=12)
        self.btn_salir.pack(side="right", padx=6)


        self.cargar_listado()
        self.actualizar_estado_botones()


    def conectar(self):
        return Usuario._conn()

    def cargar_listado(self):
        for x in self.tabla.get_children():
            self.tabla.delete(x)
        with self.conectar() as conn:
            cur = conn.execute("SELECT id_usuario, usuario, rol FROM usuarios ORDER BY id_usuario")
            for fila in cur.fetchall():
                iid = str(fila["id_usuario"])
                self.tabla.insert("", "end", iid=iid, values=(fila["id_usuario"], fila["usuario"], fila["rol"]))
        self.boton_limpiar_formulario()

    def seleccionar_fila(self, event=None):
        sel = self.tabla.selection()
        if not sel:
            self.id_seleccionado = None
            self.modo_edicion = False
            self.actualizar_estado_botones()
            return
        iid = sel[0]
        vals = self.tabla.item(iid, "values")
        self.id_seleccionado = vals[0]


        try:
            self.caja_id.config(state="normal")
            self.caja_id.delete(0, tk.END); self.caja_id.insert(0, vals[0])
            self.caja_id.config(state="disabled")
        except Exception:
            pass

        self.caja_usuario.delete(0, tk.END); self.caja_usuario.insert(0, vals[1])
        self.combo_rol.set(vals[2] or "Vendedor")


        self.caja_contra.delete(0, tk.END)
        self.caja_contra2.delete(0, tk.END)

        self.modo_edicion = True
        self.actualizar_estado_botones()

    def leer_formulario(self):
        usuario = self.caja_usuario.get().strip().lower()
        contra = self.caja_contra.get()
        contra2 = self.caja_contra2.get()
        rol = self.combo_rol.get()

        if not usuario:
            raise ValueError("El usuario es obligatorio.")
        if not contra or contra2:
            raise ValueError("Las Contraseñas con obligatorias")
        if contra or contra2:
            if contra != contra2:
                raise ValueError("Las contraseñas no coinciden.")
            if len(contra) < 5:
                raise ValueError("La contraseña debe tener al menos 4 caracteres.")
        if rol not in ("Administrador", "Vendedor"):
            raise ValueError("Rol inválido.")
        return {"usuario": usuario, "contrasenia": contra, "rol": rol}


    def boton_guardar(self):
        if self.modo_edicion or self.id_seleccionado:
            messagebox.showinfo("Guardar", "No puedes guardar mientras estás editando un elemento seleccionado. Usa 'Editar' para aplicar cambios o 'Limpiar' para cancelar.")
            return
        try:
            data = self.leer_formulario()
        except ValueError as e:
            messagebox.showerror("Validación", str(e))
            return

        try:
            with self.conectar() as conn:
                conn.execute(
                    "INSERT INTO usuarios (usuario, contrasenia, rol) VALUES (?, ?, ?)",
                    (data["usuario"], data["contrasenia"], data["rol"])
                )
                conn.commit()
            messagebox.showinfo("Guardado", f"Usuario '{data['usuario']}' guardado con éxito.")
            self.cargar_listado()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Duplicado/Error", f"No se pudo guardar: {e}")

    def boton_editar(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Editar", "Selecciona un usuario del listado.")
            return
        if not messagebox.askyesno("Confirmar edición", "¿Deseas aplicar los cambios al usuario seleccionado?"):
            return
        try:
            data = self.leer_formulario()
        except ValueError as e:
            messagebox.showerror("Validación", str(e))
            return

        try:
            with self.conectar() as conn:
                if data["contrasenia"]:
                    conn.execute("UPDATE usuarios SET usuario=?, contrasenia=?, rol=? WHERE id_usuario=?",
                                 (data["usuario"], data["contrasenia"], data["rol"], self.id_seleccionado))
                else:
                    conn.execute("UPDATE usuarios SET usuario=?, rol=? WHERE id_usuario=?",
                                 (data["usuario"], data["rol"], self.id_seleccionado))
                conn.commit()
            messagebox.showinfo("Editado", "Usuario actualizado con éxito.")
            self.cargar_listado()
            self.modo_edicion = False
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Duplicado/Error", f"No se pudo actualizar: {e}")

    def boton_eliminar(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Eliminar", "Selecciona un usuario del listado.")
            return

        iid = sel[0]
        valores = self.tabla.item(iid, "values")
        nombre_usuario = valores[1]


        if nombre_usuario.lower() == "admin":
            messagebox.showwarning("Acción no permitida", "El usuario 'admin' no puede eliminarse.")
            return

        if not messagebox.askyesno("Confirmar eliminación",
                                   f"¿Está seguro de eliminar el usuario con ID '{iid}'? Esta acción no se puede deshacer?"):
            return

        with self.conectar() as conn:
            cur = conn.execute("DELETE FROM usuarios WHERE id_usuario = ?", (iid,))
            conn.commit()
            if cur.rowcount == 0:
                messagebox.showwarning("Info", "No se encontró el usuario.")
            else:
                messagebox.showinfo("Eliminado", "Usuario eliminado con éxito.")

            cur = conn.execute("SELECT COUNT(*) FROM usuarios")
            total = cur.fetchone()[0]

            if total == 1:
                conn.execute("DELETE FROM sqlite_sequence WHERE name='usuarios';")
                conn.commit()

        self.cargar_listado()

    def boton_limpiar_formulario(self):
        self.id_seleccionado = None
        self.modo_edicion = False
        try:
            self.caja_id.config(state="normal")
            self.caja_id.delete(0, tk.END)
            self.caja_id.config(state="disabled")
        except Exception:
            pass
        self.caja_usuario.delete(0, tk.END)
        self.caja_contra.delete(0, tk.END)
        self.caja_contra2.delete(0, tk.END)
        self.combo_rol.set("Vendedor")

        for item in self.tabla.selection():
            self.tabla.selection_remove(item)

        self.actualizar_estado_botones()

    def boton_salir(self):
        if hasattr(self.principal, "deiconify"):
            try:
                self.principal.deiconify()
            except Exception:
                pass
        self.ventana.destroy()

    def actualizar_estado_botones(self):
        if self.modo_edicion or self.id_seleccionado:
            self.btn_guardar.config(state="disabled")
            self.btn_editar.config(state="normal")
            self.btn_eliminar.config(state="normal")
        else:
            self.btn_guardar.config(state="normal")
            self.btn_editar.config(state="disabled")
            self.btn_eliminar.config(state="disabled")
