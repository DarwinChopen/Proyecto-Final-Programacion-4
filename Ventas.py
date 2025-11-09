import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime

DB_NAME = "autoventas.db"
class Venta:
    def __init__(self, idventa, vin, id_usuario, tipo_pago, precio_inicial, descuento, precio_final, num_pagos=1):
        self.idventa = idventa
        self.vin = vin
        self.id_usuario = id_usuario
        self.tipo_pago = tipo_pago
        self.precio_inicial = precio_inicial
        self.descuento = descuento
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
                tipo_pago TEXT NOT NULL CHECK(tipo_pago IN ('Contado','Plazos')),
                precio_inicial REAL NOT NULL,
                descuento REAL DEFAULT 0,
                precio_final REAL NOT NULL,
                num_pagos INTEGER DEFAULT 1,
                FOREIGN KEY (vin) REFERENCES vehiculos(vin),
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)
            );
        """)
        conn.commit()
        return conn

    def guardar(self):
        with Venta._conn() as conn:
            cur = conn.execute("""
                INSERT INTO ventas (vin, id_usuario, tipo_pago, precio_inicial, descuento, precio_final, num_pagos)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (self.vin, self.id_usuario, self.tipo_pago, self.precio_inicial, self.descuento, self.precio_final, self.num_pagos))
            self.idventa = cur.lastrowid

    @staticmethod
    def listar(order_by="idventa"):
        with Venta._conn() as conn:
            cur = conn.execute(f"SELECT * FROM ventas ORDER BY {order_by}")
            return cur.fetchall()

    @staticmethod
    def eliminar(idventa):
        with Venta._conn() as conn:
            conn.execute("DELETE FROM ventas WHERE idventa = ?", (idventa,))
            conn.commit()

