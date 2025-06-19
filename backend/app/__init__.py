from flask import Flask
from app.extensions import db, login_manager
from config import Config

# Export db so it can be imported from app
__all__ = ['create_app', 'db']

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Login configuration
    login_manager.login_view = "main.index"
    login_manager.login_message = 'Please login to access this feature.'
    login_manager.login_message_category = 'danger'
    
    # Register blueprints/routes here
    from . import routes
    app.register_blueprint(routes.bp)
    
    # Create all database tables
    with app.app_context():
        db.create_all()
    
    return app