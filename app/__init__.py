from flask import Flask
from flask_cors import CORS
from app.config import Config
from flask_caching import Cache

from app.routes import register_routes

def create_app(config_class=Config):
    app = Flask(__name__, static_folder="views", static_url_path="")
    app.config.from_object(config_class)
    CORS(app)

    register_routes(app)
    cache = Cache(app)
    with app.app_context():
        """Clear the cache when the server starts."""
        cache.clear()

    
    return app
