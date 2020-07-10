---
title: Instalación
type: guide
order: 2
---

Se recomienda utilizar un [entorno virutal](#crear-entorno-virtual-en-python) para trabajar.

```sh

# Instalar la última versión estable de Retic
pip install -U retic

```

Las notas de lanzamiento detalladas para cada versión están disponibles en [GitHub][repository_releases].

## Crear entorno virtual en Python

Un [virtualenv][virtualenv_official] permite aislar recursos como **librerías y entornos de ejecución** del sistema principal. Es decir, poder utilizar **diferentes versiones** de un mismo paquete para cada proyecto.

Para instalar un entorno virtual son requeridos los siguientes paquetes.

### Instalar Python

Retic es compatible con la versión 2.7 de [Python][python_downloads] y superiores, sin embargo, se recomienda utilizar la última versión de Python 3.

### Instalar pip

Instalación en Mac OS:

```sh

# Instalar el paquete
sudo easy_install pip

# Ver la versión instalada
pip --version

```

Instalación en Linux:

```sh

# Instalar el paquete
sudo apt-get install python-pip
sudo apt-get install python3-pip

# Ver la versión instalada
pip --version

```

Instalación en Windows:

* Descargar la ultima versión desde [get-pip.py][pip_download]
* Dentro de la carpeta donde se encuentre el archivo ``get-pip.py`` ejecutar

```sh

# Instalar el paquete
python get-pip.py

# Ver la versión instalada
pip --version

```

### Instalar virtualenv

```sh

# Opción con pip
pip install virtualenv

# Opción con pip3
sudo pip3 install virtualenv

```

### Crear un entorno virtual

Crear un directorio para el proyecto y un directorio para el entorno virtual

```sh

# Crear carpeta del proyecto
mkdir retic-example

# Ingresar a la carpeta
cd retic-example

# Crear entorno virtual

# Opción 1
python -m venv venv

# Opción 2
python3 -m venv venv

```

### Activar un entorno virtual

Cada vez que trabajes en tu proyecto, activa tu entorno virtual primero.

En Linux/MacOS:

```sh

# Ejecutar el script de activación
. venv/bin/activate

# Versión de pip instalada en el entorno virtual
pip --version

```

En Windows:

```sh

# Ejecutar el script de activación
venv\Scripts\activate

# Versión de pip instalada en el entorno virtual
pip --version

```

#### Actualizar paquete Pip

```sh

# Actualizar el paquete pip a la última versión

# Opción 1
python -m pip install --upgrade pip

# Opción 2
python3 -m pip install --upgrade pip

```

#### Instalar Retic

```sh

# Instalar la última versión estable de Retic
pip install -U retic

```

### Crear una aplicación inicial

Crear el archivo ``app.py`` con el siguiente codigo:

```python

# Retic
from retic import App as app

# Crear el servidor
app.listen()

```

Inicia tu servidor con el siguiente comando:

```sh

# Opción 1
python app.py

# Opción 2
python3 app.py

```

Listo, has creado tu primera API. Visita el siguiente enlace <http://localhost:1801/> para ver el resultado.

![alt text](https://github.com/reticpy/retic/raw/dev_documentation/docs/es/images/api_rest_app.png "API REST")

[repository_releases]: https://github.com/reticpy/retic/releases

[pip_download]: https://bootstrap.pypa.io/get-pip.py

[virtualenv_official]: https://docs.python.org/3/library/venv.html#module-venv

[python_downloads]: https://www.python.org/downloads/
