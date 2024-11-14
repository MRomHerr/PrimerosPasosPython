# Definimos la clase Coche
class Coche:
    # Método constructor (__init__) para inicializar los atributos
    def __init__(self, marca, modelo, año):
        self.marca = marca
        self.modelo = modelo
        self.año = año

    # Un método para mostrar la información del coche
    def mostrar_info(self):
        print(f"Coche: {self.marca} {self.modelo} ({self.año})")

# Crear un objeto de la clase Coche
mi_coche = Coche("Toyota", "Corolla", 2020)

# Llamar al método mostrar_info
mi_coche.mostrar_info()