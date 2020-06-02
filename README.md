# Retic.<span></span>py

Fastest, easiest and simplest web framework for Python.

* Building secure and **fast** REST API Services with Python
* A **easy** python web framework for beginners.
* **Simple** integration with frontend frameworks to deploying a machine learning model in a modern web application.

## Installation

Install and update using [Pip](https://pypi.org/):

```sh
# Get the latest stable release of Retic
$ pip install -U retic
```

### Simple rest api example in python
```python
from retic import Router, App as app

router = Router()
router.get("/", lambda req, res, next: res.ok({"msg": "Welcome to Retic ^^"}))

app.use(router)

app.listen(
    use_reloader=True,
    use_debugger=True,
    port=1801,
    hostname="localhost"
)
```

## Documentation
In progress...

## License

[MIT](LICENSE)