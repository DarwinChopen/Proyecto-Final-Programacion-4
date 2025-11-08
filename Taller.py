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
        conn = sqlite3.connect(DB_FILE)
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