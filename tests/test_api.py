# -*- coding: utf-8 -*-
import json
import os
import uuid

from flask import Response
import pytest

from bookmarks.app import create_app
from bookmarks.extensions import db
from bookmarks.models import Category, Tag, URL


class ResponseForTest(Response):
    def json(self):
        return json.loads(self.data.decode('utf8'))


def init_db():
    db.session.add(Category(name='test1'))
    db.session.add(Category(name='test2'))
    db.session.commit()


@pytest.yield_fixture
def context():
    from flask import url_for
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': os.environ[
            'BOOKMARKS_TEST_SQLALCHEMY_DATABASE_URI'
        ],
    })
    app.response_class = ResponseForTest
    db.create_all()
    context = type('TestContext', (object,), {})
    context.app = app
    context.client = app.test_client()

    def _url_for(*args, **kwargs):
        with app.test_request_context():
            return url_for(*args, **kwargs)
    context.url_for = _url_for
    yield context
    db.session.remove()
    db.drop_all()


class TestTag:

    def test_list_get(self, context):
        client = context.client
        url_for = context.url_for

        for name in ('abc', 'efg', 'hij'):
            db.session.add(Tag(name=name))
        db.session.commit()

        rv = client.get(url_for('api.taglistview'))
        dic = rv.json()
        assert rv.status_code == 200
        assert len(dic) == 3


class TestCategory:

    def test_list_get(self, context):
        client = context.client
        url_for = context.url_for
        for name in ('abc', 'efg', 'hij'):
            db.session.add(Category(name=name))
        db.session.commit()

        rv = client.get(url_for('api.categorylistview'))
        dic = rv.json()
        assert rv.status_code == 200
        assert len(dic) == 3


class TestURL:

    def test_list_get(self, context):
        client = context.client
        url_for = context.url_for
        for name in ('abc', 'efg', 'hij'):
            url = 'http://a.com/b/c' + name
            db.session.add(URL(title=name, url=url))
        db.session.commit()

        rv = client.get(url_for('api.urllistview'))
        dic = rv.json()
        assert rv.status_code == 200
        assert len(dic) == 3

    def test_list_post(self, context):
        init_db()
        client = context.client
        url_for = context.url_for
        data = {
            'title': 'test',
            'url': 'http://a.com/b',
            'starred': True,
            'tags': 'abc, test',
            'categories': 'test1, abc',
        }
        category_ids = set([x.id for x in Category.query.all()])
        rv = client.post(url_for('api.urllistview'), data=data)
        url_obj = URL.query.first()
        dic = rv.json()
        assert rv.status_code == 201
        assert dic['id'] == url_obj.id
        assert dic['title'] == url_obj.title
        assert dic['starred'] == url_obj.starred
        assert rv.headers['location'] == url_for(
            'api.urldetailview', id=url_obj.id, _external=True
        )
        assert set(x['id'] for x in dic['tags']) == set(
            x.id for x in Tag.query.all()
        )
        assert set([x['id'] for x in dic['categories']]) & category_ids

    def test_detail_get(self, context):
        client = context.client
        url_for = context.url_for
        urls = []
        for x in ['a', 'b', 'c']:
            obj = URL(title=x, url='http://a.com/' + x)
            db.session.add(obj)
            urls.append(obj)
        db.session.commit()

        rv = client.get(url_for('api.urldetailview', id=urls[0].id))
        dic = rv.json()
        assert rv.status_code == 200
        assert dic['id'] == urls[0].id

    def test_detail_404(self, context):
        client = context.client
        url_for = context.url_for

        rv = client.get(url_for('api.urldetailview', id=123))
        assert rv.status_code == 404
        rv = client.get(url_for('api.urldetailview', id=str(uuid.uuid4())))
        assert rv.status_code == 404

    def test_detail_patch(self, context):
        client = context.client
        url_for = context.url_for
        urls = []
        for x in ['a', 'b', 'c']:
            obj = URL(title=x, url='http://a.com/' + x)
            db.session.add(obj)
            urls.append(obj)
        db.session.commit()

        data = {
            'url': 'http://a.com',
            'title': 'patch',
            'starred': False,
            'tags': 'test, abc',
            'categories': 'test1, test2',
        }
        url_obj = urls[0]
        rv = client.patch(url_for('api.urldetailview', id=url_obj.id),
                          data=data)
        dic = rv.json()
        assert rv.status_code == 200
        assert dic['id'] == url_obj.id
        assert dic['starred'] == url_obj.starred
        assert dic['url'] == data['url'] == URL.query.get(url_obj.id).url
        assert dic['url'] != url_obj.url
        assert len(dic['tags']) == 2
        assert len(dic['categories']) == 0

    def test_detail_patch_categories(self, context):
        client = context.client
        url_for = context.url_for
        urls = []
        for x in ['a']:
            obj = URL(title=x, url='http://a.com/' + x)
            db.session.add(obj)
            urls.append(obj)
        init_db()
        db.session.commit()

        data = {
            'url': 'http://a.com',
            'starred': True,
            'tags': 'test, abc',
            'categories': 'test1, abc',
        }
        url_obj = urls[0]
        data['url'] = 'http://a.com/2'
        rv = client.patch(url_for('api.urldetailview', id=url_obj.id),
                          data=data)
        dic = rv.json()
        assert len(dic['categories']) == 1
        assert dic['starred'] == data['starred']

    def test_detail_delete(self, context):
        client = context.client
        url_for = context.url_for
        urls = []
        for x in ['a', 'b', 'c']:
            obj = URL(title=x, url='http://a.com/' + x)
            db.session.add(obj)
            urls.append(obj)
        db.session.commit()

        url_obj = urls[0]
        rv = client.delete(url_for('api.urldetailview', id=url_obj.id))
        assert rv.status_code == 204
        assert URL.query.get(url_obj.id) is None
