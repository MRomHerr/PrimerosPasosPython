import peewee
import datetime

DDBBhospital = peewee.MySQLDatabase(
    "hospital", host='localhost', port=3306, user='root', password='MRomHerr'
)

class USERS(peewee.Model):
    username = peewee.CharField(unique=True)
    email = peewee.CharField(index=True)
    created_date = peewee.DateTimeField(default=datetime.datetime.now)  # Default value for the date

    class Meta:
        database = DDBBhospital  #connects the USERS model to the 'DDBBhospital' database

if __name__ == '__main__':
    #connect to the database
    DDBBhospital.connect()

    #create the table only if it does not exist
    DDBBhospital.create_tables([USERS], safe=True)  # 'safe=True' ensures the table is only created if it doesn't already exist

    #get user input for username and email
    username_input = input("Enter a username: ")
    email_input = input("Enter an email: ")

    #insert a new user into the USERS table
    new_user = USERS.create(
        username=username_input,
        email=email_input
    )

    print(f"User {new_user.username} created successfully with email {new_user.email}.")
    DDBBhospital.close()
