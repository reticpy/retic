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
│   app.py
│   requirements.txt
```

## Controladores

Los controladores están vinculados a las rutas de su aplicación, gestionan las solicitudes HTTP entrantes y deciden que servicios deben realizar el trabajo para dar una respuesta correcta al cliente.

Por ejemplo, la ruta GET ``/files/:id`` en su aplicación podría estar vinculada a un controlador como:

```python

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

## Utilerias

Retic cuenta con una biblioteca de servicios más utilizados para dar ayudarte en que te enfoques en lo que verdaderamente importa, la lógica de tu aplicación.

Para más detalles visita la [guía de utilerias][docs_utils].

[firefox_http_methods]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods

[wiki_crud]: https://en.wikipedia.org/wiki/Create,_read,_update_and_delete

[docs_routing]: https://github.com/reticpy/retic/blob/dev_documentation/docs/es/guide/routing.md

[docs_hooks_req]: https://github.com/reticpy/retic/blob/dev_documentation/docs/es/hooks/request.md

[docs_hooks_res]: https://github.com/reticpy/retic/blob/dev_documentation/docs/es/hooks/response.md

[docs_hooks_next]: https://github.com/reticpy/retic/blob/dev_documentation/docs/es/hooks/next.md

[docs_utils]: https://github.com/reticpy/retic/blob/dev_documentation/docs/es/guide/utils.md
