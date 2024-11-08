import mysql.connector as bd

bd_conexion = bd.connect(host='localhost', port='3306',
                                   user='prueba1', password='prueba1', database='prueba1')
cursor = bd_conexion.cursor()
try:
    cursor.execute("SELECT Codalumno, Nombrealumno, Dirección, Localidad FROM alumno")

    for ID, nombre, direccion, localidad in cursor:
        print("ID: " , str(ID))
        print("Nombre: " , nombre)
        print("Direccion: " , direccion)
        print("Localidad: " , localidad)

except bd_conexion.Error as error:
    print("Error: ",error)

bd_conexion.close()