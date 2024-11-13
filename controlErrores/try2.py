def controlErrores():
    try:
        numero = int(input("Introduce número:"))
        print("Número:",numero)
    except ValueError:
        print ("Error, debes introducir un número")
        controlErrores()

controlErrores()