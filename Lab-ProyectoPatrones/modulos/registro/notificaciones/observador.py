import logging
from abc import ABC, abstractmethod

# Configurar logging para guardar registro en archivo con codificación UTF-8
logging.basicConfig(
    filename="modulos/registro/logs/registro.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

class Observador(ABC):
    @abstractmethod
    def actualizar(self, registro):
        pass

class UsuarioNotificador(Observador):
    def actualizar(self, registro):
        mensaje = f"[Usuario] Se envió alerta al usuario {registro.usuario_email} por su registro negativo."
        print(mensaje)
        logging.info(mensaje)

class AdminNotificador(Observador):
    def actualizar(self, registro):
        mensaje = f"[Admin] Atención: registro negativo registrado de {registro.usuario_email}: '{registro.texto}'"
        print(mensaje)
        logging.info(mensaje)
