from modulos.registro.acceso_datos.Registro_dao import RegistroDAOMySQL
from modulos.registro.acceso_datos.dao_factory import RegistroDAOFactory

class MySQLRegistroDAOFactory(RegistroDAOFactory):
    def crear_dao(self):
        return RegistroDAOMySQL()

