from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, db
from werkzeug.security import generate_password_hash, check_password_hash

change_password_service = Blueprint('change_password_service', __name__)

@change_password_service.route('/changePassword', methods=['POST'])
@jwt_required()  # Requires authentication
def change_password():
    data = request.json

    # Retrieve the current user's email or ID from the JWT token
    current_user_email = get_jwt_identity()

    try:
        # Validate the request body
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not old_password or not new_password:
            return jsonify({'message': 'Both old and new passwords are required'}), 400

        # Fetch the user from the database
        user = User.query.filter_by(email=current_user_email).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Verify the old password
        if not check_password_hash(user.password, old_password):
            return jsonify({'message': 'Old password is incorrect'}), 401

        # Ensure the new password is different from the old one
        if check_password_hash(user.password, new_password):
            return jsonify({'message': 'New password cannot be the same as the old password'}), 400

        # Update the password
        hashed_new_password = generate_password_hash(new_password, method='sha256')
        user.password = hashed_new_password
        db.session.commit()

        return jsonify({'message': 'Password changed successfully'}), 200

    except Exception as e:
        db.session.rollback()  # Rollback in case of errors
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
