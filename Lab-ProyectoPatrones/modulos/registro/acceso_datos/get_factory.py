from modulos.registro.configuracion.config import cargar_configuracion
from modulos.registro.acceso_datos.Registro_dao import RegistroDAOMySQL, RegistroDAOPostgres

def obtener_dao():
    config = cargar_configuracion()
    motor = config.get("db_engine")
    if motor == "mysql":
        return RegistroDAOMySQL()
    elif motor == "postgres":
        return RegistroDAOPostgres()
    else:
        raise ValueError("Motor de base de datos no soportado")

