# proyecto_modulo_4

la ruta del proyecto es https://github.com/joseGallardocollab/proyecto_modulo_4.git

El ingreso del login es y solo permite 3 intentos.

user: admin
pass: 1234

En este proyecto añadi demaciadas funciones como por ejemplo el login que no se solicitaba pero lo quise añadir.
La modulación de las carpetas contiene:

    -Carpeta raíz app donde se aloja el archivo de la aplicación "app_tkinter.py", ".gitignore", "datos_cliente_log" y el UML de clases.
    -Carpeta clases, donde se aloja el archivo clientes.py.
    -Carpeta config, donde se aloja el usuario y contrasela simulando un mok de una base de datos o dato externo desde api.

El proyecto contiene una clase principal Cliente y subClases Regular, Primium y Corporativo con sus diferentes getters y setters y la función __str__ para listar
--------------------------------------

-La estructura del desarrollo permite acceder con el login, ingresar nombre de cliente, email y telefono con sus respectivas validaciones.
-La estructura de la aplicación es basica pero cumple con ser simple para un uso intuitivo.
-Para editar y eliminar clientes se debe seleccionar desde la lista.

-Las validaciones cuentan con try y funciones que solicitan el ingreso de formato correcto al escribir levantando ventanas de mensaje en caso de no cumplir el formato.
-Añadi la validación para que el nombre de un cliente no se pueda repetir al crear un cliente.
-Añadi funciones a los campos para que en caso de seleccionar un tipo de cliente en el dropbox, se habilite o deshabilite el campo empresa.
-Añadi una funcionalidad para que los campos se limpien luego de cualquier función por botón.
-Añadi una función para actualizar la lista de cliente al crear, editar y eliminar clientes.
-Añadi una función que rellena los campos al seleccionar una lista y que además mantiene el foco de lista seleecionado para poder editar.

Por último añadi una funcionalidad extra que recupera y genera un log a tiempo real con las iteraciones crear, editar y eliminar en el archivo "dato_cliente_log.txt".
Este log esta generado para obtener los datos a tiempo real y terminar la función cuando termina su uso.


