from datetime import date
import mysql.connector as bd

"""
Modulo para gestionar operaciones CRUD en la tabla EMP de una base de datos MySQL.
"""


def conectar():
    """
    Establece una conexion con la base de datos MySQL.

    :return: Objeto de conexion a la base de datos.
    """
    return bd.connect(
        host='localhost',
        port='3306',
        user='root',
        password='MRomHerr',
        database='hospital'
    )


def mostrar_empleados(cursor):
    """
    Muestra todos los empleados de la tabla EMP.

    :param cursor: Cursor de la base de datos.
    """
    query = "SELECT * FROM EMP"
    cursor.execute(query)
    empleados = cursor.fetchall()

    print("\nDatos de la tabla EMP:")
    for empleado in empleados:
        print(f"EMP_NO: {empleado[0]}, APELLIDO: {empleado[1]}, OFICIO: {empleado[2]}, "
              f"DIRECCION: {empleado[3]}, FECHA_ALT: {empleado[4]}, SALARIO: {empleado[5]}, "
              f"COMISION: {empleado[6]}, DEPT_NO: {empleado[7]}")


def insertar_empleado(cursor):
    """
    Inserta un nuevo empleado en la tabla EMP.

    :param cursor: Cursor de la base de datos.
    """
    # solicita los datos al usuario
    emp_no = int(input("Introduce el número de empleado (EMP_NO): "))
    apellido = input("Introduce el apellido del empleado: ")
    oficio = input("Introduce el oficio del empleado: ")
    dir_emp = int(input("Introduce el número de director (DIR): "))
    fecha_alt = input("Introduce la fecha de alta (formato YYYY-MM-DD): ")
    salario = float(input("Introduce el salario del empleado: "))
    comision = float(input("Introduce la comisión del empleado: "))
    dept_no = int(input("Introduce el número de departamento (DEPT_NO): "))

    # crea la consulta sql utilizando preparedstatement
    consulta_alta = (
        "INSERT INTO EMP (EMP_NO, APELLIDO, OFICIO, DIR, FECHA_ALT, SALARIO, COMISION, DEPT_NO) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    )

    # prepara los datos para insertar
    datos_empleado = (emp_no, apellido, oficio, dir_emp, fecha_alt, salario, comision, dept_no)

    # ejecuta la consulta de insercion
    cursor.execute(consulta_alta, datos_empleado)


def main():
    """
    Funcion principal que ejecuta el menu de opciones.
    """
    # conecta a la base de datos
    conexion = conectar()
    cursor = conexion.cursor()

    while True:
        # menu de opciones
        print("\nMenú de opciones:")
        print("1. Mostrar los datos de los empleados")
        print("2. Insertar un nuevo empleado")
        print("3. Salir")
        opcion = input("Selecciona una opción (1, 2 o 3): ")

        if opcion == "1":
            mostrar_empleados(cursor)
        elif opcion == "2":
            insertar_empleado(cursor)
            conexion.commit()  # confirma la insercion en la base de datos
            print("Empleado insertado correctamente.")
        elif opcion == "3":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

    # cierra cursor y conexion al salir
    cursor.close()
    conexion.close()


if __name__ == "__main__":
    main()
