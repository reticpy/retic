# Retic.<span></span>py

Fastest, easiest and simplest web framework for Python.

* Building secure and **fast** REST services with Python
* A **easy** Python web framework for beginners.
* **Simple** integration with frontend frameworks to deploying a machine learning model in a modern web application.

## Install a Python rest api framework

Install and update using [Pip](https://pypi.org/):

```sh
# Get the latest stable release of Retic
$ pip install -U retic
```

## Simple rest api example in Python

```Python
# Retic
from retic import Router, App as app

router = Router()
router \
    .get("/", lambda req, res, next: res.ok({"msg": "Welcome to Retic ^^"})) \
    .get("/example", lambda req, res: res.ok({"msg": "Simple rest api example in Python"})) \
    .get("/withoutres", lambda req, res: print("REST api Python example"))

app.use(router)

app.listen(
    use_reloader=True,
    use_debugger=True,
    port=1801,
    hostname="localhost"
)
```

## Quickstart

Build a Python rest api in 5 minutes.

## Changelog

[Learn about the latest improvements][changelog].

## Want to help?

Do you want to send an error, contribute some code or improve the documentation? Great, you can do it! Read our guidelines to [contribute][contribute] and then review one of our issues in the [hotlist: community-help][hotlist].

## License

[MIT][LICENSE]

[LICENSE]: https://github.com/reticpy/retic/blob/dev_initial_app/LICENSE
[changelog]: https://github.com/reticpy/retic/blob/dev_initial_app/CHANGELOG.md
[contribute]: https://github.com/reticpy/retic/blob/dev_initial_app/CONTRIBUTING.md
[hotlist]: https://github.com/reticpy/retic/labels/hotlist%3A%20community-help