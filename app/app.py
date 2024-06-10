from flask import Flask, redirect, url_for, send_from_directory
from flask_migrate import Migrate  
from routes import bp as routes_bp
import os

app = Flask(__name__)
app.config.from_pyfile("config.py")

from models import db

db.init_app(app)
migrate = Migrate(app, db)

from auth import bp as auth_bp, init_login_manager

app.register_blueprint(auth_bp)
app.register_blueprint(routes_bp)

init_login_manager(app)

@app.route('/')
def index():
    return redirect(url_for('routes.index'))

@app.route("/media/images/<path:filename>")
def image_path(filename):
    return send_from_directory(
        os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "media", "images"),
        filename,
    )