---
title: Environment
type: services
order: 2
---

Retic proporciona fácil acceso a las variables del sistema. Se utiliza la clase ``Env`` de la biblioteca ``environs`` para definir sus rutas en la aplicación. Consulte la [documentación oficial][git_environs] para conocer todas las posibles combinaciones y cómo acceder a las variables de entorno de la mejor forma.

## Funciones de la clase Env

## env.read_env(*path: str* = None, *recurse: bool* = True, *verbose: bool* = False, *override: bool*)

Por defecto se buscan variables en el archivo ``.env`` de existir. Sin embargo, en algunas ocaciones es necesario tener más de un archivo de entorno. Esta función permite leer tantos archivos de entorno como se le indique.

**Parámetros:**

* path: Directorio donde se encuentra el archivo de enterno.

* recurse: Realiza una busqueda de forma recursiva desde la raiz.

* verbose: Define si se deben mostar las advertencias cuando un archivo no existe. El valor predeterminado es `False`.

* override: Sobreescribe las variables actuales en el sistema operativo. El valor predeterminado es ``False``.

```sh

# .env.development

#App
APP_HOSTNAME            =localhost
APP_PORT                =1801

```

```python

# Retic
from retic import App as app

# Routes
from routes.routes import router

# Configurar la ruta del archivo de entorno
app.env.read_env('.env.development', override=True)

```

## Uso básico

La busqueda de una variable de entorno se realiza por su nombre, de no existir, se puede asignar un valor por defecto, caso contrario devolverá una excepción que indica que la variable no existe en el sistema.

### Tipos soportados

Por defecto Retic retorna el valor en formato ``str``, sin embargo, Retic permite realizar el casteo automatico de las variables de entorno a un tipo especifico. A continuación se presenta los posibles formatos de salida al consultar una variable de entorno:

* env.str
* env.bool
* env.int
* env.float
* env.decimal
* env.list (accepts optional subcast keyword argument)
* env.dict (accepts optional subcast keyword argument)
* env.json
* env.datetime
* env.date
* env.timedelta (assumes value is an integer in seconds)
* env.url
* env.uuid
* env.log_level
* env.path (casts to a pathlib.Path)

```sh

# .env

#App
APP_HOSTNAME            =localhost
APP_PORT                =1801

```

```python

# Retic
from retic import App as app

# Routes
from routes.routes import router

# Configurar la ruta del archivo de entorno
app.env.read_env('.env.development')

# Agregar rutas a la aplicación
app.use(router)

# Crear el servidor web
app.listen(
    use_reloader=True,
    use_debugger=True,
    # Obtener la variable de entorno APP_HOSTNA en el formato por defecto (str)
    hostname=app.env('APP_HOSTNAME', "localhost"),
    # Obtener la variable de entorno APP_PORT en formato númerico. De no existir, retorna 1801.
    port=app.env.int('APP_PORT', 1801),
)

```

[git_environs]: https://github.com/sloria/environs
