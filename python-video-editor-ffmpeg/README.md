# Crear un entorno virtual

### Código windows:

`py -m venv my_venv`

### Código Linux

`python3 -m venv my_venv`

# Activar entorno virtual

### Código windows:

`.\my_venv\Scripts\activate`

### Código Linux

`source my_venv/bin/activate`

### Instalar dependencias

`pip install -r requirements.txt`

# Iniciar Script

### Código windows:

`py main_mejorado.py`

### Código Linux

`python3 main_mejorado.py`

# Inputs de datos

> Al comenzar el script nos pedirá ingresar 2 datos esenciales:

- La ruta del directorio de los videos sin editar
- La ruta en donde se guardarán los videos editados

# Aclaraciones

- Es importante saber que los videos que se van a editar deben tener formato MP4
- Se recomienda que el nombre del archivo sea exactamente el ID del recurso.

# Formato de archivo CSV

> El archivo CSV debe tener 3 columnas, **ID**, **TYPE** y **CORTES** para que pueda ser válido, de lo contrario el script dará error.
> La columna ID se usará para buscar dentro de la carpeta de los videos sin editar el archivo MP4 que tenga de nombre este ID.
> La columna TYPE se usará para identificar si el archivo en efecto es un **Video** o si se debe ignorar, si ponemos algo diferente a **video** el script ignorará esa fila
> La columna CORTES es dónde van los tiempos de cortes del video que se deben visualizar en la edición y estos van separados por el caracter "|"
> Los cortes pueden ser varios, pero siempre deben ser par, ya que el script siempre tomará un inicio y un fin de un corte.
> Por ejemplo:
>
> - 00:00:00|00:01:52
> - 00:00:21|00:02:30|00:02:56|00:04:05
>
> **En el primer ejemplo** estamos diciendo que nuestro corte empieza en la hora 00, segundo 00, minuto 00 y va hasta la hora 00, minuto 01 y segundo 52.
>
> **En el segundo ejemplo** tenemos 2 cortes que se unirán para formar 1 solo video. Ahí estamos diciendo que el primer corte empieza en la hora 00, el minuto 00 y el segundo 21
> hasta la hora 00, el minuto 02 y el segundo 30.
> Luego tenemos un segundo corte que empieza en la hora 00, el minuto 02 y el segundo 56 hasta la hora 00, el minuto 04 y el segundo 05.
