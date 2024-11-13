def controlErrores():
    try:
        dividendo = int(input("Introduce dividendo:"))
        divisor = int(input("Introduce divisor:"))
        resultado = dividendo / divisor
        print(f"Resultado división: {resultado}")
    except ValueError:
        print("Error, debes introducir un número")
    except ZeroDivisionError:
        print("¡¡¡Error!!!. El divisor no puede ser cero")
    finally:
        print("ENTRA")

controlErrores()