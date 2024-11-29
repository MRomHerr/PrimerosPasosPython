from peewee import SqliteDatabase, Model, CharField, DateTimeField, ForeignKeyField, TextField
from datetime import datetime
import os

# Ruta absoluta para la base de datos
DATABASE_PATH = 'C:\\Users\\aludam2\\PycharmProjects\\pythonProject\\BBDD\\SQLite\\example.db'

# Crear directorio si no existe
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

# Instancia de la base de datos
database = SqliteDatabase(DATABASE_PATH)


# Definición del modelo base
class BaseModel(Model):
    class Meta:
        database = database  # Asocia el modelo con la base de datos


# Definición del modelo User
class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField()
    join_date = DateTimeField(default=datetime.now)

    # Método para obtener a quién sigue el usuario
    def following(self):
        return (
            User
            .select()
            .join(Relationship, on=Relationship.to_user)
            .where(Relationship.from_user == self)
            .order_by(User.username)
        )

    # Método para obtener los seguidores del usuario
    def followers(self):
        return (
            User
            .select()
            .join(Relationship, on=Relationship.from_user)
            .where(Relationship.to_user == self)
            .order_by(User.username)
        )


# Definición del modelo Relationship (muchos a muchos)
class Relationship(BaseModel):
    from_user = ForeignKeyField(User, backref='relationships', on_delete='CASCADE')
    to_user = ForeignKeyField(User, backref='related_to', on_delete='CASCADE')

    class Meta:
        indexes = (
            (('from_user', 'to_user'), True),
        )


# Definición del modelo Message (uno a muchos)
class Message(BaseModel):
    user = ForeignKeyField(User, backref='messages', on_delete='CASCADE')
    content = TextField()
    pub_date = DateTimeField(default=datetime.now)


# Función para crear las tablas
def create_tables():
    with database:
        database.create_tables([User, Relationship, Message])


# Conexión y creación de tablas
if __name__ == "__main__":
    create_tables()  # Llama a la función para crear las tablas
    print(f"Base de datos creada en: {DATABASE_PATH} y tablas creadas con éxito.")

    # Ejemplo de uso
    database.connect()
    try:
        user1 = User.create(username="alice", password="1234", email="alice@example.com")
        user2 = User.create(username="bob", password="1234", email="bob@example.com")

        Relationship.create(from_user=user1, to_user=user2)

        print(f"Alice sigue a: {[u.username for u in user1.following()]}")
        print(f"Bob es seguido por: {[u.username for u in user2.followers()]}")
    finally:
        database.close()
