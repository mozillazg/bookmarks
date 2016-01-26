# -*- coding: utf-8 -*-
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_cache import Cache
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

admin = Admin(name='Bookmarks')
bcrypt = Bcrypt()
cache = Cache()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
