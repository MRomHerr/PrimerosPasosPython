class Estudiante:
    def __init__(self, nombre, edad, universidad):
        # Crear un objeto de la clase Persona
        self.persona = Persona(nombre, edad)
        self.universidad = universidad

    def mostrar_info(self):
        # Llamar al método saludar de la clase Persona
        print(self.persona.saludar())  # Información de la persona
        # Información adicional del estudiante
        print(f"Estudio en {self.universidad}.")


# Crear un objeto de la clase Estudiante
estudiante = Estudiante("Carlos", 21, "Universidad Nacional")

# Llamar al método mostrar_info
estudiante.mostrar_info()