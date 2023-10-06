# Processes and threads
### Adriana N Hernández Vega
### CCOM4017 - Operating Systems

Processes and threads es un proyecto que consiste en realizar el Producer-Consumer Problem. La ejecución del mismo se realiza de la siguiente manera:

Un edevice: Genera trabajos. Los trabajos consisten de un edevice id y un tiempo para que este duerma.

Un servidor: Recibe los trabajos y los ejecuta usando dos threads: un Producer y un Consumer

Producer: Thread que se encarga de recibir los trabajos y colocarlos en un queue compartido para el consumidor

Consumer: Thread que se encarga de ejecutar los trabajos y removerlos del queue 

# Cómo correr el programa

Para correr el programa es necesario descargar ambos scripts y ejecutar

```
python server.py
```

para tener el servidor corriendo 

```
python edevice.py 1 localhost 42069
```

donde 1 es el device que va a mandar los mensajes

# Documentacion de codigo para proyecto 1 
## Implementacion de edevice.py

edevice.py es el script que genera los "trabajos" que serán enviados al servidor. Cada trabajo consiste en un device y un sleep time (duración).

El edevice es seleccionado por nosotros mientras que la duración del trabajo es generada de forma aleatoria. Estos se mandan en formato edevice : duración.

Es necesario decirle al programa cuál es nuestro device, servidor, y puerto. Para obtener esa información utilizamos la librería sys leyendo los argumentos del terminal.

```
python edevice.py <device> <servidor> <puerto>
```

Esa información es colocada en un for loop para enviarle 5 trabajos de una vez.

La implementación del servidor UDP fue sacado de la [internet](https://pythontic.com/modules/socket/udp-client-server-example).

Adicional a eso se le asignó un tiempo para dormir aleatorio cada vez que envía un trabajo para no sobrecargar el servidor. 


## Implementación de server.py

server.py es el script que recibe los "trabajos" y los ejecuta con 2 threads: **Producer** y **Consumer**.

La implementacion de ambos fue basada en el materia discutido en la clase de CCOM4017 - Producer-Consumer problem.

Para poder comenzar a implementar eso se utilizaron varias variables globales para ambos threads.


## Implementación de Producer()

El thread Producer corre en un loop infinito recibiendo y preparando trabajos para enviárselos a Consumer.

El string recibido tiene formato b'id:tiempo', por lo que lo ponemos en el formato deseado (diccionario) antes de mandarlo a JOB_QUEUE.

Utlizamos los objetos semáforo globales para entrar / salir de la región crítica y actualizar nuestros trabajos y nuestra lista sin race condition.


## Implementacion de Consumer()

El thread Consumer recibe los trabajos en JOB_QUEUE y los va "ejecutando" (poner cada device a dormir por un tiempo pre determinado).

El consumer se subdivide en diferentes fases:

### Longest Job First (LJF)

Es necesario acomodar los trabajos en el algoritmo LJF a medida que van llegando. Para eso es necesario hacerle sort a la lista constantemente. 

La lista que queremos ordenar es una lista de diccionarios, por lo que se usó  [esta página](https://note.nkmk.me/en/python-dict-list-sort/) como referencia.

El ordenar la lista nos coloca en región crítica para evitar race condition. 


### Ejecucion del trabajo 

Una vez los trabajos estan ordenados podemos comenzar a ejecutarlos (poner el device a dormir).

Una vez este termina, este es sacado de LJF y guardado en una variable. Esta variable nos dice cuál trabajo sacar de JOB_QUEUE y nos ayuda a calcular el tiempo que cada trabajo se tardó en realizarse.


### Calculando tiempo

Cada vez que ejecutamos un trabajo tenemos que añadirlo al tiempo del CPU.

Tenemos que chequear si el edevice trabajado ya tuvo algún trabajo. Si es así, le sumamos a la duración de este en el CPU. De lo contrario se añade.

Esto es otra lista de diccionarios, así que usamos el mismo método para ordenarla de menor a mayor.


### Resultados del programa

Para poder desplagar cuánto se tardó cada proceso en el CPU, es necesario tener una cantidad limitada de procesos. Una vez esta cantidad sea ancanzada, se va a desplegar el tiempo consumido por cada device.

Cada vez que un trabajo es terminado en el consumer se le anade uno a un contador global. Una vez este llega a 20 los resultados calculados en la funcion **sumatoria()** son desplegados con la funcion **display().**


### Threads

Una vez el Producer() y Consumer() estan implementados, los threads se ejecutan así

```
producer_thread = Producer()
producer_thread.start()
consumer_thread = Consumer()
consumer_thread.start()
producer_thread.join()
consumer_thread.join()
```


# Docmunentación del bono

En el proyecto original era necesario colocar el script que envía los trabajos a dormir por un periodo aleatorio entre cada trabajo.

El bono consiste en cambiar esa implementación para que el edevice tenga que esperar hasta que el servidor comunique que el trabajo ha sido ejecutado. Una vez reciba este mensaje puede enviar el siguiente trabajo.


## Cambios realizados en server.py

### a) bytesAddressPair

bytesAddressPair fue cambiado a una variable global para saber de dónde vino el trabajo. Necesitamos guardar esa información para devolverle un mensaje una vez ejecute el trabajo. 

```
bytesAddressPair = ()
```

### b) Creacion de una funcion 

Se añadió la función **avisar(bytesAddresPair)**, la cual es la encargada de notificar que el trababajo ha finalizado.

Recibe como argumento a bytesAddressPair para saber a dónde mandar el mensaje utliizando el método **UDPServerSocket.sendto(msg, address)**, donde msg es un string codificado y address es bytesAddressPair[1]


## Cambios realizados en edevice.py

Anteriormente había un número aleatorio para que el edevice durmiera. Este fue reemplazado con la función **ejecutar()** que espera por el mensaje del servidor con el método **UDPClientSocket.recvfrom(bufferSize)**.

Una vez este recibe el mensaje del servidor este lo despliega y el for loop itera de nuevo, enviando un nuevo trabajo.
