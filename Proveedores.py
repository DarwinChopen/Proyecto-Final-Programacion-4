import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_FILE = "autoventas.db"


class Proveedor:
    def __init__(self, id=None, nombres="", apellidos="", telefono="", direccion="", correo=""):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.telefono = telefono
        self.direccion = direccion
        self.correo = correo

    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        conn.execute("""
            CREATE TABLE IF NOT EXISTS proveedores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombres TEXT NOT NULL,
                apellidos TEXT NOT NULL,
                telefono TEXT NOT NULL,
                direccion TEXT NOT NULL,
                correo TEXT NOT NULL
            );
        """)
        conn.commit()
        return conn

    def guardar(self):
        with Proveedor._conn() as conn:
            cur = conn.execute(
                "INSERT INTO proveedores (nombres, apellidos, telefono, direccion, correo) VALUES (?, ?, ?, ?, ?)",
                (self.nombres, self.apellidos, self.telefono, self.direccion, self.correo)
            )
            self.id = cur.lastrowid

    @staticmethod
    def listar():
        with Proveedor._conn() as conn:
            cur = conn.execute("SELECT * FROM proveedores ORDER BY nombres, apellidos")
            return cur.fetchall()

    @staticmethod
    def modificar(id_original, proveedor_nuevo: "Proveedor"):
        with Proveedor._conn() as conn:
            conn.execute(
                """
                UPDATE proveedores
                SET nombres=?, apellidos=?, telefono=?, direccion=?, correo=?
                WHERE id=?
                """,
                (proveedor_nuevo.nombres, proveedor_nuevo.apellidos, proveedor_nuevo.telefono,
                 proveedor_nuevo.direccion, proveedor_nuevo.correo, id_original),
            )

    @staticmethod
    def eliminar(id):
        with Proveedor._conn() as conn:
            conn.execute("DELETE FROM proveedores WHERE id = ?", (id,))


class VentanaProveedores:
    def __init__(self, principal):
        self.principal = principal
        self.ventana = tk.Toplevel(principal)
        self.ventana.title("Registrar Proveedores")
        self.ventana.geometry("1200x700")
        self.ventana.configure(bg="#0D1B2A")

        self.id_seleccionado = None
        self.modo_edicion = False

        tk.Label(self.ventana, text="Registro de Proveedores", bg="#0D1B2A", fg="white", font=("Arial", 16, "bold")).pack(pady=8)

        botones_principales = tk.Frame(self.ventana, bg="#0D1B2A")
        botones_principales.pack(fill="both", expand=True, padx=10, pady=8)

        form = tk.Frame(botones_principales, bg="#0D1B2A")
        form.pack(side="left", fill="y", padx=(4, 14))

        tk.Label(form, text="Nombres :", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=0, column=0, padx=4, pady=10, sticky="w")
        self.caja_nombres = tk.Entry(form, font=("Arial", 11), width=30)
        self.caja_nombres.grid(row=0, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="Apellidos :", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=1, column=0, padx=4, pady=10, sticky="w")
        self.caja_apellidos = tk.Entry(form, font=("Arial", 11), width=30)
        self.caja_apellidos.grid(row=1, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="Telefono :", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=2, column=0, padx=4, pady=10, sticky="w")
        self.caja_telefono = tk.Entry(form, font=("Arial", 11), width=30)
        self.caja_telefono.grid(row=2, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="Direccion :", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=3, column=0, padx=4, pady=10, sticky="w")
        self.caja_direccion = tk.Entry(form, font=("Arial", 11), width=30)
        self.caja_direccion.grid(row=3, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="Correo :", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=4, column=0, padx=4, pady=10, sticky="w")
        self.caja_correo = tk.Entry(form, font=("Arial", 11), width=30)
        self.caja_correo.grid(row=4, column=1, padx=4, pady=10, sticky="w")

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

        columnas = ("id", "nombres", "apellidos", "telefono", "direccion", "correo")
        self.tabla = ttk.Treeview(panel_listado, columns=columnas, show="headings", height=18)

        encabezados = {"id": "ID", "nombres": "Nombres", "apellidos": "Apellidos", "telefono": "Teléfono", "direccion": "Dirección", "correo": "Correo"}
        for col, txt in encabezados.items():
            self.tabla.heading(col, text=txt)

        anchos = {"id":60,"nombres":150,"apellidos":150,"telefono":100,"direccion":200,"correo":180}
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
        self.cargar_listado()

        pie = tk.Frame(self.ventana, bg="#0D1B2A")
        pie.pack(fill="x", padx=10, pady=8)

        self.btn_guardar = tk.Button(pie, text="Guardar 💾", command=self.boton_guardar, bg="dim grey", fg="white", font=("Arial", 13), width=12)
        self.btn_guardar.pack(side="left", padx=6)

        self.btn_editar = tk.Button(pie, text="Editar 📝", command=self.boton_editar, bg="DodgerBlue4", fg="white", font=("Arial", 13), width=12)
        self.btn_editar.pack(side="left", padx=6)

        self.btn_eliminar = tk.Button(pie, text="Eliminar 🗑️", command=self.boton_eliminar, bg="red4", fg="white", font=("Arial", 13), width=12)
        self.btn_eliminar.pack(side="left", padx=6)

        self.btn_limpiar = tk.Button(pie, text="Limpiar/Cancelar ❌", command=self.boton_limpiar_formulario, bg="dark slate gray", fg="white", font=("Arial", 13), width=12)
        self.btn_limpiar.pack(side="right", padx=6)

        self.btn_salir = tk.Button(pie, text="Salir ↩️", command=self.boton_salir, bg="green", fg="white", font=("Arial", 13), width=12)
        self.btn_salir.pack(side="right", padx=6)

        self.actualizar_estado_botones()

    def cargar_listado(self):
        for x in self.tabla.get_children():
            self.tabla.delete(x)
        for p in Proveedor.listar():
            self.tabla.insert("", "end", iid=str(p["id"]), values=(p["id"], p["nombres"], p["apellidos"], p["telefono"], p["direccion"], p["correo"]))

    def seleccionar_fila(self, event=None):
        sel = self.tabla.selection()
        if not sel:
            self.id_seleccionado = None
            self.modo_edicion = False
            self.actualizar_estado_botones()
            return
        id_str = sel[0]
        vals = self.tabla.item(id_str, "values")
        self.id_seleccionado = int(vals[0])

        self.caja_nombres.delete(0, tk.END); self.caja_nombres.insert(0, vals[1])
        self.caja_apellidos.delete(0, tk.END); self.caja_apellidos.insert(0, vals[2])
        self.caja_telefono.delete(0, tk.END); self.caja_telefono.insert(0, vals[3] or "")
        self.caja_direccion.delete(0, tk.END); self.caja_direccion.insert(0, vals[4] or "")
        self.caja_correo.delete(0, tk.END); self.caja_correo.insert(0, vals[5] or "")

        self.modo_edicion = True
        self.actualizar_estado_botones()

    def leer_formulario(self):
        nombres = self.caja_nombres.get().strip()
        apellidos = self.caja_apellidos.get().strip()
        telefono = self.caja_telefono.get().strip()
        direccion = self.caja_direccion.get().strip()
        correo = self.caja_correo.get().strip()

        if not nombres:
            raise ValueError("Los nombres son obligatorios.")
        if not apellidos:
            raise ValueError("Los apellidos son obligatorios.")
        if not telefono:
            raise ValueError("El teléfono es obligatorio.")
        if not direccion:
            raise ValueError("La dirección es obligatoria.")
        if not correo or "@" not in correo:
            raise ValueError("Correo inválido. Debe contener '@'.")

        return Proveedor(None, nombres, apellidos, telefono, direccion, correo)

    def boton_guardar(self):
        if self.modo_edicion:
            messagebox.showinfo("Guardar", "No puedes guardar mientras estás editando un elemento seleccionado. Usa 'Editar' para aplicar cambios o 'Limpiar' para cancelar.")
            return
        try:
            p = self.leer_formulario()
            p.guardar()
        except ValueError as e:
            messagebox.showerror("Validación", str(e))
            return
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar: {e}")
            return

        messagebox.showinfo("Guardado", f"Proveedor '{p.nombres} {p.apellidos}' guardado con éxito.")
        self.cargar_listado()
        self.boton_limpiar_formulario()

    def boton_editar(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Editar", "Selecciona un proveedor del listado.")
            return
        if not messagebox.askyesno("Confirmar edición", "¿Deseas aplicar los cambios al proveedor seleccionado?"):
            return
        try:
            p_nuevo = self.leer_formulario()
            Proveedor.modificar(self.id_seleccionado, p_nuevo)
        except ValueError as e:
            messagebox.showerror("Validación", str(e))
            return
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al actualizar: {e}")
            return

        messagebox.showinfo("Editado", f"Proveedor con ID '{self.id_seleccionado}' actualizado con éxito.")
        self.cargar_listado()
        self.modo_edicion = False
        for item in self.tabla.selection():
            self.tabla.selection_remove(item)
        self.boton_limpiar_formulario()

    def boton_eliminar(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Eliminar", "Selecciona un proveedor del listado.")
            return
        id_str = sel[0]
        if not messagebox.askyesno("Confirmar eliminación", f"¿Está seguro de eliminar el proveedor con ID '{id_str}'? Esta acción no se puede deshacer."):
            return
        Proveedor.eliminar(int(id_str))
        messagebox.showinfo("Eliminado", "Proveedor eliminado con éxito.")
        self.cargar_listado()
        self.boton_limpiar_formulario()

    def boton_limpiar_formulario(self):
        self.id_seleccionado = None
        self.modo_edicion = False
        self.caja_nombres.delete(0, tk.END)
        self.caja_apellidos.delete(0, tk.END)
        self.caja_telefono.delete(0, tk.END)
        self.caja_direccion.delete(0, tk.END)
        self.caja_correo.delete(0, tk.END)

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
