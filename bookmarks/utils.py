# -*- coding: utf-8 -*-
from collections import namedtuple


def copy_reqparse_for_update(reqparse, exclude=None):
    """复用 create 时的 reqparse"""
    exclude = exclude or []
    parser_update = reqparse.copy()
    for name in exclude:
        parser_update.remove_argument(name)
    for arg in parser_update.args:
        arg.required = False
        arg.ignore = True
        arg.default = None

    return parser_update


def parse_pagination_args(request_args, default=None):
    """解析请求参数中的分页相关参数
    :param request_args: request.args
    :param default: 默认值字典, (默认: {'per_page': 10, 'page': 1}
    :rtype: namedtuple('Args', 'per_page page offset')
    """
    default = default or {'per_page': 10, 'page': 1}
    per_page = request_args.get('perPage', default['per_page'], type=int)
    if per_page <= 0:
        per_page = default['per_page']
    page = request_args.get('page', default['page'], type=int)
    if page < 1:
        page = 1
    offset = (page - 1) * per_page
    cls = namedtuple('Args', 'per_page page offset')
    return cls(per_page, page, offset)
