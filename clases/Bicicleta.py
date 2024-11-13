class Bicicleta:
    color = ""
    tamanio = ""
    Vel_max=15
    def __init__(self):
        self.velocidad = 0
    def subirmarcha (self):
        self.velocidad = self.velocidad+1
    def bajarmarcha(self):
        self.velocidad = self.velocidad - 1
    def cambiarVelMax(self,maxVel):
        self.Vel_max = maxVel


mibici = Bicicleta()
print (mibici.velocidad)
mibici.subirmarcha()
mibici.subirmarcha()
print (mibici.velocidad)
mibici.bajarmarcha()
print (mibici.velocidad)
mibici.cambiarVelMax(25)
print (mibici.Vel_max)
