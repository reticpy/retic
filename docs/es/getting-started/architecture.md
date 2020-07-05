# Introducción a los conceptos de Retic

Retic es un marco de trabajo para crear **aplicaciónes del lado del servidor**. Retic está escrito en Python. Utiliza Werkzeug como servidor y está basado en los conceptos de **express.js**.

Una aplicación basicamente está definida por **rutas y servicios**. Retic provee la clase ``Router`` que ayuda a definir los puntos de acceso de la aplicación.

## Controladores

Consta de Request, Response, Next...

Para más detalles visita la [guía de controladores][docs_controllers].

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

Para más detalles visita la [guía de utilerias][docs_utils].

[firefox_http_methods]: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
[wiki_crud]: https://en.wikipedia.org/wiki/Create,_read,_update_and_delete
[docs_routing]: https://github.com/reticpy/retic/blob/dev_documentation/docs/es/guide/routing.md
[docs_controllers]: https://github.com/reticpy/retic/blob/dev_documentation/docs/es/guide/controllers.md
[docs_utils]: https://github.com/reticpy/retic/blob/dev_documentation/docs/es/guide/utils.md