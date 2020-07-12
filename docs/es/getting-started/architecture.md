# Introducción a los conceptos de Retic

Retic es un marco de trabajo para crear **aplicaciónes del lado del servidor**. Retic está escrito en Python. Utiliza Werkzeug como servidor y está basado en los conceptos de **express.js**.

Una aplicación se define por **rutas y servicios**. Retic provee la clase ``Router`` que ayuda a definir los puntos de acceso de la aplicación.

Retic recomienda la siguiente estructura de directorios para una fácil escalabilidad y mantenibilidad de la aplicación.

```sh
retic-example
│
└───controllers
│   │   controller1.py
│   │   controller2.py
│   │   ...
│
└───models
│   │   __init__.py
│   │   model1.py
|   │   model2.py
|   │   ...
│
└───routes
│   │   routes.py
|   │   ...
│
└───services
│   │
│   └───service1
│       │   service1.py
│       │   service2.py
│       │   ...
|   │   ...
│
│   .env
│   app.py
│   requirements.txt
```

## Controladores

Los controladores están vinculados a las rutas de su aplicación, gestionan las solicitudes HTTP entrantes y deciden que servicios deben realizar el trabajo para dar una respuesta correcta al cliente.

Por ejemplo, la ruta GET ``/files/:id`` en su aplicación podría estar vinculada a un controlador como:

```python

# controllers\files.py

# Retic
from retic import Request, Response, Next

# Services
import services.files.files as files

def get_by_id(req: Request, res: Response, next: Next):
    """Obtener un archivo por su ientificador"""

    _file_db = files.get_by_id_db(req.param("id"))

    """Revisar si se encontró el archivo, caso contrario, responder un mensaje de error"""
    if _file_db['valid'] is False:
        res.not_found(_file_db)
    else:
        res.ok(_file_db)


```

Cada controlador recibe los siguientes parametros:

* [Request][docs_hooks_req]: Representa una solicitud HTTP hacia el servidor.
  
* [Response][docs_hooks_res]: Representa una respuesta al cliente desde el servidor.
  
* [Next][docs_hooks_next]: Permite pasar el control de la petición al siguiente controlador.

## Enrutamiento

Se refiere a definir cómo una aplicación responde a una solicitud del cliente, utilizando metodos HTTP.

Cada ruta puede tener una o más controladores, los cuales se ejecutan cuando la ruta coincide.

La definición de una ruta toma la siguiente estructura:

```python
app.METHOD(PATH, [HANDLER, ...])
```

Dónde:

* ``app`` es una instancia de la clase ``Router``.

* ``METHOD`` es un [método HTTP][firefox_http_methods] el cual debe estar en minúsculas.

* ``PATH`` es una ruta en el servidor.

* ``HANDLER`` es el controlador que se ejecuta cuando la ruta coincide. Cada ruta puede tener una o más controladores.
  
Los siguientes ejemplos ilustran la definición de rutas con los metodos más utilizados en un [CRUD][wiki_crud].

Responde con ``Hola mundo`` en la página de inicio:

```python

# routes\routes.py

# Retic
from retic import Router

router = Router()

router \
    .get("/", lambda req, res, next: res.send({"msg": "Hola mundo - HTTP GET"})) \
    .post("/", lambda req, res, next: res.send({"msg": "Hola mundo - HTTP POST"})) \
    .put("/", lambda req, res, next: res.send({"msg": "Hola mundo - HTTP PUT"})) \
    .delete("/", lambda req, res, next: res.send({"msg": "Hola mundo - HTTP DELETE"}))
```

Para más detalles visita la [guía de enrutamiento][docs_routing].

## Servicios

Retic recomienda estructurar la aplicación de forma modular. Independizar el funcionamiento de los controladores de los servicios que realizan su acción. Fácilitando la integración con las diferentes pruebas que la aplicación requiera. Además, de minimizar el código repetido.

```python

# services\files\files.py

"""Services for files controller"""

# Retic
from retic import env, App as app

# Google
from services.googledrive.googledrive import GoogleDrive

# Filetype
import filetype

# Models
from models import File, Folder

# Services
from retic.services.responses import success_response_service, error_response_service

# Utils
from services.utils.general import get_bytes_from_mb, get_mb_from_bytes

def get_by_id_db(id):
    """Encontrar un archivo en la base de datos en base a un identificador

    :param id: Identificador en la base de datos
    """

    """Realizar la busqueda"""
    _session = app.apps.get("db_sqlalchemy")()
    _file = _session.query(File).filter_by(cloud=id).first()
    _session.close()

    """Validar que el archivo exista, caso contrario, mostrar un error"""
    if not _file:
        return error_response_service(msg="File not found.")
    else:
        return success_response_service(
            data=_file.to_dict(), msg="File found."
        )

```

## Archivo principal de la Aplicación

El archivo principal únifica los controladores, las rutas, los servicios y crea el servidor de la aplicación.

```python

# app.py

"""Main app"""

# Retic
from retic import App as app

# Routes
from routes.routes import router

# SQLAlchemy
from services.sqlalchemy.sqlalchemy import config_sqlalchemy

# Definir la ruta del archivo de variables de entorno
app.env.read_env('.env')

# Agregar las rutas a la aplicación
app.use(router)

# Agregar configuración de la base de datos
app.use(config_sqlalchemy(), "db_sqlalchemy")

# Crear un servidor web
app.listen(
    use_reloader=True,
    use_debugger=True,
    hostname=app.env('APP_HOSTNAME', "localhost"),
    port=app.env.int('APP_PORT', 1801),
)

```

Por defecto retic utiliza el archivo ``.env`` para buscar las variables de entorno, sin embargo, la ruta del archivo puede ser diferente e incluso cargarlas directamente desde el sistema. Para más información visita la sección de [environment][docs_services_env].

## Utilerias

Retic cuenta con una biblioteca de servicios más utilizados para dar ayudarte en que te enfoques en lo que verdaderamente importa, la lógica de tu aplicación.

Para más detalles visita la [guía de utilerias][docs_services].

[firefox_http_methods]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods

[wiki_crud]: https://en.wikipedia.org/wiki/Create,_read,_update_and_delete

[docs_routing]: https://github.com/reticpy/retic/blob/dev_initial_app/docs/es/guide/routing.md

[docs_hooks_req]: https://github.com/reticpy/retic/blob/dev_initial_app/docs/es/hooks/request.md

[docs_hooks_res]: https://github.com/reticpy/retic/blob/dev_initial_app/docs/es/hooks/response.md

[docs_hooks_next]: https://github.com/reticpy/retic/blob/dev_initial_app/docs/es/hooks/next.md

[docs_services_env]: https://github.com/reticpy/retic/blob/dev_initial_app/docs/es/services/enviroment.md

[docs_services]: https://github.com/reticpy/retic/blob/dev_initial_app/docs/es/services/services.md
