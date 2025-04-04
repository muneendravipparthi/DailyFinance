from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Transaction, User, db
from datetime import datetime, timedelta

finance_service = Blueprint('finance_service', __name__)

@finance_service.route('/finance', methods=['POST'])
@jwt_required()
def create_finance():
    data = request.json
    try:
        # Validate mandatory fields
        mandatory_fields = ['customer_id', 'loan_amount', 'repayment_type', 'tenure', 'transaction_type', 'amount_disbursed']
        for field in mandatory_fields:
            if not data.get(field):
                return jsonify({'message': f'{field} is required'}), 400

        # Retrieve interest rate
        interest_rate = data.get('rate_of_interest')
        if data.get('interest_type') == 'Default':
            # Assuming `default_interest_rate` comes from `User` table (retrieve it from DB)
            user_id = get_jwt_identity()
            user = User.query.filter_by(email=user_id).first()
            interest_rate = user.default_interest_rate

        # Calculate installment details
        loan_amount = data['loan_amount']
        tenure = int(data['tenure'])
        repayment_type = data['repayment_type']  # Monthly/Daily/Weekly
        installment_amount = loan_amount * (1 + interest_rate / 100) / tenure

        # Generate transaction record
        transaction = Transaction(
            customer_id=data['customer_id'],
            loan_date=datetime.today(),
            loan_amount=loan_amount,
            no_of_installments=tenure,
            installment_amount=installment_amount,
            payment_status='Pending',
            payment_type=data['transaction_type']
        )
        db.session.add(transaction)
        db.session.commit()

        return jsonify({'message': 'Finance record created successfully', 'transaction_id': transaction.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
