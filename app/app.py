from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from models import db
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
# db = SQLAlchemy()

# Lazy initialization
db.init_app(app)

# Add JWT configuration
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Replace with your actual secret key
app.config['JWT_TOKEN_LOCATION'] = ['headers']   # Specify token location (e.g., headers or cookies)

jwt = JWTManager(app)

# Import and register Blueprints
from routes.signup import signup
from routes.login import login
from routes.protected import protected
from routes.update_user_details import update_user_details

app.register_blueprint(signup)
app.register_blueprint(login)
app.register_blueprint(protected)
app.register_blueprint(update_user_details)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database initialized!")
    app.run(debug=True)
