from flask import Flask
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app.routes import routes

app.register_blueprint(routes)