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
      # vamos guardar el indice de esa pagina para eliminarla
      candidatos_eliminacion.append(list_index)
    list_index += 1
      
  if len(candidatos_eliminacion) != 0:
    return candidatos_eliminacion[0]
    # ya no las voy a volver a ver, no me importa que hay, saca lo primero
```
Una vez la pagina mas vieja haya sido decidida, su indice es devuelto.

Luego se busca en la lista de paginas y se elimina. Una vez esta es eliminada, insertamos nuestra nueva pagina al final. 

### WSClock 

WSClock fue implementado con clases y objetos. 

Lo primero que se hizo fue un constructor para crear objetos del tipo Paging (las paginas en la memoria).

```
class Paging:
  def __init__(self, page, time):
    self.page = page  #num de pagina
    self.tola = time  #tola
    self.ref = 1      #como la estoy creando, la estoy referenciando
  def getPage(self):
    return [self.page, self.tola, self.ref]  #objeto clase paging
```

Esta clase es usada unicamente cuando tengo que crear o reemplazar una pagina.

Creamos una segunda clase encargada de manejar todas las paginas en memoria, llamada WSClock.

Esta clase tiene dos funciones prinipales junto a varias funciones auxiliares.

#### mas_vieja

```
def mas_vieja(self):
    NW = self.notWorking()
  	#pags que no estan el WS

    oldest = 3000
    #asegurar que sea mayor al virtual time

    oldInd = self.index
    #donde estoy parada ahora mismo; saber desde donde empezar

    if len(NW) > 0:
    #tengo al menos una pag fuera del WS, pudo evitar sacar paginas que me son necearias
    #items estan construidos [[pag, tiempo, ref bit], indice lista pags]

      for item in NW:
        if item[0][1] < oldest:
          #campo del tiempo de la pag

          oldest = item[0][1]  #actualizar el tiempo
          oldInd = item[1]  #indice de la lista de pags

        if item[0][2] == 0:
          #el ref bit de la pag es 0, es lo que voy a reemplazar
          return oldInd

        elif item[0][2] == 1:
          #pon el ref en 0
          item[0][2] = 0
          continue

      #apuntado a donde cambie la pag
      self.index = oldInd
      return oldInd

    else:

      #lo mismo que en NW, pero usando enumerate para indexar la lista
      for index, item in enumerate(self.pags):
        if item[1] < oldest:
          oldest = item[1]
          oldInd = index
        if item[2] == 0:
          return oldInd
        elif item[2] == 1:
          item[2] = 0
          continue
      self.index = oldInd
      return oldInd
```

mas_vieja requiere la funcion auxiliar notWorking, que es una funcion que me dice las paginas que NO estan en el WS. Es decir, su edad es mayor al TAU dado.

Si tengo al menos una pagina que no este en el WS voy a chequear eso primero.

#### clocking

clocking el la funcion que recorre la lista. Esta funcion mantiene registro de que paginas a visto y cuales no para saber si las tiene que cambiar o no. Es aqui donde se usa la clase Paging, previamente mencionada. 

Tambien tiene que acordarse de por donde va en el reloj para saber desde donde empezar a chequear paginas para removerlas.

```
  def clocking(self, pages):
    for page in pages:
      if page not in self.memory:
        if len(self.pags) < self.cap:
          self.memory.append(page)
          #que pags tengo en memoria, los nums de las paginas

          self.create_page(page, self.VIRTUAL_CLOCK)
          #crear una nueva pagina con mi contructor Paging

          self.pageFaults += 1
          self.tick()  #mover la manecilla por cada page fault
        else:
        #no tengo espacio, tengo que cambiar algo

          indiceCambio = self.mas_vieja()
          self.memory[indiceCambio] = page
          #actualizar la memoria

          self.replacePage(page, self.VIRTUAL_CLOCK, indiceCambio)
          #tengo que cambiar lo que tengo en la posicion donde se quedo la manecilla

          self.pageFaults += 1
          self.tick() 
      else:
        self.update_page(page, self.VIRTUAL_CLOCK)
        #vi la pagina de nuevo, tengo que actualizar el time of last access de esta pag en esepcifico

      self.VIRTUAL_CLOCK += 1  #cada iteracion es 1s
    print("page faults: ", self.pageFaults)
```

Las funciones auxiliares son las que ayudan que el programa se actualize correctamente. Esas se encuentran en el codigo fuente.

## Fuentes consultadas

list-remove dupes: 
https://www.w3schools.com/python/python_howto_remove_duplicates.asp 

optimal source: 
https://www.youtube.com/watch?v=jeJIKKQcqpU&t=518s

clases: 
https://www.w3schools.com/python/python_classes.asp

Modern Operating Systems Third Edition Book

## Personas consultadas

Dr. Jose Ortiz Ubarri

Sergio Rodriguez
