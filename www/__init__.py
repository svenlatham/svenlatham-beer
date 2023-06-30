from flask import Flask

def create_app():
    app = Flask(__name__)
    from .standard import standard as blueprint_standard
    app.register_blueprint(blueprint_standard)
    return app

