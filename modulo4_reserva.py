from modulo1_logs import ReservaError, registrar_log
from modulo2_cliente import Cliente
from modulo3_servicios import Servicio

# ==========================================
# CLASE RESERVA
# ==========================================
class Reserva:
    def __init__(self, id_reserva, cliente, servicio, duracion):
        # Validamos que los objetos sean del tipo correcto (Integridad del sistema)
        if not isinstance(cliente, Cliente):
            raise ReservaError("El cliente proporcionado no es válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaError("El servicio proporcionado no es válido.")
            
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente" # Estados posibles: Pendiente, Confirmada, Cancelada, Pagada

    def confirmar(self):
        """Cambia el estado de la reserva a Confirmada."""
        if self.estado == "Cancelada":
            raise ReservaError("No se puede confirmar una reserva que ya fue cancelada.")
        self.estado = "Confirmada"
        registrar_log(f"Reserva {self.id_reserva} confirmada para {self.cliente.get_nombre()}", "INFO")

    def cancelar(self):
        """Cancela la reserva."""
        if self.estado == "Pagada":
            raise ReservaError("No se puede cancelar una reserva que ya fue pagada.")
        self.estado = "Cancelada"
        registrar_log(f"Reserva {self.id_reserva} cancelada.", "WARNING")

    def procesar_pago(self):
        """Calcula el costo total y cambia el estado a Pagada."""
        if self.estado != "Confirmada":
            raise ReservaError("La reserva debe estar confirmada antes de procesar el pago.")
        
        try:
            # Aquí usamos el método calcular_costo del servicio (Polimorfismo en acción)
            costo_total = self.servicio.calcular_costo(self.duracion)
            self.estado = "Pagada"
            registrar_log(f"Pago procesado para reserva {self.id_reserva}. Total: ${costo_total}", "INFO")
            return costo_total
        except Exception as e:
            # Si el servicio falla (ej. no está disponible), registramos y lanzamos error
            registrar_log(f"Error al procesar pago de reserva {self.id_reserva}: {e}", "ERROR")
            raise ReservaError(f"No se pudo procesar el pago: {e}")

    def __str__(self):
        return f"Reserva #{self.id_reserva} | Cliente: {self.cliente.get_nombre()} | Servicio: {self.servicio.nombre_servicio} | Estado: {self.estado}"


# ==========================================
# BLOQUE DE PRUEBA (Para verificar que funciona)
# ==========================================
if __name__ == "__main__":
    print("--- Probando el Módulo 4 ---")
    
    # Importamos lo necesario para la prueba
    from modulo3_servicios import ReservaSala

    # 1. Creamos un cliente válido
    cliente1 = Cliente(10, "Laura Torres", "10203040", "laura@correo.com")
    
    # 2. Creamos un servicio
    sala = ReservaSala("Sala de Juntas", 40, 8)
    
    # 3. Creamos la reserva
    reserva1 = Reserva(100, cliente1, sala, 3)
    print(f"Creada: {reserva1}")
    
    # 4. Probamos confirmar y pagar
    try:
        reserva1.confirmar()
        print(f"Estado después de confirmar: {reserva1.estado}")
        
        total_pagar = reserva1.procesar_pago()
        print(f"Estado después de pagar: {reserva1.estado}")
        print(f"Total pagado: ${total_pagar}")
    except ReservaError as e:
        print(f"Error: {e}")

    print("-" * 30)
    
    # 5. Probamos una reserva inválida (intentar pagar sin confirmar)
    reserva2 = Reserva(101, cliente1, sala, 2)
    try:
        reserva2.procesar_pago() # Esto debe fallar
    except ReservaError as e:
        print(f"Error controlado: {e}")