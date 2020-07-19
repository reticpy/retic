---
title: Services
type: services
order: 1
---


Retic cuenta con un conjunto de servicios para apoyarte en cierto tipo de funcionalidades que tu aplicacion necesita.

## Servicios de respuesta

Es importante definir un estandar de respuesta a una petición del cliente, para la mantenibilidad de una aplicación. Retic recomienda seguir una estructura de 3 atributos.

```json

{
    "valid": bool,
    "msg": str,
    "data": dict
}

```

Donde:

* valid: Representa que una petición se ha realizado correctamente cuando su valor es ``True``, o en caso contrario contiene errores, su valor es ``False``.

* msg: Mensaje que describe el resultado de la petición.

* data: Información de respuesta a la petición del cliente.

### success_response_service(*data: any* = None, *msg: str* = "")

Define la estructura de una respuesta a una petición del cliente en formato JSON e indica que todo finalizó correctamente.

**Parámetros:**

* data: Información a enviar al cliente.

* msg: Mensaje que indica que la petición se completó correctamente.

```python

# Retic
from retic import Request, Response
from retic.services.responses import success_response_service

def upload(req: Request, res: Response):
    """Upload to Storage"""
    res.ok(success_response_service(
        data={u'msg': 'say hi!'},
        msg="The upload finishied."
    ))

```

A continuación se presenta el resulta de la petición en formato JSON.

```json

{
    "valid": true,
    "msg": "The upload finishied.",
    "data":{
        "msg":"say hi!"
    }

}

```

### error_response_service(*msg: str* = "")

Define la estructura de una respuesta a una petición del cliente en formato JSON la cual contiene errores.

**Parámetros:**

* msg: Mensaje que indica que la petición no sé completo correctamente porque contiene errores.

```python

# Retic
from retic import Request, Response
from retic.services.responses import error_response_service

def upload(req: Request, res: Response):

    """Return a error message."""
    return res.bad_request(
        error_response_service(
            "The param files is necesary."
        )
    )

```

A continuación se presenta el resulta de la petición en formato JSON.

```json

{
    "valid": false,
    "msg": "The param files is necesary."
}

```

## Servicios generales

Retic proporciona una variedad de servicios generalizados, con enfoque en validación de parámetros obligatorios y otras funcionalidades.

### Servicios de URLs

#### urlencode(*url: str*)

Esta función es conveniente cuando se codifica una cadena para usar parte de una URL en una consulta como una forma conveniente de pasar variables a la página siguiente.

**Parámetros:**

* url: URL a codificar.

```python

# Retic
from retic.services.general.urls import urlencode

def get_from_req(url):
    """Codificar la url"""
    url_encode = urlencode(url)

```

```sh
# Entrada
"http://example.com/"

# Salida
"http%3A%2F%2Fexample.com%2F"

```

#### slugify(*text: str* = "")

Simplifica las cadenas feas en URL amigables.

**Parámetros:**

* text: Texto a simplificar de tipo ``str``.

```python

# Retic
from retic.services.general.urls import slugify

def get_slug_from_title(title):
    """Get slug from a title"""
    return slugify(title)

```

```sh
# Entrada
"This Alpha’s Pheromones Are Exploding"

# Salida
"this-alphas-pheromones-are-exploding"

```

### Servicios del Tiempo

#### sleep(*seconds: int* = 0)

El método de tiempo Python sleep() suspende la ejecución por el número de segundos dado. El argumento puede ser un número de coma flotante para indicar un tiempo de descanso más preciso.

**Parámetros:**

* seconds: Total de segundos que el programa estará durmiendo.

```python

# Retic
from retic.services.general.time import sleep

# Contantes
SLEEP_TIME=2

def download_from_url(url):
    """Dormir el programa durante un tiempo especifico"""
    sleep(SLEEP_TIME)

```

## Sericios de validación

Retic ofrece la capacidad de validar ciertos requisitos en una petición de forma nativa. Por ejemplo que los parámetros obligatorios en una petición sean válidos.

### validate_obligate_fields(*fields: any* = None)

La mayoría de las veces existen valores que son obligatorios, Retic ofrece el servicio ``validate_obligate_fields(...)`` que verifica si una lista de parámetros obligatorios son validos.

**Parámetros:**

* fields: Diccionario que contiene todos los parámetros que son obligatorios, esos valores pueden ser de tipo ``list`` o simples valores.

El siguiente ejemplo valida que exista el parametro ``files`` el cual se obtiene cuando se envia un archivo en una petición.

```python

# Retic
from retic import Request, Response

# Services
from retic.services.validations import validate_obligate_fields
from retic.services.responses import error_response_service

def upload(req: Request, res: Response):
    """Obtener una lsita desde la petición, si no existe, retorna una lista vacia por defecto.
    """

    _files = req.files.getlist('files') or list()

    """Validar si todos los campos obligatorios son validos"""
    _validate = validate_obligate_fields({
        u'files': _files
    })

    """Si existe algún campo invalido, retorna un mensaje de error y una respuesta de tipo 400 Bad request.
    """
    if _validate["valid"] is False:
        return res.bad_request(
            error_response_service(
                "The param {} is necesary.".format(_validate["error"])
            )
        )

```

## Servicios JSON

Servicios para la manipulación de objetos tipo JSON y su equivalente en otros formatos.

### jsonify(*object: any*)

Convierte un diccionario JSON a su equivalente en cadena de texto.

**Parámetros:**

* object: Es el objeto de respuesta del cliente, si el objeto es str, devuelve su valor sin transformación, de lo contrario crea una representación del objeto en formato JSON.

```python

# Retic
from retic import Request, Response
from retic.services.general.json import jsonify

def upload(req: Request, res: Response):
    text = jsonify({u'msg': 'say hi!'})

```

A continuación se presenta el resulta de la petición en cadena de texto.

```sh

text: '{"msg": "say hi!"}'

```

### parse(*content: str*)

Deserializar (una instancia de str, bytes o bytearray que contiene un documento JSON) a un objeto Python.

**Parámetros:**

* object: Contenido de type str, bytes o bytearray que contiene un JSON válido.

```python

# Retic
from retic import Request, Response
from retic.services.general.json import parse

def upload(req: Request, res: Response):
    text_json = parse('{"msg": "say hi!"}')

```

A continuación se presenta el resulta de la petición en formato JSON.

```sh

text_json: {"msg": "say hi!"}

```
