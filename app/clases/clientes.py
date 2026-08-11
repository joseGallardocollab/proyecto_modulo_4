class Cliente:
    def __init__(self, nombre, email, telefono):
        self.nombre = nombre
        self.__email = email
        self.__telefono = telefono
        self.tipo = "Genérico"

    def set_email(self, email):
        self.__email = email

    def set_telefono(self, telefono):
        self.__telefono = telefono

    def __str__(self):
        return f"{self.tipo} - Cliente: {self.nombre}, Email: {self.__email}, Tel: {self.__telefono}"


class ClienteRegular(Cliente):
    def __init__(self, nombre, email, telefono):
        super().__init__(nombre, email, telefono)
        self.tipo = "Regular"

class ClientePremium(Cliente):
    def __init__(self, nombre, email, telefono):
        super().__init__(nombre, email, telefono)
        self.tipo = "Premium"

class ClienteCorporativo(Cliente):
    def __init__(self, nombre, email, telefono, empresa):
        super().__init__(nombre, email, telefono)
        self.tipo = "Corporativo"
        self.empresa = empresa

#Reutilización de __str__ para las diferentes clases cliente
    def __str__(self):
        return f"{self.tipo} - Cliente: {self.nombre}, Email: {self._Cliente__email}, Tel: {self._Cliente__telefono}, Empresa: {self.empresa}"
