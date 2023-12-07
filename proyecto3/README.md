# Distributed File System Implementation

## Adiriana N Hernandez Vega

## CCOM 4017 - Operating Systems

El proyecto consiste en la implementacion de un sistema de archivos distribuido que contiene

  - Un meta data server 

  - Una data node server

  - Un cliente copy

  - Un cliente ls

  - Una base de datos para los inodes


## Metadata server

Meta data consiste en el servidor principal. Este es el que se encarga de insertar todas las funciones en la base de datos. 

Al tener acceso a la base de datos, este tambien se encarga de aceptar y progresar los "requests" de los diferentes requests de los clientes. 

### Como correr el metadata: 

```
python meta-data.py <port, default=8000>
```
## Data node server

Data node es el segundo componenente importante del DFS. Este se encarga de dos funciones prinicipales: put y get

### Comando put:

El comando put se encarga de insertar cualquier file que quieras copiar (copy cliente) al meta data server. 

La manera en que hace esto es que genera un ID unico (para que se puede identificar en el metadata facilmente). 

EL file generado de este comando es creado recibiendo la informacion que va en el file en pedazos de tamano 4kb hasta que llega al tamano de la particion eespecificado por el copy client. Esto nos permite guardar files de gran tamano usando pocos servers/nodos. Todos estos pedazos son guardados en una lista de pedazos para luego ser concatenados y escritos en el file identificado por el ID con "wb". 

### Comando get:

El comando get se encarga de reconstruir cualquier file insertado en el data node por el comamdo put. Esencialemte es lo opuesto a put. Este comando tiene el tamano de las particion. El server va leyendo el file (en pedazos de 4k) hasta llegar al tamano de la particion y se los va enviando al cliente copy. Una vez lee una particion completa, este sigue con la siguiente hasta terminar.

### Como correr data node:

```
python data-node.py <server address> <port> <data path> <metadata port,default=8000>
```

## Copy client

El copy client es la otra parte importante para que el metadata funcione. Tiene las mismas dos funciones que el data node server, solo que con funcionalidad opuesta. 

### CopyToDfs

CopyToDfs se encarga, junto al put en data node, de almaacenar un archivo de tu computadora en el server metadata. Para lograr esto hay que tener dos cosas importantes:

  - Los data nodes a donde voy a mandar los pedazos del file - En un for loop se hace la conexion con cada uno de ellos para mandarle la informacion
    
  - El tamano de la parte del file que le voy a mandar (tamano del file total / cantidad de nodos)
    
Copy va leyendo la informacion en el file que se desea copiar y se la manda al data node en pedazos de tamano 4k haste llegar al tamano de la particion.

Una vez se termina de leer y almacenar en el meta data, el data node server le manda un id unico al copy. Luego el copy se encarga de preparar la informacion para mbdarsela al meta data server de la siguiente manera.

```
[(ip, port, uid1), (ip, port, uid2)]
```

donde cada uno de los ip y ports son la conexion al nodo que contiene ese pedazo de file en el metadata.

### Como correr el copytodfs:

```
python copy.py <source file> <server>:<port>:<dfs file path>
*el server y port son esos correspondientes al meta-data server
```

### CopyFromDfs

CopyFromDfs se encarga, junto al get en data node, de reconstruir los files en el metadata server y devolverlos al usuario. Para lograr esto solo necesitamos el destintion file. Esta funcion solo se encarga de recibir toda la imformacion por parte de get e irla escribieno en el file. 

Una vez este termina de recibir / escribir informacion, obtenemos el file que habiamos partido en el meta-data server reconstruido en nuestra computadora. 

### Como corrrer el copyfromdfs:

```
python copy.py <server>:<port>:<dfs file path> <destination file>
```

## LS client

El cliente ls se encarga de conectarse con el meta data server y obtener todos los files que se encuentran en el DFS.

Luego este le despliega los nombres de los files junto al tamano de cada uno al usuario en la pantalla del meta data server.

### Como correr ls:

```
python ls.py <server>:<port, default = 8000>
```

## Base de datos

El proyecto viene con su propia base de datos para poder copiar, desplegar, y recuperar files

### Como crear la base de datos: 

```
python createdb.py
```

### Como borrar la base de datos

```
rm dfs.db
```
## Colaboradores

Sergio Rodriguez

Yadiel Camis

Sergio Mattei

Jose Ortiz
