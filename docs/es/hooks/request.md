---
title: Request
type: hooks
order: 1
---

El objeto ``req`` es una instancia de la clase ``Request``. Representa la solicitud HTTP y tiene propiedades como parámetros, cuerpo de la solicitud, encabezados de la petición, etc.

## Propiedades de la clase Request

Algunas propiedades son una implementación de [ImmutableMultiDict][doc_werkzeug_multi_dict] e [ImmutableList][doc_werkzeug_immu_list] para representar su valor.

A continuación se presentan las principales propiedades de la clase ``Request`` y su funcionalidad. Se utiliza el siguiente [archivo de Postman][retic_postman_collection] para ejemplicar su uso.

### access_route

Lista todas las direcciones IP que intervienen en la petición.

```python

# Valor actual de access_route
req.access_route: ImmutableList(['172.18.5.107'])

```

### args

Lista todos los parametros en la URL de la petición.

```python

# URL de la petición HTTP
GET http://localhost:1801/files/123?queryparam=13344

# Valor actual de args
req.args: ImmutableMultiDict([('queryparam', '13344')])

```

Por defecto un ``ImmutableMultiDict`` es retornado en esta función, contiene funciones como ```getlist```, ``get``, ``get_all`` para interactuar de los párametros en la URL de una petición. Para más detalles visita la documentación oficial sobre la clase [ImmutableMultiDict][doc_werkzeug_immu_list].

### base_url

URL de la petición sin paramertros *querystring*.

```python

# Valor actual de base_url
req.base_url: 'http://172.18.5.107:1801/files/123'

```

### body

Instancia de la clase ``Body``. Contiene el cuerpo de la petición.

```python

# Valor actual de body
req.body:
    type: 'form'
    body: ImmutableMultiDict([('filename', 'fullname')])

```

### cookies

Lista todas las cookies de la petición.

```python

# Valor actual de cookies
req.cookies: ImmutableMultiDict([('cookie1', '123456')])

```

### data

Contiene la data entrante de la petición en formato binario.

```python

# Valor actual de data
req.data: b'{\r\n    "filename":"name of the file"\r\n}'

```

### environ

Entorno WSGI utilizado para extraer la información de la petición.

```python

# Valor actual de environ
req.environ: {'CONTENT_LENGTH': '39', 'CONTENT_TYPE': 'text/plain', 'HTTP_ACCEPT': '*/*', 'HTTP_ACCEPT_ENCODING': 'gzip, deflate, br', 'HTTP_CACHE_CONTROL': 'no-cache', 'HTTP_CONNECTION': 'keep-alive', 'HTTP_COOKIE': 'example1=123456', 'HTTP_HOST': 'localhost:1801', 'HTTP_USER_AGENT': 'PostmanRuntime/7.26.1', 'PATH_INFO': '/files/123', 'QUERY_STRING': 'queryparam=13344', 'RAW_URI': '/files/123?queryparam=13344', 'REMOTE_ADDR': 'localhost', ...}

```

### files

Lista todos los archivos de la petición HTTP. Cada valor es una instancia de la clase [FileStorage][doc_werkzeug_file_storage].

Cada elemento se comporta como un *file object* reconocido por **Python**, con la diferencia de que también tiene una función ``save()`` que puede almacenar el archivo en un sistema de archivos.

```python

# Valor actual de files
req.files: ImmutableMultiDict([('files', <FileStorage: '200px-Flag_of_Spain.svg.png' ('image/png')>)])

```

### form

Contiene todos los valores en un formulario de una petición tipo: ``application/x-www-form-urlencoded``.

```python

# Valor actual de form
req.form: ImmutableMultiDict([('size', '123456')])

```

### full_path

URL completa de la petición.

```python

# Valor actual de full_path
req.full_path: '/files/123?queryparam=13344'

```

### headers

Lista de todas las cabeceras de la petición.

```python

# Valor actual de headers
EnvironHeaders([('Cookie', 'cookie1=123456'), ('User-Agent', 'PostmanRuntime/7.26.1'), ('Accept', '*/*'), ('Cache-Control', 'no-cache'), ('Postman-Token', 'a0c82eb0-7864-472f-8991-5fce2c250554'), ('Host', 'localhost:1801'), ('Accept-Encoding', 'gzip, deflate, br'), ('Connection', 'keep-alive'), ('Content-Type', 'application/x-www-form-urlencoded'), ('Content-Length', '11')])

```

### host

Contiene el nombre del host y el puerto si este está disponible.

```python

# URL de la petición HTTP
GET http://localhost:1801/files/123?queryparam=13344

# Valor actual de host
req.host: 'localhost:1801'

```

### method

El método de la petición, por ejemplo: ``GET``, ``POST``, ``DELETE`` y ``PUT``.

```python

# Valor actual de method
req.method: 'GET'

```

### params

Objeto que contiene todos los parametros en la URL de petición: ``GET``, ``POST``, ``DELETE`` y ``PUT``.

```python

# URL de la petición HTTP
GET http://localhost:1801/files/123?queryparam=13344

# Valor actual de params
req.params: {'id': '123'}

```

### path

Contiene la ruta de acceso en la URL de la petición.

```python

# URL de la petición HTTP
GET http://localhost:1801/files/123?queryparam=13344

# Valor actual de params
req.path: '/files/123'

```

### retic

Diccionario utilizado para agregar valores personalizados a la petición y compartirlos entre controladores. Utiliza las funciones ``req.set()`` y ``req.get()`` para manipular sus valores.

```python

# Asignar el objeto JSON con nombre app1
req.set('app1', {u"msg": "say hi!"})

# Valor actual de retic
req.retic: {'app1': {'msg': 'say hi!'}}

```

## Funciones de la clase Request

La clase Request utiliza las siguientes funciones para manipulación de su información.

### param(*key: str*, *default_value: any* = None)

Devuelve el valor del parámetro con el nombre especificado.

``req.param(...)`` busca en los parámetros analizados desde la [ruta URL](#params), el [cuerpo de la solicitud](#body), la [cadena de consulta](#args), en ese orden. Si no existe el valor en la solicitud, devuelve ``None`` o el valor predeterminado por defecto especificado.

**Parámetros:**

* key: Nombre del parámetro a buscar.
  
* default_value: Valor por defecto si el parámetro no existe.

```python

# URL de la petición HTTP
GET http://localhost:1801/files/123?queryparam=13344

# Imprimir el valor actual del parámetro id, o utilizar un valor por defecto
print(req.param('id', 'default_value'))
print(req.param('id3')

# Salida: 123
# Salida: None

```

### set(*key: str*, *value: any* = None)

Asigna un objeto en el [diccionario retic](#retic) con un nombre específico. Tenga en cuenta que los nombres no distinguen entre mayúsculas y minúsculas y si ya existe se sobreescribirá su valor. Si el valor a asignar no existe, por defecto se guardará con valor ``None``.

**Parámetros:**

* key: Nombre del objeto a guardar.

* value: Valor con el que se guardará el objeto.
  
```python

# Asignar el objeto JSON con nombre app1
req.set('app1', {u"msg": "say hi!"})

```

### get(*key: str*, *default_value: any* = None)

Retorna el valor de un objeto en el [diccionario retic](#retic) con un nombre en especifico. Tenga en cuenta que los nombres no distinguen entre mayúsculas y minúsculas. Si no existe el valor en la solicitud, devuelve ``None`` o el valor predeterminado por defecto especificado.

**Parámetros:**

* key: Nombre del objeto a buscar.

* default_value: Valor por defecto si el objeto no existe.
  
```python

# Asignar el objeto JSON con nombre app1
req.set('app1', {u"msg": "say hi!"})

# Imprimir el valor actual de los parámetros, o utilizar un valor por defecto
print(req.get('app1'))
print(req.get('app2', 2233))

# Salida: {'msg': 'say hi!'}
# Salida: 2233

```

### all_params()

Devuelve el valor de todos los parámetros enviados en la solicitud,  y el diccionario retic combinado en un solo diccionario.

Incluye parámetros analizados desde la [ruta URL](#params), el [cuerpo de la solicitud](#body), la [cadena de consulta](#args), y el [diccionario retic](#retic), en ese orden.

#### Parámetros

*Ninguno.*

```python

# URL de la petición HTTP
GET http://localhost:1801/files/123?queryparam=13344

# Imprimir todos los parámetros de la petición
print(req.all_params())

# Salida: {'id': '123', 'size': '123456', 'queryparam': '13344', 'app1': {'msg': 'say hi!'}}

```

## Otras propiedades y funciones

Retic hereda de la clase ``Request de Werkzeug`` para la gestión de sus peticiones, visita la documentación acerca de su clase [Request][doc_werkzeug_req] para complementar la información aquí mencionada.

[doc_werkzeug_req]: https://werkzeug.palletsprojects.com/en/1.0.x/wrappers/#base-wrappers

[doc_werkzeug_multi_dict]: https://werkzeug.palletsprojects.com/en/1.0.x/datastructures/#werkzeug.datastructures.ImmutableMultiDict

[doc_werkzeug_immu_list]: https://werkzeug.palletsprojects.com/en/1.0.x/datastructures/#werkzeug.datastructures.ImmutableList

[doc_werkzeug_file_storage]: https://werkzeug.palletsprojects.com/en/1.0.x/datastructures/#werkzeug.datastructures.FileStorage

[retic_postman_collection]: https://github.com/reticpy/retic/blob/dev_initial_app/docs\es\guide\Retic.postman_collection.json
