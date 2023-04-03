from argparse import ArgumentParser

from aiohttp.web import Application
from aiohttp_jinja2 import setup as setup_jinja
from jinja2.loaders import PackageLoader
from trafaret_config import commandline

from sqli.middlewares import session_middleware, error_middleware
from sqli.schema.config import CONFIG_SCHEMA
from sqli.services.db import setup_database
from sqli.services.redis import setup_redis
from sqli.utils.jinja2 import csrf_processor, auth_user_processor
from .routes import setup_routes
import flask
import sqlite3

password = "$ecurePa$$w0rd"

def init(argv):
    ap = ArgumentParser()
    commandline.standard_argparse_options(ap, default_config='./config/dev.yaml')
    options = ap.parse_args(argv)

    config = commandline.config_from_options(options, CONFIG_SCHEMA)

    app = Application(
        debug=True,
        middlewares=[
            session_middleware,
            # csrf_middleware,
            error_middleware,
        ]
    )
    app['config'] = config

    setup_jinja(app, loader=PackageLoader('sqli', 'templates'),
                context_processors=[csrf_processor, auth_user_processor],
                autoescape=False)
    setup_database(app)
    setup_redis(app)
    setup_routes(app)

    return app




def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)

    results = cursor.fetchall()
    conn.close()

    return results

@app.route(/users)
def get_users(num):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    username = request.args.get('username')
    password = request.args.get('password')
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return str(results)

-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQClY0n4BCnfMR/F
R11gT8TioIElsgU5Oe9kVluKSzlPEZmpJwdseeGOWIPPi5JyoyBM//+VnBaDkdrr
+HwiuZwWsWLPN8Fk8nzRgriHOE5XWDFdyS2vF55TrT5Sv8HEWmbXXukPRgohL78a
8z5oO0pYfzW7Mh2lEt0xmPZFsXa4lHnXhC0dZJKBB057UxUdn3ozVo6wB7QytZ0a
nESSIs8xWz7SP94FGHbtSmFpLM4/rl8NHOEfMVMC9OX+8AAkn580mGD1vz6Y0UUI
/hiibZ2/ZRJ8fh1eVVWBfj02AZLqp7/cXGL82s3QLMhKv74yKhZiv2fp/gPejFk7
Oes1sDXHAgMBAAECggEABrGBAdzxRjYlFK/cXenR4bYgjpeo0csVdC3Gi09GD3wl
MuJV0Om8hi1GOwppWo2y4KA6W3deCznGRBHiEZRfdnpRXGo46nlMhzzPc7GErNDw
loduJjhCJnLMIz8y0Vvd7k4fXTM2ymcLSJpFkU8CUEM9t8jByGIoujl4O2krkTFo
apOOEB75n2isU7IFm0jgSqdEzMdAeQNuGG5CqjggSJKsYj+s89x1ozGh8kOkmxQE
yTatEXRP6Z8UpjE+BX2b+EEMS99k/GY+6XWrIGrjaUwe2mojrUD4aY8O6r2SeJ8x
p2+7Ek111Gw+DbUbtVhv9Aa3xY+rM7iUNwnlgx/wIQKBgQDdx5ogK2g4b00I0dLo
3WcWQ2B1ntn48adU+p7IpicUcN0Xz2MY+vJ64GJbZ5+Su3hY9a3WRdRSlfBF8b4Z
9opAoOjBptRysIRL4fGrcGde7ZEKb4CAHyf/ZVFiNJUfRz5Hak7soSUKZo4h4zwz
9CMIH7CVVDw6vjdK0MnmE8sKlwKBgQC+6C73tdGWKdQqJp6kxfLfl1XNAXknGrcM
6HUgPzwflCmjZjTnce4+vwWTrGW8lsdk6jfnKB46ohJmuab8630t4VmJ68IDz8ty
eRDPUIXcGF1EQk1MOsVzNSkLmym8nrcDRnQLgjvpY06Oy1SwMdolSQJsYHfgByl3
2efwkmSEUQKBgQC0IQNIr5jFhXjO+gTQh8rLpUu6HJwzeqqK9cdzdqf1DTo1tYZq
ap/5NzgLv103AzbbIifgCfVKYme1l4PseHaPyWFir8qLoFzDeS8dLH1494E/NZLr
/OIyqCrylXys2+N0g564yKVaDjPQyExEcjzlwz9b+f+1QnuMM4pYaakW3wKBgGsv
eY9i6jXhblnsLQ5ehaq8EVR1C0zFVxlMOtbMKjmgunAfpnx8H0PjhIIRPV3RWkpy
psiGYdKRxLsgaX1/ylzENb2WPOxe8t9m0eVUVJPqqhL1FulB5jJ1GoKFr71Tb3XL
TMRZbsHvG+BYkUgL9WsRvuaSkzuZSdMc6XjM+NrBAoGBAMZ93P9XuwH5vWysIq8j
UQveP6TqiZQOzRo3ndoOMK9tY9hRo0gbZ3//7CeyqUXZtlgTxFlDPHEGe6Xakx47
7bjmECShLXakrEsvGvXQp2HyLkfOonXgHrR1M8n5pOJBteNn3px3SgP4IK2de8jF
AdkveyGbQEr14F4gjV06ZbRT
-----END PRIVATE KEY-----
