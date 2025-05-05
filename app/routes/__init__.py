from flask import Flask
from .bot_bp_route import bot_bp

def register_routes(app: Flask):
    app.register_blueprint(bot_bp, url_prefix='/api')
