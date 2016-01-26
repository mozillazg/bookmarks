# -*- coding: utf-8 -*-

DEBUG = False
TESTING = False

# account
SECRET_KEY = 'your secret key'

# session
# SESSION_COOKIE_NAME = 'sid'
# SESSION_COOKIE_SECURE = True
# PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30

# Flask-SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'postgresql://scott:tiger@localhost/mydatabase'
# SQLALCHEMY_POOL_SIZE = 100
# SQLALCHEMY_POOL_TIMEOUT = 10
# SQLALCHEMY_POOL_RECYCLE = 3600

# Flask-Cache
CACHE_TYPE = 'simple'  # memcached, redis
