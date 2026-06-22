
import socket 

HOST = "127.0.0.1"
PORT = 9090

# Completar los campos vacios
def iniciar_cliente(): 
    # 1. Instanciamos el socket TCP 
    # cliente = socket.socket(socket.AF_INET, socket.[ ___ 1 ___ ])
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 2. Solicitamos al SO que inicie el Three-way Handshake con el servidor
        # cliente.[ ___ 2 ___ ]((HOST_DESTINO, PUERTO_DESTINO))
        cliente.connect((HOST, PORT))
        print("Conectado al servidor")

        # 3. Recibimos el mensaje de bienvenida del servidor (máx 1024 bytes)
        # bienvenida = cliente.[ ___ 3 ___ ](1024).decode()
        bienvenida = cliente.recv(1024).decode()
        print(f"Servidor dice: {bienvenida}")

        # 4. Enviamos el comando para ver los hilos activos
        comando = "STATS"
        # cliente.send(comando.[ ___ 4 ___ ]())
        cliente.send(comando.encode('UTF-8'))

        respuesta = cliente.recv(1024).decode()
        print(f"Respuesta STAT:\n{respuesta}")

    except Exception as e: 
        print(f"Error de conexión: {e}")
    finally:
        cliente.close()

if __name__ == '__main__':
    iniciar_cliente()

