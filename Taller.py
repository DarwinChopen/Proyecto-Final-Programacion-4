import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

DB_NAME = "autoventas.db"

class TrabajoTaller:
    def __init__(self, id_taller, vin, nombre_taller, fecha_ingreso, descripcion, precio_costo, estado):
        self.id_taller = id_taller
        self.vin = vin
        self.nombre_taller = nombre_taller
        self.fecha_ingreso = fecha_ingreso or date.today().isoformat()
        self.descripcion = descripcion
        self.precio_costo = precio_costo
        self.estado = estado

    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        conn.execute("""
            CREATE TABLE IF NOT EXISTS taller (
                id_taller INTEGER PRIMARY KEY AUTOINCREMENT,
                vin TEXT NOT NULL,
                nombre_taller TEXT NOT NULL,
                fecha_ingreso TEXT NOT NULL,
                descripcion TEXT,
                precio_costo REAL,
                estado TEXT NOT NULL CHECK(estado IN ('Pendiente','Reparado'))
            );
        """)
        conn.commit()
        return conn

    def guardar(self):
        with TrabajoTaller._conn() as conn:
            cur = conn.execute(
                "INSERT INTO taller (vin, nombre_taller, fecha_ingreso, descripcion, precio_costo, estado) VALUES (?, ?, ?, ?, ?, ?)",
                (self.vin, self.nombre_taller, self.fecha_ingreso, self.descripcion, self.precio_costo, self.estado)
            )
            self.id_taller = cur.lastrowid

    @staticmethod
    def listar(order_by="id_taller", filtro_estado=None):
        with TrabajoTaller._conn() as conn:
            if filtro_estado in ("Pendiente", "Reparado"):
                cur = conn.execute("SELECT * FROM taller WHERE estado = ? ORDER BY " + order_by, (filtro_estado,))
            else:
                cur = conn.execute("SELECT * FROM taller ORDER BY " + order_by)
            return cur.fetchall()

    @staticmethod
    def modificar(id_original, trabajo_nuevo: "TrabajoTaller"):
        with TrabajoTaller._conn() as conn:
            conn.execute("""
                UPDATE taller
                SET vin=?, nombre_taller=?, fecha_ingreso=?, descripcion=?, precio_costo=?, estado=?
                WHERE id_taller=?
            """, (trabajo_nuevo.vin, trabajo_nuevo.nombre_taller, trabajo_nuevo.fecha_ingreso,
                  trabajo_nuevo.descripcion, trabajo_nuevo.precio_costo, trabajo_nuevo.estado, id_original))
            conn.commit()

    @staticmethod
    def eliminar(id_taller):
        with TrabajoTaller._conn() as conn:
            conn.execute("DELETE FROM taller WHERE id_taller = ?", (id_taller,))
            conn.commit()

class VentanaTaller:
    def __init__(self, principal):
        self.principal = principal
        self.ventana = tk.Toplevel(principal)
        self.ventana.title("Taller - Registro de trabajos")
        self.ventana.state("zoomed")
        self.ventana.configure(bg="#0D1B2A")

        self.id_seleccionado = None
        self.modo_edicion = False
        self.filtro_estado = tk.StringVar(value="Todos")

        tk.Label(self.ventana, text="Registro Taller", bg="#0D1B2A", fg="white", font=("Arial", 16, "bold")).pack(pady=8)

        botones_principales = tk.Frame(self.ventana, bg="#0D1B2A")
        botones_principales.pack(fill="both", expand=True, padx=8, pady=8)

        form = tk.Frame(botones_principales, bg="#0D1B2A")
        form.pack(side="left", fill="y", padx=(4, 12))

        tk.Label(form, text="VIN (Vehículo):", bg="#0D1B2A", fg="white", font=("Arial", 11), anchor="w").grid(row=0, column=0, padx=4, pady=6, sticky="w")
        self.combo_vin = ttk.Combobox(form, width=30, state="readonly")
        self.combo_vin.grid(row=0, column=1, padx=4, pady=6, sticky="w")

        tk.Label(form, text="Taller/Responsable:", bg="#0D1B2A", fg="white", font=("Arial", 11), anchor="w").grid(row=1, column=0, padx=4, pady=6, sticky="w")
        self.caja_taller = tk.Entry(form, width=25, font=("Arial", 11))
        self.caja_taller.grid(row=1, column=1, padx=4, pady=6, sticky="w")

        tk.Label(form, text="Fecha ingreso (YYYY-MM-DD):", bg="#0D1B2A", fg="white", font=("Arial", 11), anchor="w").grid(row=2, column=0, padx=4, pady=6, sticky="w")
        self.caja_fecha = tk.Entry(form, width=25, font=("Arial", 11))
        self.caja_fecha.insert(0, date.today().isoformat())
        self.caja_fecha.grid(row=2, column=1, padx=4, pady=6, sticky="w")

        tk.Label(form, text="Estado:", bg="#0D1B2A", fg="white", font=("Arial", 11), anchor="w").grid(row=3, column=0, padx=4, pady=6, sticky="w")
        self.combo_estado = ttk.Combobox(form, state="readonly", width=30, values=["Pendiente", "Reparado"])
        self.combo_estado.set("Pendiente")
        self.combo_estado.grid(row=3, column=1, padx=4, pady=6, sticky="w")

        tk.Label(form, text="Descripción:", bg="#0D1B2A", fg="white", font=("Arial", 11), anchor="w").grid(row=4, column=0, padx=4, pady=6, sticky="nw")
        self.text_descripcion = tk.Text(form, width=28, height=6, font=("Arial", 10))
        self.text_descripcion.grid(row=4, column=1, padx=4, pady=6, sticky="w")

        tk.Label(form, text="Precio costo:", bg="#0D1B2A", fg="white", font=("Arial", 11), anchor="w").grid(row=5, column=0, padx=4, pady=6, sticky="w")
        self.caja_precio = tk.Entry(form, width=25, font=("Arial", 11))
        self.caja_precio.grid(row=5, column=1, padx=4, pady=6, sticky="w")

        tk.Label(form, text="Filtrar estado:", bg="#0D1B2A", fg="white", font=("Arial", 11)).grid(row=6, column=0,padx=4, pady=6, sticky="w")
        combo_filtro = ttk.Combobox(form, textvariable=self.filtro_estado, state="readonly",values=["Todos", "Pendiente", "Reparado"], width=25)
        combo_filtro.grid(row=6, column=1, padx=4, pady=6, sticky="w")
        combo_filtro.bind("<<ComboboxSelected>>", lambda e: self.cargar_listado())

        self.cargar_vins_desperfecto()

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
        columnas = ("id_taller", "vin", "nombre_taller", "fecha_ingreso", "descripcion", "precio_costo", "estado")
        self.tabla = ttk.Treeview(panel_listado, columns=columnas, show="headings", height=18)

        encabezados = {"id_taller": "ID","vin": "VIN", "nombre_taller": "Taller","fecha_ingreso": "Fecha ingreso","descripcion": "Descripción","precio_costo": "Precio costo","estado": "Estado"}
        anchos = {"id_taller": 60,"vin": 200,"nombre_taller": 160,"fecha_ingreso": 110,"descripcion": 260,"precio_costo": 100,"estado": 100
        }
        for col in columnas:
            self.tabla.heading(col, text=encabezados[col])
            self.tabla.column(col, width=anchos[col], anchor="w")

        scroll_y = ttk.Scrollbar(panel_listado, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll_y.set)

        scroll_x = ttk.Scrollbar(panel_listado, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(xscrollcommand=scroll_x.set)

        self.tabla.pack(side="top", fill="both", expand=True, padx=(4, 0), pady=(4, 0))
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

        pie = tk.Frame(self.ventana, bg="#0D1B2A")
        pie.pack(fill="x", padx=10, pady=6)

        self.btn_guardar = tk.Button(pie, text="Guardar 💾", command=self.boton_guardar, bg="dim grey", fg="white", font=("Arial", 12), width=12)
        self.btn_guardar.pack(side="left", padx=6)
        self.btn_editar = tk.Button(pie, text="Editar 📝", command=self.boton_editar, bg="DodgerBlue4", fg="white", font=("Arial", 12), width=12)
        self.btn_editar.pack(side="left", padx=6)
        self.btn_eliminar = tk.Button(pie, text="Eliminar 🗑️", command=self.boton_eliminar, bg="red4", fg="white", font=("Arial", 12), width=12)
        self.btn_eliminar.pack(side="left", padx=6)
        self.btn_limpiar = tk.Button(pie, text="Limpiar/Cancelar ❌", command=self.boton_limpiar_formulario, bg="dark slate gray", fg="white", font=("Arial", 12), width=14)
        self.btn_limpiar.pack(side="right", padx=6)
        self.btn_salir = tk.Button(pie, text="Salir ↩️", command=self.boton_salir, bg="green", fg="white", font=("Arial", 12), width=12)
        self.btn_salir.pack(side="right", padx=6)

        self.cargar_listado()
        self.actualizar_estado_botones()

    def cargar_vins_desperfecto(self):
        try:
            with sqlite3.connect(DB_NAME) as conn:
                conn.row_factory = sqlite3.Row
                cur = conn.execute("SELECT vin FROM vehiculos WHERE lower(trim(estado)) = 'desperfecto' ORDER BY vin")
                vins = [r["vin"] for r in cur.fetchall()]
                if vins:
                    self.combo_vin["values"] = vins
                    self.combo_vin.set(vins[0])
                else:
                    self.combo_vin["values"] = ()
                    self.combo_vin.set("")
                    messagebox.showinfo("Info", "No se encontraron vehículos en estado 'Desperfecto'.")
        except Exception:
            self.combo_vin["values"] = ()
            self.combo_vin.set("")
            messagebox.showwarning("Aviso", "No se encontró la tabla 'vehiculos'. El combo VIN quedó vacío.")

    def conectar(self):
        return TrabajoTaller._conn()

    def cargar_listado(self):
        filtro = self.filtro_estado.get()
        filtro_db = None if filtro == "Todos" else filtro
        for x in self.tabla.get_children():
            self.tabla.delete(x)
        for t in TrabajoTaller.listar(order_by="id_taller", filtro_estado=filtro_db):
            precio = f"{t['precio_costo']:.2f}" if t['precio_costo'] is not None else "0.00"
            self.tabla.insert("", "end", iid=str(t["id_taller"]), values=(t["id_taller"], t["vin"], t["nombre_taller"], t["fecha_ingreso"], t["descripcion"], precio, t["estado"]))
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
        self.id_seleccionado = int(vals[0])
        self.combo_vin.set(vals[1])
        self.caja_taller.delete(0, tk.END); self.caja_taller.insert(0, vals[2])
        self.caja_fecha.delete(0, tk.END); self.caja_fecha.insert(0, vals[3])
        self.text_descripcion.delete("1.0", tk.END); self.text_descripcion.insert("1.0", vals[4] or "")
        self.caja_precio.delete(0, tk.END); self.caja_precio.insert(0, vals[5] or "0.00")
        self.combo_estado.set(vals[6])
        self.modo_edicion = True
        self.actualizar_estado_botones()

    def leer_formulario(self):
        vin = self.combo_vin.get().strip()
        nombre_taller = self.caja_taller.get().strip()
        fecha_ingreso = self.caja_fecha.get().strip()
        descripcion = self.text_descripcion.get("1.0", tk.END).strip()
        precio_txt = self.caja_precio.get().strip() or "0"
        estado = self.combo_estado.get().strip()

        if not vin:
            raise ValueError("El VIN es obligatorio. Seleccione un vehículo del combo.")
        if not nombre_taller:
            raise ValueError("El nombre del taller/responsable es obligatorio.")
        try:
            datetime.strptime(fecha_ingreso, "%Y-%m-%d")
        except Exception:
            raise ValueError("Fecha inválida. Use formato YYYY-MM-DD.")
        try:
            precio = float(precio_txt)
            if precio < 0:
                raise ValueError("El precio costo no puede ser negativo.")
        except ValueError:
            raise ValueError("Precio inválido. Ingrese un número válido.")
        if estado not in ("Pendiente", "Reparado"):
            raise ValueError("Estado inválido.")
        return TrabajoTaller(None, vin, nombre_taller, fecha_ingreso, descripcion, precio, estado)

    def _sync_vehiculo_estado(self, vin, estado):
        try:
            with sqlite3.connect(DB_NAME) as conn:
                if estado == "Reparado":
                    conn.execute("UPDATE vehiculos SET estado = ? WHERE vin = ?", ("Reparado", vin))
                else:
                    conn.execute("UPDATE vehiculos SET estado = ? WHERE vin = ?", ("Desperfecto", vin))
                conn.commit()
        except Exception:
            pass

    def boton_guardar(self):
        if self.modo_edicion:
            messagebox.showinfo("Guardar", "No puedes guardar mientras estás editando. Usa 'Editar' para aplicar cambios o 'Limpiar' para cancelar.")
            return
        try:
            trabajo = self.leer_formulario()
            trabajo.guardar()
            self._sync_vehiculo_estado(trabajo.vin, trabajo.estado)
        except ValueError as e:
            messagebox.showerror("Validación", str(e))
            return
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar: {e}")
            return

        messagebox.showinfo("Guardado", f"Trabajo registrado con ID {trabajo.id_taller}.")
        self.cargar_vins_desperfecto()
        self.cargar_listado()

    def boton_editar(self):
        if not self.id_seleccionado:
            messagebox.showwarning("Editar", "Selecciona un trabajo del listado.")
            return
        if not messagebox.askyesno("Confirmar edición", "¿Deseas aplicar los cambios al trabajo seleccionado?"):
            return
        try:
            trabajo = self.leer_formulario()
            TrabajoTaller.modificar(self.id_seleccionado, trabajo)
            self._sync_vehiculo_estado(trabajo.vin, trabajo.estado)
        except ValueError as e:
            messagebox.showerror("Validación", str(e))
            return
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al actualizar: {e}")
            return

        messagebox.showinfo("Editado", f"Trabajo con ID {self.id_seleccionado} actualizado.")
        self.cargar_vins_desperfecto()
        self.cargar_listado()
        self.modo_edicion = False

    def boton_eliminar(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Eliminar", "Selecciona un trabajo del listado.")
            return
        id_str = sel[0]
        if not messagebox.askyesno("Confirmar eliminación", f"¿Está seguro de eliminar el trabajo con ID '{id_str}'? Esta acción no se puede deshacer."):
            return
        vals = self.tabla.item(id_str, "values")
        vin = vals[1] if vals else None
        TrabajoTaller.eliminar(int(id_str))
        messagebox.showinfo("Eliminado", "Trabajo eliminado con éxito.")
        self.cargar_vins_desperfecto()
        self.cargar_listado()
        self.boton_limpiar_formulario()

    def boton_limpiar_formulario(self):
        self.id_seleccionado = None
        self.modo_edicion = False
        self.combo_vin.set("")
        self.caja_taller.delete(0, tk.END)
        self.caja_fecha.delete(0, tk.END)
        self.caja_fecha.insert(0, date.today().isoformat())
        self.text_descripcion.delete("1.0", tk.END)
        self.caja_precio.delete(0, tk.END)
        self.caja_precio.insert(0, "0.00")
        self.combo_estado.set("Pendiente")
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
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    VentanaTaller(root)
    root.mainloop()