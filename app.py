# Retic
from retic import Router, App as app, Response
from retic.lib.api.middlewares import cors

# Set environment file path
app.env.read_env('.env')

def files(req, res):
    _body = req.body
    print(_body)


router = Router()
router.use(cors())

router \
    .options("/*", cors()) \
    .get("/", lambda req, res, next: res.ok({"msg": "Welcome to Retic ^^"})) \
    .get("/example", lambda req, res: res.ok({"msg": "Simple rest api example in Python"})) \
    .get("/withoutres", lambda req, res: print("REST api Python example 🐍")) \
    .post("/files", files)


app.use(router)

settings = {
    u'port': 80
}
app.config.clear()
app.listen(
    use_reloader=True,
    use_debugger=True,
    hostname=app.env('APP_HOSTNAME', "localhost"),
    port=app.env.int('APP_PORT', 1801),
)
