from abc import ABC, abstractmethod
# Importamos la excepción de nuestro Módulo 1
from modulo1_logs import ServicioNoDisponibleError, registrar_log

# ==========================================
# 1. CLASE ABSTRACTA BASE
# ==========================================
class Servicio(ABC):
    def __init__(self, nombre_servicio, tarifa_base, disponible=True):
        self.nombre_servicio = nombre_servicio
        self.tarifa_base = tarifa_base
        self.disponible = disponible

    @abstractmethod
    def calcular_costo(self, duracion, *args, **kwargs):
        """Método abstracto que debe ser implementado por las clases hijas."""
        pass

    @abstractmethod
    def obtener_descripcion(self):
        """Método abstracto para describir el servicio."""
        pass

    def validar_disponibilidad(self):
        """Método general para validar si el servicio se puede usar."""
        if not self.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre_servicio}' no está disponible en este momento.")


# ==========================================
# 2. CLASES DERIVADAS (HERENCIA Y POLIMORFISMO)
# ==========================================

class ReservaSala(Servicio):
    def __init__(self, nombre_servicio, tarifa_base, capacidad_personas):
        super().__init__(nombre_servicio, tarifa_base)
        self.capacidad_personas = capacidad_personas

    def obtener_descripcion(self):
        return f"Sala de estudio: {self.nombre_servicio} (Capacidad: {self.capacidad_personas} personas). Tarifa base: ${self.tarifa_base}/hora."

    def calcular_costo(self, duracion, *args, **kwargs):
        self.validar_disponibilidad()
        if duracion <= 0:
            raise ValueError("La duración debe ser mayor a cero.")
            
        costo_total = self.tarifa_base * duracion
        
        # Sobrecarga: Si se envía un descuento por kwargs
        if 'descuento' in kwargs:
            costo_total -= costo_total * (kwargs['descuento'] / 100)
            
        # Sobrecarga: Si se envía un recargo por args (ej. uso de proyector)
        if len(args) > 0:
            costo_total += args[0] 
            
        return costo_total


class AlquilerEquipo(Servicio):
    def __init__(self, nombre_servicio, tarifa_base, tipo_equipo):
        super().__init__(nombre_servicio, tarifa_base)
        self.tipo_equipo = tipo_equipo

    def obtener_descripcion(self):
        return f"Alquiler de Equipo: {self.nombre_servicio} (Tipo: {self.tipo_equipo}). Tarifa base: ${self.tarifa_base}/hora."

    def calcular_costo(self, duracion, *args, **kwargs):
        self.validar_disponibilidad()
        if duracion <= 0:
            raise ValueError("La duración debe ser mayor a cero.")
            
        seguro = 10.0 
        costo_total = (self.tarifa_base * duracion) + seguro
        
        if len(args) > 0:
            costo_total += args[0] 
            
        return costo_total


class AsesoriaEspecializada(Servicio):
    def __init__(self, nombre_servicio, tarifa_base, area_conocimiento):
        super().__init__(nombre_servicio, tarifa_base)
        self.area_conocimiento = area_conocimiento

    def obtener_descripcion(self):
        return f"Asesoría Especializada: {self.nombre_servicio} (Área: {self.area_conocimiento}). Tarifa base: ${self.tarifa_base}/hora."

    def calcular_costo(self, duracion, *args, **kwargs):
        self.validar_disponibilidad()
        if duracion <= 0:
            raise ValueError("La duración debe ser mayor a cero.")
            
        costo_total = self.tarifa_base * duracion
        
        # Sobrecarga: Si el cliente es VIP (kwargs), se cobra un 20% más
        if kwargs.get('es_vip') == True:
            costo_total *= 1.20
            
        return costo_total

# ==========================================
# BLOQUE DE PRUEBA (Para verificar que funciona)
# ==========================================
if __name__ == "__main__":
    print("--- Probando el Módulo 3 ---")
    
    # 1. Creamos los servicios
    sala_vip = ReservaSala("Sala VIP 1", 50, 10)
    equipo_camara = AlquilerEquipo("Cámara 4K", 30, "Video")
    asesoria_mate = AsesoriaEspecializada("Refuerzo Cálculo", 80, "Matemáticas")
    
    # 2. Imprimimos sus descripciones (Polimorfismo)
    print(sala_vip.obtener_descripcion())
    print(equipo_camara.obtener_descripcion())
    print(asesoria_mate.obtener_descripcion())
    print("-" * 30)
    
    # 3. Probamos los cálculos con Sobrecarga
    # Reserva de sala por 2 horas, con descuento del 10%
    print(f"Costo Sala VIP (2h, 10% desc): ${sala_vip.calcular_costo(2, descuento=10)}")
    
    # Alquiler de cámara por 3 horas, con un recargo extra de $15
    print(f"Costo Alquiler Cámara (3h + $15 extra): ${equipo_camara.calcular_costo(3, 15)}")
    
    # Asesoría por 1 hora, cliente VIP
    print(f"Costo Asesoría (1h, VIP): ${asesoria_mate.calcular_costo(1, es_vip=True)}")
    
    # 4. Probamos la excepción (Apagamos la cámara)
    print("-" * 30)
    equipo_camara.disponible = False
    try:
        equipo_camara.calcular_costo(2)
    except ServicioNoDisponibleError as e:
        print(f"Error controlado: {e}")
        registrar_log(f"Se intentó usar un servicio no disponible: {equipo_camara.nombre_servicio}", "ERROR")
        