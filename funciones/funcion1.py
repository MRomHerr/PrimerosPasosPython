def calcularIVA():
    importe = int(input("Precio del producto: "))
    total = importe* 1.21
    print (f"IVA incluido (21%): {total}")
    return

print("LLAMANDO A LA FUNCIÓN")
calcularIVA()