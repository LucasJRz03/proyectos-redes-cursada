# TEORÍA INT. A LAS REDES.

## PREGUNTAS MÚLTIPLE CHOISE.

1. Transporte y Garantías (TCP vs UDP)
Imaginá que estás diseñando un servicio para la universidad que transmite video en vivo de las clases. Decidís usar sockets con la familia `AF_INET`y el tipo `SOCK_DGRAM` (UDP). Durante la transmisión, un router en el medio descarta el paquete número 45 por congestión en la red. 
¿Qué hará el sistema operativo del servidor o del cliente para recuperar ese paquete? 
- [ ] A) El protocolo de la capa de transporte detectará la secuencia faltante y solicitará una retransmisión automática del paquete 45.
- [x] B) No hará absolutamente nada. El paquete se pierde y el reproductor de video del cliente tendrá un pequeño salto o glitch visual.
- [ ] C) El socket de Python lanzará un ConnectionResetError informando que el flujo de datos se rompió.
- [ ] D) El paquete quedará guardado en el buffer de la capa de enlace hasta que la congestión pase y luego se enviará.

**Explicación:** Por qué está bien: Entendiste perfectamente la naturaleza de UDP. Es un protocolo *"fire and forget"* (orientado a datagramas, sin conexión). Al no haber un mecanismo de control de flujo ni de acuses de recibo (ACKs), el sistema operativo no se entera de que el paquete se perdió en el router. Simplemente el video pega un salto.

2. Anatomía de un servidor TCP
En el ciclo de vida un servidor TCP clásico en Python, hay una secuencia estricta de métodos que se deben llamar para que el sistema operativo prepare la infraestructura de la red. ¿Cuál de estas afirmaciones sobre esos métodos es correcta? 
- [ ] A) El método `bind()` es el que bloquea el hilo principal esperando a que un cliente se conecte.
- [x] B) El método `listen()` crea la cola de conexiones entrantes en el kernel de Linux y pone al puerto en estado de escucha.
- [ ] C) El método `accept()` le asigna un puerto de rango efímero al servidor para que no choque con otros servicios.
- [ ] D) El método `socket()` inicia el Three-way handshake con el primer cliente que encuentre en la red LAN.

**Explicación:** El método `listen()` es el que le dice al kernel de Linux: "Convertí este socket en pasivo y armame una cola en memoria para guardar a los clientes que intenten hacer el handshake".

3. Concurrencia y Sockets
Cuando un cliente TCP se conecta a nuestro servidor multihilo, el método `server.accept()` devuelve una tupla `(conn, addr)`. ¿Qué representa exactamente la variable `conn`? 
- [ ] A) Es un string que contiene la dirección IP y el puerto de origen del cliente.
- [ ] B) Es un clon exacto del socket principal del servidor (server), escuchando en el mismo puerto 9090.
- [x] C) Es un nuevo objeto socket (con su propio File Descriptor) dedicado única y exclusivamente para transferir datos con ese cliente específico.
- [ ] D) Es el primer paquete de datos (payload) que el cliente envió durante el handshake.

**Explicación:** Por qué está bien: Este es el concepto más importante de la concurrencia. `accept()` fabrica un nuevo socket dedicado exclusivamente a hablar con ese cliente particular, permitiendo que el socket original del servidor siga escuchando en el puerto 9090 para recibir a los demás.

4. Arquitectura de Red y Multiplexación (Puertos)
Imaginá que tenés un servidor web Nginx productivo corriendo en tu máquina y está escuchando en el puerto TCP `80`. En un momento de pico de tráfico, 500 clientes se conectan simultáneamente para descargar una imagen. A nivel del sistema operativo del servidor, ¿cuántos puertos locales se están utilizando para mantener esas 500 conexiones vivas? 
- [ ] A) Se usan 501 puertos: el puerto 80 para escuchar y 500 puertos de rango efímero asignados dinámicamente para cada cliente.
- [x] B) Se usa únicamente 1 puerto (el `80`). El sistema operativo diferencia las conexiones utilizando la tupla de 4 elementos (IP origen, Puerto origen, IP destino, Puerto destino).
- [ ] C) Se usan 500 puertos en total, ya que el puerto 80 se cierra una vez que se acepta la primera conexión.
- [ ] D) Depende de la cantidad de hilos (threads) que el servidor web levante para atender las peticiones.

**Explicación:** El Sistema Operativo diferencia a los 500 clientes gracias a la multiplexación, usando lo que se llama la "tupla de 4" (IP Origen, Puerto Origen, IP Destino, Puerto Destino). Como el puerto origen de cada cliente es diferente (son puertos efímeros aleatorios), el kernel sabe exactamente a qué hilo o proceso mandarle cada paquete de datos, sin necesidad de abrir el puerto 81, 82, 83, etc.

5. Herramientas de Diagnóstico y Modelo OSI
Estás en la terminal de tu entorno Linux administrando el servidor y notas que no hay conectividad. Ejecutas un `ping 8.8.8.8` para verificar si tus paquetes llegan a internet y recibís respuestas exitosas. ¿Qué protocolo viaja por debajo de esa herramienta y en qué capa del Modelo OSI opera? 
- [ ] A) Protocolo ARP - Capa de Enlace (Capa 2).
- [ ] B) Protocolo TCP - Capa de Transporte (Capa 4).
- [x] C) Protocolo ICMP - Capa de Red (Capa 3).
- [ ] D) Protocolo DNS - Capa de Aplicación (Capa 7).

**Explicación:** El comando `ping` no usa TCP ni UDP (Capa 4), sino que envía paquetes ICMP (Internet Control Message Protocol), que vive directamente en la Capa 3 (Red), justo por encima de IP.

6. Diseño de Protocolos de Aplicación sobre UDP 
Retomando el concepto del laboratorio de transferencia de archivos (`srv_udp_file.py`). Como sabemos, UDP es un protocolo no orientado a la conexión que no garantiza la entrega ni el orden. Si envías una imagen particionada en 100 datagramas UDP, ¿qué mecanismo deberías implementar obligatoriamente en el código Python (Capa de Aplicación) para poder rearmar la imagen correctamente en el servidor? 
- [ ] A) Configurar la opción `SO_REUSEADDR` en el socket para evitar pérdida de paquetes.
- [x] B) Incluir un número de secuencia personalizado dentro del cuerpo (payload) de cada mensaje enviado.
- [ ] C) Usar el método `recvfrom()` dentro de un bloque `try...except` para forzar la retransmisión de paquetes perdidos.
- [ ] D) No es necesario hacer nada, el Checksum nativo de UDP se encarga de reordenar los datagramas en el kernel.

**Explicación:** UDP no tiene idea del orden. Si el paquete 2 viaja por una ruta más rápida que el paquete 1, van a llegar invertidos. Si el servidor escribe eso directamente con `f.write()`, la imagen va a quedar corrupta. Al usar UDP para archivos grandes, sos vos como desarrollador el que tiene que programar en la Capa de Aplicación (en Python) un número de secuencia (ej: `001|datos`, `002|datos`) para que el servidor sepa cómo reordenarlos antes de guardarlos.

7. Interfaces de Red y el Método `bind()`
Supongamos que por error en tu servidor TCP pones `HOST = '127.0.0.1` en lugar de `0.0.0.0`. Si un compañero intenta conectarse a tu servidor desde otra notebook en la misma red WIFI usando la IP local de tu máquina (ej. `192.168.1.50`), ¿qué sucederá a nivel de infraestructura?
- [ ] A) Se conectará perfectamente, ya que `127.0.0.1` hace un puente automático con la tarjeta de red Wi-Fi.
- [x] B) La conexión será rechazada. La IP `127.0.0.1` (loopback) le indica al kernel que solo escuche conexiones originadas desde el propio sistema operativo local, aislando el puerto del exterior.
- [ ] C) El socket lanzará la excepción `Address already in use` porque el puerto está reservado por el sistema.
- [ ] D) La conexión quedará en estado `SYN_SENT` infinitamente hasta que el cliente cancele la ejecución.

**Explicación:** Entender que `127.0.0.1` (localhost) aísla el servicio del mundo exterior es fundamental para administrar servidores en Linux. Si querés que te vean desde afuera de tu máquina virtual, tiene que ser `0.0.0.0` o la IP específica de la placa de red.

8. Resolución de Nombres (DNS) en la Librería Socket
En los ejercicios anteriores nos conectamos directamente usando IPs (`192.168.1.50` o `0.0.0.0`). Sin embargo, en un entorno de producción, es normal hacer `cliente.connect(('api.github.com', 443))`. ¿Qué función nativa de la librería de Python ejecuta el sistema operativo por debajo para traducir ese dominio a una IP real de poder iniciar el *Three-way handshake*? 

- [x] A) `socket.gethostbyname()`
- [ ] B) `socket.dns_lookup()`
- [ ] C) `socket.resolve_ip()`
- [ ] D) `socket.arp_request()`

**Explicación:** El método oficial, heredado de la API de sockets en C del sistema operativo, es `socket.gethostbyname('example.com')`.

9. Capa de Transporte: Control de Flujo (TCP) 
TCP es un protocolo robusto que implementa un mecanismo llamado "Control de Flujo" (Flow Control), usualmente gestionado a través de una "Ventana Deslizante" (sliding Window). ¿Cuál es el propósito exacto de este mecanismo entre 2 sockets conectados? 
- [ ] A) Evitar la congestión general de los routers intermedios en la red pública de Internet.
- [ ] B) Encriptar los paquetes de datos para que no puedan ser leídos si son interceptados.
- [x] C) Evitar que un emisor muy rápido sature de bytes el buffer de recepción de un receptor más lento, dándole tiempo a la aplicación de leer los datos con `.recv()`.
- [ ] D) Aumentar la velocidad de transferencia comprimiendo los segmentos TCP en tránsito.

**Explicación:** El Flow Control es puramente entre emisor y receptor para no saturar el buffer local (no confundir con el Congestion Control, que es para no romper los routers de internet en el camino).