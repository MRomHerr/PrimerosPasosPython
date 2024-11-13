def calcularIVA(importe):
    print (f"Precio del producto: {importe}")
    total = importe* 1.21
    return total


print("LLAMANDO A LA FUNCIÓN")
result=calcularIVA(1000)
print(f"IVA incluido (21%): {result}")