# -*- coding: utf-8 -*-


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
