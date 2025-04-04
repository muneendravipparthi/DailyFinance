from app import app, db

# Activate application context and create the database
with app.app_context():
    db.create_all()
    print("Database has been created successfully!")

