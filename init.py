from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import os

db = SQLAlchemy()
csrf = CSRFProtect()

def init_app(app):
    # Configure app
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-123')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///football.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'static/uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register blueprints
    from blueprints.auth import auth_bp
    from blueprints.team import team_bp
    from blueprints.player import player_bp
    from blueprints.match import match_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(team_bp, url_prefix='/team')
    app.register_blueprint(player_bp, url_prefix='/player')
    app.register_blueprint(match_bp, url_prefix='/match')

    # Create database tables
    with app.app_context():
        db.create_all()
