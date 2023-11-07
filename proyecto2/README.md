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

- Chequear que la pagina no este referenciada. Si lo esta, cambiar el reference bit a 0

- Buscar la pagina mas vieja que no este en el working set (edad es menor al tau)

- Reemplazar la pagina mas vieja y hacer que la manecilla se mueva a la pagina reemplezada

```
python wsclock.py <capacidad de la memoria> <tau (tiempo max de una pag en la memoria)> <file con las paginas a accesar>
python wsclock.py           5                                     3                                      index.txt
```

## Explicacion de codigo

Cada uno de estos aloritmos debe devolver la cantidad de page faults generadas.

En cada uno de los algoritmos hay que leer un file. Se lee de la siguiente manera: 

```
with open(file, 'r') as f:
  for line in f:
    line = line.split()  # cada instruccion en cada linea
    # ya sea vertical u horizontal
    for thing in line:
      pages.append(int(thing[2:]))  # los primeros 2 chars son "W:" o "R:"
      # eliminamos y lo convertimos a un int
```

### FIFO

```
for item in pages:
# cada pagina que tengo que chequear

  if item not in memory:
  # no lo tengo en memoria aun

    if len(memory) < N:
    # puedo insertar

      memory.append(item)
      page_fault += 1

    else: # esta lleno, tengo que remover para hacer espacio

      memory.pop(0)
      # remover el primero

      memory.append(item)
      page_fault += 1
```

### OPTIMAL

Optimal debe buscar la pagina que me voy a tardar mas en usar. Se implemento usando esta funcion: 

```
def calculate_position(list_index, used_pages):
  viejas = [] #las voy a volver a usar
  candidatos_eliminacion = [] #paginas que no voy a volver a usar

  for pos in range(list_index, len(pages)):
  #chequeo las paginas de donde me quede al final

    if pages[pos] in used_pages:
    # paginas que ya he visto | esta en memoria

      viejas.append(pages[pos])
      # guardamos la ultima vez que la vemos para saber cuanto hay
      # que esperar por volverla a usar

  # solo me interesa la primera instancia de cada pagina
  viejas = list(dict.fromkeys(viejas))

  list_index = 0
  for num in used_pages:
  #iterar por los nums que he visto antes

    if num not in viejas:
      # la pag esta en uso, pero ya no la voy a volver a usar
      # vamos a borrar esa pagina
      candidatos_eliminacion.append(list_index)
    list_index += 1
      
  if len(candidatos_eliminacion) != 0:
    return candidatos_eliminacion[0]
    # ya no las voy a volver a ver, no me importa que hay, saca lo primero
```

## WSClock 

