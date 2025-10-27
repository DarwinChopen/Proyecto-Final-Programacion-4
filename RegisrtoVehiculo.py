import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

DB_NAME = "autoventas.db"

class Vehiculo:
    def __init__(self, vin, marca, modelo, color, anio, caja, kilometraje, estado, procedencia, impuesto, placa, precio_costo):
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
                precio_costo REAL
            );
        """)
        conn.commit()
        return conn

    def guardar(self):
        with Vehiculo._conn() as conn:
            conn.execute(
                """INSERT INTO vehiculos (vin, marca, modelo, color, anio, caja, kilometraje,estado, procedencia, impuesto, placa, precio_costo)VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (self.vin, self.marca, self.modelo, self.color, self.anio, self.caja,self.kilometraje, self.estado, self.procedencia, self.impuesto,self.placa, self.precio_costo))
        print(f"Vehículo '{self.vin}' guardado con éxito.")

    @staticmethod
    def listar():
        with Vehiculo._conn() as conn:
            cur = conn.execute("SELECT * FROM vehiculos ORDER BY marca, modelo, anio DESC")
            return cur.fetchall()

    @staticmethod
    def modificar(vin_original, vehiculo_nuevo: "Vehiculo"):
        with Vehiculo._conn() as conn:
            conn.execute(
                """
                UPDATE vehiculos
                SET vin=?, marca=?, modelo=?, color=?, anio=?, caja=?, kilometraje=?,estado=?, procedencia=?, impuesto=?, placa=?, precio_costo=?WHERE vin=?
            """, (vehiculo_nuevo.vin, vehiculo_nuevo.marca, vehiculo_nuevo.modelo,
                  vehiculo_nuevo.color, vehiculo_nuevo.anio, vehiculo_nuevo.caja,
                  vehiculo_nuevo.kilometraje, vehiculo_nuevo.estado,
                  vehiculo_nuevo.procedencia, vehiculo_nuevo.impuesto,
                  vehiculo_nuevo.placa, vehiculo_nuevo.precio_costo, vin_original))
        print(f"Vehículo '{vin_original}' actualizado con éxito.")

    @staticmethod
    def eliminar(vin):
        with Vehiculo._conn() as conn:
            conn.execute("DELETE FROM vehiculos WHERE vin = ?", (vin,))
        print(f"Vehículo '{vin}' eliminado con éxito.")

class VentanaAutos:
    def __init__(self, principal):
        self.ventana = tk.Toplevel(principal)
        self.ventana.title("Registrar Vehículo")
        self.ventana.geometry("1200x560")
        self.ventana.configure(bg="#0D1B2A")

