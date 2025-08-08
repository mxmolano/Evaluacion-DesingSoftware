from modulos.registro.acceso_datos.Registro_dao import RegistroDAOPostgres
from modulos.registro.acceso_datos.dao_factory import RegistroDAOFactory

class PostgresRegistroDAOFactory(RegistroDAOFactory):
    def crear_dao(self):
        return RegistroDAOPostgres()