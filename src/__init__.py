from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '233e21149414a095c88f9eb8413d7a96'

    from src.main.routes import main

    app.register_blueprint(main)

    return app