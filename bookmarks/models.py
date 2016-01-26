# -*- coding: utf-8 -*-
import datetime
import uuid

from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr

from bookmarks.extensions import db

utcnow = datetime.datetime.utcnow


def gen_uuid():
    return str(uuid.uuid4())


class UUIDPrimaryKeyMixin:

    @declared_attr
    def id(cls):
        return db.Column(UUID(), primary_key=True, default=gen_uuid)


class TimestampMixin:

    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime(timezone=True), default=utcnow,
                         nullable=False)

    @declared_attr
    def updated_at(cls):
        return db.Column(db.DateTime(timezone=True), default=utcnow,
                         onupdate=utcnow, nullable=False)


class TagMixin:

    @declared_attr
    def name(cls):
        return db.Column(db.String(100), nullable=False, unique=True)

    @declared_attr
    def note(cls):
        return db.Column(db.String(200), default='', nullable=False)

    @declared_attr
    def url_number(cls):
        return db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)


class User(UserMixin, TimestampMixin, UUIDPrimaryKeyMixin, db.Model):
    __tablename__ = 'users'

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), default='', nullable=False)

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.username)


tags_urls = db.Table(
    'tags_urls',
    db.Column('tag_id', UUID, db.ForeignKey('tags.id')),
    db.Column('url_id', UUID, db.ForeignKey('urls.id'))
)
categories_urls = db.Table(
    'categories_urls',
    db.Column('category_id', UUID, db.ForeignKey('categories.id')),
    db.Column('url_id', UUID, db.ForeignKey('urls.id'))
)


class Tag(TagMixin, TimestampMixin, UUIDPrimaryKeyMixin, db.Model):
    __tablename__ = 'tags'


class Category(TagMixin, TimestampMixin, UUIDPrimaryKeyMixin, db.Model):
    __tablename__ = 'categories'


class URL(TimestampMixin, UUIDPrimaryKeyMixin, db.Model):
    __tablename__ = 'urls'

    url = db.Column(db.String(1200), nullable=False)
    note = db.Column(db.String(200), default='', nullable=False)
    starred = db.Column(db.Boolean(), default=False, nullable=False)
    tags = db.relationship('Tag', secondary=tags_urls,
                           backref=db.backref('urls', lazy='dynamic'))
    categories = db.relationship('Category', secondary=categories_urls,
                                 backref=db.backref('urls', lazy='dynamic'))

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.url)
