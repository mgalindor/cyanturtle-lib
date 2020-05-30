from dataclasses import dataclass
from functools import wraps
from typing import List

from flask import request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims, get_jwt_identity
from marshmallow import ValidationError
from werkzeug.exceptions import Forbidden, BadRequest

from cyanturtle.persistence import Entity


@dataclass
class Principal(Entity):
    user_name: str
    name: str
    year: str
    authorities: List[str]


def get_principal() -> Principal:
    return Principal(user_name=get_jwt_identity(), name=get_jwt_claims().get('name', None),
                     year=get_jwt_claims().get('year', None),
                     authorities=get_jwt_claims().get('authorities', None))


def get_current_user():
    return {'user_name': get_jwt_identity(),
            'authorities': get_jwt_claims().get('authorities', None),
            'name': get_jwt_claims().get('name', None)
            }


def require_authority(authority):
    def decorator_require_authority(func):
        @wraps(func)
        def wrapper_require_authority(*args, **kwargs):
            verify_jwt_in_request()
            authorities = get_jwt_claims().get('authorities', [])
            to_check = [authority] if type(authority) is not list else authority
            if set(to_check).intersection(authorities):
                return func(*args, **kwargs)
            else:
                raise Forbidden()

        return wrapper_require_authority

    return decorator_require_authority


def validate_schema(model):
    def decorator_validate_schema(func):
        @wraps(func)
        def wrapper_validate_schema(*args, **kwargs):
            try:
                req_data = model.load(request.json)
                kwargs['req_data'] = req_data
                return func(*args, **kwargs)
            except ValidationError as err:
                e = BadRequest()
                e.data = {
                    'message': 'Input payload validation failed',
                    'errors': err.messages
                }
                raise e

        return wrapper_validate_schema

    return decorator_validate_schema
