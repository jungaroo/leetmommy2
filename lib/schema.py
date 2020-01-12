from .config import CONFIG
from schematics.models import Model
from schematics.types import StringType
from schematics.exceptions import DataError

from functools import wraps
from flask import request
from flask_api import status
import json


class LeetMommyValidator(Model):
    """Validator to be used for most LeetMommy routes requiring a cohort"""
    cohort = StringType(required=True, choices=CONFIG.COHORTS)


class QueryValidator(LeetMommyValidator):
    """Validator to use for searching and autocomplete."""
    query = StringType(required=True)


def validator(model):
    """A decorator factory for Flask routes to validate the body/args
    :param model: A schematics :class:`Model` for validation
    :return: Decorator for validating flask route functions
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if request.method == 'POST':
                    validator = model(request.json)
                elif request.method == 'GET':
                    validator = model(request.args)
                else:  # not supported
                    raise Exception(f'{request.method} is not yet implemented')
                validator.validate()
                return func(*args, **kwargs)
            except DataError as e:
                error_message = json.loads(str(e))
                return {'errors': error_message}, status.HTTP_400_BAD_REQUEST
        return wrapper
    return decorator
