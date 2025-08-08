from datetime import datetime


class RegistroDTO:
    def __init__(self, id=None, nombre="", apellido="", nacimiento=None, email="", contraseña=""):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        # Si nacimiento es string, intenta convertirlo a datetime
        if nacimiento and isinstance(nacimiento, str):
            try:
                self.nacimiento = datetime.strptime(nacimiento, "%Y-%m-%d")
            except ValueError:
                self.nacimiento = nacimiento 
        else:
            self.nacimiento = nacimiento
        self.email = email
        self.contraseña = contraseña

    def __str__(self):
        return f"registro(id={self.id}, nombre={self.nombre}, apellido={self.apellido}, nacimiento={self.nacimiento}, email={self.email}, contraseña={self.contraseña})"

    def __repr__(self):
        return self.__str__()
