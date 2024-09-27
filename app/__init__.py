from flask import Flask
from app.config import config
from app.models import db
from flask_migrate import Migrate
from flask_login import LoginManager
from app.routes.auth import auth_bp
from app.routes.dashboard import dashboard_bp
from app.routes.registerations import registration_bp
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # Redirect to 'auth.login' for login
migrate = Migrate()


def create_app(configname: str = "development") -> Flask:
    """
    Creates an instance of the Flask application.

    Returns:
        Flask: An instance of the Flask application.
    """
    from app.models.user import User
    from app.models.account import Account, History
    from app.models.goods import Purchase, Items, ItemCategory

    app = Flask(__name__)
    app.config.from_object(config[configname])

    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(registration_bp)

    @login_manager.user_loader
    def load_user(user_id):
            return db.session.get(User, int(user_id))

    return app
