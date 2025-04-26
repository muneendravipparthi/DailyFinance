from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from models import db
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__,static_folder='static')
CORS(app)
app.config.from_object(Config)
# db = SQLAlchemy()

# Lazy initialization
db.init_app(app)

# Add JWT configuration
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Replace with your actual secret key
app.config['JWT_TOKEN_LOCATION'] = ['headers']   # Specify token location (e.g., headers or cookies)

jwt = JWTManager(app)

SWAGGER_URL = '/swagger'  # Swagger UI URL
API_URL = '/static/swagger.yaml' # Path to Swagger file

swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Import and register Blueprints
from routes.signup import signup
from routes.login import login
from routes.protected import protected
from routes.update_user_details import update_user_details
from routes.change_password_service import change_password_service
from routes.customers import customers
from routes.account_service import account_service
from routes.finance_service import finance_service
from routes.financing_service import financing_service
from routes.installmentDetails_service import installmentDetails_service

app.register_blueprint(signup)
app.register_blueprint(login)
app.register_blueprint(protected)
app.register_blueprint(update_user_details)
app.register_blueprint(change_password_service)
app.register_blueprint(customers)
app.register_blueprint(account_service)
app.register_blueprint(finance_service)
app.register_blueprint(financing_service)
app.register_blueprint(installmentDetails_service)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database initialized!")
    app.run(debug=True)
