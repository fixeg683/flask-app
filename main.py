from app import app, db
import models
import routes
import auth
import chatbot_routes

# Register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(chatbot_routes.chatbot_bp)

# Default route (this is likely what's missing!)
@app.route('/')
def index():
    return '🚀 Flask app is running on Render!'

# User loader for Flask-Login
@app.login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Initialize the database and mock data
with app.app_context():
    db.create_all()
    
    # Optional: only initialize mock data if DB is empty
    from models import User
    if not User.query.first():
        from mock_data import initialize_mock_data
        initialize_mock_data()

# Required for Render to detect the app (entrypoint for gunicorn)
if __name__ == '__main__':
    app.run(debug=True)
