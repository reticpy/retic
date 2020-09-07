# Retic

Retic is a framework for Python.

Designed to attack the following points in software development:

- **Learning curve**: Python has a short learning curve.

- **Hosting**: Quick and easy configuration on the servers.

- **Artificial intelligence**: The most important libraries are written in Python.

## Install a Python rest api framework

Install and update using [Pip](https://pypi.org/):

```bash
# Get the latest stable release of Retic
pip install -U retic
```

## Simple rest api example in Python

```Python

# app.py

"""Main app"""

# Retic
from retic import Router, App as app

"""Define Router instance"""
router = Router()

"""Define paths"""
router \
    .get("/", lambda req, res, next: res.ok({"msg": "Hello world! - HTTP GET"})) \
    .post("/", lambda req, res, next: res.ok({"msg": "Hello world! - HTTP POST"})) \
    .put("/", lambda req, res, next: res.send({"msg": "Hello world! - HTTP PUT"})) \
    .delete("/", lambda req, res: res.send({"msg": "Hello world! - HTTP DELETE"}))

"""Import router to App"""
app.use(router)

"""Create web server"""
app.listen(
    hostname="localhost",
    port=1801
)


```

## Want to help?

Do you want to send an error, contribute some code or improve the documentation? Great, you can do it! Read our guidelines to contribute and then review one of our issues in the [hotlist: community-help][hotlist].

## License

[MIT][LICENSE]

[LICENSE]: https://github.com/reticpy/retic/blob/development/LICENSE
[hotlist]: https://github.com/reticpy/retic/labels/hotlist%3A%20community-hel