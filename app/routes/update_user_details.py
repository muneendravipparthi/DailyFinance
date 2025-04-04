from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, db
from utils import token_required

update_user_details = Blueprint('update_user_details', __name__)

@update_user_details.route('/updateUser', methods=['PUT'])
@jwt_required()  # Custom decorator for token validation
def update_user():
    # Retrieve the user ID (or identity) stored in the token
    current_user_id = get_jwt_identity()
    data = request.json

    # Validate request payload
    if not data:
        return jsonify({'message': 'Invalid request: No data provided'}), 400

    try:
        # Query the user by ID
        user = User.query.filter_by(email=current_user_id).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        # Validate and update fields
        if 'firstname' in data:
            if not isinstance(data['firstname'], str):
                return jsonify({'message': 'Invalid value for firstname'}), 400
            user.firstname = data['firstname']

        if 'lastname' in data:
            if not isinstance(data['lastname'], str):
                return jsonify({'message': 'Invalid value for lastname'}), 400
            user.lastname = data['lastname']

        if 'phone' in data:
            if not isinstance(data['phone'], str):
                return jsonify({'message': 'Invalid value for phone'}), 400
            user.phone = data['phone']

        if 'defaultInterestRate' in data:
            if not isinstance(data['defaultInterestRate'], (float, int)):
                return jsonify({'message': 'Invalid value for defaultInterestRate'}), 400
            user.default_interest_rate = float(data['defaultInterestRate'])

        if 'defaultFinancePeriod' in data:
            if not isinstance(data['defaultFinancePeriod'], int):
                return jsonify({'message': 'Invalid value for defaultFinancePeriod'}), 400
            user.default_finance_period = data['defaultFinancePeriod']

        # Commit changes to the database
        db.session.commit()

        return jsonify({'message': 'User details updated successfully'}), 200

    except Exception as e:
        db.session.rollback()  # Rollback transaction in case of error
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
