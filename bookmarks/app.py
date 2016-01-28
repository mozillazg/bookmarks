# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask_admin.contrib.sqla import ModelView
from flask_envconfig import EnvConfig
from flask_migrate import Migrate
from .extensions import admin, cache, db


def create_app(config=None):
    app = Flask(__name__, template_folder='templates')
    app.config.from_pyfile('config.py')
    env = EnvConfig()
    env.init_app(app, 'BOOKMARKS_')
    if isinstance(config, dict):
        app.config.update(config)
    elif config:
        app.config.from_pyfile(os.path.realpath(config))
    app.static_folder = app.config.get('STATIC_FOLDER')

    register_exts(app)
    register_bps(app)

    return app


def register_exts(app):
    db.init_app(app)
    db.app = app
    cache.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)
    register_login(app)
    if not app.config.get('TESTING'):
        register_admins(app)


def register_admins(app):
    from .models import Category, Tag, User, URL

    class MyModelAdmin(ModelView):
        column_display_pk = True
        form_excluded_columns = ('created_at', 'updated_at')

        def __init__(self, Model, **kwargs):
            super(MyModelAdmin, self).__init__(Model, db.session, **kwargs)

    admin.add_view(MyModelAdmin(Category))
    admin.add_view(MyModelAdmin(Tag))
    admin.add_view(MyModelAdmin(User))
    admin.add_view(MyModelAdmin(URL))
    admin.init_app(app)


def register_login(app):
    pass


def register_bps(app):
    from .views import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')


def create_db():
    db.create_all()


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
