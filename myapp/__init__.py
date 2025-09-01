from flask import Flask
from .database import Base, engine, SessionLocal

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev"

    # Register blueprint
    from .routes import main
    app.register_blueprint(main)

    # Create tables
    with app.app_context():
        import myapp.models
        Base.metadata.create_all(bind=engine)

    # Remove session after request
    @app.teardown_appcontext
    def remove_session(exception=None):
        SessionLocal.remove()

    return app
