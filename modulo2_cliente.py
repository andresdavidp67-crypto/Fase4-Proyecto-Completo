# Importamos las excepciones y la función de log que creamos en el Módulo 1
from modulo1_logs import ClienteInvalidoError, registrar_log

# ==========================================
# 1. CLASE ABSTRACTA BASE
# ==========================================
class EntidadBase:
    """Clase base para representar entidades generales del sistema."""
    def __init__(self, id_entidad):
        self.id_entidad = id_entidad

# ==========================================
# 2. CLASE CLIENTE (CON VALIDACIONES Y ENCAPSULAMIENTO)
# ==========================================
class Cliente(EntidadBase):
    def __init__(self, id_cliente, nombre, cedula, correo):
        # Llamamos al constructor de la clase padre (EntidadBase)
        super().__init__(id_cliente)
        self.nombre = nombre
        # Usamos doble guion bajo (__) para encapsular (hacer privados) los datos sensibles
        self.__cedula = cedula 
        self.__correo = correo
        
        # Al momento de crear el cliente, validamos que los datos sean correctos
        self.validar_datos()

    def validar_datos(self):
        """Método que verifica que los datos cumplan con las reglas de negocio."""
        # Validación del nombre
        if not self.nombre or len(self.nombre.strip()) == 0:
            registrar_log("Intento de crear cliente sin nombre", "ERROR")
            raise ClienteInvalidoError("El nombre del cliente no puede estar vacío.")
            
        # Validación de la cédula (solo números y mínimo 7 dígitos)
        if not self.__cedula.isdigit() or len(self.__cedula) < 7:
            registrar_log(f"Cédula inválida registrada: {self.__cedula}", "ERROR")
            raise ClienteInvalidoError("La cédula debe tener solo números y al menos 7 dígitos.")
            
        # Validación del correo (que tenga @ y .)
        if "@" not in self.__correo or "." not in self.__correo:
            registrar_log(f"Correo inválido registrado: {self.__correo}", "ERROR")
            raise ClienteInvalidoError("El formato del correo electrónico es inválido.")

    # Métodos GETTERS para poder leer los atributos privados de forma segura
    def get_cedula(self):
        return self.__cedula

    def get_correo(self):
        return self.__correo

    def get_nombre(self):
        return self.nombre

    def __str__(self):
        return f"Cliente: {self.nombre} (ID: {self.id_entidad})"

# ==========================================
# BLOQUE DE PRUEBA (Para verificar que funciona)
# ==========================================
if __name__ == "__main__":
    print("--- Probando el Módulo 2 ---")
    
    # Prueba 1: Cliente correcto
    try:
        cliente_bueno = Cliente(1, "Andrés Paz", "123456789", "andres@correo.com")
        print(f"Éxito: Cliente creado -> {cliente_bueno}")
        registrar_log(f"Cliente {cliente_bueno.get_nombre()} creado exitosamente.", "INFO")
    except ClienteInvalidoError as e:
        print(f"Error inesperado: {e}")

    # Prueba 2: Cliente con cédula inválida (letras)
    try:
        cliente_malo = Cliente(2, "Carlos Ruiz", "ABC123", "carlos@correo.com")
    except ClienteInvalidoError as e:
        print(f"Error controlado (Cédula): {e}")

    # Prueba 3: Cliente con correo inválido
    try:
        cliente_malo2 = Cliente(3, "Ana Gómez", "98765432", "ana_correo_invalido")
    except ClienteInvalidoError as e:
        print(f"Error controlado (Correo): {e}")