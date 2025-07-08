from app import app, db
import models
import routes
import auth
import chatbot_routes

# Register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(chatbot_routes.chatbot_bp)

# User loader
@app.login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Initialize database and data
with app.app_context():
    db.create_all()
    # Initialize mock data
    from mock_data import initialize_mock_data
    initialize_mock_data()
