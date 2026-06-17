import socket

HOST= '127.0.0.1'
PORT= 6000
BUFFER_SIZE = 20

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor escuchando en {HOST}:{PORT}")

    #acepta la conexión
    conn, addr = s.accept()
    with conn:
        print(f"Conectado exitosamente con:{addr}")

        with open('prueba_recibida', 'wb') as f:
            while True:
                # recibe el máximo de 20 bytes a la vez
                data = conn.recv(BUFFER_SIZE)

                if not data:
                    break
                
                f.write(data)
        print("archivo recibido y guardado como 'prueba_recibida'.")
