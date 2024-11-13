def calcularIVA(importe):
    total = importe* 1.21
    return importe,total


print("LLAMANDO A LA FUNCIÓN")
precio,result=calcularIVA(2000)

print(f"Precio del producto: {precio}")
print(f"IVA incluido (21%): {result}")