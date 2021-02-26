from flask import Flask, request, jsonify, g
import sqlite3
import urllib.parse
import hashlib

DATABASE="pavise.db"

def create_app(config_name):
    app = Flask(__name__)

    config_module = f"pavise.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)

    init_db(app)

    populate_db(app)

    @app.route("/", methods=["GET"])
    def home():
        return "<h1>Welcome to Pavise</h1><p>This is a test to make sure things are working.</p>"


    @app.route("/urlinfo/1/", methods=["GET"], defaults={"url": ""})
    @app.route("/urlinfo/1/<path:url>", methods=["GET"])
    def check_for_malware(url):
        print(f"base url: {request.url}")
        malware_path = get_malware_path(request.url)
        print(f"malware path: {malware_path}")
        encoded_path = normalize_path(malware_path)
        print(f"encoded path: {encoded_path}")
        malware_hash = get_hash(encoded_path)
        print(f"resulting hash: {malware_hash}")
        return malware_path

    return app


def get_malware_path(url):
    """Extract the path after '/urlinfo/1/' from a given URL."""
    if url is not None:
        malware_path = url.split("/urlinfo/1/")[1]
        return malware_path
    
    return None


def normalize_path(path):
    """Ensure that the malware path is in a consistent form. In short,
    make the string lowercase, quote the path"""
    path = path.lower()

    encoded_path = urllib.parse.quote(path)

    return encoded_path


def get_hash(path):
    """Returns the SHA-256 hash of a path."""
    hash = hashlib.sha256(bytes(path, encoding="utf8")).hexdigest()
    return hash

def connect_db(app):
    """Connect to the database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(app):
    with app.app_context():
        db = get_db(app)
        with app.open_resource("pavise_schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()
 

def populate_db(app):
    with app.app_context():
        db = get_db(app)
        with app.open_resource("../tests/test_data.txt", mode="r") as f:
            urls = f.read()
            print(urls)
            for url in urls:
                print(url)
                path = url.split("//")[1]
                encoded_path = normalize_path(path)
                path_hash = get_hash(encoded_path)
                c = db.cursor()
                # TODO: Fix the unsanitized SQL
                sql_string =\
                    f"INSERT INTO malware_sites (site_url, sha256_hash) VALUES ('{encoded_path}', '{path_hash}')"
                c.execute(sql_string)
        db.commit()


def get_db(app):
    if not(hasattr(g, "pavise_db")):
        g.pavise_db = connect_db(app)
    return g.pavise_db
