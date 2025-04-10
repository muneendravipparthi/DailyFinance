from flask import Blueprint, request, jsonify, current_app
from models import User, db
from werkzeug.security import generate_password_hash

signup = Blueprint('signup', __name__)

@signup.route('/api/v1/register', methods=['POST'])
def register_user():
    data = request.json
    try:
        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']
        phone = data['phone']
        password = data['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'message': 'Email already registered'}), 400

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(
            firstname=firstname,
            lastname=lastname,
            email=email,
            phone=phone,
            password=hashed_password  # Hash in production
        )
        from app import db  # Import `db` here temporarily to avoid circular imports
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
