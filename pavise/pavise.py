from flask import Flask, request, jsonify, g
import sqlite3

DATABASE = "pavise.db"
DEBUG = True

app = Flask(__name__)

app.config.from_object(__name__)


def connect_db():
    """Connect to the database."""
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource("pavise_schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    if not(hasattr(g, "pavise_db")):
        g.pavise_db = connect_db()
    return g.pavise_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "pavise_db"):
        g.pavise_db.close()


@app.route("/", methods=["GET"])
def home():
    return "<h1>Welcome to Pavise</h1><p>This is a test to make sure things are working.</p>"

if __name__ == "__main__":
    app.run()
