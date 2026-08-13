from flask import Flask
from flask_migrate import Migrate
from .config import Config
from .database import db
from .health import health_bp
from .routes import student_bp
from .error_handlers import register_error_handlers
from app.metrics import register_metrics

migrate = Migrate()


def create_app(test_config=None):

    app = Flask(__name__)

    app.config.from_object(Config)

    # Override configuration when testing
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(health_bp)
    app.register_blueprint(student_bp)

    register_error_handlers(app)
    register_metrics(app)

    return app
