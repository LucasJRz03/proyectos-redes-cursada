import socket

HOST = '0.0.0.0'
PORT = 8080

def iniciar_servidor_udp():
    # 1. Instanciamos el socket específico para UDP
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # 2. Asociamos el socket a la interfaz y al puerto local
    server.bind((HOST, PORT))
    print(f"Servidor UDP encendido y escuchando en puerto {PORT}...")

    # Abrimos un archivo en modo escritura binaria
    with open("imagen_recibida.jpg", "wb") as f:
        while True:
            # 3. Leemos los datos entrantes y capturamos la IP/Puerto de quien los manda
            # Recordá que en UDP los paquetes llegan sueltos
            data, addr = server.recvfrom(1024)
            
            # Condición de corte (In-band signaling)
            if data == b"DONE":
                print(f"Transferencia desde {addr} finalizada.")
                break
                
            # 4. Escribimos los bytes puros directamente en el archivo
            f.write(data)

    # Cerramos el socket al terminar
    server.close()

if __name__ == "__main__":
    iniciar_servidor_udp()