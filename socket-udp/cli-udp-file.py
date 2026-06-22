import socket
import time

HOST_DESTINO = '127.0.0.1' # Se cambia en desarrollo
PUERTO_DESTINO = 8080

def enviar_archivo_udp():
    # 1. Instanciamos el socket específico para UDP
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # La tupla de destino la guardamos en una variable
    direccion_servidor = (HOST_DESTINO, PUERTO_DESTINO)
    
    try:
        # 2. Abrimos la imagen a enviar en modo lectura binaria (reader binary -> 'rb' )
        with open("foto_perfil.jpg", "rb") as f:
            while True:
                # Leemos fragmentos del archivo de a 1024 bytes
                chunk = f.read(1024)
                
                # Si 'chunk' está vacío, llegamos al final del archivo
                if not chunk:
                    break 
                    
                # 3. Enviamos el fragmento especificando a qué IP y Puerto debe ir
                cliente.sendto(chunk, direccion_servidor)
                
                # Agregamos una pausa artificial de 1 milisegundo.
                # Como UDP no tiene control de flujo, esto evita que nuestro
                # veloz bucle while sature el buffer de recepción del servidor.
                time.sleep(0.001) 
                
        # 4. Enviamos el literal de bytes que usamos como In-band signaling 
        # para que el servidor sepa que terminamos
        cliente.sendto(b'DONE', direccion_servidor)
        
        print("Archivo enviado con éxito al servidor UDP.")

    except FileNotFoundError:
        print("Error: El archivo foto_perfil.jpg no se encuentra en este directorio.")
    except Exception as e:
        print(f"Error de red general: {e}")
    finally:
        # Siempre cerramos el descriptor de archivo del socket
        cliente.close()

if __name__ == "__main__":
    enviar_archivo_udp()