from peewee import *
import mysql.connector
import os

# Configuración de la base de datos MySQL
db = MySQLDatabase('tienda',  # Nombre de la base de datos
                   user='root',  # Usuario de MySQL
                   password='MRomHerr',  # Contraseña de MySQL
                   host='localhost',  # Dirección del servidor MySQL
                   port=3306  # Puerto de conexión
                   )


# Función para crear la base de datos si no existe
def create_database_if_not_exists():
    try:
        # Conexión directa usando mysql.connector para crear la base de datos si no existe
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='MRomHerr',
        )
        cursor = conn.cursor()

        # Crear la base de datos si no existe
        cursor.execute("CREATE DATABASE IF NOT EXISTS tienda")
        print("Base de datos 'tienda' creada o ya existente.")

        # Cerrar la conexión
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error al conectar a MySQL: {err}")
        exit()


# Crear la base de datos si no existe
create_database_if_not_exists()

# Conexión y creación de las tablas usando Peewee
try:
    db.connect()
    print("Conexión exitosa a la base de datos MySQL.")

    db.create_tables([Cliente, Proveedor, Articulo, Compra, DetalleCompra])
    print("Tablas creadas exitosamente.")
except Exception as e:
    print(f"Error: {e}")
finally:
    db.close()
