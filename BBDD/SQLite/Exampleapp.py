from peewee import *
from datetime import datetime
import os  # importa os para interactuar con el sistema de archivos


DATABASE_PATH = 'C:\\Users\\aludam2\\PycharmProjects\\pythonProject\\BBDD\\SQLite\\Exampleapp.db'

# crea el directorio para la base de datos si no existe
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

# instancia de la base de datos sqlite que se usara para las operaciones
db = SqliteDatabase(DATABASE_PATH)


# clase base para todos los modelos, define que la base de datos usada es 'db'
class BaseModel(Model):
    class Meta:
        database = db


# modelo de la tabla 'user', que representa usuarios con campos para nombre, contraseña, correo y fecha de registro
class User(BaseModel):
    username = CharField(unique=True)  # nombre de usuario, debe ser unico
    password = CharField()  # contraseña del usuario
    email = CharField()  # correo electronico del usuario
    join_date = DateTimeField(default=datetime.now)  # fecha de registro, por defecto es la fecha actual

    # metodo para obtener los usuarios que este usuario sigue
    def following(self):
        return (
            User
            .select()
            .join(Relationship, on=Relationship.to_user)  # une con la tabla de relaciones
            .where(Relationship.from_user == self)  # filtra por el usuario actual
            .order_by(User.username)  # ordena alfabeticamente por nombre de usuario
        )

    # metodo para obtener los seguidores de este usuario
    def followers(self):
        return (
            User
            .select()
            .join(Relationship, on=Relationship.from_user)  # une con la tabla de relaciones
            .where(Relationship.to_user == self)  # filtra por los seguidores del usuario actual
            .order_by(User.username)  # ordena alfabeticamente por nombre de usuario
        )


# modelo de la tabla 'relationship' para gestionar relaciones entre usuarios (quien sigue a quien)
class Relationship(BaseModel):
    from_user = ForeignKeyField(User, backref='relationships', on_delete='CASCADE')  # usuario que sigue a otro
    to_user = ForeignKeyField(User, backref='related_to', on_delete='CASCADE')  # usuario que es seguido

    class Meta:
        indexes = (
            (('from_user', 'to_user'), True),  # define un indice unico en la combinacion de 'from_user' y 'to_user'
        )


# modelo de la tabla 'message', cada mensaje tiene un usuario asociado y un contenido de texto
class Message(BaseModel):
    user = ForeignKeyField(User, backref='messages', on_delete='CASCADE')  # relaciona el mensaje con un usuario
    content = TextField()  # contenido del mensaje
    pub_date = DateTimeField(default=datetime.now)  # fecha de publicacion del mensaje, por defecto la actual


# funcion para crear las tablas en la base de datos
def create_tables():
    with db:  # usa un contexto seguro para las operaciones de base de datos
        db.create_tables([User, Relationship, Message])  # crea las tablas especificadas si no existen


# funcion para insertar datos de ejemplo en la base de datos
def insertar_datos():
    try:
        # inserta usuarios usando get_or_create para evitar duplicados
        User.get_or_create(username="alice", defaults={"password": "pass123", "email": "alice@example.com"})
        User.get_or_create(username="bob", defaults={"password": "pass456", "email": "bob@example.com"})
        User.get_or_create(username="charlie", defaults={"password": "pass789", "email": "charlie@example.com"})

        # inserta relaciones entre usuarios
        Relationship.get_or_create(from_user=User.get(User.username == "alice"),
                                   to_user=User.get(User.username == "bob"))
        Relationship.get_or_create(from_user=User.get(User.username == "bob"),
                                   to_user=User.get(User.username == "charlie"))
        Relationship.get_or_create(from_user=User.get(User.username == "charlie"),
                                   to_user=User.get(User.username == "alice"))

        # inserta mensajes para cada usuario
        Message.get_or_create(user=User.get(User.username == "alice"), defaults={"content": "Hola, soy Alice."})
        Message.get_or_create(user=User.get(User.username == "bob"), defaults={"content": "Hola, soy Bob."})
        Message.get_or_create(user=User.get(User.username == "charlie"), defaults={"content": "Hola, soy Charlie."})

        print("Datos insertados correctamente.")
    except IntegrityError as e:
        print(f"Error de integridad: {e}")  # captura errores de integridad, como duplicados
    except Exception as e:
        print(f"Error: {e}")  # captura cualquier otro error inesperado


# punto de entrada del programa
if __name__ == "__main__":
    create_tables()  # crea las tablas en la base de datos
    print(f"Base de datos creada en: {DATABASE_PATH} y tablas creadas con éxito.")

    db.connect()  # establece la conexion con la base de datos
    try:
        insertar_datos()  # inserta los datos de ejemplo

        # muestra a quien sigue cada usuario y quienes los siguen
        print("\nRelaciones de seguimiento:")
        for user in User.select():
            print(f"\n{user.username} sigue a: {[u.username for u in user.following()]}")
            print(f"{user.username} es seguido por: {[u.username for u in user.followers()]}")

    finally:
        db.close()  # cierra la conexion con la base de datos
