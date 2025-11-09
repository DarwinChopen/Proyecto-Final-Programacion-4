import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


DB_NAME = "autoventas.db"

class Venta:
    def __init__(self, idventa, vin, id_usuario, id_cliente, tipo_pago, precio_inicial, ganancia, precio_final, num_pagos=1):
        self.idventa = idventa
        self.vin = vin
        self.id_usuario = id_usuario
        self.id_cliente = id_cliente
        self.tipo_pago = tipo_pago
        self.precio_inicial = precio_inicial
        self.ganancia = ganancia
        self.precio_final = precio_final
        self.num_pagos = num_pagos

    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                idventa INTEGER PRIMARY KEY AUTOINCREMENT,
                vin TEXT NOT NULL,
                id_usuario INTEGER NOT NULL,
                id_cliente TEXT,
                tipo_pago TEXT NOT NULL CHECK(tipo_pago IN ('Contado','Plazos')),
                precio_inicial REAL NOT NULL,
                ganancia REAL DEFAULT 0,
                precio_final REAL NOT NULL,
                num_pagos INTEGER DEFAULT 1,
                FOREIGN KEY (vin) REFERENCES vehiculos(vin),
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
                FOREIGN KEY (id_cliente) REFERENCES clientes(dpi)
            );
        """)
        conn.commit()
        return conn

    def guardar(self):
        with Venta._conn() as conn:
            cur = conn.execute("SELECT IFNULL(vendido,0) as vendido FROM vehiculos WHERE vin = ?", (self.vin,))
            fila = cur.fetchone()
            if fila is None:
                raise Exception(f"Vehículo con VIN '{self.vin}' no encontrado en la base de datos.")
            if fila["vendido"] == 1:
                raise Exception(f"El vehículo con VIN '{self.vin}' ya está marcado como VENDIDO.")

            cur = conn.execute("""
                INSERT INTO ventas (vin, id_usuario, id_cliente, tipo_pago, precio_inicial,ganancia, precio_final, num_pagos)VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.vin, self.id_usuario, self.id_cliente, self.tipo_pago, self.precio_inicial, self.ganancia, self.precio_final,self.num_pagos))
            self.idventa = cur.lastrowid

            conn.execute("UPDATE vehiculos SET vendido = 1 WHERE vin = ?", (self.vin,))
            conn.commit()

    @staticmethod
    def listar(order_by="idventa"):
        with Venta._conn() as conn:
            cur = conn.execute(f"SELECT * FROM ventas ORDER BY {order_by}")
            return cur.fetchall()

    @staticmethod
    def eliminar(idventa):
        with Venta._conn() as conn:
            cur = conn.execute("SELECT vin FROM ventas WHERE idventa = ?", (idventa,))
            fila = cur.fetchone()
            if not fila:
                raise Exception(f"No se encontró la venta con ID {idventa}.")
            vin = fila["vin"]
            conn.execute("DELETE FROM ventas WHERE idventa = ?", (idventa,))
            conn.execute("UPDATE vehiculos SET vendido = 0 WHERE vin = ?", (vin,))
            conn.commit()

class VentanaVentas:
    def __init__(self, principal):
        self.principal = principal
        self.ventana = tk.Toplevel(principal)
        self.ventana.title("Registro de Ventas")
        self.ventana.state("zoomed")
        self.ventana.configure(bg="#0D1B2A")

        self.id_seleccionado = None
        self.modo_edicion = False

        tk.Label(self.ventana, text="Registro de Ventas", bg="#0D1B2A", fg="white", font=("Arial", 16, "bold")).pack(pady=8)

        contenedor = tk.Frame(self.ventana, bg="#0D1B2A")
        contenedor.pack(fill="both", expand=True, padx=8, pady=8)

        form = tk.Frame(contenedor, bg="#0D1B2A")
        form.pack(side="left", fill="y", padx=(4,12))

        tk.Label(form, text="VIN (Vehículo):", bg="#0D1B2A", fg="white", font=("Arial",11), anchor="w").grid(row=0,column=0,padx=4,pady=6,sticky="w")
        self.combo_vin = ttk.Combobox(form, width=30, state="readonly")
        self.combo_vin.grid(row=0,column=1,padx=4,pady=6,sticky="w")
        self.combo_vin.bind("<<ComboboxSelected>>", lambda e: self._on_vin_selected())

        tk.Label(form, text="Vendedor/Usuario:", bg="#0D1B2A", fg="white", font=("Arial",11), anchor="w").grid(row=1,column=0,padx=4,pady=6,sticky="w")
        self.combo_usuario = ttk.Combobox(form, width=30, state="readonly")
        self.combo_usuario.grid(row=1,column=1,padx=4,pady=6,sticky="w")

        tk.Label(form, text="Cliente (DPI):", bg="#0D1B2A", fg="white", font=("Arial",11), anchor="w").grid(row=2,column=0,padx=4,pady=6,sticky="w")
        self.combo_cliente = ttk.Combobox(form, width=30, state="readonly")
        self.combo_cliente.grid(row=2,column=1,padx=4,pady=6,sticky="w")

        tk.Label(form, text="Tipo de pago:", bg="#0D1B2A", fg="white", font=("Arial",11), anchor="w").grid(row=3,column=0,padx=4,pady=6,sticky="w")
        self.combo_pago = ttk.Combobox(form, state="readonly", width=30, values=["Contado","Plazos"])
        self.combo_pago.set("Contado")
        self.combo_pago.grid(row=3,column=1,padx=4,pady=6,sticky="w")
        self.combo_pago.bind("<<ComboboxSelected>>", lambda e: self.actualizar_pago_final())

        tk.Label(form, text="Número de pagos:",bg="#0D1B2A", fg="white", font=("Arial",11), anchor="w").grid(row=4,column=0,padx=4,pady=6,sticky="w")
        self.combo_num_pagos = ttk.Combobox(form, state="disabled", width=30, values=["1", "2", "3", "4", "5"])
        self.combo_num_pagos.set("1")
        self.combo_num_pagos.grid(row=4, column=1, padx=4, pady=6)

        tk.Label(form, text="Precio inicial:", bg="#0D1B2A", fg="white", font=("Arial",11), anchor="w").grid(row=5,column=0,padx=4,pady=6,sticky="w")
        self.caja_precio_inicial = tk.Entry(form, width=25, font=("Arial",11))
        self.caja_precio_inicial.grid(row=5,column=1,padx=4,pady=6,sticky="w")
        self.caja_precio_inicial.bind("<KeyRelease>", lambda e: self.actualizar_pago_final())

        tk.Label(form, text="Ganancia:", bg="#0D1B2A", fg="white", font=("Arial",11), anchor="w").grid(row=6,column=0,padx=4,pady=6,sticky="w")
        self.caja_ganancia = tk.Entry(form, width=25, font=("Arial",11))
        self.caja_ganancia.insert(0,"0")
        self.caja_ganancia.grid(row=6,column=1,padx=4,pady=6,sticky="w")
        self.caja_ganancia.bind("<KeyRelease>", lambda e: self.actualizar_pago_final())

        tk.Label(form, text="Precio final:", bg="#0D1B2A", fg="white", font=("Arial",11), anchor="w").grid(row=7,column=0,padx=4,pady=6,sticky="w")
        self.caja_precio_final = tk.Entry(form, width=25, font=("Arial",11))
        self.caja_precio_final.grid(row=7,column=1,padx=4,pady=6,sticky="w")

        panel_listado = tk.Frame(contenedor, bg="#0D1B2A")
        panel_listado.pack(side="right", fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#0D1B2A", foreground="white", rowheight=25, fieldbackground="#0D1B2A", font=("Arial",10))
        style.configure("Treeview.Heading", background="#1B263B", foreground="white", font=("Arial",10,"bold"))
        style.map("Treeview", background=[("selected","#1E6091")], foreground=[("selected","white")])

        columnas = ("idventa","vin","usuario","tipo_pago","num_pagos","precio_inicial","descuento","precio_final")
        self.tabla = ttk.Treeview(panel_listado, columns=columnas, show="headings", height=18)

        encabezados = {"idventa":"ID","vin":"VIN","usuario":"Usuario","tipo_pago":"Pago","num_pagos":"Pagos","precio_inicial":"Precio Inicial","descuento":"Descuento","precio_final":"Precio Final"}
        anchos = {"idventa":60,"vin":200,"usuario":160,"tipo_pago":80,"num_pagos":60,"precio_inicial":100,"descuento":80,"precio_final":100}

        for col in columnas:
            self.tabla.heading(col,text=encabezados[col])
            self.tabla.column(col,width=anchos[col],anchor="w")

        scroll_y = ttk.Scrollbar(panel_listado, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll_y.set)
        scroll_x = ttk.Scrollbar(panel_listado, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(xscrollcommand=scroll_x.set)

        self.tabla.pack(side="top", fill="both", expand=True, padx=(4,0), pady=(4,0))
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

        pie = tk.Frame(self.ventana, bg="#0D1B2A")
        pie.pack(fill="x", padx=10, pady=6)

        self.btn_guardar = tk.Button(pie, text="Guardar 💾", command=self.boton_guardar, bg="dim grey", fg="white", font=("Arial",12), width=12)
        self.btn_guardar.pack(side="left", padx=6)
        self.btn_eliminar = tk.Button(pie, text="Eliminar 🗑️", command=self.boton_eliminar, bg="red4", fg="white", font=("Arial",12), width=12)
        self.btn_eliminar.pack(side="left", padx=6)
        self.btn_limpiar = tk.Button(pie, text="Limpiar/Cancelar ❌", command=self.boton_limpiar_formulario, bg="dark slate gray", fg="white", font=("Arial",12), width=14)
        self.btn_limpiar.pack(side="right", padx=6)
        self.btn_salir = tk.Button(pie, text="Salir ↩️", command=self.boton_salir, bg="green", fg="white", font=("Arial",12), width=12)
        self.btn_salir.pack(side="right", padx=6)

        self.cargar_vins()
        self.cargar_usuarios()
        self.cargar_clientes()
        self.cargar_listado()
        self.actualizar_pago_final()

    def cargar_vins(self):
        try:
            with sqlite3.connect(DB_NAME) as conn:
                conn.row_factory = sqlite3.Row
                cur = conn.execute(
                    "SELECT vin, marca, modelo, precio_costo, impuesto FROM vehiculos WHERE IFNULL(vendido,0) = 0 ORDER BY vin")
                rows = cur.fetchall()
                vins = [f"{r['vin']} - {r['marca']} - {r['modelo']}" for r in rows]
                self.vehiculos_map = {f"{r['vin']} - {r['marca']} - {r['modelo']}": r for r in rows}
                self.combo_vin["values"] = vins
                if vins:
                    self.combo_vin.set(vins[0])
                else:
                    self.combo_vin.set("")
        except Exception:
            self.combo_vin["values"] = ()
            self.combo_vin.set("")

    def cargar_usuarios(self):
        try:
            with sqlite3.connect(DB_NAME) as conn:
                conn.row_factory = sqlite3.Row
                cur = conn.execute("SELECT id_usuario || ' - ' || usuario as u FROM usuarios ORDER BY usuario")
                usuarios = [r["u"] for r in cur.fetchall()]
                self.combo_usuario["values"] = usuarios
                if usuarios: self.combo_usuario.set(usuarios[0])
        except Exception:
            self.combo_usuario["values"] = ()
            self.combo_usuario.set("")

    def cargar_clientes(self):
        try:
            with sqlite3.connect(DB_NAME) as conn:
                conn.row_factory = sqlite3.Row
                cur = conn.execute("SELECT dpi || ' - ' || nombres || ' ' || apellidos AS c FROM clientes ORDER BY nombres, apellidos")
                clientes = [r["c"] for r in cur.fetchall()]
                self.combo_cliente["values"] = clientes
                if clientes:
                    self.combo_cliente.set(clientes[0])
                else:
                    self.combo_cliente.set("")
        except Exception:
            self.combo_cliente["values"] = ()
            self.combo_cliente.set("")

    def _on_vin_selected(self):
        try:
            key = self.combo_vin.get()
            if hasattr(self, "vehiculos_map") and key in self.vehiculos_map:
                row = self.vehiculos_map[key]
                precio = (row["precio_costo"] or 0) + (row["impuesto"] or 0)

                self.caja_precio_inicial.delete(0, tk.END)
                self.caja_precio_inicial.insert(0, f"{precio:.2f}")
        except Exception:
            pass

        self.actualizar_pago_final()

    def actualizar_pago_final(self):
        tipo = self.combo_pago.get()
        if tipo == "Plazos":
            self.combo_num_pagos.config(state="readonly")
        else:
            self.combo_num_pagos.config(state="disabled")
            self.combo_num_pagos.set("1")

        try:
            precio = float(self.caja_precio_inicial.get() or 0)
            ganancia = float(self.caja_ganancia.get() or 0)
            num_pagos = int(self.combo_num_pagos.get() or 1)

            total = precio + ganancia
            if tipo == "Plazos" and num_pagos > 1:
                recargo = 0.05 * total * num_pagos
                total += recargo

            self.caja_precio_final.config(state="normal")
            self.caja_precio_final.delete(0, tk.END)
            self.caja_precio_final.insert(0, f"{total:.2f}")
            self.caja_precio_final.config(state="readonly")
        except Exception:
            pass

    def cargar_listado(self):
        for x in self.tabla.get_children():
            self.tabla.delete(x)
        for v in Venta.listar():
            usuario_txt = str(v["id_usuario"])
            num_p = v["num_pagos"] if (v["num_pagos"] is not None) else 1
            precio_ini = v["precio_inicial"] if (v["precio_inicial"] is not None) else 0.0
            ganancia = v["ganancia"] if (v["ganancia"] is not None) else 0.0
            precio_fin = v["precio_final"] if (v["precio_final"] is not None) else 0.0
            self.tabla.insert("", "end", iid=str(v["idventa"]),
                               values=(v["idventa"], v["vin"], usuario_txt, v["tipo_pago"], num_p,
                                       f"{precio_ini:.2f}", f"{ganancia:.2f}", f"{precio_fin:.2f}"))
        self.boton_limpiar_formulario()

    def seleccionar_fila(self, event):
        seleccion = self.tabla.focus()
        if not seleccion:
            return
        vals = self.tabla.item(seleccion, "values")
        self.vin_seleccionado = vals[1]
        self.combo_vin.set(vals[1])
        self.combo_usuario.set(vals[2])
        try:
            self.combo_pago.set(vals[3])
            self.combo_num_pagos.set(str(vals[4]))  # ← CORREGIDO
            self.caja_precio_inicial.delete(0, tk.END)
            self.caja_precio_inicial.insert(0, vals[5])
            self.caja_ganancia.delete(0, tk.END)
            self.caja_ganancia.insert(0, vals[6])
            self.caja_precio_final.delete(0, tk.END)
            self.caja_precio_final.insert(0, vals[7])
        except Exception:
            pass
        self.actualizar_pago_final()

    def leer_formulario(self):
        vin_sel = self.combo_vin.get().strip()
        vin = vin_sel.split(" - ")[0] if " - " in vin_sel else vin_sel
        usuario_sel = self.combo_usuario.get().strip()
        id_usuario = int(usuario_sel.split(" - ")[0]) if " - " in usuario_sel else int(usuario_sel) if usuario_sel else 0

        cliente_sel = self.combo_cliente.get().strip() if hasattr(self, "combo_cliente") else ""
        id_cliente = None
        if cliente_sel:
            id_cliente = cliente_sel.split(" - ")[0] if " - " in cliente_sel else cliente_sel

        tipo_pago = self.combo_pago.get()
        num_pagos = int(self.combo_num_pagos.get() or 1)
        precio_inicial = float(self.caja_precio_inicial.get() or 0)
        ganancia = float(self.caja_ganancia.get() or 0)
        precio_final = float(self.caja_precio_final.get() or 0)
        return Venta(None, vin, id_usuario, id_cliente, tipo_pago, precio_inicial, ganancia, precio_final, num_pagos)

    def boton_guardar(self):
        try:
            venta = self.leer_formulario()
            venta.guardar()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        messagebox.showinfo("Guardado", f"Venta registrada con ID {venta.idventa}")
        self.cargar_listado()
        self.cargar_vins()

    def boton_eliminar(self):
        sel = self.tabla.selection()
        if not sel: return
        idventa = int(sel[0])
        if messagebox.askyesno("Eliminar", f"Eliminar venta ID {idventa}?"):
            Venta.eliminar(idventa)
            self.cargar_listado()
            self.cargar_vins()

    def boton_limpiar_formulario(self):
        self.vin_seleccionado = None
        self.combo_vin.set("— Selecciona vehículo —")
        self.combo_usuario.set("— Selecciona usuario —")
        if hasattr(self, "combo_cliente"):
            self.combo_cliente.set("")
        self.combo_pago.set("— Selecciona tipo —")
        self.combo_num_pagos.set("1")
        self.combo_num_pagos.config(state="disabled")
        self.caja_precio_inicial.delete(0, tk.END)
        self.caja_ganancia.delete(0, tk.END)
        self.caja_precio_final.delete(0, tk.END)
        for item in self.tabla.selection():
            self.tabla.selection_remove(item)

    def boton_salir(self):
        if hasattr(self.principal,"deiconify"):
            try: self.principal.deiconify()
            except: pass
        self.ventana.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    VentanaVentas(root)
    root.mainloop()
