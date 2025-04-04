from flask import jsonify
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity

def token_required(f):
    @wraps(f)
    @jwt_required()  # Automatically validates the token
    def wrapper(*args, **kwargs):
        try:
            # Get the current user's identity (e.g., email or ID)
            current_user_id = get_jwt_identity()

            # Pass the user's identity into the wrapped function
            return f(current_user_id, *args, **kwargs)
        except Exception as e:
            return jsonify({'message': f'Error: {str(e)}'}), 500

    return wrapper
