# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
import nltk
import os
from app.documents_reader import DocumentReader

nltk.download('punkt')

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()
document_reader = DocumentReader()

def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///app.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER='app/uploads'
    )
    
    db.init_app(app)
    migrate.init_app(app)
    
    # Import blueprint after db initialization
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    socketio.init_app(app)
    
    return app