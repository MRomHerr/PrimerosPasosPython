import mysql.connector as bd

bd_conexion = bd.connect(host='localhost', port='1521',
                                   user='system', password='MRomHerr', database='hospital')
cursor = bd_conexion.cursor()
try:
    cursor.execute("SELECT apellido,oficio,salario FROM emp")

    for ape, ofi, sal in cursor:
        print("Apellido: " + ape)
        print("Oficio: " + ofi)
        print("Salario: " + str(sal))

except bd_conexion.Error as error:
    print("Error: ",error)

bd_conexion.close()