from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Transaction, User, db

account_service = Blueprint('account_service', __name__)

@account_service.route('/api/v1/account/overview', methods=['GET'])
@jwt_required()
def get_account_overview():
    try:
        # Retrieve the logged-in user's ID and query their capital investment
        user_id = get_jwt_identity()
        user = User.query.filter_by(email=user_id).first()

        if not user:
            return jsonify({'message': 'User not found'}), 404

        capital_investment = user.capital_investment

        # Query all transactions for all customers associated with this user
        transactions = Transaction.query.all()
        if not transactions:
            return jsonify({'message': 'No transactions found'}), 404

        # Perform calculations based on transaction data
        total_account_balance = capital_investment + sum([transaction.loan_amount for transaction in transactions if transaction.payment_status == 'Paid'])
        total_circulating_amount = sum([transaction.loan_amount for transaction in transactions])
        profit = sum([transaction.loan_amount * 0.1 for transaction in transactions if transaction.payment_status == 'Paid'])  # 10% profit from paid loans
        loss = sum([transaction.loan_amount * 0.05 for transaction in transactions if transaction.payment_status == 'Pending'])  # 5% loss from pending loans
        amount_to_be_collected = sum([transaction.installment_amount for transaction in transactions if transaction.payment_status == 'Pending'])

        # Return calculated stats
        return jsonify({
            'capital_investment': capital_investment,
            'total_account_balance': total_account_balance,
            'total_circulating_amount': total_circulating_amount,
            'profit': profit,
            'loss': loss,
            'amount_to_be_collected': amount_to_be_collected
        }), 200

    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
