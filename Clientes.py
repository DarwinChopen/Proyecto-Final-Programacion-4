import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_FILE = "autoventas.db"


class Cliente:
    def __init__(self, dpi, nombres, apellidos, telefono, departamento, municipio, direccion):
        self.dpi = dpi
        self.nombres = nombres
        self.apellidos = apellidos
        self.telefono = telefono
        self.departamento = departamento
        self.municipio = municipio
        self.direccion = direccion

    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        conn.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                dpi TEXT PRIMARY KEY,
                nombres TEXT NOT NULL,
                apellidos TEXT NOT NULL,
                telefono TEXT,
                departamento TEXT,
                municipio TEXT,
                direccion TEXT
            );
        """)
        conn.commit()
        return conn

    def guardar(self):
        with Cliente._conn() as conn:
            conn.execute(
                "INSERT INTO clientes (dpi, nombres, apellidos, telefono, departamento, municipio, direccion) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (self.dpi, self.nombres, self.apellidos, self.telefono, self.departamento, self.municipio, self.direccion)
            )

    @staticmethod
    def listar():
        with Cliente._conn() as conn:
            cur = conn.execute("SELECT * FROM clientes ORDER BY nombres, apellidos")
            return cur.fetchall()

    @staticmethod
    def modificar(dpi_original, cliente_nuevo: "Cliente"):
        with Cliente._conn() as conn:
            conn.execute(
                """
                UPDATE clientes
                SET dpi=?, nombres=?, apellidos=?, telefono=?, departamento=?, municipio=?, direccion=?
                WHERE dpi=?
                """,
                (cliente_nuevo.dpi, cliente_nuevo.nombres, cliente_nuevo.apellidos, cliente_nuevo.telefono,
                 cliente_nuevo.departamento, cliente_nuevo.municipio, cliente_nuevo.direccion, dpi_original),
            )

    @staticmethod
    def eliminar(dpi):
        with Cliente._conn() as conn:
            conn.execute("DELETE FROM clientes WHERE dpi = ?", (dpi,))

Dic_DepartamentosyMunicipios = {
    "Guatemala": ["Guatemala", "Santa Catarina Pinula", "San José Pinula", "San José del Golfo", "Palencia","Chinautla", "San Pedro Ayampuc", "Mixco", "San Pedro Sacatepéquez", "San Juan Sacatepéquez","Chuarrancho", "Fraijanes", "Amatitlán", "Villa Nueva", "Villa Canales", "San Miguel Petapa"],
    "El Progreso": ["Guastatoya", "Morazán", "San Agustín Acasaguastlán", "San Cristóbal Acasaguastlán","El Jícaro", "Sansare", "Sanarate", "San Antonio La Paz"],
    "Sacatepéquez": ["Antigua Guatemala", "Jocotenango", "Pastores", "Sumpango", "Santo Domingo Xenacoj","Santiago Sacatepéquez", "San Bartolomé Milpas Altas", "San Lucas Sacatepéquez","Santa Lucía Milpas Altas", "Magdalena Milpas Altas", "Santa María de Jesús",    "Ciudad Vieja", "San Miguel Dueñas", "Alotenango", "San Antonio Aguas Calientes",   "Santa Catarina Barahona"],
    "Chimaltenango": ["Chimaltenango", "San José Poaquil", "San Martín Jilotepeque", "Comalapa", "Santa Apolonia","Tecpán Guatemala", "Patzún", "Pochuta", "Patzicía", "Santa Cruz Balanyá","Acatenango", "Yepocapa", "San Andrés Itzapa", "Parramos", "Zaragoza", "El Tejar"],
    "Escuintla": ["Escuintla", "Santa Lucía Cotzumalguapa", "La Democracia", "Siquinalá", "Masagua","Tiquisate", "La Gomera", "Guanagazapa", "San José", "Iztapa", "Palín", "San Vicente Pacaya", "Nueva Concepción"],
    "Santa Rosa": ["Cuilapa", "Barberena", "Santa Rosa de Lima", "Casillas", "San Rafael las Flores","Oratorio", "San Juan Tecuaco", "Chiquimulilla", "Taxisco", "Santa María Ixhuatán", "Guazacapán", "Santa Cruz Naranjo", "Pueblo Nuevo Viñas", "Nueva Santa Rosa" ],
    "Sololá": ["Sololá", "San José Chacayá", "Santa María Visitación", "Santa Lucía Utatlán", "Nahualá","Santa Catarina Ixtahuacán", "Santa Clara La Laguna", "Concepción", "San Andrés Semetabaj","Panajachel", "Santa Catarina Palopó", "San Antonio Palopó", "San Lucas Tolimán","Santa Cruz La Laguna", "San Pablo La Laguna", "San Marcos La Laguna", "San Juan La Laguna","San Pedro La Laguna", "Santiago Atitlán"],
    "Totonicapán": ["Totonicapán", "San Cristóbal Totonicapán", "San Francisco El Alto", "San Andrés Xecul","Momostenango", "Santa María Chiquimula", "Santa Lucía La Reforma", "San Bartolo"],
    "Quetzaltenango": [ "Quetzaltenango", "Salcajá", "Olintepeque", "San Carlos Sija", "Sibilia", "Cabricán", "Cajolá", "San Miguel Sigüilá", "Ostuncalco", "San Mateo", "Concepción Chiquirichapa","San Martín Sacatepéquez", "Almolonga", "Cantel", "Huitán", "Zunil", "Colomba","San Francisco La Unión", "El Palmar", "Coatepeque", "Génova", "Flores Costa Cuca","La Esperanza", "Palestina de Los Altos"],
    "Suchitepéquez": ["Mazatenango", "Cuyotenango", "San Francisco Zapotitlán", "San Bernardino","San José El Ídolo", "Santo Domingo Suchitepéquez", "San Lorenzo", "Samayac", "San Pablo Jocopilas","San Antonio Suchitepéquez", "San Miguel Panán", "San Gabriel", "Chicacao","Patulul", "Santa Bárbara", "San Juan Bautista", "Santo Tomás La Unión", "Zunilito", "Pueblo Nuevo", "Río Bravo"],
    "Retalhuleu": ["Retalhuleu", "San Sebastián", "Santa Cruz Muluá", "San Martín Zapotitlán", "San Felipe","San Andrés Villa Seca", "Champerico", "Nuevo San Carlos", "El Asintal"],
    "San Marcos": ["San Marcos", "San Pedro Sacatepéquez", "San Antonio Sacatepéquez", "Comitancillo","San Miguel Ixtahuacán", "Concepción Tutuapa", "Tacaná", "Sibinal", "Tajumulco","Tejutla", "San Rafael Pie de la Cuesta", "Nuevo Progreso", "El Tumbador", "San José El Rodeo","Malacatán", "Catarina", "Ayutla (Tecún Umán)", "Ocós", "San Pablo", "El Quetzal","La Reforma", "Pajapita", "Ixchiguán", "San José Ojetenam", "San Cristóbal Cucho", "Esquipulas Palo Gordo", "Río Blanco", "San Lorenzo"],
    "Huehuetenango": ["Huehuetenango", "Chiantla", "Malacatancito", "Cuilco", "Nentón", "San Pedro Necta","Jacaltenango", "Soloma", "Ixtahuacán", "Santa Bárbara", "La Libertad", "La Democracia","San Miguel Acatán", "San Rafael La Independencia", "Todos Santos Cuchumatán", "San Juan Atitán","Santa Eulalia", "San Mateo Ixtatán", "Colotenango", "San Sebastián Huehuetenango", "Tectitán","Concepción Huista", "San Juan Ixcoy", "San Antonio Huista", "Santa Cruz Barillas", "Aguacatán", "San Rafael Petzal", "San Gaspar Ixchil", "Santiago Chimaltenango", "Santa Ana Huista"],
    "Quiché": ["Santa Cruz del Quiché", "Chiché", "Chinique", "Zacualpa", "Chajul", "Santo Tomás Chichicastenango","Patzité", "San Antonio Ilotenango", "San Pedro Jocopilas", "Cunén", "San Juan Cotzal","Joyabaj", "Nebaj", "San Andrés Sajcabajá", "Uspantán", "Sacapulas", "San Bartolomé Jocotenango", "Canillá", "Chicamán", "Ixcan", "Pachalum"],
    "Baja Verapaz": ["Salamá", "San Miguel Chicaj", "Rabinal", "Cubulco", "Granados", "Santa Cruz El Chol", "San Jerónimo", "Purulhá"],
    "Alta Verapaz": ["Cobán", "Santa Cruz Verapaz", "San Cristóbal Verapaz", "Tactic", "Tamahú","Tucurú", "Panzós", "Senahú", "San Pedro Carchá", "San Juan Chamelco", "Lanquín","Cahabón", "Chisec", "Fray Bartolomé de las Casas", "Santa Catalina La Tinta", "Raxruhá"],
    "Petén": ["Flores", "San José", "San Benito", "San Andrés", "La Libertad", "San Francisco","Santa Ana", "Dolores", "San Luis", "Sayaxché", "Melchor de Mencos", "Poptún"],
    "Izabal": [ "Puerto Barrios", "Livingston", "El Estor", "Morales", "Los Amates"],
    "Zacapa": ["Zacapa", "Estanzuela", "Río Hondo", "Gualán", "Teculután", "Usumatlán", "Cabañas", "San Diego", "La Unión", "Huité"],
    "Chiquimula": ["Chiquimula", "San José La Arada", "San Juan Ermita", "Jocotán", "Camotán","Olopa", "Esquipulas", "Concepción Las Minas", "Quezaltepeque", "San Jacinto", "Ipala"],
    "Jalapa": ["Jalapa", "San Pedro Pinula", "San Luis Jilotepeque", "San Manuel Chaparrón", "San Carlos Alzatate", "Monjas", "Mataquescuintla"],
    "Jutiapa": ["Jutiapa", "El Progreso", "Santa Catarina Mita", "Agua Blanca", "Asunción Mita","Yupiltepeque", "Atescatempa", "Jerez", "El Adelanto", "Zapotitlán", "Comapa","Jalpatagua", "Conguaco", "Moyuta", "Pasaco", "Quesada"]
}

class VentanaClientes:
    def __init__(self, principal):
        self.principal = principal
        self.ventana = tk.Toplevel(principal)
        self.ventana.title("Registrar Clientes")
        self.ventana.geometry("1200x700")
        self.ventana.configure(bg="#0D1B2A")

        self.dpi_seleccionado = None
        self.modo_edicion = False

        tk.Label(self.ventana, text="Registro de Clientes", bg="#0D1B2A", fg="white", font=("Arial", 16, "bold")).pack(pady=8)

        botones_principales = tk.Frame(self.ventana, bg="#0D1B2A")
        botones_principales.pack(fill="both", expand=True, padx=10, pady=8)

        form = tk.Frame(botones_principales, bg="#0D1B2A")
        form.pack(side="left", fill="y", padx=(4, 14))

        tk.Label(form, text="DPI :", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=0, column=0, padx=4, pady=10, sticky="w")
        self.caja_dpi = tk.Entry(form, font=("Arial", 11), width=30)
        self.caja_dpi.grid(row=0, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="Nombres :", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=1, column=0, padx=4, pady=10, sticky="w")
        self.caja_nombres = tk.Entry(form, font=("Arial", 11), width=30)
        self.caja_nombres.grid(row=1, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="Apellidos :", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=2, column=0, padx=4, pady=10, sticky="w")
        self.caja_apellidos = tk.Entry(form, font=("Arial", 11), width=30)
        self.caja_apellidos.grid(row=2, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="Telefono :", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=3, column=0, padx=4, pady=10, sticky="w")
        self.caja_telefono = tk.Entry(form, font=("Arial", 11), width=30)
        self.caja_telefono.grid(row=3, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="Departamento:", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=4, column=0, padx=4, pady=10, sticky="w")
        self.combo_depa = ttk.Combobox(form, state="readonly", width=38, values=sorted(Dic_DepartamentosyMunicipios.keys()))
        self.combo_depa.set("— Seleccione Departamento —")
        self.combo_depa.grid(row=4, column=1, padx=4, pady=10, sticky="w")
        self.combo_depa.bind("<<ComboboxSelected>>", self.actualizar_municipios)

        tk.Label(form, text="Municipio:", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=5, column=0, padx=4, pady=10, sticky="w")
        self.combo_muni = ttk.Combobox(form, state="readonly", width=38)
        self.combo_muni.set("— Seleccione municipio —")
        self.combo_muni.grid(row=5, column=1, padx=4, pady=10, sticky="w")

        tk.Label(form, text="Direccion :", bg="#0D1B2A", fg="white", font=("Arial", 11), width=18, anchor="w").grid(row=6, column=0, padx=4, pady=10, sticky="w")
        self.caja_direccion = tk.Entry(form, font=("Arial", 11), width=30)
        self.caja_direccion.grid(row=6, column=1, padx=4, pady=10, sticky="w")

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

        columnas = ("dpi", "nombres", "apellidos", "telefono", "departamento", "municipio", "direccion")
        self.tabla = ttk.Treeview(panel_listado, columns=columnas, show="headings", height=18)

        encabezados = {"dpi": "DPI", "nombres": "Nombres", "apellidos": "Apellidos", "telefono": "Teléfono", "departamento": "Departamento", "municipio": "Municipio", "direccion": "Dirección"}
        for col, txt in encabezados.items():
            self.tabla.heading(col, text=txt)

        anchos = {"dpi":140,"nombres":110,"apellidos":120,"telefono":80,"departamento":60,"municipio":90,"direccion":100}
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


    def actualizar_municipios(self, event=None):
        depto = self.combo_depa.get()
        municipios = Dic_DepartamentosyMunicipios.get(depto, [])
        self.combo_muni["values"] = municipios
        self.combo_muni.set("— Seleccione municipio —")

    def cargar_listado(self):
        for x in self.tabla.get_children():
            self.tabla.delete(x)
        for c in Cliente.listar():
            self.tabla.insert("", "end", iid=c["dpi"], values=(c["dpi"], c["nombres"], c["apellidos"], c["telefono"], c["departamento"], c["municipio"], c["direccion"]))
    def seleccionar_fila(self, event=None):
        sel = self.tabla.selection()
        if not sel:
            self.dpi_seleccionado = None
            self.modo_edicion = False
            self.actualizar_estado_botones()
            return
        dpi = sel[0]
        vals = self.tabla.item(dpi, "values")
        self.dpi_seleccionado = vals[0]

        self.caja_dpi.delete(0, tk.END); self.caja_dpi.insert(0, vals[0])
        self.caja_nombres.delete(0, tk.END); self.caja_nombres.insert(0, vals[1])
        self.caja_apellidos.delete(0, tk.END); self.caja_apellidos.insert(0, vals[2])
        self.caja_telefono.delete(0, tk.END); self.caja_telefono.insert(0, vals[3] or "")

        depto = vals[4] or "— Seleccione departamento —"
        muni = vals[5] or "— Seleccione municipio —"
        if depto in Dic_DepartamentosyMunicipios:
            self.combo_depa.set(depto)
            self.actualizar_municipios()
            if muni in Dic_DepartamentosyMunicipios.get(depto, []):
                self.combo_muni.set(muni)
            else:
                self.combo_muni.set("— Seleccione municipio —")
        else:
            self.combo_depa.set("— Seleccione departamento —")
            self.combo_muni.set("— Seleccione municipio —")

        self.caja_direccion.delete(0, tk.END); self.caja_direccion.insert(0, vals[6] or "")
        try:
            self.caja_dpi.config(state="disabled")
        except Exception:
            pass

        self.modo_edicion = True
        self.actualizar_estado_botones()

    def leer_formulario(self):
        dpi = self.caja_dpi.get().strip()
        nombres = self.caja_nombres.get().strip()
        apellidos = self.caja_apellidos.get().strip()
        telefono = self.caja_telefono.get().strip()
        departamento = self.combo_depa.get()
        municipio = self.combo_muni.get()
        direccion = self.caja_direccion.get().strip()

        if not dpi:
            raise ValueError("El DPI es obligatorio.")
        if not nombres:
            raise ValueError("Los nombres son obligatorios.")
        if not apellidos:
            raise ValueError("Los apellidos son obligatorios.")
        if not dpi.isdigit():
            raise ValueError("El DPI debe contener solo dígitos.")
        if not telefono:
            raise ValueError("El Telefono Es Obligatorio.")
        if departamento.startswith("—") or not departamento:
            raise ValueError("Selecciona Departamento.")
        if municipio.startswith("—") or not municipio:
            raise ValueError("Selecciona Municipio.")
        if not direccion:
            raise ValueError("La Direccion es Obligatoria.")

        return Cliente(dpi, nombres, apellidos, telefono, departamento, municipio, direccion)

    def boton_guardar(self):
        if self.modo_edicion:
            messagebox.showinfo("Guardar", "No puedes guardar mientras estás editando un elemento seleccionado. Usa 'Editar' para aplicar cambios o 'Limpiar' para cancelar.")
            return
        try:
            v = self.leer_formulario()
            v.guardar()
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicado", "El DPI ya existe.")
            return
        except ValueError as e:
            messagebox.showerror("Validación", str(e))
            return
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar: {e}")
            return

        messagebox.showinfo("Guardado", f"Cliente '{v.nombres} {v.apellidos}' guardado con éxito.")
        self.cargar_listado()
        self.boton_limpiar_formulario()

    def boton_editar(self):
        if not self.dpi_seleccionado:
            messagebox.showwarning("Editar", "Selecciona un cliente del listado.")
            return
        if not messagebox.askyesno("Confirmar edición", "¿Deseas aplicar los cambios al cliente seleccionado?"):
            return
        try:
            c = self.leer_formulario()
            Cliente.modificar(self.dpi_seleccionado, c)
            self.dpi_seleccionado = c.dpi
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicado", "El nuevo DPI ya existe.")
            return
        except ValueError as e:
            messagebox.showerror("Validación", str(e))
            return
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al actualizar: {e}")
            return

        messagebox.showinfo("Editado", f"Cliente '{self.dpi_seleccionado}' actualizado con éxito.")
        self.cargar_listado()
        self.modo_edicion = False

        self.tabla.selection_remove(self.tabla.selection())
        for item in self.tabla.selection():
            self.tabla.selection_remove(item)
        self.boton_limpiar_formulario()

    def boton_eliminar(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Eliminar", "Selecciona un cliente del listado.")
            return
        dpi = sel[0]
        if not messagebox.askyesno("Confirmar eliminación", f"¿Está seguro de eliminar el cliente con DPI '{dpi}'? Esta acción no se puede deshacer."):
            return
        Cliente.eliminar(dpi)
        messagebox.showinfo("Eliminado", "Cliente eliminado con éxito.")
        self.cargar_listado()
        self.boton_limpiar_formulario()

    def boton_limpiar_formulario(self):
        self.dpi_seleccionado = None
        self.modo_edicion = False
        try:
            self.caja_dpi.config(state="normal")
        except Exception:
            pass
        self.caja_dpi.delete(0, tk.END)
        self.caja_nombres.delete(0, tk.END)
        self.caja_apellidos.delete(0, tk.END)
        self.caja_telefono.delete(0, tk.END)
        self.combo_depa.set("— Seleccione departamento —")
        self.combo_muni.set("— Seleccione municipio —")
        self.combo_muni["values"] = ()
        self.caja_direccion.delete(0, tk.END)

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
        if self.modo_edicion or self.dpi_seleccionado:
            self.btn_guardar.config(state="disabled")
            self.btn_editar.config(state="normal")
            self.btn_eliminar.config(state="normal")
        else:
            self.btn_guardar.config(state="normal")
            self.btn_editar.config(state="disabled")
            self.btn_eliminar.config(state="disabled")
