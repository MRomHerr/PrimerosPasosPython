from peewee import *
from datetime import date

# Configuración de la base de datos MySQL
db = MySQLDatabase('tienda',  # Nombre de la base de datos
                   user='root',  # Usuario de MySQL
                   password='MRomHerr',  # Contraseña de MySQL
                   host='localhost',  # Dirección del servidor MySQL
                   port=3306)  # Puerto de conexión


# Definición del modelo Cliente
class Cliente(Model):
    codigo_cli = SmallIntegerField(primary_key=True)
    nombre = CharField(max_length=20)
    localidad = CharField(max_length=15, null=True)
    tlf = CharField(max_length=10, null=True)

    class Meta:
        database = db
        table_name = 'clientes'


# Definición del modelo Proveedor
class Proveedor(Model):
    codigo_prov = SmallIntegerField(primary_key=True)
    nombre = CharField(max_length=20)
    localidad = CharField(max_length=15, null=True)
    fecha_alta = DateField(null=True)
    comision = FloatField()  # Corregido: Sin max_digits ni decimal_places

    class Meta:
        database = db
        table_name = 'proveedores'


# Definición del modelo Articulo
class Articulo(Model):
    codarticulo = SmallIntegerField(primary_key=True)
    denominacion = CharField(max_length=25, null=True)
    precio = FloatField()  # Corregido
    stock = SmallIntegerField(null=True)
    zona = CharField(max_length=10, null=True)
    codigo_prov = ForeignKeyField(Proveedor, backref='articulos', on_delete='CASCADE')

    class Meta:
        database = db
        table_name = 'articulos'


# Definición del modelo Compra
class Compra(Model):
    numcompra = SmallIntegerField(primary_key=True)
    codigo_cli = ForeignKeyField(Cliente, backref='compras', on_delete='CASCADE')
    fechacompra = DateField(null=True)

    class Meta:
        database = db
        table_name = 'compras'


# Definición del modelo DetalleCompra
class DetalleCompra(Model):
    numcompra = ForeignKeyField(Compra, backref='detalle', on_delete='CASCADE')
    codarticulo = ForeignKeyField(Articulo, backref='detalle', on_delete='CASCADE')
    unidades = SmallIntegerField()

    class Meta:
        database = db
        table_name = 'detallecompras'
        primary_key = CompositeKey('numcompra', 'codarticulo')


def insertar_datos():
    try:
        # Insertar 3 clientes, usando get_or_create para evitar duplicados
        Cliente.get_or_create(codigo_cli=1, nombre='Juan Perez', localidad='Madrid', tlf='600123456')
        Cliente.get_or_create(codigo_cli=2, nombre='Ana López', localidad='Barcelona', tlf='601987654')
        Cliente.get_or_create(codigo_cli=3, nombre='Carlos Ruiz', localidad='Valencia', tlf='602345678')

        # Insertar 3 proveedores
        Proveedor.get_or_create(codigo_prov=1, nombre='Proveedor A', localidad='Sevilla', fecha_alta=date(2021, 5, 1), comision=5.5)
        Proveedor.get_or_create(codigo_prov=2, nombre='Proveedor B', localidad='Bilbao', fecha_alta=date(2022, 3, 15), comision=4.0)
        Proveedor.get_or_create(codigo_prov=3, nombre='Proveedor C', localidad='Granada', fecha_alta=date(2023, 7, 10), comision=6.0)

        # Insertar 3 artículos
        Articulo.get_or_create(codarticulo=101, denominacion='Laptop', precio=799.99, stock=10, zona='A1', codigo_prov=1)
        Articulo.get_or_create(codarticulo=102, denominacion='Mouse', precio=19.99, stock=100, zona='B1', codigo_prov=2)
        Articulo.get_or_create(codarticulo=103, denominacion='Teclado', precio=49.99, stock=50, zona='C1', codigo_prov=3)

        # Insertar 3 compras
        Compra.get_or_create(numcompra=1001, codigo_cli=1, fechacompra=date(2024, 11, 15))
        Compra.get_or_create(numcompra=1002, codigo_cli=2, fechacompra=date(2024, 11, 16))
        Compra.get_or_create(numcompra=1003, codigo_cli=3, fechacompra=date(2024, 11, 17))

        # Insertar 3 detalles de compra
        DetalleCompra.get_or_create(numcompra=1001, codarticulo=101, unidades=2)
        DetalleCompra.get_or_create(numcompra=1002, codarticulo=102, unidades=5)
        DetalleCompra.get_or_create(numcompra=1003, codarticulo=103, unidades=3)

        print("Datos insertados correctamente.")
    except IntegrityError as e:
        print(f"Error de integridad: {e}")
    except Exception as e:
        print(f"Error: {e}")



# Conexión a la base de datos y creación de tablas
try:
    db.connect()
    print("Conexión exitosa a la base de datos MySQL.")

    # Crear las tablas
    db.create_tables([Cliente, Proveedor, Articulo, Compra, DetalleCompra])
    print("Tablas creadas exitosamente.")

    # Insertar los datos
    insertar_datos()
except Exception as e:
    print(f"Error al crear las tablas o insertar los datos: {e}")
finally:
    db.close()
