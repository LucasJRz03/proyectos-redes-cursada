import socket

HOST = 'example.com'
# 1. El puerto TCP estándar reservado para tráfico HTTP sin encriptar
PORT = 80
# Nota: el de HTTPS es 443 

def test_servidor_web():
    # 2. Instanciamos el socket para TCP
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 3. Configuramos un límite de tiempo de 5 segundos. 
    # Si el servidor no responde en ese tiempo, el socket abortará.
    cliente.settimeout(5.0)

    try:
        cliente.connect((HOST, PORT))

        # Armamos la petición HTTP GET cruda según el RFC de IETF
        # Requiere salto de línea doble al final (\r\n\r\n) para indicar el fin de los headers
        peticion = f"GET / HTTP/1.1\r\nHost: {HOST}\r\nConnection: close\r\n\r\n"
        cliente.send(peticion.encode('utf-8'))

        respuesta = cliente.recv(4096).decode('utf-8')
        print("=== RESPUESTA DEL SERVIDOR ===")
        print(respuesta)

    # 4. Capturamos específicamente la excepción de tiempo de espera agotado
    except socket.timeout:
        print("[ERROR] El servidor tardó demasiado en responder.")
    except Exception as e:
        print(f"[ERROR] Fallo general: {e}")
    finally:
        cliente.close()

if __name__ == "__main__":
    test_servidor_web()