import sqlite3

DB_NAME = "autoventas.db"

class Clientes:
    def __init__(self,DPI,NIT, nombres,apellidos, telefono,departamento,municipio,direccion):
        self.DPI=DPI
        self.NIT=NIT
        self.nombres = nombres
        self.apellidos = apellidos
        self.telefono= telefono
        self.departamento=departamento
        self.municipio=municipio
        self.direccion = direccion
    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        conn.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                DPI INTEGER PRIMARY KEY AUTOINCREMENT,
                NIT TEXT NOT NULL,
                nombres TEXT NOT NULL,
                apellidos TEXT NOT NULL,
                telefono INTEGER NOT NULL,
                departamento TEXT NOT NULL,
                municipio TEXT NOT NULL,
                direccion=TEXT NOT NULL
            );
        """)
        conn.commit()
        return conn
    def guardar(self):
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO clientes (DPI,NIT, nombres,apellidos,telefono,departamento,municipio,direccion ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (self.DPI,self.NIT, self.nombres, self.apellidos, self.telefono, self.departamento,self.municipio,self.direccion)
            )
        print(f"Cliente '{self.nombres},{self.apellidos}' guardado con éxito.")

    @staticmethod
    def listar():
        with Clientes._conn() as conn:
            cur = conn.execute("SELECT * FROM clientes")
            filas = cur.fetchall()
            if not filas:
                print("No hay clientes registrados.")
                return
            print("\n--- LISTADO DE CLIENTES ---")
            for f in filas:
                print(f"DPI: {f['DPI']} |NIT: {f['NIT']} | Nombres: {f['nombres']} | Apellidos: {f['apellidos']} | Telefono: {f['telefono']} Departamento: {f['departamento']} |Municipio: {f['municipio']} |Direccion: {f['direccion']} ")

    @staticmethod
    def modificar():
        ide = input("Ingrese DPI del cliente a modificar: ")
        with Clientes._conn() as conn:
            cur = conn.execute("SELECT * FROM clientes WHERE DPI = ?", (ide,))
            fila = cur.fetchone()
            if not fila:
                print("No se encontró el clientes.")
                return
            nombres = input(f"Nuevo nombre [{fila['nombres']}]: ") or fila['nombres']
            apellidos = input(f"Nuevo apellido [{fila['apellidos']}]: ") or fila['apellidos']
            telefono = input(f"Nuevo telefono [{fila['telefono']}]: ") or fila['telefono']
            departamento = input(f"Nuevo departamento [{fila['departamento']}]: ") or fila['departamento']
            municipio = input(f"Nuevo municipio [{fila['municipio']}]: ") or fila['municipio']
            direccion = input(f"Nueva direccion [{fila['direccion']}]: ") or fila['direccion']
            conn.execute("UPDATE Clientes SET nombre=?, apellidos=?, telefono=?,departamento=?,municipio=?,direccion=? WHERE DPI=?",
                         (nombres, apellidos, telefono,departamento,municipio,direccion))
        print("Cliente actualizado con éxito.")

    @staticmethod
    def eliminar():
        ide = input("Ingrese ID del cliente a eliminar: ")
        with Clientes._conn() as conn:
            cur = conn.execute("DELETE clientes WHERE DPI = ?", (ide,))
            if cur.rowcount == 0:
                print("No se encontró el cliente.")
            else:
                print("Cliente eliminado con éxito.")

