## PRE-PARCIAL: INTRODUCCIÓN A LAS REDES (TUDA - UNTDF)

**Fecha:** 17 de Junio  
**Duración Total:** 3 horas  
**Modalidad:** Mixta (Parte 1: Preguntas de opciones múltiples / Parte 2: Desarrollo en Laboratorio)

---

## PARTE 1: Evaluación Teórica 
*Instrucciones: Selecciona la opción correcta marcando con una 'X' dentro del checkbox `[ ]` basándote en los estándares de red (IETF, OSI) y el comportamiento del Sistema Operativo.*

### 1. Mecánica de Bloqueos en Sockets TCP
Analizando un servidor multihilo en Python, sabemos que el hilo principal se encuentra esperando conexiones. Si un cliente inicia exitosamente el *Three-way handshake*, el servidor le asigna un hilo exclusivo para su atención. Si ese cliente, una vez conectado, **se queda en silencio y nunca envía datos**, ¿en qué línea del código del hilo asignado se congelará la ejecución y qué recurso de infraestructura se ve afectado?
- [ ] a) Se bloquea en `server.accept()`, consumiendo ancho de banda de la interfaz de red de la VM.
- [ ] b) Se bloquea en `conn.recv(1024)`, manteniendo un hilo activo en el kernel y un descriptor de archivo (File Descriptor) abierto en el sistema operativo.
- [ ] c) Se bloquea en `conn.send()`, saturando el buffer de transmisión de la capa de transporte.
- [ ] d) El código no se bloquea; Python cierra el socket automáticamente por timeout de capa de aplicación.

### 2. Sockets vs. Protocolo de Transporte (Concurrencia)
En el servidor base, la verificación del límite de clientes activos (`if threading.active_count() <= MAX_CLIENTS:`) se ejecuta **después** de que la función `server.accept()` retorna el socket de la conexión. Desde la perspectiva de la infraestructura de red y el protocolo TCP: ¿En qué estado se encuentra la conexión del cliente sobrante antes de que el código decida ignorarlo o cerrarlo?
- [ ] a) La conexión está en tránsito; el *Three-way handshake* se encuentra pausado en el segundo paso (SYN-ACK).
- [ ] b) La conexión ya está completamente establecida en la pila TCP/IP del Sistema Operativo, ya que el handshake terminó antes de que `accept()` extraiga la conexión de la cola del kernel.
- [ ] c) El cliente todavía no sabe si se conectó, porque el protocolo TCP espera a que el método `thread.start()` de Python le dé autorización.
- [ ] d) La conexión fue rechazada por el Firewall del sistema operativo automáticamente debido a que superó el límite de la directiva `listen()`.

### 3. Delimitación de Mensajes en Capa 7 (Diseño de Protocolos)
En nuestro laboratorio de transferencia de archivos por UDP (`srv_udp_file.py`), utilizamos el literal de bytes `b"DONE"` como marcador de Fin de Archivo (EOF). Si un alumno intenta transferir una imagen binaria cuyos datos contienen la secuencia exacta de bytes correspondiente a los caracteres "D, O, N, E", ¿cuál será el impacto en la infraestructura del servicio?
- [ ] a) El protocolo UDP detectará el error mediante el Checksum de la capa de transporte y retransmitirá el fragmento corrupto.
- [ ] b) El servidor ignorará los bytes y continuará la lectura, ya que UDP es un protocolo orientado a flujos continuos (*streams*).
- [ ] c) El servidor interpretará prematuramente que la transmisión finalizó, cerrando el archivo y provocando una pérdida de integridad (archivo corrupto/truncado). 
- [ ] d) El socket del cliente lanzará un error de tipo `BrokenPipeError` al no poder codificar caracteres ASCII en un flujo binario.

### 4. Anatomía de Protocolos de Aplicación (HTTP)
Un desarrollador backend observa en las herramientas de diagnóstico (F12) que al intentar realizar un login enviando un JSON en el cuerpo del mensaje utilizando el método `GET`, el servidor web (Nginx/Apache) responde inmediatamente con un código `405 Method Not Allowed`. Según el estándar del IETF (RFC 9110), ¿cuál es la razón técnica de este rechazo?
- [ ] a) El método `GET` cifra automáticamente el cuerpo, y el servidor no cuenta con las llaves SSL/TLS para decodificarlo.
- [ ] b) El código `405` indica que la URI no existe en el servidor físico.
- [ ] c) El método `GET` está definido estructuralmente para solicitar recursos (semántica segura e idempotente) y no debe procesar ni depender de un cuerpo de petición (Request Body); se debe utilizar `POST` para el envío de credenciales. 
- [ ] d) El switch de la red LAN bloqueó el paquete porque los métodos `GET` superaron el tamaño máximo de la MTU (1500 bytes).

### 5. Diagnóstico de Servicios y Estados de Sockets
Tu servidor TCP en Python se cierra abruptamente por una excepción. Al intentar levantarlo de inmediato en la misma terminal de tu VM Linux, el intérprete lanza: `OSError: [Errno 98] Address already in use`. Si ejecutas la herramienta de diagnóstico `netstat -tuln`, verás que el puerto sigue ocupado. ¿En qué estado de la máquina de estados de TCP se encuentra el puerto y cómo se soluciona desde el código de Python?
- [ ] a) El puerto quedó en estado `LISTEN`; se soluciona cambiando el puerto por uno de rango efímero (ej. 60000).
- [ ] b) El puerto quedó en estado `TIME_WAIT` (esperando el cierre formal del socket por seguridad); se soluciona configurando la opción de socket `SO_REUSEADDR` en `True` antes de hacer el `bind()`. 
- [ ] c) El puerto quedó en estado `ESTABLISHED`; se soluciona reinventando la placa de red virtual de VirtualBox.
- [ ] d) El puerto quedó en estado `SYN_SENT`; se soluciona enviando un paquete UDP para limpiar la caché del socket.

---

## PARTE 2: DESARROLLO PRÁCTICO EN ENTORNO VIRTUAL 

### La Consigna del Alumno: "Módulo de Robustez y Telemetría para DevOps"
**Contexto de Infraestructura:** El equipo de administración de servidores de la universidad te ha entregado un script base de Python (`srv_telemetry_base.py`) que implementa un shell remoto TCP multihilo en el puerto `9090`. Actualmente, el script funciona en condiciones ideales, pero es **muy inestable**: si un cliente se desconecta sin escribir `EXIT` (ej. si se le corta internet o presiona Ctrl+C), el servidor lanza excepciones en el hilo que saturan los logs y no liberan los descriptores adecuadamente.

Tu tarea como desarrollador de aplicaciones es modificar **exclusivamente el servidor** para cumplir con los siguientes tres requerimientos de producción:

1. **Robustez ante Desconexiones Abruptas:** Capturar de forma precisa las excepciones de sockets (`ConnectionResetError`, `socket.error`) dentro del hilo del cliente. Si el cliente desaparece de la red de forma imprevista, el hilo no debe romper el servidor; debe cerrar el socket limpiamente (`conn.close()`) y registrar en la consola del servidor: `[ALERTA] Cliente <IP:Puerto> desconectado abruptamente.`
2. **Comando de Telemetría (`STATS`):** Agregar soporte para el comando `STATS` (en mayúsculas o minúsculas). Cuando un cliente conectado envíe este comando, el servidor **no debe ejecutar nada en el sistema operativo**. Debe responderle al cliente con un string de texto plano estructurado que informe:
   * La cantidad de hilos activos totales en ese instante.
   * La ruta del directorio de trabajo actual (utilizando el módulo `os`).
3. **Control de Saturación Activo (Capa de Aplicación):** Actualmente, si se supera el límite de `MAX_CLIENTS = 5`, las conexiones extras se quedan colgadas en un hilo secundario sin hacer nada. Debes modificar la lógica de aceptación para que, si el servidor ya llegó al máximo de clientes permitidos, acepte la conexión entrante, le envíe inmediatamente al cliente el mensaje: `[ERROR] Servidor saturado. Intente más tarde.\n`, y **cierre la conexión inmediatamente sin crear un hilo** para él, protegiendo los recursos de la VM.

---

### Código Fuente Base (`srv_telemetry_base.py`)

```python
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
                respuesta = "REQUERIMIENTO NO IMPLEMENTADO"
            # =========================================================

            else:
                respuesta = "Comando no reconocido."

            # Enviar la respuesta agregando el prompt del shell
            conn.send((respuesta + "\n> ").encode())

        except Exception as e:
            # =========================================================
            # TO-DO 1: MEJORAR LA GESTIÓN DE EXCEPCIONES DE RED AQUÍ
            # =========================================================
            print(f"Error general con el cliente {addr}: {e}")
            break

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
        if threading.active_count() <= MAX_CLIENTS:
            thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
            thread.start()
            print(f"[HILOS ACTIVOS] Clientes concurrentes: {threading.active_count() - 1}")
        else:
            # Actualmente los ignora... ¡Debes cambiar este comportamiento!
            print(f"[RECHAZADO] Conexión desde {addr} ignorada por saturación.")
            # =========================================================

if __name__ == "__main__":
    iniciar_servidor()
```
---
### Condiciones de Entrega 
El código modificado debe funcionar en el entorno de red de las máquinas virtuales configuradas (Red interna/Bridge).

Deberá subirse a un repositorio público propio de GitHub bajo el formato estricto: intro-redes-tuda-pre-examen-<nombre_apellido>.

El archivo fuente deberá llamarse obligatoriamente proy-pre-parcial-srv-tcp.py.