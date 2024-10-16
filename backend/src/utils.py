# Helper functions go in here
from flask import request, g, jsonify
from functools import wraps
from flask_jwt_extended import decode_token


# Custom decorator to run middleware before specific routes
def with_user_middleware(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')  # Extract token from headers (e.g., Bearer token)
        
        if token:
            decoded_token = decode_token(token)  # Extract or decode the token to get user_id
            g.user_id = decoded_token['id']  # Store the user_id in g (global context for the request)
        else:
            g.user_id = None
        
        return f(*args, **kwargs)
    
    return decorated_function