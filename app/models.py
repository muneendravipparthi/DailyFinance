from flask_sqlalchemy import SQLAlchemy

# `db` will be initialized lazily
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    default_interest_rate = db.Column(db.Float, nullable=True)
    default_finance_period = db.Column(db.Integer, nullable=True)

def __repr__(self):
        return f'<User {self.email}>'


