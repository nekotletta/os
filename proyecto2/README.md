# Page Replacement Algorithms

### Adriana N Hernandez Vega
### CCOM4017 - Operating Systems

Page replacement algorithms es un proyecto que consiste en implementar tres algoritmos de reemplazo de pagina: FIFO, Optimal, WSClock.

Los algorithmos pueden describirse de la siguiente manera: 

### FIFO

Tal y como el nombre lo sugiere, una vez la memoria de nuestro programa se quede sin espacio, este va a realizar los siguientes passos: 

- Tomar el primer elemento en la lista y removerlo
  
- Colocar el elemento que queremos insertar al final de la lista

```
python fifo.py <capacidad de la memoria> <file con las paginas a accesar>'
python fifo.py                5                       index.txt
```

### Optimal

Aunque este algoritmo no es realizable en vida real, vamos a simulalo en este proyecto. 

Consiste en buscar la pagina que mas me voy a tardar en reutilizar. Esto minimiza la cantidad de page faults lo mas posible. La ejecucion se ve asi:

- Me quedo sin espacio en memoria
  
- Recorro la lista de todos los accesos a paginas

- Chequeo si tengo que volver a usar una pagina

- Si no, enotnces puedo remover esa.

- Si si, entonces tengo que asegurarme que esa pagina es la que voy a usar mas en el futuro y la elimino si ese el caso

```
python optimal.py <capacidad de la memoria> <file con las paginas a accesar>
python optimal.py               5                       index.txt
```
### Working Set Clock 

El WSClock funciona como un reloj. La manera en que recorremos los page accesses es en una lista circular. Es decir, una vez se llegue al ultimo elemento de la lista caemos en el primero de nuevo. 

La razon por la que se le dice Clock, es porque tambien tenemos un apuntador (como una manecilla) que nos dice por donde vamos (indice de la lista). 

![image](https://github.com/nekotletta/os/assets/99048617/c73c18b1-6e00-4716-b329-12bf6968a194)


Cada elemento de esta lista se ve de la siguiente manera: 

```
<el numero de la pagina que estoy viendo> <el tiempo en que accese la pagina> <si la estoy referenciando al momento o no>
              2                                          1005                     0 (no la referencie ahora mismo)

*el tiempo esta dado por un tiempo inicial (1000) que aumenta de 1 en 1 por cada iteracion del programa
```
Cada pagina en el wsclock algorithm tiene un tiempo maximo que puede estar en memoria antes de ser considerado viejo. Las paginas que sean consideradas viejas deben ser eliminadas para dar paso a paginas nuevas

La manera en que se calcula la edad es la siguiente: 

```
edad de la pagina = <tiempo actual en el programa> - <tiempo en el que accese la pagina por ultima vez>
```

Una vez la memoria se llena el algoritmo corre de la siguiente manera:

- Recorro la lista

- 
