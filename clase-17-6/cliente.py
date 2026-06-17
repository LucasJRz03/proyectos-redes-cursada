import socket

HOST = '127.0.0.1'
PORT = 6000
BUFFER_SIZE = 20

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    print("Conectado al servidor.") 

    with open('prueba', 'rb') as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
        
            if not bytes_read:
                break
        
            #envía el buffer por el socket
            s.sendall(bytes_read)

    print("Archivo enviado completamente.")




