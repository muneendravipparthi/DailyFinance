from flask import Blueprint, jsonify
from utils import token_required

protected = Blueprint('protected', __name__)

@protected.route('/dashboard', methods=['GET'])
@token_required
def dashboard():
    return jsonify({'message': 'Welcome to the protected dashboard!'}), 200
