from flask import Flask, request, jsonify, g
import sqlite3
import urllib.parse
import hashlib

DATABASE="pavise.db"

def create_app(config_name):
    app = Flask(__name__)

    config_module = f"pavise.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)

    @app.route("/", methods=["GET"])
    def home():
        return "<h1>Welcome to Pavise</h1><p>This is a test to make sure things are working.</p>"


    @app.route("/urlinfo/1/", methods=["GET"], defaults={"url": ""})
    @app.route("/urlinfo/1/<path:url>", methods=["GET"])
    def check_for_malware(url):
        malware_path = get_malware_path(request.url)
        encoded_path = normalize_path(malware_path)
        malware_hash = get_hash(encoded_path)
        
        check_result = {
            url: malware_path,
            sha256_hash: malware_hash
        }

        # return 1 if either the URL or hash is in the db, 0 otherwise
        query = "SELECT count(*) FROM malware_sites WHERE site_url=? OR sha256_hash=? LIMIT 1"

        with app.app_context():
            db = get_db(app)
            cur = db.cursor()
            cur.execute(query, (encoded_path, malware_hash))

            results = cur.fetchall()
            # now, check if we have a result.
            if len(results) != 1:
                response = app.response_class(
                    response = "Error in results",
                    status = 500,
                )
                return response
            else:
                if results[0][0] = 1: # At least one component of the pair is in the database
                    check_result["is_malware"] = True
                else:
                    check_result["is_malware"] = False

                return jsonify(check_result)

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
    """Create the database."""
    with app.app_context():
        db = get_db(app)
        with app.open_resource("pavise_schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()
 

def populate_db(app):
    query f"INSERT INTO malware_sites (site_url, sha256_hash) VALUES (?, ?)"
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

                c.execute(query, encoded_path, path_hash)
        db.commit()


def get_db(app):
    if not(hasattr(g, "pavise_db")):
        g.pavise_db = connect_db(app)
    return g.pavise_db
