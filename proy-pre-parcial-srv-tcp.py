import socket
import threading
import os

HOST = '0.0.0.0'  # Escucha en todas las interfaces de la VM
PORT = 9090
MAX_CLIENTS = 5

def manejar_cliente(conn, addr):
    print(f"[NUEVA CONEXIÓN] {addr} conectado exitosamente.")
    conn.send("Bienvenido al Servidor de Telemetría UNTDF.\nComandos disponibles: LS, PWD, STATS, EXIT\n> ".encode())

    while True:
        try:
            # Recibir datos del buffer del socket
            data = conn.recv(1024).decode().strip()
            
            # Si no hay datos, el cliente cerró el socket de su lado de forma limpia
            if not data:
                break

            partes = data.split(" ", 1)
            comando = partes[0].upper()
            
            if comando == "EXIT":
                break
            
            elif comando == "LS":
                archivos = os.listdir('.')
                respuesta = "\n".join(archivos)
            
            elif comando == "PWD":
                respuesta = os.getcwd()

            # =========================================================
            # TO-DO 2: IMPLEMENTAR AQUÍ EL COMANDO 'STATS'
            # =========================================================
            elif comando == "STATS":
                # La función active_count() incluye al hilo principal del servidor.
                # Para devolver el valor real de infraestructura restamos 1. 
                clientes_activos = threading.active_count() -1
                ruta_actual = os.getcwd()

                respuesta = f"Hilos activos: {clientes_activos}\nDirectorio actual:{ruta_actual}"
            # =========================================================

            else:
                respuesta = "Comando no reconocido."

            # Enviar la respuesta agregando el prompt del shell
            conn.send((respuesta + "\n> ").encode())
        
        # =========================================================
        # TO-DO 1: MEJORAR LA GESTIÓN DE EXCEPCIONES DE RED AQUÍ
        # =========================================================
        except (socket.error, ConnectionResetError) as e:
            print(f"[ALERTA] Cliente {addr} desconectado abruptamente. Motivo: {e}")
            break
        except Exception as e:
            print(f"[ERROR SOFTWARE] Excepción interna en el hilo de {addr}: {e}")
            break
        # ==========================================================

    # Cierre limpio al salir del bucle
    print(f"[DESCONEXIÓN] {addr} finalizó sesión de forma limpia.")
    conn.close()

def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Evitar el error: Address already in use
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server.bind((HOST, PORT))
    server.listen(MAX_CLIENTS)
    print(f"[LISTO] Servidor de infraestructura escuchando en puerto {PORT}...")

    while True:
        conn, addr = server.accept()
        
        # =========================================================
        # TO-DO 3: MODIFICAR ESTA LÓGICA PARA CONTROL DE SATURACIÓN
        # =========================================================
        # Contabilizar hilos activos (Nota: el hilo principal cuenta como 1)
        # Recordar: active_count() incluye el hilo de escucha principal.
        if threading.active_count() <= MAX_CLIENTS:
            thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
            thread.start()
            print(f"[HILOS ACTIVOS] Clientes concurrentes: {threading.active_count() -1 }")
        else:
            # Mecanismo de mitigación y protección de infraestructura
            print(f"[RECHAZADO] Conexión desde {addr} ignorada por saturación. Limite máx: {MAX_CLIENTS}")
            try:
                # Se le notifica el estado al cliente antes de cortar la comunicación
                conn.send("[ERROR] Servidor saturado. Intente más tarde. \n".encode())
            except socket.error:
                pass # Previene caídas si el cliente cerró el socket inmediatamente
            finally:
                conn.close() # Cerramos el File Descriptor inmediatamente sin crear hilos
            # =========================================================

if __name__ == "__main__":
    iniciar_servidor()