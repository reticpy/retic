---
title: Middlewares
type: services
order: 3
---

Retic proporciona servicios que funcionan como middlewares de la aplicación los cuales se aplican a una o varias rutas **especificadas**.

## cors(*methods: str*,*has_credentials: bool*,*origin: str*, *headers: str*, *expose_headers: str*)

CORS es una abreviatura que significa 'Intercambio de recursos de origen cruzado' y, como su nombre lo indica, le permite compartir recursos de una variedad de fuentes.

**Parámetros:**

* methods: El encabezado de respuesta Access-Control-Allow-Methods indica qué métodos HTTP están permitidos en un punto final particular para solicitudes de origen cruzado.

* has_credentials: El encabezado de respuesta Access-Control-Allow-Credentials le dice el navegador que el servidor permite credenciales para una solicitud de origen cruzado.

* origin: El encabezado de respuesta Access-Control-Allow-Origin indica si los recursos en la respuesta se pueden compartir con el origen dado.

* headers: El encabezado de respuesta Access-Control-Allow-Headers se usa en respuesta a una solicitud de verificación previa que incluye los encabezados de solicitud de control de acceso para indicar qué encabezados HTTP se pueden usar durante la solicitud real.

* expose_headers: El encabezado de respuesta Access-Control-Expose-Headers indica qué encabezados se pueden exponer como parte de la respuesta al enumerar.

Por seguridad, Retic protege las rutas con el método ``options`` de accesos no autorizados. Es por ello que se debe definir las rutas de acceso con el método ``option`` especificas. Se pueden utilizar expresiones regulares como se muestra en el ejemplo siguiente.

```python

# Retic
from retic import Router
from retic.lib.api.middlewares import cors

# Controllers
import controllers.files as files

"""Definir la instancia de Router"""
router = Router()

"""Define CORS"""
_cors = cors(
    headers="Content-Type,source",
    expose_headers="Content-Type,source"
)

"""Agergar las cabeceras que proporciona la función cors a todas las rutas"""
router.use(_cors)

"""Define el metodo options para todas las rutas que comiencen con /"""
router.options("/*", _cors)

```
