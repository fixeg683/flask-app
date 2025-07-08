import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
mail = Mail()

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL environment variable is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Mail configuration
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", "587"))
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS", "true").lower() in ["true", "on", "1"]
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER", app.config["MAIL_USERNAME"])

# Initialize the app with the extensions
db.init_app(app)
login_manager.init_app(app)
mail.init_app(app)

# Configure Flask-Login
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"

# PayPal configuration
app.config["PAYPAL_CLIENT_ID"] = os.environ.get("PAYPAL_CLIENT_ID", "ATeu5CLtb_KasnrA46vNPgaNrmcG1BpjEml_qYBThs3ImNdagp9NW0l0yF6KpCBUD9kBhAAafG3cWf2i")
app.config["PAYPAL_CLIENT_SECRET"] = os.environ.get("PAYPAL_CLIENT_SECRET", "EF-FXUMAXfWMVtd3jWU-Pri9NPajE6Jjw3SLjcgMbfuvlmG3qROLenB8iBm6Md1IqqoPQ5BTdZUzoKzk")
app.config["PAYPAL_SANDBOX"] = True

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
