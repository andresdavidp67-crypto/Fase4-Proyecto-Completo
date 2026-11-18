#Andres David Paz Botina
#Ingenieria en sistemas -UNAD
import datetime

# 1. EXCEPCIONES PERSONALIZADAS
class ClienteInvalidoError(Exception):
    pass

class ReservaError(Exception):
    pass

class ServicioNoDisponibleError(Exception):
    pass

# 2. FUNCIÓN DE REGISTRO (LOGGING)
def registrar_log(mensaje, tipo="INFO"):
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"[{fecha_hora}] [{tipo}] {mensaje}\n")

# 3. PRUEBA
if __name__ == "__main__":
    print("--- Probando el Módulo 1 ---")
    registrar_log("El sistema se ha iniciado correctamente.", "INFO")
    registrar_log("Intento fallido de conexión.", "ERROR")
    print("¡Revisa el archivo logs.txt en la izquierda!")