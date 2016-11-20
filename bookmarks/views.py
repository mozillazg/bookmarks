# -*- coding: utf-8 -*-
import uuid

from flask import Blueprint
from flask_restful import abort, Api, marshal_with, Resource

from .extensions import db
from .models import Tag, Category, URL
from .serializers import (
    tag_fields, category_fields, url_fields,
    url_parser_create, url_parser_update
)

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


def get_instance_or_404_by_id(cls, id):
    try:
        id = str(id)
        uuid.UUID(id)
    except ValueError:
        abort(404)
    instance = db.session.query(cls).get(id)
    if instance is None:
        abort(404)
    return instance


class TagListView(Resource):
    @marshal_with(tag_fields)
    def get(self):
        return Tag.query.order_by(Tag.url_number.desc()).all()


class CategoryListView(Resource):
    @marshal_with(category_fields)
    def get(self):
        return Category.query.order_by(Category.url_number.desc()).all()


class URLListView(Resource):
    @marshal_with(url_fields)
    def get(self):
        return URL.query.order_by(URL.updated_at.desc()).all()

    @marshal_with(url_fields)
    def post(self):
        args = url_parser_create.parse_args()
        instance = URL.new_url(title=args['title'], url=args['url'],
                               starred=args['starred'],
                               tags_str=args['tags'],
                               categories_str=args['categories'])
        db.session.add(instance)
        db.session.commit()
        return instance, 201, {
            'Location': api.url_for(
                URLDetailView, id=instance.id, _external=True
            )
        }


class URLDetailView(Resource):
    @marshal_with(url_fields)
    def get(self, id):
        return get_instance_or_404_by_id(URL, id)

    @marshal_with(url_fields)
    def patch(self, id):
        args = url_parser_update.parse_args()
        instance = get_instance_or_404_by_id(URL, id)
        instance.update_url(url=args.get('url'),
                            title=args.get('title'),
                            starred=args.get('starred'),
                            tags_str=args.get('tags'),
                            categories_str=args.get('categories'))
        db.session.add(instance)
        db.session.commit()
        return instance

    def delete(self, id):
        obj = get_instance_or_404_by_id(URL, id)
        db.session.delete(obj)
        db.session.commit()
        return '', 204, {}


api.add_resource(CategoryListView, '/categories')
api.add_resource(TagListView, '/tags')
api.add_resource(URLDetailView, '/urls/<id>')
api.add_resource(URLListView, '/urls')
