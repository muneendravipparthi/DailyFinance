from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Customer, db

customers = Blueprint('customers', __name__)
# Get All Customer
@customers.route('/customers', methods=['GET'])
@jwt_required()  # Requires authentication
def get_all_customers():
    user_id = get_jwt_identity()  # Retrieve the logged-in user's ID

    try:
        # Query all customers belonging to the logged-in user
        customers = Customer.query.filter_by(user_id=user_id).all()

        if not customers:
            return jsonify({'message': 'No customers found'}), 404

        # Create a list of customer details
        customer_list = [
            {
                'id': customer.id,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'mobile': customer.mobile,
                'contact_1': customer.contact_1,
                'contact_2': customer.contact_2,
                'aadhar_number': customer.aadhar_number,
                'home_address': customer.home_address,
                'business_address': customer.business_address,
                'occupation': customer.occupation,
                'rating': customer.rating,
            }
            for customer in customers
        ]

        return jsonify(customer_list), 200

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

# Create Customer
@customers.route('/createCustomer', methods=['POST'])
@jwt_required()
def create_customer():
    data = request.json
    user_id = get_jwt_identity()  # Get logged-in user's ID

    # Validate mandatory fields
    mandatory_fields = ['first_name', 'last_name', 'mobile', 'contact_1', 'aadhar_number', 'home_address']
    for field in mandatory_fields:
        if not data.get(field):
            return jsonify({'message': f'{field} is required'}), 400

    try:
        # Create a new Customer
        customer = Customer(
            user_id=user_id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            mobile=data['mobile'],
            contact_1=data['contact_1'],
            contact_2=data.get('contact_2'),
            aadhar_number=data['aadhar_number'],
            home_address=data['home_address'],
            business_address=data.get('business_address'),
            occupation=data.get('occupation'),
            rating=data.get('rating')
        )
        db.session.add(customer)
        db.session.commit()

        return jsonify({'message': 'Customer created successfully', 'customer_id': customer.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

# Read Customer
@customers.route('/customer/<int:id>', methods=['GET'])
@jwt_required()
def get_customer(id):
    user_id = get_jwt_identity()  # Get logged-in user's ID
    customer = Customer.query.filter_by(id=id, user_id=user_id).first()

    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    return jsonify({
        'id': customer.id,
        'first_name': customer.first_name,
        'last_name': customer.last_name,
        'mobile': customer.mobile,
        'contact_1': customer.contact_1,
        'contact_2': customer.contact_2,
        'aadhar_number': customer.aadhar_number,
        'home_address': customer.home_address,
        'business_address': customer.business_address,
        'occupation': customer.occupation,
        'rating': customer.rating
    }), 200

# Update Customer
@customers.route('/UpdateCustomer/<int:id>', methods=['PUT'])
@jwt_required()
def update_customer(id):
    data = request.json
    user_id = get_jwt_identity()  # Get logged-in user's ID
    customer = Customer.query.filter_by(id=id, user_id=user_id).first()

    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    try:
        # Update fields if present in request
        if 'first_name' in data:
            customer.first_name = data['first_name']
        if 'last_name' in data:
            customer.last_name = data['last_name']
        if 'mobile' in data:
            customer.mobile = data['mobile']
        if 'contact_1' in data:
            customer.contact_1 = data['contact_1']
        if 'contact_2' in data:
            customer.contact_2 = data['contact_2']
        if 'aadhar_number' in data:
            customer.aadhar_number = data['aadhar_number']
        if 'home_address' in data:
            customer.home_address = data['home_address']
        if 'business_address' in data:
            customer.business_address = data['business_address']
        if 'occupation' in data:
            customer.occupation = data['occupation']
        if 'rating' in data:
            customer.rating = data['rating']

        db.session.commit()

        return jsonify({'message': 'Customer updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

# Delete Customer
@customers.route('/DeleteCustomer/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_customer(id):
    user_id = get_jwt_identity()  # Get logged-in user's ID
    customer = Customer.query.filter_by(id=id, user_id=user_id).first()

    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    try:
        db.session.delete(customer)
        db.session.commit()

        return jsonify({'message': 'Customer deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
