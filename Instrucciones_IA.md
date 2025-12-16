# Prompt para el código

Neceisto crear un API REST en python (falsk) que implemente un CRUD de las siguientes entidades:
- Comercial, con los campos: Id, Nombre, Apellidos
- Cliente, con los campos: Id, Nombre
- Tipo de Actividad: con los campos: id, descripcion
- Actividad, con los campos: Id, fecha, id_tipo_actividad, id_comercial, id_cliente, titulo, descripcion

Me gustaria adicionalmente cerar test unitarios y un dockerfile , lo mas peuqeño posible, para construir la imagen con el código y subirla a un registry.

Adicionalmente, necesito crear un programa en Rust que lea un fichero excel y linea por linea vaya realizando las siguientes tareas:
- Comprobando la existencia o no del cliente (campo Company / Account) en el sistema y creandolo en caso de no existir, guardadndo el id para usarlo posteriomente
- Recuperando el Id dle comercial (campo Created by)

- Recuperando el Id del comercial de la actividad y crando una actividad con los campos necesarios, leyendo los campos del fichero y llamando al API del paso anterior.


