# Processes and threads
### Adriana N Hernandez
### CCOM4017 - Operating Systems

Processes and threads es un proyecto que consiste en realizar el Producer-Consumer Problem. La ejecucion del mismo se realiza de la siguiente manera:
Un edevice: Genera trabajos. Los trabajos consisten de un edevice id y un tiempo para que este duerma.
Un servidor: Recibe los trabajos y los ejecuta usando dos threads: un Producer y un Consumer
Producer: Thread que se encarga de recibir los trabajos y colocarlos en un queue compartido para el consumidor
Consumer: Thread que se encarga de ejecutar los trabajos y removerlos del queue 

# Como correr el programa

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

edevice.py es el script que genera los "trabajos" que seran enviados al servidor. Cada trabajo consiste en un device y un sleep time (duracion). 

El edevice es seleccionado por nosotros mientras que la duracion del trabajo es generada de forma aleatoria. Estos se mandan en formato **edevice : duracion**.

Es necesario decirle al programa cual es nuestro device, servidor, y puerto. Para obtener esa informacion utlizamos la libreria **sys** leyendo los argumentos del terminal. 

Esa informacion es colocada en un for loop para enviarle 5 trabajos de una vez.

![image](https://github.com/nekotletta/os/assets/99048617/1ff9c5e6-5105-43a9-8c56-06f5ad43d237)


La implementacion del servidor UDP fue sacado de la [internet](https://pythontic.com/modules/socket/udp-client-server-example).

Adicional a eso se le asigno un tiempo para dormir aleatorio cada vez que envia un trabajo para no sobrecargar el servidor. 

![image](https://github.com/nekotletta/os/assets/99048617/10f141be-756c-4161-91b5-d3c489cf8ac9)


## Implementacion de server.py

server.py es el script que recibe los "trabajos" y los ejecuta con 2 threads: **Producer** y **Consumer**.

La implementacion de ambos fue basada en el materia discutido en la clase de CCOM4017 - Producer-Consumer problem.

Para poder comenzar a implementar eso se utilizaron varias variables globales para ambos threads.

![image](https://github.com/nekotletta/os/assets/99048617/a5a4ca5f-015a-4877-b127-ab8db18326cd)


## Implementacion de Producer()

El thread Producer corre en un loop infinito recibiendo y preparando trabajos para enviarselos a Consumer.

El string recibido tiene formato b'id:tiempo', por lo que lo ponemos en el formato deseado (diccionario) antes de mandarlo a JOB_QUEUE.

Utlizamos los objetos semaforo globales para entrar / salir de la region critica y actualizar nuestros trabajos y nuestra lista sin race condition.

![image](https://github.com/nekotletta/os/assets/99048617/ef96cb5e-c3d6-44c4-bbd2-70c6cb09ad2a)

## Implementacion de Consumer()

El thread Consumer recibe los trabajos en JOB_QUEUE y los va "ejecutando" (poner cada device a dormir por un tiempo pre determinado).

El consumer se subdivide en diferentes fases:

### Longest Job First (LJF)

Es necesario acomodar los trabajos en el algoritmo LJF a medida que van llegando. Para eso es necesario hacerle sort a la lista constantemente. 

La lista que queremos ordenar es una lista de diccionarios, por lo que se uso [esta pagina](https://note.nkmk.me/en/python-dict-list-sort/) como referencia.

El ordenar la lista nos colca en region critica para evitar race condition. 

![image](https://github.com/nekotletta/os/assets/99048617/52d7b995-0b30-4a28-b375-1df8b8128df1)

### Ejecucion del trabajo 

Una vez los trabajos estan ordenados podemos comenzar a ejecutarlos (poner el device a dormir).

Una vez este termina, este es sacado de LJF y guardado en una variable. Esta variable nos dice cual trabajo sacar de JOB_QUEUE y nos ayuda a calcular el tiempo que cada trabajo se tardo en realizarse

![image](https://github.com/nekotletta/os/assets/99048617/dd69c9fc-7c77-4ed1-b6f8-2858abed643a)

### Calculando tiempo

Cada vez que ejecutamos un trabajo tenemos que anadirlo al tiempo del CPU.

Tenemos que chequear si el edevice trabajado ya tuvo algun trabajo. Si es asi le sumamos a la duracion de este en el CPU. De lo contrario se anade.

Esto es otra lista de diccionarios, asi que usamos el mismo metodo para ordenarla de menor a mayor.

![image](https://github.com/nekotletta/os/assets/99048617/f5a4235b-7f2e-47d7-b4e0-4cc025f39735)

![image](https://github.com/nekotletta/os/assets/99048617/f801b22a-c0a0-44a4-a8fd-8b08c7a867d7)


### Resultados del programa

Para poder desplagar cuanto se tardo cada proceso en el CPU, es necesario tener una cantidad limitada de procesos. Una vez esta cantidad sea ancanzada, se va a desplegar el tiempo consumido por cada device.

Cada vez que un trabajo es terminado en el consumer se le anade uno a un contador global. Una vez este llega a 20 los resultados calculados en la funcion sumatoria() son desplegados.

![image](https://github.com/nekotletta/os/assets/99048617/8630418c-309d-44e0-aca8-6d4eb844086b)

### Threads

Una vez el Producer() y Consumer() estan implementados, los threads se ejecutan asi

![image](https://github.com/nekotletta/os/assets/99048617/5c59506a-b6d7-4ce9-aa3e-fe28892ee846)

## server.py

![image](https://github.com/nekotletta/os/assets/99048617/697a970d-b360-4ec9-b294-cf5a92edc048)

