# Processes and threads
### Adriana N Hernandez
### CCOM4017 - Operating Systems

Processes and threads es un proyecto que consiste en realizar el Producer-Consumer Problem. La ejecucion del mismo se realiza de la siguiente manera:
Un edevice: Genera trabajos. Los trabajos consisten de un edevice id y un tiempo para que este duerma.
Un servidor: Recibe los trabajos y los ejecuta usando dos threads: un Producer y un Consumer
Producer: Thread que se encarga de recibir los trabajos y colocarlos en un queue compartido para el consumidor
Consumer: Thread que se encarga de ejecutar los trabajos y removerlos del queue 

# Documentacion de codigo para proyecto 1 


Este proyecto se divide en dos partes principales
