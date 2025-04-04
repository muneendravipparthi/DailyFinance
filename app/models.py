from flask_sqlalchemy import SQLAlchemy

# `db` will be initialized lazily
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    default_interest_rate = db.Column(db.Float, nullable=True)
    default_finance_period = db.Column(db.Integer, nullable=True)
    capital_investment = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f'<User {self.email}>'


class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)  # Auto-generated primary key
    user_id = db.Column(db.Integer, nullable=False)  # Foreign key for login user-specific details
    first_name = db.Column(db.String(50), nullable=False)  # Mandatory
    last_name = db.Column(db.String(50), nullable=False)  # Mandatory
    mobile = db.Column(db.String(15), nullable=False)  # Mandatory
    contact_1 = db.Column(db.String(15), nullable=False)  # Mandatory
    contact_2 = db.Column(db.String(15), nullable=True)  # Optional
    aadhar_number = db.Column(db.String(12), nullable=False)  # Mandatory
    home_address = db.Column(db.String(255), nullable=False)  # Mandatory
    business_address = db.Column(db.String(255), nullable=True)  # Optional
    occupation = db.Column(db.String(50), nullable=True)  # Optional
    rating = db.Column(db.Integer, nullable=True)  # Optional

    def __repr__(self):
        return f'<Customer {self.first_name} {self.last_name}>'

class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)  # Auto-generated primary key
    customer_id = db.Column(db.Integer, nullable=False)  # Foreign key to link to customer
    loan_date = db.Column(db.Date, nullable=False)  # Loan initiation date
    loan_amount = db.Column(db.Float, nullable=False)  # Total loan amount
    no_of_installments = db.Column(db.Integer, nullable=False)  # Total number of installments
    installment_amount = db.Column(db.Float, nullable=False)  # Amount per installment
    payment_status = db.Column(db.String(20), nullable=False)  # "Paid" or "Pending"
    payment_type = db.Column(db.String(20), nullable=False)  # "Online", "Cash", or "Check"

class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)  # Auto-generated primary key
    customer_id = db.Column(db.Integer, nullable=False)  # Customer-specific account
    account_balance = db.Column(db.Float, nullable=False)  # Balance in the account
    profit = db.Column(db.Float, nullable=False)  # Profit earned
    loss = db.Column(db.Float, nullable=False)  # Loss incurred
    circulating_amount = db.Column(db.Float, nullable=False)  # Total circulating amount
    amount_to_be_collected = db.Column(db.Float, nullable=False)  # Unpaid installment amounts
    amount_to_be_deducted = db.Column(db.Float, nullable=False)  # Deduction amount
