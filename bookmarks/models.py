# -*- coding: utf-8 -*-
import collections
import datetime

from flask_login import UserMixin
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func

from bookmarks.extensions import db

utcnow = datetime.datetime.utcnow


class UUIDPrimaryKeyMixin:

    @declared_attr
    def id(cls):
        return db.Column(
            UUID(), primary_key=True, server_default=text('gen_random_uuid()')
        )


class TimestampMixin:

    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime(timezone=True),
                         server_default=func.now(), nullable=False)

    @declared_attr
    def updated_at(cls):
        return db.Column(db.DateTime(timezone=True), server_default=func.now(),
                         server_onupdate=func.now(), nullable=False)


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

    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(1200), nullable=False, unique=True)
    note = db.Column(db.String(200), default='', nullable=False)
    starred = db.Column(db.Boolean(), default=False, nullable=False)
    tags = db.relationship('Tag', secondary=tags_urls,
                           backref=db.backref('urls', lazy='dynamic'))
    categories = db.relationship('Category', secondary=categories_urls,
                                 backref=db.backref('urls', lazy='dynamic'))

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.url)

    @classmethod
    def new_url(cls, tags_str='', categories_str='', **kwargs):
        instance = cls(**kwargs)

        tags, categories = cls.new_tags_categories(tags_str, categories_str)
        for tag in tags:
            db.session.add(tag)
        instance.tags = tags
        instance.categories = categories
        db.session.add(instance)
        return instance

    def update_url(self, tags_str=None, categories_str=None, **kwargs):
        for field in ('title', 'url', 'note', 'starred'):
            value = kwargs.get(field)
            if value is not None:
                setattr(self, field, value)

        tags, categories = self.new_tags_categories(tags_str or '',
                                                    categories_str or '')

        for tag in tags:
            db.session.add(tag)
        if tags_str is not None:
            self.tags = tags
        if categories_str is not None:
            self.categories = categories
        db.session.add(self)
        return self

    @classmethod
    def new_tags_categories(cls, tags_str, categories_str):
        tags = []
        categories = []
        for tg in (x.strip() for x in tags_str.split(',') if x.strip()):
            tag = Tag.query.filter_by(name=tg).first()
            if tag is None:
                tag = Tag(name=tg)
            tags.append(tag)

        for cy in (x.strip() for x in categories_str.split(',') if x.strip()):
            category = Category.query.filter_by(name=cy).first()
            if category is not None:
                categories.append(category)

        return collections.namedtuple(
            'TagsCategories', 'tags, categories'
        )(tags, categories)
