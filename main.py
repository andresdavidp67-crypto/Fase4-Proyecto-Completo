import time
from modulo1_logs import registrar_log, ClienteInvalidoError, ReservaError, ServicioNoDisponibleError
from modulo2_cliente import Cliente
from modulo3_servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from modulo4_reserva import Reserva

def simular_sistema():
    print("==================================================")
    print("   SISTEMA INTEGRAL - SOFTWARE FJ (SIMULACIÓN)")
    print("==================================================")
    
    # Listas para almacenar los objetos creados
    clientes = []
    servicios = []
    reservas = []

    print("\n--- INICIANDO LAS 10 OPERACIONES DE PRUEBA ---")

    # ---------------------------------------------------------
    # OPERACIÓN 1: Crear Cliente VÁLIDO (Éxito)
    # ---------------------------------------------------------
    print("\n[OP 1] Intentando crear cliente VÁLIDO...")
    try:
        c1 = Cliente(1, "Juan Perez", "1234567890", "juan@correo.com")
        clientes.append(c1)
        print("-> ÉXITO: Cliente 'Juan Perez' registrado.")
    except Exception as e:
        print(f"-> FALLÓ: {e}")

    # ---------------------------------------------------------
    # OPERACIÓN 2: Crear Cliente INVÁLIDO (Falla esperada)
    # ---------------------------------------------------------
    print("\n[OP 2] Intentando crear cliente INVÁLIDO (cédula con letras)...")
    try:
        c2 = Cliente(2, "Maria Gomez", "ABC123", "maria@correo.com")
        clientes.append(c2)
    except ClienteInvalidoError as e:
        print(f"-> ERROR CONTROLADO: {e}")

    # ---------------------------------------------------------
    # OPERACIÓN 3: Crear un Servicio VÁLIDO
    # ---------------------------------------------------------
    print("\n[OP 3] Creando servicios...")
    s1 = ReservaSala("Sala Proyectos", 50, 5)
    s2 = AlquilerEquipo("Computador Gamer", 30, "PC")
    s3 = AsesoriaEspecializada("Asesoría Python", 100, "Programación")
    servicios.extend([s1, s2, s3])
    print("-> ÉXITO: Sala, Computador y Asesoría dados de alta.")

    # ---------------------------------------------------------
    # OPERACIÓN 4: Crear Reserva VÁLIDA
    # ---------------------------------------------------------
    print("\n[OP 4] Creando reserva válida...")
    try:
        # Juan Perez reserva la Sala por 2 horas
        r1 = Reserva(100, clientes[0], servicios[0], 2)
        reservas.append(r1)
        print(f"-> ÉXITO: {r1}")
    except Exception as e:
        print(f"-> FALLÓ: {e}")

    # ---------------------------------------------------------
    # OPERACIÓN 5: Confirmar Reserva y Pagar
    # ---------------------------------------------------------
    print("\n[OP 5] Procesando pago de la reserva...")
    try:
        r1.confirmar()
        total = r1.procesar_pago()
        print(f"-> ÉXITO: Pago procesado. Total: ${total}. Estado: {r1.estado}")
    except Exception as e:
        print(f"-> FALLÓ: {e}")

    # ---------------------------------------------------------
    # OPERACIÓN 6: Crear Reserva INVÁLIDA (Duración negativa)
    # ---------------------------------------------------------
    print("\n[OP 6] Intentando reservar con duración negativa...")
    try:
        r2 = Reserva(101, clientes[0], servicios[2], -5)
        r2.confirmar()
        r2.procesar_pago() # El servicio lanzará ValueError por duración negativa
    except ValueError as e:
        print(f"-> ERROR CONTROLADO (Validación): {e}")
        registrar_log(f"Intento de reserva con duración negativa", "ERROR")
    except Exception as e:
        print(f"-> ERROR CONTROLADO: {e}")

    # ---------------------------------------------------------
    # OPERACIÓN 7: Intentar usar Servicio No Disponible
    # ---------------------------------------------------------
    print("\n[OP 7] Intentando usar un servicio apagado (Computador)...")
    s2.disponible = False # Apagamos el equipo
    try:
        r3 = Reserva(102, clientes[0], s2, 1)
        r3.confirmar()
        r3.procesar_pago()
    except Exception as e:
        print(f"-> ERROR CONTROLADO: {e}")

    # ---------------------------------------------------------
    # OPERACIÓN 8: Crear un cliente para el bucle automático
    # ---------------------------------------------------------
    print("\n[OP 8] Creando segundo cliente para reservas masivas...")
    try:
        c3 = Cliente(3, "Ana Martinez", "987654321", "ana@correo.com")
        clientes.append(c3)
        print("-> ÉXITO: Cliente Ana registrado.")
    except Exception as e:
        print(f"-> FALLÓ: {e}")

    # ---------------------------------------------------------
    # OPERACIÓN 9: Reserva exitosa de Asesoría (Sobrecarga)
    # ---------------------------------------------------------
    print("\n[OP 9] Reservando Asesoría con cliente VIP (Sobrecarga)...")
    try:
        r4 = Reserva(103, clientes[1], servicios[2], 1)
        r4.confirmar()
        # Aplicamos la sobrecarga enviando el parámetro es_vip
        costo_vip = r4.servicio.calcular_costo(r4.duracion, es_vip=True)
        r4.estado = "Pagada"
        print(f"-> ÉXITO: Asesoría reservada. Costo VIP aplicado: ${costo_vip}")
    except Exception as e:
        print(f"-> FALLÓ: {e}")

    # ---------------------------------------------------------
    # OPERACIÓN 10: Cancelar Reserva y reembolsar
    # ---------------------------------------------------------
    print("\n[OP 10] Cancelando una reserva confirmada...")
    try:
        r5 = Reserva(104, clientes[1], servicios[0], 3)
        r5.confirmar()
        r5.cancelar()
        print(f"-> ÉXITO: Reserva cancelada. Estado actual: {r5.estado}")
    except Exception as e:
        print(f"-> FALLÓ: {e}")

    print("\n==================================================")
    print("   FIN DE LA SIMULACIÓN. REVISA EL ARCHIVO logs.txt")
    print("==================================================")

if __name__ == "__main__":
    simular_sistema()