---
title: Response
type: hooks
order: 2
---

El objeto ``res`` es una instancia de la clase ``Response``. Representa la respuesta a una petición HTTP realizada por un cliente.

## Propiedades de la clase Response

A continuación se presentan las principales propiedades de la clase ``Response`` y su funcionalidad. Se utiliza el siguiente [archivo de Postman][retic_postman_collection] para ejemplicar su uso.

### default_mimetype

Todas las respuestas tienen un por defecto un mimetype  ``text/plain``.

```python

# Valor actual de default_mimetype
res.default_mimetype: 'text/plain'

```

### default_status

Todas las respuestas tienen un por defecto un codigo de estado de respuesta ``status 200``.

```python

# Valor actual de default_status
res.default_status: 200

```

### headers

Lista de todas las cabeceras de la respuesta. Por defecto, todas las peticiones tienen la cabecera. ``'content-type': 'application/json'``

```python

# Valor actual de headers
Headers([('content-type', 'application/json'), ('Access-Control-Allow-Methods', 'True'), ('Access-Control-Allow-Credentials', 'GET,POST,DELETE,PUT,OPTIONS'), ('Access-Control-Allow-Origin', '*'), ('Access-Control-Allow-Headers', 'Content-Type'), ('Access-Control-Expose-Headers', 'Content-Type')])

```

### status

Código de estado de la respuesta en formato de cadena de texto.

```python

# Valor actual de status
res.status: '200 OK'

```

### status_code

Código de estado de la respuesta en formato númerico.

```python

# Valor actual de status_code
res.status_code: 200

```

## Funciones de la clase Response

La clase Response utiliza las siguientes funciones para manipulación de su información.

### bad_request(*content: any* = "")

Este método responde con un *400 Bad Request* a la petición del cliente, esto indica que la solicitud no es válida.

Esto generalmente significa que la solicitud contenía parámetros o cabeceras no válidas, o que intentó hacer algo que la lógica de su aplicación no admite.

**Parámetros:**

* content: Información para enviar al cliente, un mensaje, un diccionario, etc. Si no existe, envía un mensaje de estado basado en el código de estado.
  
```python

# Retic
from retic.services.responses import error_response_service
from retic.services.general import validate_obligate_fields

def upload(req: Request, res: Response):

    """Revisar que todos los parametros obligatorios sean validos"""
    _validate = validate_obligate_fields({
        u'files': _files
    })

    if _validate["valid"] is False:
        return res.bad_request(
            error_response_service(
                "The param {} is necesary.".format(_validate["error"])
            )
        )

```

```sh

# Salida:
{
    "valid": false,
    "msg": "The param files is necesary."
}

```

### forbidden(*content: any* = "")

Este método se utiliza para enviar una respuesta *403 forbidden* al cliente, indicando que una solicitud no está autorizada.

Esto generalmente significa que el agente de usuario intentó hacer algo que ellos no estaban autorizados para hacerlo, como cambiar la contraseña de otro usuario.

**Parámetros:**

* content: Información para enviar al cliente, un mensaje, un diccionario, etc. Si no existe, envía un mensaje de estado basado en el código de estado.
  
```python

# Retic
from retic import Request, Response
from retic.services.responses import error_response_service

# Services
from services.users.users as users

def login(req: Request, res: Response):

    """Revisar que todos los parametros obligatorios sean validos"""
    _user = users.login({
        u'username': "user1",
        u'password': "123",
    })

    if _user["valid"] is False:
        return res.forbidden(
            error_response_service("User is invalid.")
        )

```

```sh

# Salida:
{
    "valid": false,
    "msg": "User is invalid."
}

```

### not_found(*content: any* = "")

Este método se utiliza para enviar una respuesta *404 not_found*.

Cuando se llama manualmente desde el código de su aplicación, este método normalmente se usa para indica que el cleinte intentó encontrar, actualizar o eliminar algo que no existe.

**Parámetros:**

* content: Información para enviar al cliente, un mensaje, un diccionario, etc. Si no existe, envía un mensaje de estado basado en el código de estado.
  
```python

# URL de la petición HTTP
GET: http://localhost:1801/folders/86698adcb9b711eaa7524c0082ae1a80

# Retic
from retic import Request, Response

# Services
from services.files.files as files

def get_by_folder(req: Request, res: Response):
    """Obtener archivos en base a su directorio"""
    _files_db = files.get_all_by_folder_db(
        req.param("folder")
    )

    """Revisar si se encontró el folder, caso contrario, retornar un error."""
    if _files_db['valid'] is False:
        res.not_found(_files_db)
    else:
        res.ok(_files_db)

```

```sh

# Salida:
{
    "valid": false,
    "msg": "Folder not found."
}

```

### ok(*content: dict* = None)

Este método se utiliza para enviar una respuesta *200 OK* al cliente.

**Parámetros:**

* content: Información para enviar al cliente, un mensaje, un diccionario, etc. Si no existe, envía un mensaje de estado basado en el código de estado.
  
```python

# URL de la petición HTTP
GET: http://localhost:1801/folders/77698adcb9b711eaa7524c0082ae1a80

#Retic
from retic import Request, Response

# Services
from services.files.files as files

def get_by_folder(req: Request, res: Response):
    """Obtener archivos en base a su directorio"""
    _files_db = files.get_all_by_folder_db(
        req.param("folder")
    )

    """Revisar si se encontró el folder, caso contrario, retornar un error."""
    if _files_db['valid'] is False:
        res.not_found(_files_db)
    else:
        res.ok(_files_db)

```

```sh

# Salida:
{
    "valid": true,
    "msg": "Files found.",
    "data": {
        "success": [
            {
                "mimetype": "image/png",
                "filename": "200px-Flag_of_Spain.svg.png",
                "created_at": "2020-06-28 22:20",
                "cloud": "87PMm6OqszntRW3EyvVEbExRGOlpdQBay",
                "parent": "981PKTP0_qmfuAtFjbvF1bU6uiUv8UERs",
                "size": 4880,
                "extension": "png",
                "file": 1
            }
        ],
        "code": "78698adcb9b711eaa7524c0082ae1a90",
        "description": "",
        "created_at": "2020-06-28 22:20",
        "parent": null
    }
}

```

### server_error(*content: any* = "")

Este método se utiliza para enviar una respuesta *500 Server error* al cliente, indicando que ocurrió algún tipo de error del servidor

**Parámetros:**

* content: Información para enviar al cliente, un mensaje, un diccionario,  etc. Si no existe, envía un mensaje de estado basado en el código de estado.
  
```python

#Retic
from retic import Request, Response

def undefined(req: Request, res: Response):
    res.server_error(
        error_response_service("Controller is invalid.")
    )

```

```sh

# Salida:
{
    "valid": false,
    "msg": "Controller is invalid."
}

```

### send(*content: any* = "")

Envia una respuesta de cadena en un formato(XML, CSV, texto plano). Respuestas en formato JSON, etc. Se recomienda su uso en el caso que se necesite enviar una respuesta de éxito al cliente con un codigo de estado diferente de 200. Ver [set_status](#set_statuscode-int).

Este método se utiliza en la implementación subyacente de la mayoría de los otros métodos de respuesta de terminal.

**Parámetros:**

* content: Información para enviar al cliente, un mensaje, un diccionario, etc. Si no existe, envía un mensaje de estado basado en el código de estado.
  
```python

#Retic
from retic import Request, Response

def say_hi(req: Request, res: Response):

    return res.send("Hi!")

```

```sh

# Salida:
Hi!

```

### set_headers(*headers: dict*, *value: str* = None)

Establece cabeceras de respuesta con valores especificos.

Alternativamente, se puede pasar un objeto que contenga cabeceras para configurar múltiples valores a la vez, donde las claves son los nombres de las cabeceras y los valores correspondientes son los valores deseados.

**Parámetros:**

* headers: Puede ser de tipo ``dict``, para representar un objeto de cabeceras que se agregarán a las cabeceras actuales. Si es de tipo ``str`` se utilizará para acceder a una cabecera en especifico. Cualquier otro formato provocará una excepción de error.

* value: Valor a asignar a la cabecera especificada. Por defecto tiene un valor de ``None``.
  
```python

#Retic
from retic import Request, Response

def say_hi(req: Request, res: Response):

    res.set_headers('content-type', "text/plane")

    res.ok({u"msg": "say hi!"})

```

```sh

# Salida:
{"msg": "say hi!"}

## Cabeceras de la respuesta
content-type: text/plane

```

### set_status(*code: int*)

Establezca el código de estado para la respuesta HTTP.

**Parámetros:**

* code: Número que representa el código de estado de la respuesta HTTP
  
```python

#Retic
from retic import Request, Response

def upload(req: Request, res: Response):

    res.set_status(201).send({u"msg": "file created!"})

```

```sh

# Salida:
{
    "msg": "file created!"
}

## Código de estado
201 Created

```

### redirect(*new_url: str*)

Redirige a otra url. Utiliza redirección permanente con código de estado 308.

**Parámetros:**

* new_utl: URL a redirigir.
  
```python

#Retic
from retic import Request, Response

def upload(req: Request, res: Response):

    return res.redirect("http://example.com/")

```

```sh

## Código de estado
308 Permanent Redirect
...

```

## Otras propiedades y funciones

Retic hereda de la clase ``Response de Werkzeug`` para la gestión de las respuestas de peticiones, visita la documentación acerca de su clase [Response][doc_werkzeug_res] para complementar la información aquí mencionada.

[doc_werkzeug_res]: https://werkzeug.palletsprojects.com/en/1.0.x/wrappers/#werkzeug.wrappers.Response

[retic_postman_collection]: https://github.com/reticpy/retic/blob/dev_documentation/docs\es\guide\Retic.postman_collection.json