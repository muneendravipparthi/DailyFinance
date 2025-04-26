from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from models import Installment, Finance, db
from flask import Flask, Blueprint, request, jsonify

installmentDetails_service = Blueprint('installmentDetails_service', __name__)

@installmentDetails_service.route("/api/v1/installmentDetails", methods=["GET"])
def get_installment_details():
    # Retrieve query parameters from request
    customer_id = request.args.get("customer_id")
    finance_amount = float(request.args.get("finance_amount", 0))
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    finance_type = request.args.get("finance_type")
    interest_rate = float(request.args.get("interestRate", 0))

    # Validate mandatory fields
    if not (customer_id and finance_amount and start_date and end_date and finance_type and interest_rate):
        return jsonify({"error": "Missing required parameters"}), 400

    # Calculate the number of installments (assuming daily payments)
    start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    num_installments = (end_date_obj - start_date_obj).days

    # Compute daily installment amount
    total_payable = finance_amount + (finance_amount * (interest_rate / 100))
    daily_installment = round(total_payable / num_installments, 2)

    # Generate installment schedule
    installments = []
    outstanding_balance = total_payable
    for i in range(num_installments):
        date = (start_date_obj + timedelta(days=i)).strftime("%Y-%m-%d")
        amount_paid = daily_installment if i == 0 else 0  # First day's payment upfront
        outstanding_balance = max(0, round(outstanding_balance - daily_installment, 2))

        installments.append({
            "s_no": i + 1,
            "date": date,
            "amount_paid": amount_paid,
            "amount_to_be_paid": daily_installment if i > 0 else "",
            "outstanding_balance": outstanding_balance
        })

    # Construct response
    response_data = {
        "finance_amount": finance_amount,
        "interest_rate": interest_rate,
        "disbursed_amount": finance_amount * 0.9,  # Assuming 10% fee deducted
        "num_installments": num_installments,
        "start_date": start_date,
        "end_date": end_date,
        "installments": installments
    }

    return jsonify(response_data)
