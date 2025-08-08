class RegistroSubject:
    def __init__(self):
        self.observadores = []

    def agregar_observador(self, observador):
        if observador not in self.observadores:
            self.observadores.append(observador)

    def quitar_observador(self, observador):
        if observador in self.observadores:
            self.observadores.remove(observador)

    def notificar(self, registro):
        for observador in self.observadores:
            observador.actualizar(registro)
