from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import datetime, timedelta
from flask import Flask, Blueprint, request, jsonify
from models import Installment, Finance, Customer, db
from sqlalchemy import text
# from app.models import Finance

financing_service = Blueprint('financing_service', __name__)
# Fetch All Finance Accounts
@financing_service.route('/api/v1/finance', methods=['GET'])
def get_accounts():
    result = db.session.execute(text("SELECT f.*, c.first_name, c.last_name FROM finance f join customer c on f.customer_id = c.id"))
    accounts = result.fetchall();
    # accounts = Finance.query.all()
    # Print the retrieved data before processing
    print("Accounts Retrieved:", accounts)
    # Get today's date
    today = datetime.today().date()
    formatted_accounts = []

    for a in accounts:
        print("Finance Record:", a)  # Debugging each object

        # Try printing ID separately
        print("Finance ID:", getattr(a, "id", "ID Not Found"))
        # Convert string dates to datetime objects
        start_date = datetime.strptime(a.start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(a.end_date, "%Y-%m-%d").date()

        # Calculate number of installments (assuming daily frequency)
        no_of_installments = (end_date - start_date).days if a.finance_type == "Daily" else 0

        # Calculate paid and pending installments
        paid_installments = (today - start_date).days if today > start_date else 0
        pending_installments = (end_date - today).days if today < end_date else 0

        # Calculate installment amount
        dispersed_amount = a.finance_amount - (a.finance_amount * (a.interest_rate / 100))
        installment_amount = a.finance_amount / no_of_installments if no_of_installments > 0 else 0

        # Calculate cleared and pending amounts
        cleared_amount = installment_amount * paid_installments
        pending_amount = installment_amount * pending_installments

        formatted_accounts.append({
            "id": a.id,
            "customer_name": f"{a.first_name} {a.last_name}",
            "loan_amount": a.finance_amount,
            "dispersed_amount": dispersed_amount,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "finance_type": a.finance_type,
            "collection_time": a.collection_time,
            "interest_rate": a.interest_rate,
            "no_of_installments": no_of_installments,
            "paid_installments": paid_installments,
            "pending_installments": pending_installments,
            "installment_amount": round(installment_amount, 0),
            "cleared_amount": round(cleared_amount, 0),
            "pending_amount": round(pending_amount, 0),
            "status": a.status,
        })

    if not accounts:  # If empty, return a message
        return jsonify({"message": "No finance records found"}), 404

    return jsonify(formatted_accounts)

@financing_service.route('/api/v1/createFinance', methods=['POST'])
@jwt_required()
def create_finance():
    user_id = get_jwt_identity()
    data = request.json

    # Check if customer has an active finance
    existing_finance = Finance.query.filter_by(customer_id=data["customer_id"], status="Active").first()
    if existing_finance:
        return jsonify({"message": "Customer already has an active finance account"}), 400

    # Create new finance record
    new_finance = Finance(
        customer_id=data["customer_id"],
        finance_amount=data["finance_amount"],
        start_date=datetime.strptime(data["start_date"], "%Y-%m-%d"),
        end_date=datetime.strptime(data["end_date"], "%Y-%m-%d"),
        finance_type=data["finance_type"],
        collection_time=data.get("collection_time"),
        interest_rate=data.get("interest_rate")
    )

    db.session.add(new_finance)
    db.session.commit()

    # Get today's date for calculations
    today = datetime.today().date()

    # Convert dates for calculations
    start_date = new_finance.start_date
    end_date = new_finance.end_date

    # Compute installment-related attributes
    no_of_installments = (end_date - start_date).days if new_finance.finance_type == "Daily" else 0
    paid_installments = (today - start_date).days if today > start_date else 0
    pending_installments = (end_date - today).days if today < end_date else 0
    dispersed_amount = new_finance.finance_amount - (new_finance.finance_amount * (new_finance.interest_rate / 100))
    installment_amount = new_finance.finance_amount / no_of_installments if no_of_installments > 0 else 0
    cleared_amount = installment_amount * paid_installments
    pending_amount = installment_amount * pending_installments

    # Fetch customer details for response
    customer = Customer.query.filter_by(id=new_finance.customer_id).first()

    # Construct response with detailed finance record
    response_data = {
        "id": new_finance.id,
        "customer_name": f"{customer.first_name} {customer.last_name}",
        "loan_amount": new_finance.finance_amount,
        "dispersed_amount": dispersed_amount,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "finance_type": new_finance.finance_type,
        "collection_time": new_finance.collection_time,
        "interest_rate": new_finance.interest_rate,
        "no_of_installments": no_of_installments,
        "paid_installments": paid_installments,
        "pending_installments": pending_installments,
        "installment_amount": round(installment_amount, 0),
        "cleared_amount": round(cleared_amount, 0),
        "pending_amount": round(pending_amount, 0),
        "status": new_finance.status,
    }

    return jsonify(response_data), 201

# # Create New Finance
# @financing_service.route('/api/v1/createFinance', methods=['POST'])
# @jwt_required()
# def create_finance():
#     user_id = get_jwt_identity()
#     data = request.json
#
#     # Check if customer has an active finance
#     existing_finance = Finance.query.filter_by(customer_id=data["customer_id"], status="Active").first()
#     if existing_finance:
#         return jsonify({"message": "Customer already has an active finance account"}), 400
#
#     # Restrict customers who already have an active finance account
#     existing_finance_count = Finance.query.filter_by(customer_id=data["customer_id"], status="Active").count()
#     if existing_finance_count > 0:
#         return jsonify({"message": "Customer already has an active finance account"}), 400
#
#     new_finance = Finance(
#         customer_id=data["customer_id"],
#         finance_amount=data["finance_amount"],
#         start_date=datetime.strptime(data["start_date"], "%Y-%m-%d"),
#         end_date=datetime.strptime(data["end_date"], "%Y-%m-%d"),
#         finance_type=data["finance_type"],
#         collection_time=data.get("collection_time"),
#         interest_rate=data.get("interest_rate")
#     )
#
#     db.session.add(new_finance)
#     db.session.commit()
#     print(new_finance.id)
#
#     # Generate Installments
#     # generate_installments(new_finance)
#
#     return jsonify({"message": "Finance created successfully"}), 201

# # Generate Installments Based on Finance Type
# def generate_installments(finance):
#     start_date = finance.start_date
#     end_date = finance.end_date
#     installments = []
#
#     if finance.finance_type == "Daily":
#         days = (end_date - start_date).days
#         for i in range(days):
#             installments.append(Installment(
#                 finance_id=finance.id,
#                 due_date=start_date + timedelta(days=i),
#                 amount=finance.finance_amount / days
#             ))
#
#     elif finance.finance_type == "Weekly":
#         for i in range(4):  # Assuming 4 weeks for simplicity
#             installments.append(Installment(
#                 finance_id=finance.id,
#                 due_date=start_date + timedelta(days=(i * 7)),
#                 amount=finance.finance_amount / 4
#             ))
#
#     elif finance.finance_type == "Monthly":
#         installments.append(Installment(
#             finance_id=finance.id,
#             due_date=end_date,
#             amount=finance.finance_amount
#         ))
#
#     db.session.add_all(installments)
#     db.session.commit()
