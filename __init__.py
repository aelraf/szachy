# -*- coding: utf-8 -*-

import os

from flask import Flask


def create_app(test_config=None):
    # tworzy i konfiguruje aplikację
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE =
    # )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError as err:
        print("błąd w create_app: {}".format(err))

    @app.route('/hello')
    def hello():
        return 'Hello, world!'

    return app
