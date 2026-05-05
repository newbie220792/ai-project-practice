from flask import Flask
from app.api import bp

def create_app():
    app = Flask(__name__)
    # if config:
    #     app.config.from_object(config)
    app.config.from_envvar("ENV_FILE", silent=True)
    app.register_blueprint(bp, url_prefix="/api")
    return app