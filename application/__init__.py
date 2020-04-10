from flask import Flask, jsonify, request
from flask_login import LoginManager
from config import Config

app = Flask(__name__)

login = LoginManager(app)
login.login_view = 'login'

app.config.from_object(Config)

from application import routes
