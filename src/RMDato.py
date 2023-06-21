
class RMDato:
  
  nombre = ""
  valor = -1

  def __init__(self,nombre,valor):
     self.nombre = nombre
     self.valor = valor

  def __str__(self):
    return self.nombre + ": " + str(self.valor)