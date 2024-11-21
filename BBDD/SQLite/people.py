from peewee import *
from datetime import date
import os

# Ruta personalizada para la base de datos
db_directory = 'C:\\Users\\aludam2\\PycharmProjects\\pythonProject\\BBDD\\SQLite\\'

# Aseguramos que la carpeta exista, si no la creamos
if not os.path.exists(db_directory):
    os.makedirs(db_directory)

# Crear la ruta completa para la base de datos
db_path = os.path.join(db_directory, 'people.db')

# Configuración de la base de datos
db = SqliteDatabase(db_path)

# Definición del modelo persona
class Person(Model):
    name = CharField()  # campo para el nombre
    birthday = DateField()  # campo para la fecha de nacimiento

    class Meta:
        database = db  # especifica la base de datos a usar

# Definición del modelo mascota
class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')  # clave foránea al dueño
    name = CharField()  # campo para el nombre de la mascota
    animal_type = CharField()  # campo para el tipo de animal

    class Meta:
        database = db  # especifica la base de datos a usar

# Intentamos conectar a la base de datos
try:
    db.connect()
    print("Conexión exitosa a la base de datos.")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
    exit()  # Salimos si la conexión falla

# Intentamos crear las tablas, si no existen
try:
    db.create_tables([Person, Pet])
    print("Tablas creadas exitosamente.")
except Exception as e:
    print(f"Error al crear las tablas: {e}")
    db.close()  # Cerramos la conexión en caso de error
    exit()  # Salimos si la creación de tablas falla

# Agregar datos de personas
uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15))
uncle_bob.save()  # guarda bob en la base de datos

# Crear personas usando el método create
grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1))
herb = Person.create(name='Herb', birthday=date(1950, 5, 5))

# Actualizar datos
grandma.name = 'Grandma L.'
grandma.save()  # actualiza el nombre de la abuela en la base de datos

# Agregar mascotas
bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
herb_fido = Pet.create(owner=herb, name='Fido', animal_type='dog')
herb_mittens = Pet.create(owner=herb, name='Mittens', animal_type='cat')
herb_mittens_jr = Pet.create(owner=herb, name='Mittens Jr', animal_type='cat')

# Eliminar una mascota
herb_mittens.delete_instance()  # elimina a mittens de la base de datos

# Cambiar el dueño de una mascota
herb_fido.owner = uncle_bob
herb_fido.save()  # actualiza el dueño de fido en la base de datos

# Consultas

# Obtener un registro único
try:
    grandma = Person.select().where(Person.name == 'Grandma L.').get()
    print(f"Encontrada persona: {grandma.name}")
except Person.DoesNotExist:
    print("Persona no encontrada.")

# Listar todas las personas
print("Listado de personas:")
for person in Person.select():
    print(person.name)

# Listar todos los gatos y sus dueños
print("Listado de gatos y sus dueños:")
query = Pet.select().where(Pet.animal_type == 'cat')
for pet in query:
    print(pet.name, pet.owner.name)

# Consulta optimizada para evitar n+1
print("Listado optimizado de gatos y sus dueños:")
query = (Pet
         .select(Pet, Person)
         .join(Person)
         .where(Pet.animal_type == 'cat'))
for pet in query:
    print(pet.name, pet.owner.name)

# Obtener todas las mascotas de Bob
print("Mascotas de Bob:")
for pet in Pet.select().join(Person).where(Person.name == 'Bob'):
    print(pet.name)

# Otra forma de obtener las mascotas de Bob
print("Mascotas de Bob (otra forma):")
for pet in Pet.select().where(Pet.owner == uncle_bob):
    print(pet.name)

# Ordenar las mascotas de Bob alfabéticamente
print("Mascotas de Bob ordenadas alfabéticamente:")
for pet in Pet.select().where(Pet.owner == uncle_bob).order_by(Pet.name):
    print(pet.name)

# Listar personas ordenadas por fecha de nacimiento descendente
print("Personas ordenadas por fecha de nacimiento (descendente):")
for person in Person.select().order_by(Person.birthday.desc()):
    print(person.name, person.birthday)

# Consulta con expresiones combinadas
d1940 = date(1940, 1, 1)
d1960 = date(1960, 1, 1)
print("Personas nacidas antes de 1940 o después de 1960:")
query = (Person
         .select()
         .where((Person.birthday < d1940) | (Person.birthday > d1960)))
for person in query:
    print(person.name, person.birthday)

# Consulta con rango de fechas
print("Personas nacidas entre 1940 y 1960:")
query = (Person
         .select()
         .where(Person.birthday.between(d1940, d1960)))
for person in query:
    print(person.name, person.birthday)

# Consulta con agregación
print("Cantidad de mascotas por persona:")
query = (Person
         .select(Person, fn.COUNT(Pet.id).alias('pet_count'))
         .join(Pet, JOIN.LEFT_OUTER)
         .group_by(Person)
         .order_by(Person.name))
for person in query:
    print(person.name, person.pet_count, 'pets')

# Consulta con join y manejo de resultados nulos
print("Personas y sus mascotas (manejando resultados nulos):")
query = (Person
         .select(Person, Pet)
         .join(Pet, JOIN.LEFT_OUTER)
         .order_by(Person.name, Pet.name))
for person in query:
    if hasattr(person, 'pet'):
        print(person.name, person.pet.name)
    else:
        print(person.name, 'no pets')

# Uso de prefetch para optimizar consultas relacionadas
print("Uso de prefetch para optimizar consultas:")
query = Person.select().order_by(Person.name).prefetch(Pet)
for person in query:
    print(person.name)
    for pet in person.pets:
        print(' *', pet.name)

# Uso de funciones SQL
print("Personas cuyo primer nombre comienza con 'g':")
expression = fn.Lower(fn.Substr(Person.name, 1, 1)) == 'g'
for person in Person.select().where(expression):
    print(person.name)

# Cerrar la conexión a la base de datos
db.close()
