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


