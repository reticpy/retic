# Introducción a los conceptos de Retic

Retic es un marco de trabajo para crear **aplicaciónes del lado del servidor**. Retic está escrito en Python. Utiliza Werkzeug como servidor y está basado en los conceptos de **express.js**.

Una aplicación se define por **rutas y servicios**. Retic provee la clase ``Router`` que ayuda a definir los puntos de acceso de la aplicación.

Retic recomienda la siguiente estructura de directorios para una fácil escalabilidad y mantenibilidad de la aplicación.

```sh
retic-example
│
└───apps
│   │   urls.py
│   │   ...
|
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
│   .env.development
│   .env.production
│   app.py
│   requirements.txt
│   settings.py
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

# Controllers
import controllers.files as files

"""Definir la instancia de las rutas"""
router = Router()

"""Definir todas las rutas - /"""
router \
    .get("/", lambda req, res, next: res.send({"msg": "Hola mundo - HTTP GET"})) \
    .post("/", lambda req, res, next: res.send({"msg": "Hola mundo - HTTP POST"})) \
    .put("/", lambda req, res, next: res.send({"msg": "Hola mundo - HTTP PUT"})) \
    .delete("/", lambda req, res, next: res.send({"msg": "Hola mundo - HTTP DELETE"}))

"""Definir todas las rutas - files"""
router \
    .post("/files", files.upload) \
    .get("/files/:id", files.get_by_id)

```

Para más detalles visita la [guía de enrutamiento][docs_routing].

## Servicios

Retic recomienda estructurar la aplicación de forma modular. Independizar el funcionamiento de los controladores de los servicios que realizan su acción. Fácilitando la integración con las diferentes pruebas que la aplicación requiera. Además, de minimizar el código repetido.

```python

# services\files\files.py

"""Servicios para el controlador de archivos"""

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

# Settings
import settings

# Apps
from apps.urls import APP_BACKEND

# Routes
from routes.routes import router

# SQLAlchemy
from services.sqlalchemy.sqlalchemy import config_sqlalchemy

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

## Archivo de configuración

Durante el desarrollo de nuestra aplicación, muchas veces es necesario declarar valores constantes al inicio de cada archivo ``.py`` y estos pueden depender de valores variables de la aplicación, por ejemplo, valores que se obtienen de los archivos de variables de entorno (.env).

Por tal razón, Retic recomiendo utilizar un archivo ``settings.py`` donde se importe todas estás variables y sean agregadas a la configuración de Retic para poder ser utilizadas dentro de toda la aplicación.

```python

# settings.py

# Retic
from retic import App as app

"""Set environment file path"""
app.env.read_env('.env.development', override=True)

```

Por defecto la función ``read_env()`` realiza una busqueda del archivo ``.env``, sin embargo, la ruta del archivo puede ser diferente. Sin embargo, cuando la aplicación sea deployada para producción, se recomienda cargarlas directamente desde el sistema. Para más información visita la sección de [environment][docs_services_env].

```sh

# .env.development

#App
#App
APP_HOSTNAME            =localhost
APP_PORT                =1801

#MYSQL database
MYSQL_DATABASE          =db_example
MYSQL_USERNAME          =root
MYSQL_PASSWORD          =root
MYSQL_PORT              =3306
MYSQL_HOST              =localhost
MYSQL_QUERY             =
MYSQL_DRIVERNAME        =mysql+pymysql
MYSQL_ECHO              =1
MYSQL_POOL_PREPING      =1
MYSQL_POOL_SIZE         =20
MYSQL_MAX_OVERFLOW      =0

#Apps
APP_BACKEND_STORAGE     =http://localhost:1802
APP_BACKEND_EPUB        =http://localhost:1803

```

## Aplicaciones externas

Retic recomienda realizar un archivo de rutas de aplicaciones externas, de esta forma se asegura la mantenibilidad y escalabilidad de la aplicación. De la misma forma, guardar la información en Retic para ser capaz de utilizarla en toda la aplicación.

```python
# apps/urls.py

# Retic
from retic import App as app

"""Define all other apps"""
BACKEND_STORAGE = {
    u"base_url": app.config.get('APP_BACKEND_STORAGE'),
    u"files": "/files",
    u"downloads": "/downloads",
}

BACKEND_EPUB = {
    u"base_url": app.config.get('APP_BACKEND_EPUB'),
    u"build_from_html": "/build/from-html",
    u"downloads": "/downloads",
}

APP_BACKEND = {
    u"storage": BACKEND_STORAGE,
    u"epub": BACKEND_EPUB,
}

"""Add Backend apps"""
app.use(APP_BACKEND, "backend")

```

A continuación se presenta una opción de cómo hacer uso de una aplicación externa dentro de un servicio.

```python

# services\epub\epub.py

# Retic
from retic import App as app

# Requests
import requests

# Constantes
URL_BUILD_FROM_HTML = app.apps['backend']['epub']['base_url'] + \
    app.apps['backend']['epub']['build_from_html']
URL_DOWNLOADS = app.apps['backend']['epub']['base_url'] + \
    app.apps['backend']['epub']['downloads']


def build_epub_from_html(filename, sections):
    """Crea un archivo .epub utilizando HTML como contenido

    :param filename: Nombre del archivo
    :param sections: Las secciones son como volumenes dentro del libro, que a su vez contienen capítulos
    """

    """Preparar el cuerpo de la petición"""
    _payload = {
        u"title": filename,
        u"sections": sections
    }
    """Crear el archivo utilizando una apliacción externa"""
    _book = requests.get(URL_BUILD_FROM_HTML, params=_payload)
    """Validar que la respuesta sea valida"""
    if _book.status_code != 200:
        """En caso de error, retornar un error al cliente"""
        raise Exception("No se puedo procesar la solicitud.")
    """Obtener el objeto JSON de la respuesta de la petición"""
    _book_json = _book.json()
    """Retornar la información"""
    return _book_json.get('data')

```

## Paquetes utilizados en la aplicación

Retic recomienda utilizar un archivo ``requirements.txt`` para llevar el control de los paquetes que se están utilizando dentro de la aplicación. Es similar al archivo ``package.json`` de **Node.js** en su sección de ``dependences``.
Facilita el control de la versión de cada paquete e instalar únicamente los que sean necesarios.

```sh

# requirements.txt

retic==0.0.14
requests==2.24.0
SQLAlchemy==1.3.18
mysql-connector-python==8.0.19
PyMySQL==0.9.
SQLAlchemy-serializer==1.3.4.2

```

Para instalar todas las dependencias de la aplicación en **node** se utiliza ``npm install`` o ``yarn install``, el equivalente en **python** es el siguiente comando:

```sh

pip install -r requirements.txt

```

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
