import socket
import os

HOST= '127.0.0.1' #Localhost
PORT= 8000        # Puerto donde escuchará el servidor
BUFFER_SIZE = 20  # Tamaño del buffer (recibimos de a 20 bytes)

MAX_FILE_SIZE = 50000 # Límite estricto: no acepta más de 50 KB
TIMEOUT_SECS = 30.0 # Si el cliente se calla por 30 segundos, lo desconectamos

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # BUENA PRÁCTICA: Permite reiniciar el servidor sin el error "PORT already in use"
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor escuchando en {HOST}:{PORT}")

    # Un loop infinito para que el servidor no se apague tras el primer cliente
    while True:
        try:  
            #acepta la conexión entrante
            conn, addr = s.accept()

            # BUENA PRÁCTICA: Establece un tiempo máximo de espera
            conn.settimeout(TIMEOUT_SECS)

            with conn:
                print(f"\n[+] Nueva conexión entrante desde:{addr}")
                bytes_recibidos = 0
                archivo_invalido = False

                # Abrimos un archivo nuevo para escribir los datos recibidos (en modo binario)
                with open('prueba_recibida', 'wb') as f:
                        while True:
                            try:        
                                # MANEJO DEL BUFFER: recibe el máximo de 20 bytes a la vez                                 
                                data = conn.recv(BUFFER_SIZE)
                                                  
                                # Si 'data' está vacío, significa que el cliente terminó de enviar                                   
                                if not data:
                                    print("[-] El cliente finalizó la transmisión de forma limpia.")                                        
                                    break
                                    
                                bytes_recibidos += len(data)

                                    
                                # BUENA PRÁCTICA: Verificamos el tamaño máximo antes de escribir                                  
                                if bytes_recibidos > MAX_FILE_SIZE:                                        
                                    print(f"[!] ALERTA: El cliente intentó enviar más de {MAX_FILE_SIZE} bytes. Cortando conexión.")                                    
                                    archivo_invalido = True                                       
                                    break # Rompemos el ciclo para dejar de leer
                         
                                # Escribe ese pequeño bloque en el archivo                                   
                                f.write(data)
        
                            # BUENA PRÁCTICA: Manejo de errores de red
                            except socket.timeout:
                                print(f"[!] ERROR: Timeout. El cliente no envió datos por {TIMEOUT_SECS}s.")
                                archivo_invalido = True
                                break
                            except ConnectionResetError:
                                print("[!] ERROR: El cliente cerró la conexión abruptamente (RESET).")
                                archivo_invalido = True
                                break

                # Si el archivo fue producto de un ataque o error, lo borramos para no guardar basura
                if archivo_invalido: 
                    print("[-] Borrando archivo corrupto/incompleto...")
                    os.remove('prueba_recibida')
                else:
                    print(f"[-] Archivo guardado con éxito. Total: {bytes_recibidos} bytes.")

        except KeyboardInterrupt:
            # Permite apagar el serivdor limpiamente con Ctrl+C
            print("\nApagando el servidor maestro...")
            break    
