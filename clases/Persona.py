class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    # Método que devuelve un saludo
    def saludar(self):
        return f"Hola, mi nombre es {self.nombre} y tengo {self.edad} años."