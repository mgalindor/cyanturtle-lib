from flask import escape
from marshmallow import Schema, ValidationError, pre_load, post_dump


def validate_not_blank(data):
    if not (data and str(data).strip()):
        raise ValidationError("Can not be empty")
    return data


def sanitize(data):
    for k, v in data.items():
        if isinstance(v, str):
            data[k] = escape(v)
    return data


class BaseSchema(Schema):
    class Meta:
        ordered = True

    @pre_load
    def sanitize(self, data, many, **kwargs):
        return sanitize(data)

    @post_dump
    def remove_skip_values(self, data, many, **kwargs):
        return {key: value for key, value in data.items() if value}
