class Cliente:
    def __init__(self, nombre, email, telefono):
        self.nombre = nombre
        self.__email = email #dato privado
        self.__telefono = telefono #dato privado

    def set_email (self, email):
        self.__email = email

    def set_telefono(self, telefono):
        self.__telefono = telefono

    def __str__(self):
        return f"Cliente: {self.nombre}, Email: {self.__email}, Tel: {self.__telefono}"

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

    def __str__(self):
        return (f"Cliente: {self.nombre}, "
                f"Email: {self._Cliente__email}, "
                f"Tel: {self._Cliente__telefono}, "
                f"Empresa: {self.empresa}")
