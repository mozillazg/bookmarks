# -*- coding: utf-8 -*-
from flask_restful import fields, reqparse, inputs

from .utils import copy_reqparse_for_update


tag_fields = {
    'id': fields.String,
    'name': fields.String,
    'url_number': fields.Integer,
}

category_fields = {
    'id': fields.String,
    'name': fields.String,
    'url_number': fields.Integer,
}

url_fields = {
    'id': fields.String,
    'title': fields.String,
    'url': fields.String,
    'note': fields.String,
    'starred': fields.Boolean,
    'tags': fields.Nested(tag_fields, default={}),
    'categories': fields.Nested(category_fields, default={}),
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
}

url_parser_create = reqparse.RequestParser()
url_parser_create.add_argument('title', required=True)
url_parser_create.add_argument('url', required=True)
url_parser_create.add_argument('starred', required=True, type=inputs.boolean,
                               default=False)
url_parser_create.add_argument('tags', default='')
url_parser_create.add_argument('categories', default='')
url_parser_update = copy_reqparse_for_update(url_parser_create)
