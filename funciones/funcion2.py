def calcularIVA(importe):
    print (f"Precio del producto: {importe}")
    total = importe* 1.21
    print (f"IVA incluido (21%): {total}")
    return

print("LLAMANDO A LA FUNCIÓN")
calcularIVA(600)