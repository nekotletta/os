# Distributed File System Implementation

### Adiriana N Hernandez Vega

### CCOM 4017 - Operating Systems

El proyecto consiste en la implementacion de un sistema de archivos distribuido que contiene

  - Un meta data server 

  - Una data node server

  - Un cliente copy

  - Un cliente ls

  - Una base de datos para los inodes


### Metadata server

Meta data consiste en el servidor principal. Este es el que se encarga de insertar todas las funciones en la base de datos. 

Al tener acceso a la base de datos, este tambien se encarga de aceptar y progresar los "requests" de los diferentes requests de los clientes. 

Como correr el metadata: 

```
python meta-data.py <port, default=8000>
```
### Data node server

Data node es el segundo componenente importante del DFS. Este se encarga de dos funciones prinicipales: put y get

#### Comando put:

El comando put se encarga de insertar cualquier file que quieras copiar (copy cliente) al meta data server. 

La manera en que hace esto es que genera un ID unico (para que se puede identificar en el metadata facilmente). Este ID es concatenado a la extension ".data" para identifcar los files de manera mucho mas facil en la computadora. 

EL file generado de este comando es creado recibiendo la informacion que va en el file en pedazos de tamano 4kb hasta que llega al tamano de la particion (size / cantidad de servers). Esto nos permite guardar files de gran tamano usando pocos servers/nodos. Todos estos pedazos son guardados en una lista de pedazos. Todos estos pedazos son escritos en el file con "wb". 

#### Comando get:

El comando get se encarga de reconstruir cualquier file insertado en el data node por el comamdo put. Esencialemte es lo opuesto a put. Este comando lee el file (en pedazos de 4kb) y manda todo lo leido al cliente copy. 

Como correr data node:

```
python data-node.py <server address> <port> <data path> <metadata port,default=8000>
```

### ls client

El cliente ls se encarga de conectarse con el meta data server y obtener todos los files que se encuentran en el DFS.

Luego este se los despliega al usuario en la pantalla del metadata.
