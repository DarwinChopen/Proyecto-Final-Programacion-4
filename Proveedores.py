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


