# app/main.py

from flask import Flask
from config.config import get_config
import os

# Import the Blueprint
from app.routes.routes import resume_tailor_bp


def create_app():
    app = Flask(__name__)

    # Get environment configuration
    env = os.environ.get('FLASK_ENV', 'development')
    app.config.from_object(get_config(env))

    # Register Blueprints
    app.register_blueprint(resume_tailor_bp, url_prefix='/api')

    @app.route('/')
    def home():
        return "Welcome to your Flask application!"

    @app.route('/about')
    def about():
        return "This is the about page."

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')
