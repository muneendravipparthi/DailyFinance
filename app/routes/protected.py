from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

protected = Blueprint('protected', __name__)

@protected.route('/dashboard', methods=['GET'])
@jwt_required()  # Validates the Bearer token automatically
def dashboard():
    # Retrieve the user ID (or identity) stored in the token
    current_user_id = get_jwt_identity()

    return jsonify({'user_id': current_user_id, 'message': 'Token is valid!'}), 200
