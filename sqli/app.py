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
