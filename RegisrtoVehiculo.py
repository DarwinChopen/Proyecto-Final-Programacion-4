import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

DB_NAME = "autoventas.db"

class Vehiculo:
    def __init__(self, vin, marca, modelo, color, anio, caja, kilometraje, estado, procedencia, impuesto, placa, precio_costo, vendido=0):
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
        self.vendido = vendido

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
                precio_costo REAL,
                vendido INTEGER DEFAULT 0
            );
        """)
        conn.commit()
        return conn

    def guardar(self):
        with Vehiculo._conn() as conn:
            conn.execute(
                """INSERT INTO vehiculos (vin, marca, modelo, color, anio, caja, kilometraje,estado, procedencia, impuesto, placa, precio_costo, vendido)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (self.vin, self.marca, self.modelo, self.color, self.anio, self.caja, self.kilometraje, self.estado, self.procedencia, self.impuesto, self.placa, self.precio_costo, self.vendido)
            )
        print(f"Vehículo '{self.vin}' guardado con éxito.")

    @staticmethod
    def listar():
        with Vehiculo._conn() as conn:
            cur = conn.execute("SELECT * FROM vehiculos")
            return cur.fetchall()

    @staticmethod
    def modificar(vin_original, vehiculo_nuevo: "Vehiculo"):
        with Vehiculo._conn() as conn:
            cur = conn.execute("SELECT vendido FROM vehiculos WHERE vin = ?", (vin_original,))
            row = cur.fetchone()
            if row and row["vendido"] == 1:
                raise Exception("No se puede editar: vehículo ya está marcado como VENDIDO.")

            conn.execute(
                """
                UPDATE vehiculos
                SET vin=?, marca=?, modelo=?, color=?, anio=?, caja=?, kilometraje=?, estado=?, procedencia=?, impuesto=?, placa=?, precio_costo=?
                WHERE vin=?
                """,
                (vehiculo_nuevo.vin, vehiculo_nuevo.marca, vehiculo_nuevo.modelo,
                 vehiculo_nuevo.color, vehiculo_nuevo.anio, vehiculo_nuevo.caja,
                 vehiculo_nuevo.kilometraje, vehiculo_nuevo.estado,
                 vehiculo_nuevo.procedencia, vehiculo_nuevo.impuesto,
                 vehiculo_nuevo.placa, vehiculo_nuevo.precio_costo, vin_original)
            )
        print(f"Vehículo '{vin_original}' actualizado con éxito.")

    @staticmethod
    def eliminar(vin):
        with Vehiculo._conn() as conn:
            cur = conn.execute("SELECT vendido FROM vehiculos WHERE vin = ?", (vin,))
            row = cur.fetchone()
            if row and row["vendido"] == 1:
                raise Exception("No se puede eliminar: vehículo ya está marcado como VENDIDO.")
            conn.execute("DELETE FROM vehiculos WHERE vin = ?", (vin,))
        print(f"Vehículo '{vin}' eliminado con éxito.")

Dic_MarcasyModelos = {
    "Toyota":     ["Corolla", "Hilux", "Yaris", "RAV4", "Land Crusier", "Tacoma"],
    "Honda":      ["Civic", "Accord", "CR-V", "Fit", "Pilot", "HR-v"],
    "Nissan":     ["Sentra", "Versa", "X-Trail", "Frontier", "Rogue", "Altima"],
    "Mazda":      ["Mazda 2", "Mazda 3", "Mazda 6", "CX-5", "BT-50"],
    "Ford":       ["Fiesta", "Focus", "Ranger", "Escape", "Mustang", "F-150"],
    "Chevrolet":  ["Spark", "Aveo", "Cruze", "Tracker"],
    "Hyundai":    ["Accent", "Elantra", "Tucson", "Santa Fe"],
    "Kia":        ["Rio", "Cerato", "Sportage", "Sorento", "Picanto"],
    "Volkswagen": ["Gol", "Jetta", "Golf", "Tiguan"],
    "Suzuki":     ["Swift", "Vitara", "S-Cross", "Ertiga"],
}
class VentanaAutos:
    def __init__(self, principal):
        self.principal = principal
        self.ventana = tk.Toplevel(principal)
        self.ventana.title("Registrar Vehículo")
        self.ventana.state("zoomed")
        self.ventana.configure(bg="#0D1B2A")

        self.vin_seleccionado = None
        self.modo_edicion = False
        self.vin_vendido = 0

        tk.Label(self.ventana, text="Registro de Vehículos", bg="#0D1B2A", fg="white",font=("Arial", 16, "bold")).pack(pady=8)

        botones_principales = tk.Frame(self.ventana, bg="#0D1B2A")
        botones_principales.pack(fill="both", expand=True, padx=10, pady=8)

        form = tk.Frame(botones_principales, bg="#0D1B2A")
        form.pack(side="left", fill="y", padx=(5, 15))

        tk.Label(form, text="Marca:", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=0, column=0, padx=4, pady=10, sticky="w")
        self.combo_marca = ttk.Combobox(form, state="readonly", width=30, values=sorted(Dic_MarcasyModelos.keys()))
        self.combo_marca.set("— Seleccione marca —")
        self.combo_marca.grid(row=0, column=1, padx=4, pady=10, sticky="w")
        self.combo_marca.bind("<<ComboboxSelected>>", self.actualizar_modelos)

        tk.Label(form, text="Modelo:", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=1, column=0, padx=4, pady=10, sticky="w")
        self.combo_modelo = ttk.Combobox(form, state="readonly", width=30)
        self.combo_modelo.set("— Seleccione modelo —")
        self.combo_modelo.grid(row=1, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="VIN :", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=2, column=0, padx=4, pady=10, sticky="w")
        self.caja_vin = tk.Entry(form, font=("Arial", 11), width=25)
        self.caja_vin.grid(row=2, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="Color:", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=3, column=0, padx=4, pady=10, sticky="w")
        self.combo_color = ttk.Combobox(form, state="readonly", width=30,values=["Rojo", "Negro", "Blanco", "Gris", "Azul", "Plateado", "Verde", "Marron", "Amarillo", "Dorado", "Otro"])
        self.combo_color.set("— Seleccione —")
        self.combo_color.grid(row=3, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="Año:", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=4, column=0, padx=4, pady=10, sticky="w")
        self.combo_anio = ttk.Combobox(form, state="readonly", width=30, values=[str(a) for a in range(1995, 2026)])
        self.combo_anio.set("— Seleccione —")
        self.combo_anio.grid(row=4, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="Caja:", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=5, column=0, padx=4, pady=10, sticky="w")
        self.combo_caja = ttk.Combobox(form, state="readonly", width=30, values=["Manual", "Automática", "Trip Tronic"])
        self.combo_caja.set("— Seleccione —")
        self.combo_caja.grid(row=5, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="Kilometraje (km):", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=6, column=0, padx=4, pady=10, sticky="w")
        self.caja_kilometraje = tk.Entry(form, font=("Arial", 11), width=25)
        self.caja_kilometraje.grid(row=6, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="Estado:", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=7, column=0, padx=4, pady=10, sticky="w")
        self.combo_estado = ttk.Combobox(form, state="readonly", width=30, values=["Bueno", "Desperfecto"])
        self.combo_estado.set("— Seleccione —")
        self.combo_estado.grid(row=7, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="Procedencia:", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=8, column=0, padx=4, pady=10, sticky="w")
        self.combo_procedencia = ttk.Combobox(form, state="readonly", width=30, values=["Nacional", "Importado"])
        self.combo_procedencia.set("— Seleccione —")
        self.combo_procedencia.grid(row=8, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="Impuesto :", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=9, column=0, padx=4, pady=10, sticky="w")
        self.caja_impuesto = tk.Entry(form, font=("Arial", 11), width=25)
        self.caja_impuesto.grid(row=9, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="Placa:", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=10, column=0, padx=4, pady=10, sticky="w")
        self.caja_placa = tk.Entry(form, font=("Arial", 11), width=25)
        self.caja_placa.grid(row=10, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="Precio costo :", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=11, column=0, padx=4, pady=10, sticky="w")
        self.caja_precio = tk.Entry(form, font=("Arial", 11), width=25)
        self.caja_precio.grid(row=11, column=1, padx=4, pady=10, sticky="w")

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

        columnas = ("vin", "marca", "modelo", "color", "anio", "caja", "km", "estado","procedencia", "impuesto", "placa", "precio", "vendido")
        self.tabla = ttk.Treeview(panel_listado, columns=columnas, show="headings", height=18)

        encabezados = {"vin": "VIN", "marca": "Marca", "modelo": "Modelo", "color": "Color","anio": "Año", "caja": "Caja", "km": "Kilometraje", "estado": "Estado","procedencia": "Procedencia", "impuesto": "Impuesto", "placa": "Placa", "precio": "Precio costo", "vendido":"Vendido"}
        for col, txt in encabezados.items():
            self.tabla.heading(col, text=txt)

        anchos = {"vin":140,"marca":110,"modelo":120,"color":80,"anio":60,"caja":90,"km":100,"estado":90,"procedencia":100,"impuesto":90,"placa":90,"precio":100,"vendido":80}
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

        self.btn_guardar = tk.Button(pie, text="Guardar 💾", command=self.boton_guardar,bg="dim grey", fg="white", font=("Arial", 13), width=12)
        self.btn_guardar.pack(side="left", padx=6)

        self.btn_editar = tk.Button(pie, text="Editar 📝", command=self.boton_editar,bg="DodgerBlue4", fg="white", font=("Arial", 13), width=12)
        self.btn_editar.pack(side="left", padx=6)

        self.btn_eliminar = tk.Button(pie, text="Eliminar 🗑️", command=self.boton_eliminar,bg="red4", fg="white", font=("Arial", 13), width=12)
        self.btn_eliminar.pack(side="left", padx=6)

        self.btn_limpiar = tk.Button(pie, text="Limpiar/Cancelar ❌", command=self.boton_limpiar_formulario,bg="dark slate gray", fg="white", font=("Arial", 13), width=12)
        self.btn_limpiar.pack(side="right", padx=6)

        self.btn_salir = tk.Button(pie, text="Salir ↩️", command=self.boton_salir,bg="green", fg="white", font=("Arial", 13), width=12)
        self.btn_salir.pack(side="right", padx=6)

        self.actualizar_estado_botones()

    def actualizar_modelos(self, event=None):
        marca = self.combo_marca.get()
        modelos = Dic_MarcasyModelos.get(marca, [])
        self.combo_modelo["values"] = modelos
        self.combo_modelo.set("— Seleccione modelo —")

    def cargar_listado(self):
        for x in self.tabla.get_children():
            self.tabla.delete(x)
        for c in Vehiculo.listar():
            vendido_txt = "Sí" if (c["vendido"] == 1) else "No"
            self.tabla.insert("", "end", iid=c["vin"], values=(c["vin"], c["marca"], c["modelo"], c["color"] or "", c["anio"] or "",c["caja"] or "", c["kilometraje"] or "", c["estado"] or "",c["procedencia"] or "", c["impuesto"] or "", c["placa"] or "",c["precio_costo"] or "", vendido_txt))

    def seleccionar_fila(self, event=None):
        sel = self.tabla.selection()
        if not sel:
            self.vin_seleccionado = None
            self.modo_edicion = False
            self.vin_vendido = 0
            self.actualizar_estado_botones()
            return

        vin = sel[0].strip().upper()
        vals = self.tabla.item(vin, "values")
        self.vin_seleccionado = vin

        self.combo_marca.set(vals[1])
        self.actualizar_modelos()
        self.combo_modelo.set(vals[2])
        self.caja_vin.config(state="normal")
        self.caja_vin.delete(0, tk.END)
        self.caja_vin.insert(0, vin)
        self.combo_color.set(vals[3] if vals[3] else "— Selecciona —")
        self.combo_anio.set(str(vals[4]) if vals[4] else "— Selecciona —")
        self.combo_caja.set(vals[5] if vals[5] else "— Selecciona —")
        self.caja_kilometraje.delete(0, tk.END)
        self.caja_kilometraje.insert(0, vals[6])
        self.combo_estado.set(vals[7] if vals[7] else "— Selecciona —")
        self.combo_procedencia.set(vals[8] if vals[8] else "— Selecciona —")
        self.caja_impuesto.delete(0, tk.END)
        self.caja_impuesto.insert(0, vals[9])
        self.caja_placa.delete(0, tk.END)
        self.caja_placa.insert(0, vals[10])
        self.caja_precio.delete(0, tk.END)
        self.caja_precio.insert(0, vals[11])
        vendido_val = vals[12] if len(vals) > 12 else "No"
        self.vin_vendido = 1 if str(vendido_val).strip().lower() in ("1", "sí", "si", "yes", "true") else 0

        try:
            self.caja_vin.config(state="disabled")
        except Exception:
            pass

        self.modo_edicion = True
        self.actualizar_estado_botones()

    def leer_formulario(self):
        vin = self.caja_vin.get().strip().upper()
        marca = self.combo_marca.get()
        modelo = self.combo_modelo.get()
        color = self.combo_color.get()
        anio = self.combo_anio.get()
        caja = self.combo_caja.get()
        estado = self.combo_estado.get()
        procedencia = self.combo_procedencia.get()
        km = self.caja_kilometraje.get().strip()
        imp = self.caja_impuesto.get().strip()
        pre = self.caja_precio.get().strip()
        placa = self.caja_placa.get().strip()

        if not vin:
            raise ValueError("El VIN es obligatorio.")
        if marca.startswith("—") or not marca:
            raise ValueError("Selecciona una marca.")
        if modelo.startswith("—") or not modelo:
            raise ValueError("Selecciona un modelo.")
        if color.startswith("—") or not color:
            raise ValueError("Selecciona un color.")
        if anio.startswith("—") or not anio:
            raise ValueError("Selecciona un año.")
        if caja.startswith("—") or not caja:
            raise ValueError("Selecciona tipo de caja.")
        if not km:
            raise ValueError("Ingresa el kilometraje.")
        if estado.startswith("—") or not estado:
            raise ValueError("Selecciona el estado.")
        if procedencia.startswith("—") or not procedencia:
            raise ValueError("Selecciona la procedencia.")
        if not imp:
            raise ValueError("Ingresa el impuesto.")
        if not pre:
            raise ValueError("Ingresa el precio.")

        color = None if color.startswith("—") else color
        anio = None if anio.startswith("—") else int(anio)
        caja = None if caja.startswith("—") else caja
        estado = None if estado.startswith("—") else estado
        procedencia = None if procedencia.startswith("—") else procedencia

        km_norm = km.replace(",", ".")
        imp_norm = imp.replace(",", ".")
        pre_norm = pre.replace(",", ".")

        try:
            kilometraje = int(float(km_norm))
        except ValueError:
            raise ValueError("Kilometraje debe ser un número entero válido.")
        if kilometraje <= 0:
            raise ValueError("El kilometraje debe ser mayor que 0.")

        try:
            impuesto = float(imp_norm)
        except ValueError:
            raise ValueError("Impuesto debe ser un número válido.")
        if impuesto <= 0:
            raise ValueError("El impuesto debe ser mayor que 0.")

        try:
            precio = float(pre_norm)
        except ValueError:
            raise ValueError("Precio debe ser un número válido.")
        if precio <= 0:
            raise ValueError("El precio de costo debe ser mayor que 0.")

        vendido_flag = self.vin_vendido

        return Vehiculo(vin, marca, modelo, color, anio, caja, kilometraje,
                        estado, procedencia, impuesto, placa, precio, vendido_flag)

    def boton_guardar(self):
        if self.modo_edicion:
            messagebox.showinfo("Guardar",
                                "No puedes guardar mientras estás editando un vehículo. Usa 'Editar' para aplicar cambios o 'Limpiar' para cancelar.")
            return
        try:
            v = self.leer_formulario()
            with Vehiculo._conn() as conn:
                cur = conn.execute("SELECT vin FROM vehiculos WHERE UPPER(TRIM(vin)) = ?", (v.vin,))
                if cur.fetchone():
                    messagebox.showerror("Duplicado", f"El VIN '{v.vin}' ya existe.")
                    return
            v.guardar()
        except ValueError as e:
            messagebox.showerror("Validación", str(e))
            return
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar: {e}")
            return

        messagebox.showinfo("Guardado", f"Vehículo '{v.vin}' guardado con éxito.")
        self.cargar_listado()
        self.boton_limpiar_formulario()

    def boton_editar(self):
        if not self.vin_seleccionado:
            messagebox.showwarning("Editar", "Selecciona un vehículo del listado.")
            return

        if self.vin_vendido == 1:
            messagebox.showwarning("Editar", "No se puede editar: vehículo marcado como VENDIDO.")
            return

        if not messagebox.askyesno("Confirmar edición", "¿Deseas aplicar los cambios al vehículo seleccionado?"):
            return

        try:
            v = self.leer_formulario()
            original_vin = self.vin_seleccionado.strip().upper()

            with Vehiculo._conn() as conn:
                cur = conn.execute(
                    "SELECT vin FROM vehiculos WHERE UPPER(TRIM(vin)) = ? AND UPPER(TRIM(vin)) != ?",
                    (v.vin, original_vin)
                )
                if cur.fetchone():
                    messagebox.showerror("Duplicado", f"El VIN '{v.vin}' ya existe en otro vehículo.")
                    return

            Vehiculo.modificar(original_vin, v)
            self.vin_seleccionado = v.vin

        except ValueError as e:
            messagebox.showerror("Validación", str(e))
            return
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al actualizar: {e}")
            return

        messagebox.showinfo("Editado", f"Vehículo '{self.vin_seleccionado}' actualizado con éxito.")
        self.cargar_listado()
        self.modo_edicion = False
        self.tabla.selection_remove(self.tabla.selection())
        self.boton_limpiar_formulario()

    def boton_eliminar(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Eliminar", "Selecciona un vehículo del listado.")
            return
        vin = sel[0]

        if self.vin_vendido == 1:
            messagebox.showwarning("Eliminar", "No se puede eliminar: vehículo marcado como VENDIDO.")
            return

        if not messagebox.askyesno("Confirmar eliminación", f"¿Está seguro de eliminar el vehículo con VIN '{vin}'? Esta acción no se puede deshacer."):
            return
        try:
            Vehiculo.eliminar(vin)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")
            return

        messagebox.showinfo("Eliminado", f"Vehículo '{vin}' eliminado con éxito.")
        self.cargar_listado()
        self.boton_limpiar_formulario()

    def boton_limpiar_formulario(self):
        self.vin_seleccionado = None
        self.modo_edicion = False
        self.vin_vendido = 0
        try:
            self.caja_vin.config(state="normal")
        except Exception:
            pass
        self.combo_marca.set("— Selecciona marca —")
        self.combo_modelo.set("— Selecciona modelo —")
        self.combo_modelo["values"] = ()
        self.combo_color.set("— Selecciona —")
        self.combo_anio.set("— Selecciona —")
        self.combo_caja.set("— Selecciona —")
        self.combo_estado.set("— Selecciona —")
        self.combo_procedencia.set("— Selecciona —")
        for e in (self.caja_vin, self.caja_kilometraje, self.caja_impuesto, self.caja_placa, self.caja_precio):
            e.delete(0, tk.END)
        for item in self.tabla.selection():
            self.tabla.selection_remove(item)
        self.actualizar_estado_botones()

    def boton_salir(self):
        if hasattr(self.principal, "deiconify"):
            try:
                self.principal.deiconify()
            except Exception as e:
                pass
        self.ventana.destroy()

    def actualizar_estado_botones(self):
        if (self.modo_edicion or self.vin_seleccionado) and self.vin_vendido == 0:
            self.btn_guardar.config(state="disabled")
            self.btn_editar.config(state="normal")
            self.btn_eliminar.config(state="normal")
        elif self.vin_vendido == 1:
            self.btn_guardar.config(state="disabled")
            self.btn_editar.config(state="disabled")
            self.btn_eliminar.config(state="disabled")
        else:
            self.btn_guardar.config(state="normal")
            self.btn_editar.config(state="disabled")
            self.btn_eliminar.config(state="disabled")
