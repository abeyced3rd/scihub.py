from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def init_app(app):
    app.config.setdefault('SQLALCHEMY_DATABASE_URI', 'sqlite:///research_assistant.db')
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)
    migrate.init_app(app, db)

    # create tables if not present (safe on app start)
    with app.app_context():
        db.create_all()
