---
title: Routing
type: guide
order: 1
---

Se refiere a cómo una aplicación responde a solicitudes del cliente por medio de puntos de acceso o rutas.

Cada ruta puede utilizar uno o más controladores para interacturar con la logica de la aplicación.

La definición de una ruta toma la siguiente estructura:

```python
app.METHOD(PATH, [HANDLER, ...])
```

Dónde:

* ``app`` es una instancia de la clase [Router](#router).

* ``METHOD`` es un [método HTTP](#route-methods) el cual debe estar en minúsculas.

* ``PATH`` es una ruta en el servidor.

* ``HANDLER`` es el controlador que se ejecuta cuando la ruta coincide. Cada ruta puede tener una o más controladores.

## Router(*strict_slashes: bool*=True)

Manejador de rutas de una aplicación. Crea la relación entre una ruta de acceso, un método HTTP, y sus acciones para interactuar con la petición del cliente.

**parámetros:**

* strict_slashe: Si una regla termina con una barra diagonal pero la URL coincidente no lo hace, redirija a la URL final sin barra diagonal.

### Funciones de la clase Router

#### use(*fn*)

Agrega una función middleware que se ejecuaráe para todas las rutas en la aplicación.

**Parámetros:**

* fn: Función middleware que se ejecuta en cada ruta en la aplicación.
  
```python

# Retic
from retic import Router
from retic.lib.api.middlewares import cors

"""Definir la instancia Router"""
router = Router()

"""Agregar configuración CORS a todas las rutas"""
router.use(cors())

```

## Métodos de ruta

Un método de ruta es el tipo de método HTTP que el cliente utiliza para acceder a cierta funcionalidad de la aplicación en una determinada ruta. De esta forma, se utiliza una ruta para más de una acción.

Retic soporta los siguientes métodos HTTP: ``get``, ``post``, ``put``, ``head``, ``delete``, ``options``, ``trace``, ``copy``, ``lock``, ``mkcol``, ``move``, ``purge``, ``propfind``, ``proppatch``, ``unlock``, ``report``, ``mkactivity``, ``checkout``, ``merge``, ``m-search``, ``notify``, ``subscribe``, ``unsubscribe``, ``patch``, ``search``, ``connect``.

```python

# Retic
from retic import Router
from retic.lib.api.middlewares import cors

# Controllers
import controllers.files as files

"""Definir la instancia Router"""
router = Router()

"""Agregar configuración CORS a todas las rutas"""
router.use(cors())

"""Definir el método options para todas las rutas utilizando una expresión regular"""
router.options("/*", cors())

"""Definir las rutas para archivos"""
# Files routes
router \
    .post("/files", files.upload) \
    .get("/files/:id", files.get_by_id)

```

### Rutas de acceso

Una ruta de acceso es el punto de acceso por el cual el usuario realizará sus peticiones. Una ruta de acceso se relaciona directamente con un método HTTP y sus controladores.

Retic utiliza la biblioteca ``repath`` para definir sus rutas en la aplicación. Consulte la 
[documentación oficial][git_repath] para conocer todas las posibles combinaciones y cómo definar sus rutas de acceso de la mejor forma.

A continuación se utiliza una expresión regular que definir el método ``options`` en todas las rutas que comiencen con ``/``, seguido de cualquier cosa. El middleware ``cors`` se aplicará a cualquier ruta antes mencionada.

```python

"""Definir el método options para todas las rutas utilizando una expresión regular"""
router.options("/*", cors())

```

Esta ruta permite acceder por medio de ``/files`` utilizando el método HTTP ``post`` y ejecutar la función ``upload`` del controlador de archivos el cual permite subir un archivo a un gestor de archivos en la nube.

```python

router.post("/files", files.upload)

```

Retic permite declarar variables y capturar su valor automaticamente dentro del atributo ``params`` de la clase [Request][docs_api_req]. Los parámetros se declaran con el prefijo ":" seguido del nombre del párametro, por ejemplo: ``/files/:id``, el cual puede ser accedido desde el controlador de la siguiente forma: ``req.params('id')``.

La siguiente ruta permite acceder por medio de ``/files`` utilizando el método HTTP ``get`` y ejecutar la función ``get_by_id` del controlador de archivos en cual obtiene la información de un archivo en base a su identificador.

```python

router.get("/files/:id", files.get_by_id)

```

### Manejadores de rutas

Cada ruta permite tener uno o más funciones asociadas a ella. Estas funciones se utilizan como middlewares o acciones espeficicas para cada ruta. Para pasar de una función a la siguiente se utiliza la ``next()`` de la clase [Response][docs_api_res].

```python

router.get("/files",
           lambda req, res, next: next(),
           lambda req, res, next: next(),
           files.get_files
           )

```

La ruta siguiente verifica si el usuario está autorizado, si tiene permisos para realizar la acción y finalmente ejecuta el controlador con la acción asociada.

```python

# Download routes
router.get("/downloads/files/:file", oauth.verify, sso.verify, files.download_by_id)

```

[git_repath]: https://github.com/nickcoutsos/python-repath

[docs_api_req]: https://github.com/reticpy/retic/blob/dev_initial_app/docs/es/api/request.md

[docs_api_res]: https://github.com/reticpy/retic/blob/dev_initial_app/docs/es/api/response.md
