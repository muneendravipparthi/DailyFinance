from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import User
from werkzeug.security import check_password_hash

login = Blueprint('login', __name__)

@login.route('/api/v1/login', methods=['POST'])
def login_user():
    data = request.json
    try:
        # Extract email and password
        email = data.get('email')
        password = data.get('password')

        # Query the user from the database
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({'message': 'Invalid credentials'}), 401

        # Generate access token (no need to manually handle expiration)
        access_token = create_access_token(identity=user.email)

        # Return the Bearer Token
        return jsonify({'token': access_token}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
