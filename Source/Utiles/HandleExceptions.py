

from Source.Utiles.CustomResponse import *

def handle_exceptions(f):
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(e)
            response = InternalServerErrorResponse()
            return response.toResponse()
    decorated_function.__name__ = f.__name__
    return decorated_function