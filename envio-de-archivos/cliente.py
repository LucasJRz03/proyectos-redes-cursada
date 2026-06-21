import socket

# Configuración
HOST = '127.0.0.1' # La IP del servidor
PORT = 8000 # El mismo puerto del servidor
BUFFER_SIZE = 20 # Tamaño del buffer (lee de a 20 bytes)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Se conecta al servidor
    s.connect((HOST,PORT))
    print("Conectado al servidor.") 

    # Abrimos el archivo que creamos con 'dd' (en modo lectura binaria 'rb')
    with open('prueba', 'rb') as f:
        while True:
            # MANEJO DEL BUFFER: Leemos un máximo de 20 bytes del archivo
            bytes_read = f.read(BUFFER_SIZE)
        
            # Si no hay más bytes para leer, llegamos al final del archivo
            if not bytes_read:
                break
        
            #envía el buffer por el socket
            s.sendall(bytes_read)

    print("Archivo enviado completamente.")




