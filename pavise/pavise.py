from flask import Flask, request, jsonify, g
import sqlite3

DATABASE = "pavise.db"
DEBUG = True

def create_app(config_name):
    app = Flask(__name__)

    config_module = f"pavise.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)


    @app.route("/", methods=["GET"])
    def home():
        return "<h1>Welcome to Pavise</h1><p>This is a test to make sure things are working.</p>"

    return app


def connect_db(app):
    """Connect to the database."""
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


def init_db(app):
    with app.app_context():
        db = get_db(app)
        with app.open_resource("pavise_schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db(app):
    if not(hasattr(g, "pavise_db")):
        g.pavise_db = connect_db(app)
    return g.pavise_db
