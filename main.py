from app import app, db
import models
import routes
import auth
import chatbot_routes

# Register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(chatbot_routes.chatbot_bp)

@app.route('/')
def index():
    return '✅ Flask is alive on Render!'

@app.login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()
    from models import User
    if not User.query.first():
        from mock_data import initialize_mock_data
        initialize_mock_data()

if __name__ == '__main__':
    app.run(debug=True)
