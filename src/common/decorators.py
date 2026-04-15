import logging
from functools import wraps
from time import time

import jwt
from flask import request, jsonify

from model.user import User

__author__ = 'smok'

def requires_login(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        jwt_token = request.headers.get('token', None)
        if jwt_token:
            try:
                from src.app import JWT_SECRET
                from src.app import JWT_ALGORITHM
                payload = jwt.decode(jwt_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return jsonify({'message': 'Token is invalid'}, status=400)

            request.user = User.get_by_id(id=payload['user_id'])
            return request.path

        return func(*args, **kwargs)

    return decorated_func


def log_on_exception(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if len(args) > 0:
                logging.error(args)
            if len(kwargs) > 0:
                logging.error(kwargs)
            logging.error(e)

    return decorated_func


def timed(our_function):
    def our_wrapped_function(*args, **kwargs):
        start = time()
        result = our_function(*args, **kwargs)
        end = time()
        print(f"Time taken is {end-start} seconds.")
        return result
    return our_wrapped_function

